# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import json
import anytree, copy, logging, pytz, queue, re, threading
#import lxml.etree as ET
from datetime import datetime, timedelta
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.job import Job
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from ncclient.manager import Manager, connect_ssh
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.tools.client.RetryDecorator import delay_exponential
from common.type_checkers.Checkers import chk_length, chk_string, chk_type, chk_float
from device.service.driver_api.Exceptions import UnsupportedResourceKeyException
from device.service.driver_api._Driver import _Driver
from device.service.driver_api.AnyTreeTools import TreeNode, get_subnode, set_subnode_value #dump_subtree
#from .Tools import xml_pretty_print, xml_to_dict, xml_to_file
from .templates import ALL_RESOURCE_KEYS, EMPTY_CONFIG, compose_config, get_filter, parse, cli_compose_config, ufi_interface, cisco_interface
from .RetryDecorator import retry

DEBUG_MODE = False
logging.getLogger('ncclient.manager').setLevel(logging.DEBUG if DEBUG_MODE else logging.WARNING)
logging.getLogger('ncclient.transport.ssh').setLevel(logging.DEBUG if DEBUG_MODE else logging.WARNING)
logging.getLogger('apscheduler.executors.default').setLevel(logging.INFO if DEBUG_MODE else logging.ERROR)
logging.getLogger('apscheduler.scheduler').setLevel(logging.INFO if DEBUG_MODE else logging.ERROR)
logging.getLogger('monitoring-client').setLevel(logging.INFO if DEBUG_MODE else logging.ERROR)

RE_GET_ENDPOINT_FROM_INTERFACE_KEY = re.compile(r'.*interface\[([^\]]+)\].*')
RE_GET_ENDPOINT_FROM_INTERFACE_XPATH = re.compile(r".*interface\[oci\:name\='([^\]]+)'\].*")

# Collection of samples through NetConf is very slow and each request collects all the data.
# Populate a cache periodically (when first interface is interrogated).
# Evict data after some seconds, when data is considered as outdated

SAMPLE_EVICTION_SECONDS = 30.0 # seconds
SAMPLE_RESOURCE_KEY = 'interfaces/interface/state/counters'

MAX_RETRIES = 15
DELAY_FUNCTION = delay_exponential(initial=0.01, increment=2.0, maximum=5.0)
RETRY_DECORATOR = retry(max_retries=MAX_RETRIES, delay_function=DELAY_FUNCTION, prepare_method_name='connect')

class NetconfSessionHandler:
    def __init__(self, address : str, port : int, **settings) -> None:
        self.__lock = threading.RLock()
        self.__connected = threading.Event()
        self.__address = address
        self.__port = int(port)
        self.__username         = settings.get('username')
        self.__password         = settings.get('password')
        self.__vendor           = settings.get('vendor')
        self.__version          = settings.get('version', "1")
        self.__key_filename     = settings.get('key_filename')
        self.__hostkey_verify   = settings.get('hostkey_verify', True)
        self.__look_for_keys    = settings.get('look_for_keys', True)
        self.__allow_agent      = settings.get('allow_agent', True)
        self.__force_running    = settings.get('force_running', False)
        self.__commit_per_rule  = settings.get('commit_per_rule', False)
        self.__device_params    = settings.get('device_params', {})
        self.__manager_params   = settings.get('manager_params', {})
        self.__nc_params        = settings.get('nc_params', {})
        self.__message_renderer = settings.get('message_renderer','jinja')
        self.__manager : Manager   = None
        self.__candidate_supported = False

    def connect(self):
        with self.__lock:
            self.__manager = connect_ssh(
                host=self.__address, port=self.__port, username=self.__username, password=self.__password,
                device_params=self.__device_params, manager_params=self.__manager_params, nc_params=self.__nc_params,
                key_filename=self.__key_filename, hostkey_verify=self.__hostkey_verify, allow_agent=self.__allow_agent,
                look_for_keys=self.__look_for_keys)
            self.__candidate_supported = ':candidate' in self.__manager.server_capabilities
            self.__connected.set()

    def disconnect(self):
        if not self.__connected.is_set(): return
        with self.__lock:
            self.__manager.close_session()

    @property
    def use_candidate(self): return self.__candidate_supported and not self.__force_running

    @property
    def commit_per_rule(self): return self.__commit_per_rule

    @property
    def vendor(self): return self.__vendor

    @property
    def version(self): return self.__version

    @property
    def message_renderer(self): return self.__message_renderer

    @RETRY_DECORATOR
    def get(self, filter=None, with_defaults=None): # pylint: disable=redefined-builtin
        with self.__lock:
            if self.__vendor == 'JUNIPER'and not 'component' in str(filter):
                return self.__manager.get_config(source="running", filter=filter, with_defaults=with_defaults)
            else:
                return self.__manager.get(filter=filter, with_defaults=with_defaults)

    @RETRY_DECORATOR
    def edit_config(
        self, config, target='running', default_operation=None, test_option=None,
        error_option=None, format='xml'                                             # pylint: disable=redefined-builtin
    ):
        if config == EMPTY_CONFIG: return
        with self.__lock:
            self.__manager.edit_config(
                config, target=target, default_operation=default_operation, test_option=test_option,
                error_option=error_option, format=format)

    @RETRY_DECORATOR
    def locked(self, target):
        return self.__manager.locked(target=target)

    @RETRY_DECORATOR
    def commit(self, confirmed=False, timeout=None, persist=None, persist_id=None):
        return self.__manager.commit(confirmed=confirmed, timeout=timeout, persist=persist, persist_id=persist_id)

