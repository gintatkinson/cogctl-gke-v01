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

import anytree, json, logging, pytz, queue, re, threading
from datetime import datetime, timedelta
from typing import Any, Iterator, List, Optional, Tuple, Union
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.job import Job
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.type_checkers.Checkers import chk_float, chk_length, chk_string, chk_type
from device.service.driver_api._Driver import _Driver
from device.service.driver_api.AnyTreeTools import TreeNode, dump_subtree, get_subnode, set_subnode_value
from .Constants import SPECIAL_RESOURCE_MAPPINGS
from .SyntheticSamplingParameters import SyntheticSamplingParameters, do_sampling
from .Tools import compose_resource_endpoint

LOGGER = logging.getLogger(__name__)

RE_GET_ENDPOINT_FROM_INTERFACE = re.compile(r'^\/interface\[([^\]]+)\].*')

DRIVER_NAME = 'emulated'
METRICS_POOL = MetricsPool('Device', 'Driver', labels={'driver': DRIVER_NAME})

class EmulatedDriver(_Driver):
    def __init__(self, address : str, port : int, **settings) -> None:
        super().__init__(DRIVER_NAME, address, port, **settings)
        self.__lock = threading.Lock()
        self.__initial = TreeNode('.')
        self.__running = TreeNode('.')
        self.__subscriptions = TreeNode('.')

        endpoints = self.settings.get('endpoints', [])
        endpoint_resources = []
        for endpoint in endpoints:
            endpoint_resource = compose_resource_endpoint(endpoint)
            if endpoint_resource is None: continue
            endpoint_resources.append(endpoint_resource)
        self.SetConfig(endpoint_resources)

        self.__started = threading.Event()
        self.__terminate = threading.Event()
        self.__scheduler = BackgroundScheduler(daemon=True) # scheduler used to emulate sampling events
        self.__scheduler.configure(
            jobstores = {'default': MemoryJobStore()},
            executors = {'default': ThreadPoolExecutor(max_workers=1)},
            job_defaults = {'coalesce': False, 'max_instances': 3},
            timezone=pytz.utc)
        self.__out_samples = queue.Queue()
        self.__synthetic_sampling_parameters = SyntheticSamplingParameters()

    def Connect(self) -> bool:
        # If started, assume it is already connected
        if self.__started.is_set(): return True

        # Connect triggers activation of sampling events that will be scheduled based on subscriptions
        self.__scheduler.start()

        # Indicate the driver is now connected to the device
        self.__started.set()
        return True

    def Disconnect(self) -> bool:
        # Trigger termination of loops and processes
        self.__terminate.set()

        # If not started, assume it is already disconnected
        if not self.__started.is_set(): return True

        # Disconnect triggers deactivation of sampling events
        self.__scheduler.shutdown()
        return True

    @metered_subclass_method(METRICS_POOL)
    def GetInitialConfig(self) -> List[Tuple[str, Any]]:
        with self.__lock:
            return dump_subtree(self.__initial)

    @metered_subclass_method(METRICS_POOL)
    def GetConfig(self, resource_keys : List[str] = []) -> List[Tuple[str, Union[Any, None, Exception]]]:
        chk_type('resources', resource_keys, list)
        with self.__lock:
            if len(resource_keys) == 0: return dump_subtree(self.__running)
            results = []
            resolver = anytree.Resolver(pathattr='name')
            for i,resource_key in enumerate(resource_keys):
                str_resource_name = 'resource_key[#{:d}]'.format(i)
                try:
                    chk_string(str_resource_name, resource_key, allow_empty=False)
                    resource_key = SPECIAL_RESOURCE_MAPPINGS.get(resource_key, resource_key)
                    resource_path = resource_key.split('/')
                except Exception as e: # pylint: disable=broad-except
                    LOGGER.exception('Exception validating {:s}: {:s}'.format(str_resource_name, str(resource_key)))
                    results.append((resource_key, e)) # if validation fails, store the exception
                    continue

                resource_node = get_subnode(resolver, self.__running, resource_path, default=None)
                # if not found, resource_node is None
                if resource_node is None: continue
                results.extend(dump_subtree(resource_node))
            return results

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(self, resources : List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        chk_type('resources', resources, list)
        if len(resources) == 0: return []
        results = []
        resolver = anytree.Resolver(pathattr='name')
        with self.__lock:
            for i,resource in enumerate(resources):
                str_resource_name = 'resources[#{:d}]'.format(i)
                try:
                    chk_type(str_resource_name, resource, (list, tuple))
                    chk_length(str_resource_name, resource, min_length=2, max_length=2)
                    resource_key,resource_value = resource
                    chk_string(str_resource_name, resource_key, allow_empty=False)
                    resource_path = resource_key.split('/')
                except Exception as e: # pylint: disable=broad-except
                    LOGGER.exception('Exception validating {:s}: {:s}'.format(str_resource_name, str(resource_key)))
                    results.append(e) # if validation fails, store the exception
                    continue

                try:
                    resource_value = json.loads(resource_value)
                except: # pylint: disable=bare-except
                    pass

                set_subnode_value(resolver, self.__running, resource_path, resource_value)

                match = RE_GET_ENDPOINT_FROM_INTERFACE.match(resource_key)
                if match is not None:
                    endpoint_uuid = match.group(1)
                    if '.' in endpoint_uuid: endpoint_uuid = endpoint_uuid.split('.')[0]
                    self.__synthetic_sampling_parameters.set_endpoint_configured(endpoint_uuid)

                results.append(True)
        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(self, resources : List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        chk_type('resources', resources, list)
        if len(resources) == 0: return []
        results = []
        resolver = anytree.Resolver(pathattr='name')
        with self.__lock:
            for i,resource in enumerate(resources):
                str_resource_name = 'resources[#{:d}]'.format(i)
                try:
                    chk_type(str_resource_name, resource, (list, tuple))
                    chk_length(str_resource_name, resource, min_length=2, max_length=2)
                    resource_key,_ = resource
                    chk_string(str_resource_name, resource_key, allow_empty=False)
                    resource_path = resource_key.split('/')
                except Exception as e: # pylint: disable=broad-except
                    LOGGER.exception('Exception validating {:s}: {:s}'.format(str_resource_name, str(resource_key)))
                    results.append(e) # if validation fails, store the exception
                    continue

                resource_node = get_subnode(resolver, self.__running, resource_path, default=None)
                # if not found, resource_node is None
                if resource_node is None:
                    results.append(False)
                    continue

                match = RE_GET_ENDPOINT_FROM_INTERFACE.match(resource_key)
                if match is not None:
                    endpoint_uuid = match.group(1)
                    if '.' in endpoint_uuid: endpoint_uuid = endpoint_uuid.split('.')[0]
                    self.__synthetic_sampling_parameters.unset_endpoint_configured(endpoint_uuid)

                parent = resource_node.parent
                children = list(parent.children)
                children.remove(resource_node)
                parent.children = tuple(children)
                results.append(True)
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
                    LOGGER.exception('Exception validating {:s}: {:s}'.format(str_subscription_name, str(resource_key)))
                    results.append(e) # if validation fails, store the exception
                    continue

                start_date,end_date = None,None
                if sampling_duration <= 1.e-12:
                    start_date = datetime.utcnow()
                    end_date = start_date + timedelta(seconds=sampling_duration)

                job_id = 'k={:s}/d={:f}/i={:f}'.format(resource_key, sampling_duration, sampling_interval)
                job = self.__scheduler.add_job(
                    do_sampling, args=(self.__synthetic_sampling_parameters, resource_key, self.__out_samples),
                    kwargs={}, id=job_id, trigger='interval', seconds=sampling_interval, start_date=start_date,
                    end_date=end_date, timezone=pytz.utc)

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
                    LOGGER.exception('Exception validating {:s}: {:s}'.format(str_subscription_name, str(resource_key)))
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
