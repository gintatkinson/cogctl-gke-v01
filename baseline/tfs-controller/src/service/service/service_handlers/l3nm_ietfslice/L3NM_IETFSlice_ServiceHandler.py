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


import ipaddress, logging
from typing import Any, List, Optional, Tuple, Union
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.proto.context_pb2 import ConfigRule, DeviceId, Service
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.ConfigRule import json_config_rule_delete, json_config_rule_set
from common.tools.object_factory.Device import json_device_id
from common.type_checkers.Checkers import chk_type
from service.service.service_handler_api._ServiceHandler import _ServiceHandler
from service.service.service_handler_api.Tools import get_device_endpoint_uuids
from service.service.task_scheduler.TaskExecutor import TaskExecutor
from .DataStoreDelta import DataStoreDelta
from .Tools import get_device_endpoint_name


LOGGER = logging.getLogger(__name__)


METRICS_POOL = MetricsPool('Service', 'Handler', labels={'handler': 'l3nm_ietfslice'})


class L3NM_IETFSlice_ServiceHandler(_ServiceHandler):
    def __init__(  # pylint: disable=super-init-not-called
        self, service: Service, task_executor: TaskExecutor, **settings
    ) -> None:
        self.__service = service
        self.__task_executor = task_executor

    @metered_subclass_method(METRICS_POOL)
    def SetEndpoint(
        self,
        endpoints: List[Tuple[str, str, Optional[str]]],
        connection_uuid: Optional[str] = None,
    ) -> List[Union[bool, Exception]]:
        LOGGER.debug('[SetEndpoint] service={:s}'.format(grpc_message_to_json_string(self.__service)))
        LOGGER.debug('[SetEndpoint] endpoints={:s}'.format(str(endpoints)))
        LOGGER.debug('[SetEndpoint] connection_uuid={:s}'.format(str(connection_uuid)))

        chk_type('endpoints', endpoints, list)
        if len(endpoints) == 0: return []

        results = []
        try:
            # 1. Identify source and destination devices
            src_device_uuid, src_endpoint_uuid = get_device_endpoint_uuids(endpoints[0])
            src_device_obj = self.__task_executor.get_device(DeviceId(**json_device_id(src_device_uuid)))
            src_device_name = src_device_obj.name
            src_endpoint_name = get_device_endpoint_name(src_device_obj, src_endpoint_uuid)
            src_controller = self.__task_executor.get_device_controller(src_device_obj)

            dst_device_uuid, dst_endpoint_uuid = get_device_endpoint_uuids(endpoints[-1])
            dst_device_obj = self.__task_executor.get_device(DeviceId(**json_device_id(dst_device_uuid)))
            dst_device_name = dst_device_obj.name
            dst_endpoint_name = get_device_endpoint_name(dst_device_obj, dst_endpoint_uuid)
            dst_controller = self.__task_executor.get_device_controller(dst_device_obj)


            # 2. Identify controller to be used
            if src_controller.device_id.device_uuid.uuid != dst_controller.device_id.device_uuid.uuid:
                raise Exception('Different Src-Dst devices not supported by now')
            controller = src_controller  # same device controller


            # 3. Load DataStore configuration
            datastore_delta = DataStoreDelta(self.__service)
            candidate_slice = datastore_delta.candidate_data

            if len(candidate_slice) != 1:
                MSG = 'Unsupported number of Slices[{:d}]({:s})'
                raise Exception(MSG.format(len(candidate_slice), str(candidate_slice)))
            candidate_slice = candidate_slice[0]

            slice_name = candidate_slice['id']

            conn_groups = candidate_slice.get('connection-groups', dict())


            # 4. Adapt SDPs
            candidate_sdps = candidate_slice.get('sdps', dict()).get('sdp', list())
            if len(candidate_sdps) != 2:
                MSG = 'Unsupported number of SDPs[{:d}]({:s})'
                raise Exception(MSG.format(len(candidate_sdps), str(candidate_sdps)))

            sdp_dict = {sdp['node-id'] : sdp for sdp in candidate_sdps}
            if src_device_name in sdp_dict and dst_device_name not in sdp_dict:
                src_device_sdp = sdp_dict.get(src_device_name)

                other_device_names = set(sdp_dict.keys())
                other_device_names.remove(src_device_name)
                unneeded_sdp_id = other_device_names.pop()

                dst_device_sdp = sdp_dict.get(unneeded_sdp_id)
                dst_device_sdp['node-id'] = dst_device_name

                try:
                    dst_mgmt_ip_address = str(ipaddress.ip_address(dst_device_name))
                except ValueError:
                    dst_mgmt_ip_address = '0.0.0.0'
                dst_device_sdp['sdp-ip-address'] = [dst_mgmt_ip_address]

                dst_ac = dst_device_sdp['attachment-circuits']['attachment-circuit'][0]
                dst_ac['id'] = 'AC {:s}'.format(str(dst_device_name))
                dst_ac['description'] = 'AC {:s}'.format(str(dst_device_name))
                dst_ac['ac-node-id'] = dst_device_name
                dst_ac['ac-tp-id'] = dst_endpoint_name

            elif dst_device_name in sdp_dict and src_device_name not in sdp_dict:
                dst_device_sdp = sdp_dict.get(dst_device_name)

                other_device_names = set(sdp_dict.keys())
                other_device_names.remove(dst_device_name)
                unneeded_sdp_id = other_device_names.pop()

                src_device_sdp = sdp_dict.get(unneeded_sdp_id)
                src_device_sdp['node-id'] = src_device_name

                try:
                    src_mgmt_ip_address = str(ipaddress.ip_address(src_device_name))
                except ValueError:
                    src_mgmt_ip_address = '0.0.0.0'
                src_device_sdp['sdp-ip-address'] = [src_mgmt_ip_address]

                src_ac = src_device_sdp['attachment-circuits']['attachment-circuit'][0]
                src_ac['id'] = 'AC {:s}'.format(str(src_device_name))
                src_ac['description'] = 'AC {:s}'.format(str(src_device_name))
                src_ac['ac-node-id'] = src_device_name
                src_ac['ac-tp-id'] = src_endpoint_name

            else:
                MSG = 'Unsupported case: sdp_dict={:s} src_device_name={:s} dst_device_name={:s}'
                raise Exception(MSG.format(str(sdp_dict), str(src_device_name), str(dst_device_name)))

            

            # 5. Compose slice and setup it

            slice_data_model = {'network-slice-services': {'slice-service': [{
                'id': slice_name,
                'description': slice_name,
                'sdps': {'sdp': [src_device_sdp, dst_device_sdp]},
                'connection-groups': conn_groups,
            }]}}

            del controller.device_config.config_rules[:]
            controller.device_config.config_rules.append(ConfigRule(**json_config_rule_set(
                '/service[{:s}]/IETFSlice'.format(slice_name), slice_data_model
            )))
            self.__task_executor.configure_device(controller)
        except Exception as e:
            LOGGER.exception('Unable to handle Slice Setup')
            results.append(e)
        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteEndpoint(
        self,
        endpoints: List[Tuple[str, str, Optional[str]]],
        connection_uuid: Optional[str] = None,
    ) -> List[Union[bool, Exception]]:
        LOGGER.debug('[DeleteEndpoint] service={:s}'.format(grpc_message_to_json_string(self.__service)))
        LOGGER.debug('[DeleteEndpoint] endpoints={:s}'.format(str(endpoints)))
        LOGGER.debug('[DeleteEndpoint] connection_uuid={:s}'.format(str(connection_uuid)))

        chk_type("endpoints", endpoints, list)
        if len(endpoints) == 0:
            return []
        service_uuid = self.__service.service_id.service_uuid.uuid
        results = []
        try:
            src_device_uuid, src_endpoint_uuid = get_device_endpoint_uuids(endpoints[0])
            src_device_obj = self.__task_executor.get_device(
                DeviceId(**json_device_id(src_device_uuid))
            )
            controller = self.__task_executor.get_device_controller(src_device_obj)

            datastore_delta = DataStoreDelta(self.__service)
            running_slice = datastore_delta.running_data

            if len(running_slice) != 1:
                MSG = 'Unsupported number of Slices[{:d}]({:s})'
                raise Exception(MSG.format(len(running_slice), str(running_slice)))
            running_slice = running_slice[0]
            slice_name = running_slice['id']

            slice_data_model = {'network-slice-services': {'slice-service': [{
                'id': slice_name,
            }]}}

            del controller.device_config.config_rules[:]
            controller.device_config.config_rules.append(ConfigRule(**json_config_rule_delete(
                '/service[{:s}]/IETFSlice'.format(slice_name), slice_data_model
            )))
            self.__task_executor.configure_device(controller)
            results.append(True)
        except Exception as e:
            LOGGER.exception('Unable to handle Slice Tear Down')
            results.append(e)
        return results

    @metered_subclass_method(METRICS_POOL)
    def SetConstraint(
        self, constraints: List[Tuple[str, Any]]
    ) -> List[Union[bool, Exception]]:
        chk_type('constraints', constraints, list)
        if len(constraints) == 0: return []
        MSG = '[SetConstraint] Method not implemented. Constraints({:s}) are being ignored.'
        LOGGER.warning(MSG.format(str(constraints)))
        return [True for _ in constraints]

    @metered_subclass_method(METRICS_POOL)
    def DeleteConstraint(
        self, constraints: List[Tuple[str, Any]]
    ) -> List[Union[bool, Exception]]:
        chk_type('constraints', constraints, list)
        if len(constraints) == 0: return []
        MSG = '[DeleteConstraint] Method not implemented. Constraints({:s}) are being ignored.'
        LOGGER.warning(MSG.format(str(constraints)))
        return [True for _ in constraints]

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(
        self, resources: List[Tuple[str, Any]]
    ) -> List[Union[bool, Exception]]:
        chk_type('resources', resources, list)
        if len(resources) == 0: return []
        MSG = '[SetConfig] Method not implemented. Resources({:s}) are being ignored.'
        LOGGER.warning(MSG.format(str(resources)))
        return [True for _ in resources]

    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(
        self, resources: List[Tuple[str, Any]]
    ) -> List[Union[bool, Exception]]:
        chk_type('resources', resources, list)
        if len(resources) == 0: return []
        MSG = '[DeleteConfig] Method not implemented. Resources({:s}) are being ignored.'
        LOGGER.warning(MSG.format(str(resources)))
        return [True for _ in resources]