def compute_delta_sample(previous_sample, previous_timestamp, current_sample, current_timestamp):
    if previous_sample is None: return None
    if previous_timestamp is None: return None
    if current_sample is None: return None
    if current_timestamp is None: return None
    delay = current_timestamp - previous_timestamp
    field_keys = set(previous_sample.keys()).union(current_sample.keys())
    field_keys.discard('name')
    delta_sample = {'name': previous_sample['name']}
    for field_key in field_keys:
        previous_sample_value = previous_sample[field_key]
        if not isinstance(previous_sample_value, (int, float)): continue
        current_sample_value = current_sample[field_key]
        if not isinstance(current_sample_value, (int, float)): continue
        delta_value = current_sample_value - previous_sample_value
        if delta_value < 0: continue
        delta_sample[field_key] = delta_value / delay
    return delta_sample

class SamplesCache:
    def __init__(self, netconf_handler : NetconfSessionHandler, logger : logging.Logger) -> None:
        self.__netconf_handler = netconf_handler
        self.__logger = logger
        self.__lock = threading.Lock()
        self.__timestamp = None
        self.__absolute_samples = {}
        self.__delta_samples = {}

    def _refresh_samples(self) -> None:
        with self.__lock:
            try:
                now = datetime.timestamp(datetime.utcnow())
                if self.__timestamp is not None and (now - self.__timestamp) < SAMPLE_EVICTION_SECONDS: return
                str_filter = get_filter(SAMPLE_RESOURCE_KEY)
                xml_data = self.__netconf_handler.get(filter=str_filter).data_ele
                interface_samples = parse(SAMPLE_RESOURCE_KEY, xml_data)
                for interface,samples in interface_samples:
                    match = RE_GET_ENDPOINT_FROM_INTERFACE_KEY.match(interface)
                    if match is None: continue
                    interface = match.group(1)
                    delta_sample = compute_delta_sample(
                        self.__absolute_samples.get(interface), self.__timestamp, samples, now)
                    if delta_sample is not None: self.__delta_samples[interface] = delta_sample
                    self.__absolute_samples[interface] = samples
                self.__timestamp = now
            except: # pylint: disable=bare-except
                self.__logger.exception('Error collecting samples')

    def get(self, resource_key : str) -> Tuple[float, Dict]:
        self._refresh_samples()
        match = RE_GET_ENDPOINT_FROM_INTERFACE_XPATH.match(resource_key)
        with self.__lock:
            if match is None: return self.__timestamp, {}
            interface = match.group(1)
            return self.__timestamp, copy.deepcopy(self.__delta_samples.get(interface, {}))

def do_sampling(
    samples_cache : SamplesCache, logger : logging.Logger, resource_key : str, out_samples : queue.Queue
) -> None:
    try:
        timestamp, samples = samples_cache.get(resource_key)
        counter_name = resource_key.split('/')[-1].split(':')[-1]
        value = samples.get(counter_name)
        if value is None:
            logger.warning('[do_sampling] value not found for {:s}'.format(resource_key))
            return
        sample = (timestamp, resource_key, value)
        out_samples.put_nowait(sample)
    except: # pylint: disable=bare-except
        logger.exception('Error retrieving samples')

