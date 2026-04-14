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


import copy, json, logging, re, threading
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.tools.rest_conf.client.RestConfClient import RestConfClient
from common.type_checkers.Checkers import chk_string, chk_type
from device.service.driver_api._Driver import _Driver, RESOURCE_ENDPOINTS, RESOURCE_SERVICES
from device.service.driver_api.ImportTopologyEnum import ImportTopologyEnum, get_import_topology
from .handlers.SubscriptionHandler import (
    SubscribedNotificationsSchema, SubscriptionHandler, UnsubscribedNotificationsSchema
)
from .TfsApiClient import TfsApiClient


LOGGER = logging.getLogger(__name__)


ALL_RESOURCE_KEYS = [
    RESOURCE_ENDPOINTS,
    RESOURCE_SERVICES,
]


RE_IETF_SLICE_DATA = re.compile(r'^\/service\[([^\]]+)\]\/IETFSlice$')


DRIVER_NAME = 'ietf_slice'
METRICS_POOL = MetricsPool('Device', 'Driver', labels={'driver': DRIVER_NAME})


class IetfSliceDriver(_Driver):
    def __init__(self, address : str, port : str, **settings) -> None:
        super().__init__(DRIVER_NAME, address, int(port), **settings)
        self.__lock = threading.Lock()
        self.__started = threading.Event()
        self.__terminate = threading.Event()

        username = self.settings.get('username')
        password = self.settings.get('password')
        scheme   = self.settings.get('scheme', 'http')
        timeout  = int(self.settings.get('timeout', 60))
        self.tac = TfsApiClient(
            self.address, self.port, scheme=scheme, username=username,
            password=password, timeout=timeout
        )

        restconf_settings = copy.deepcopy(settings)
        restconf_settings.pop('base_url', None)
        restconf_settings.pop('import_topology', None)
        restconf_settings['logger'] = logging.getLogger(__name__ + '.RestConfClient')
        self._rest_conf_client = RestConfClient(address, port=port, **restconf_settings)
        self._handler_subscription = SubscriptionHandler(self._rest_conf_client)

        # Options are:
        #    disabled --> just import endpoints as usual
        #    devices  --> imports sub-devices but not links connecting them.
        #                 (a remotely-controlled transport domain might exist between them)
        #    topology --> imports sub-devices and links connecting them.
        #                 (not supported by XR driver)
        self.__import_topology = get_import_topology(self.settings, default=ImportTopologyEnum.DEVICES)


    def Connect(self) -> bool:
        with self.__lock:
            if self.__started.is_set(): return True
            checked = self.tac.check_credentials(raise_if_fail=False)
            if checked: self.__started.set()
            return checked


    def Disconnect(self) -> bool:
        with self.__lock:
            self.__terminate.set()
            return True


    @metered_subclass_method(METRICS_POOL)
    def GetInitialConfig(self) -> List[Tuple[str, Any]]:
        with self.__lock:
            return []


    @metered_subclass_method(METRICS_POOL)
    def GetConfig(
        self, resource_keys : List[str] = []
    ) -> List[Tuple[str, Union[Any, None, Exception]]]:
        chk_type('resources', resource_keys, list)
        results = []
        with self.__lock:
            self.tac.check_credentials()
            if len(resource_keys) == 0: resource_keys = ALL_RESOURCE_KEYS

            for i, resource_key in enumerate(resource_keys):
                str_resource_name = 'resource_key[#{:d}]'.format(i)
                try:
                    chk_string(str_resource_name, resource_key, allow_empty=False)
                    if resource_key == RESOURCE_ENDPOINTS:
                        # return endpoints through TFS NBI API and list-devices method
                        results.extend(self.tac.get_devices_endpoints(self.__import_topology))
                    elif resource_key == RESOURCE_SERVICES:
                        slices_data = self.tac.list_slices()
                        slices_list = (
                            slices_data
                            .get('network-slice-services', dict())
                            .get('slice-service', list())
                        )
                        for slice_data in slices_list:
                            slice_name = slice_data['id']
                            slice_resource_key = '/service[{:s}]/IETFSlice'.format(str(slice_name))
                            results.append((slice_resource_key, slice_data))
                    else:
                        match_slice_data = RE_IETF_SLICE_DATA.match(resource_key)
                        if match_slice_data is not None:
                            slice_name = match_slice_data.groups()[0]
                            slices_data = self.tac.retrieve_slice(slice_name)
                            slices_list = (
                                slices_data
                                .get('network-slice-services', dict())
                                .get('slice-service', list())
                            )
                            for slice_data in slices_list:
                                slice_name = slice_data['id']
                                slice_resource_key = '/service[{:s}]/IETFSlice'.format(str(slice_name))
                                results.append((slice_resource_key, slice_data))
                        else:
                            results.append((resource_key, None))
                except Exception as e:
                    MSG = 'Unhandled error processing {:s}: resource_key({:s})'
                    LOGGER.exception(MSG.format(str_resource_name, str(resource_key)))
                    results.append((resource_key, e))
        return results


    @metered_subclass_method(METRICS_POOL)
    def SetConfig(
        self, resources : List[Tuple[str, Any]]
    ) -> List[Union[bool, Exception]]:
        results = []
        if len(resources) == 0: return results
        with self.__lock:
            for i, resource in enumerate(resources):
                str_resource_name = 'resource_key[#{:d}]'.format(i)
                LOGGER.info('[SetConfig] resource = {:s}'.format(str(resource)))
                resource_key, resource_value = resource

                if not RE_IETF_SLICE_DATA.match(resource_key): continue

                try:
                    resource_value = json.loads(resource_value)
                    self.tac.create_slice(resource_value)
                    results.append((resource_key, True))
                except Exception as e:
                    MSG = 'Unhandled error processing SET {:s}: resource_key({:s})'
                    LOGGER.exception(MSG.format(str_resource_name, str(resource_key)))
                    results.append((resource_key, e))
        return results


    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(
        self, resources : List[Tuple[str, Any]]
    ) -> List[Union[bool, Exception]]:
        results = []
        if len(resources) == 0: return results
        with self.__lock:
            for i, resource in enumerate(resources):
                str_resource_name = 'resource_key[#{:d}]'.format(i)
                LOGGER.info('[DeleteConfig] resource = {:s}'.format(str(resource)))
                resource_key, resource_value = resource

                if not RE_IETF_SLICE_DATA.match(resource_key): continue

                try:
                    resource_value = json.loads(resource_value)
                    slice_name = resource_value['network-slice-services']['slice-service'][0]['id']
                    self.tac.delete_slice(slice_name)
                    results.append((resource_key, True))
                except Exception as e:
                    MSG = 'Unhandled error processing DELETE {:s}: resource_key({:s})'
                    LOGGER.exception(MSG.format(str_resource_name, str(resource_key)))
                    results.append((resource_key, e))
        return results


    @metered_subclass_method(METRICS_POOL)
    def SubscribeState(
        self, subscriptions : List[Tuple[str, float, float]]
    ) -> List[Union[bool, Dict[str, Any], Exception]]:
        if len(subscriptions) != 1:
            raise ValueError('IETF Slice Driver supports only one subscription at a time')
        s = subscriptions[0]
        uri = s[0]
        #sampling_duration = s[1]
        sampling_interval = s[2]
        s_data : SubscribedNotificationsSchema = {
            'ietf-subscribed-notifications:input': {
                'datastore': 'operational',
                'ietf-yang-push:datastore-xpath-filter': uri,
                'ietf-yang-push:periodic': {'ietf-yang-push:period': str(sampling_interval)},
            }
        }
        s_id = self._handler_subscription.subscribe(s_data)
        return [s_id]


    @metered_subclass_method(METRICS_POOL)
    def UnsubscribeState(
        self, subscriptions : List[Tuple[str, float, float]]
    ) -> List[Union[bool, Dict[str, Any], Exception]]:
        if len(subscriptions) != 1:
            raise ValueError('IETF Slice Driver supports only one subscription at a time')
        s = subscriptions[0]
        identifier = s[0]
        s_data : UnsubscribedNotificationsSchema = {
            'ietf-subscribed-notifications:input': {
                'id': int(identifier),
            }
        }
        self._handler_subscription.unsubscribe(s_data)
        return [True]


    def GetState(
        self, blocking=False, terminate : Optional[threading.Event] = None
    ) -> Iterator[Tuple[float, str, Any]]:
        return []