def edit_config(                                                                                                            # edit the configuration of openconfig devices
    netconf_handler : NetconfSessionHandler, logger : logging.Logger, resources : List[Tuple[str, Any]], delete=False,
    commit_per_rule=False, target='running', default_operation='merge', test_option=None, error_option=None,
    format='xml' # pylint: disable=redefined-builtin
):
    str_method = 'DeleteConfig' if delete else 'SetConfig'
    results = []
    if netconf_handler.vendor == "CISCO":
        if "L2VSI" in resources[0][1]:
            #Configure by CLI
            logger.warning("CLI Configuration")
            cli_compose_config(resources, delete=delete, host= netconf_handler._NetconfSessionHandler__address, user=netconf_handler._NetconfSessionHandler__username, passw=netconf_handler._NetconfSessionHandler__password)
            for i,resource in enumerate(resources):
                results.append(True)
        else:
            logger.warning("CLI Configuration CISCO INTERFACE")
            cisco_interface(resources, delete=delete, host= netconf_handler._NetconfSessionHandler__address, user=netconf_handler._NetconfSessionHandler__username, passw=netconf_handler._NetconfSessionHandler__password)
            for i,resource in enumerate(resources):
                results.append(True)
    elif netconf_handler.vendor == "UFISPACE":
        #Configure by CLI
        logger.warning("CLI Configuration: {:s}".format(resources))
        ufi_interface(resources, delete=delete)
        for i,resource in enumerate(resources):
            results.append(True)
    else:
        for i,resource in enumerate(resources):
            str_resource_name = 'resources[#{:d}]'.format(i)
            try:
                logger.debug('[{:s}] resource = {:s}'.format(str_method, str(resource)))
                chk_type(str_resource_name, resource, (list, tuple))
                chk_length(str_resource_name, resource, min_length=2, max_length=2)
                resource_key,resource_value = resource
                chk_string(str_resource_name + '.key', resource_key, allow_empty=False)
                str_config_messages = compose_config(                                                                          # get template for configuration
                    resource_key, resource_value, delete=delete, vendor=netconf_handler.vendor, message_renderer=netconf_handler.message_renderer)
                for str_config_message in str_config_messages:                                                                 # configuration of the received templates
                    if str_config_message is None: raise UnsupportedResourceKeyException(resource_key)
                    logger.debug('[{:s}] str_config_message[{:d}] = {:s}'.format(
                    str_method, len(str_config_message), str(str_config_message)))
                    netconf_handler.edit_config(                                                                               # configure the device
                        config=str_config_message, target=target, default_operation=default_operation,
                        test_option=test_option, error_option=error_option, format=format)
                    if commit_per_rule:
                        netconf_handler.commit()                                                                               # configuration commit
                    if 'table_connections' in resource_key:
                        time.sleep(5) # CPU usage might exceed critical level after route redistribution, BGP daemon needs time to reload

                #results[i] = True
                results.append(True)
            except Exception as e: # pylint: disable=broad-except
                str_operation = 'preparing' if target == 'candidate' else ('deleting' if delete else 'setting')
                msg = '[{:s}] Exception {:s} {:s}: {:s}'
                logger.exception(msg.format(str_method, str_operation, str_resource_name, str(resource)))
                #results[i] = e # if validation fails, store the exception
                results.append(e)

        if not commit_per_rule:
            try:
                netconf_handler.commit()
            except Exception as e: # pylint: disable=broad-except
                msg = '[{:s}] Exception committing: {:s}'
                str_operation = 'preparing' if target == 'candidate' else ('deleting' if delete else 'setting')
                logger.exception(msg.format(str_method, str_operation, str(resources)))
                results = [e for _ in resources] # if commit fails, set exception in each resource
    return results

DRIVER_NAME = 'openconfig'
METRICS_POOL = MetricsPool('Device', 'Driver', labels={'driver': DRIVER_NAME})

class OpenConfigDriver(_Driver):
    def __init__(self, address : str, port : int, **settings) -> None:
        super().__init__(DRIVER_NAME, address, port, **settings)
        self.__logger = logging.getLogger('{:s}:[{:s}:{:s}]'.format(str(__name__), str(self.address), str(self.port)))
        self.__lock = threading.Lock()
        #self.__initial = TreeNode('.')
        #self.__running = TreeNode('.')
        self.__subscriptions = TreeNode('.')
        self.__started = threading.Event()
        self.__terminate = threading.Event()
        self.__scheduler = BackgroundScheduler(daemon=True) # scheduler used to emulate sampling events
        self.__scheduler.configure(
            jobstores = {'default': MemoryJobStore()},
            executors = {'default': ThreadPoolExecutor(max_workers=1)}, # important! 1 = avoid concurrent requests
            job_defaults = {'coalesce': False, 'max_instances': 3},
            timezone=pytz.utc)
        self.__out_samples = queue.Queue()
        self.__netconf_handler = NetconfSessionHandler(self.address, self.port, **(self.settings))
        self.__samples_cache = SamplesCache(self.__netconf_handler, self.__logger)

    def Connect(self) -> bool:
        with self.__lock:
            if self.__started.is_set(): return True
            self.__netconf_handler.connect()
            # Connect triggers activation of sampling events that will be scheduled based on subscriptions
            self.__scheduler.start()
            self.__started.set()
            return True

    def Disconnect(self) -> bool:
        with self.__lock:
            # Trigger termination of loops and processes
            self.__terminate.set()
            # If not started, assume it is already disconnected
            if not self.__started.is_set(): return True
            # Disconnect triggers deactivation of sampling events
            self.__scheduler.shutdown()
            self.__netconf_handler.disconnect()
            return True

    @metered_subclass_method(METRICS_POOL)
    def GetInitialConfig(self) -> List[Tuple[str, Any]]:
        with self.__lock:
            return []

    @metered_subclass_method(METRICS_POOL)
    def GetConfig(self, resource_keys : List[str] = []) -> List[Tuple[str, Union[Any, None, Exception]]]:
        chk_type('resources', resource_keys, list)
        results = []
        with self.__lock:
            if len(resource_keys) == 0: resource_keys = ALL_RESOURCE_KEYS
            for i,resource_key in enumerate(resource_keys):
                str_resource_name = 'resource_key[#{:d}]'.format(i)
                try:
                    chk_string(str_resource_name, resource_key, allow_empty=False)
                    str_filter = get_filter(resource_key)
                    #self.__logger.debug('[GetConfig] str_filter = {:s}'.format(str(str_filter)))
                    if str_filter is None: str_filter = resource_key
                    xml_data = self.__netconf_handler.get(filter=str_filter).data_ele
                    if isinstance(xml_data, Exception): raise xml_data
                    results.extend(parse(resource_key, xml_data))
                except Exception as e: # pylint: disable=broad-except
                    MSG = 'Exception retrieving {:s}: {:s}'
                    self.__logger.exception(MSG.format(str_resource_name, str(resource_key)))
                    results.append((resource_key, e)) # if validation fails, store the exception
        return results

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(self, resources : List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        chk_type('resources', resources, list)
        if len(resources) == 0: return []
        with self.__lock:
            if self.__netconf_handler.use_candidate:
                with self.__netconf_handler.locked(target='candidate'):
                    results = edit_config(
                        self.__netconf_handler, self.__logger, resources, target='candidate',
                        commit_per_rule=self.__netconf_handler.commit_per_rule)
            else:
                results = edit_config(self.__netconf_handler, self.__logger, resources)
        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(self, resources : List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        chk_type('resources', resources, list)
        if len(resources) == 0: return []
        with self.__lock:
            if self.__netconf_handler.use_candidate:
                with self.__netconf_handler.locked(target='candidate'):
                    results = edit_config(
                        self.__netconf_handler, self.__logger, resources, target='candidate', delete=True,
                        commit_per_rule=self.__netconf_handler.commit_per_rule)
            else:
                results = edit_config(self.__netconf_handler, self.__logger, resources, delete=True)
        return results

    @metered_subclass_method(METRICS_POOL)
    def SubscribeState(self, subscriptions : List[Tuple[str, float, float]]) -> List[Union[bool, Exception]]:
        chk_type('subscriptions', subscriptions, list)
        if len(subscriptions) == 0: return []
        results = []
        resolver = anytree.Resolver(pathattr='name')
        with self.__lock:
            for i,subscription in enumerate(subscriptions):
                str_subscription_name = 'subscriptions[#{:d}]'.format(i)
                try:
                    chk_type(str_subscription_name, subscription, (list, tuple))
                    chk_length(str_subscription_name, subscription, min_length=3, max_length=3)
                    resource_key,sampling_duration,sampling_interval = subscription
                    chk_string(str_subscription_name + '.resource_key', resource_key, allow_empty=False)
                    resource_path = resource_key.split('/')
                    chk_float(str_subscription_name + '.sampling_duration', sampling_duration, min_value=0)
                    chk_float(str_subscription_name + '.sampling_interval', sampling_interval, min_value=0)
                except Exception as e: # pylint: disable=broad-except
                    MSG = 'Exception validating {:s}: {:s}'
                    self.__logger.exception(MSG.format(str_subscription_name, str(resource_key)))
                    results.append(e) # if validation fails, store the exception
                    continue

                start_date,end_date = None,None
                if sampling_duration >= 1.e-12:
                    start_date = datetime.utcnow()
                    end_date = start_date + timedelta(seconds=sampling_duration)

                job_id = 'k={:s}/d={:f}/i={:f}'.format(resource_key, sampling_duration, sampling_interval)
                job = self.__scheduler.add_job(
                    do_sampling, args=(self.__samples_cache, self.__logger, resource_key, self.__out_samples),
                    kwargs={}, id=job_id, trigger='interval', seconds=sampling_interval,
                    start_date=start_date, end_date=end_date, timezone=pytz.utc)

                subscription_path = resource_path + ['{:.3f}:{:.3f}'.format(sampling_duration, sampling_interval)]
                set_subnode_value(resolver, self.__subscriptions, subscription_path, job)
                results.append(True)
        return results

    @metered_subclass_method(METRICS_POOL)
    def UnsubscribeState(self, subscriptions : List[Tuple[str, float, float]]) -> List[Union[bool, Exception]]:
        chk_type('subscriptions', subscriptions, list)
        if len(subscriptions) == 0: return []
        results = []
        resolver = anytree.Resolver(pathattr='name')
        with self.__lock:
            for i,resource in enumerate(subscriptions):
                str_subscription_name = 'resources[#{:d}]'.format(i)
                try:
                    chk_type(str_subscription_name, resource, (list, tuple))
                    chk_length(str_subscription_name, resource, min_length=3, max_length=3)
                    resource_key,sampling_duration,sampling_interval = resource
                    chk_string(str_subscription_name + '.resource_key', resource_key, allow_empty=False)
                    resource_path = resource_key.split('/')
                    chk_float(str_subscription_name + '.sampling_duration', sampling_duration, min_value=0)
                    chk_float(str_subscription_name + '.sampling_interval', sampling_interval, min_value=0)
                except Exception as e: # pylint: disable=broad-except
                    MSG = 'Exception validating {:s}: {:s}'
                    self.__logger.exception(MSG.format(str_subscription_name, str(resource_key)))
                    results.append(e) # if validation fails, store the exception
                    continue

                subscription_path = resource_path + ['{:.3f}:{:.3f}'.format(sampling_duration, sampling_interval)]
                subscription_node = get_subnode(resolver, self.__subscriptions, subscription_path)

                # if not found, resource_node is None
                if subscription_node is None:
                    results.append(False)
                    continue

                job : Job = getattr(subscription_node, 'value', None)
                if job is None or not isinstance(job, Job):
                    raise Exception('Malformed subscription node or wrong resource key: {:s}'.format(str(resource)))
                job.remove()

                parent = subscription_node.parent
                children = list(parent.children)
                children.remove(subscription_node)
                parent.children = tuple(children)

                results.append(True)
        return results

    def GetState(self, blocking=False, terminate : Optional[threading.Event] = None) -> Iterator[Tuple[str, Any]]:
        while True:
            if self.__terminate.is_set(): break
            if terminate is not None and terminate.is_set(): break
            try:
                sample = self.__out_samples.get(block=blocking, timeout=0.1)
            except queue.Empty:
                if blocking: continue
                return
            if sample is None: continue
            yield sample
