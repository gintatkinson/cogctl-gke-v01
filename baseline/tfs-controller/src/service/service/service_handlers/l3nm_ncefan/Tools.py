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


from common.proto.context_pb2 import Device


def get_device_endpoint_name(device_obj : Device, endpoint_uuid : str) -> str:
    '''
    Given a device object and an endpoint UUID, return the device endpoint name.
    Raises an exception if not found.
    '''
    for d_ep in device_obj.device_endpoints:
        if d_ep.endpoint_id.endpoint_uuid.uuid == endpoint_uuid:
            return d_ep.name

    device_uuid = str(device_obj.device_id.device_uuid.uuid)
    device_name = str(device_obj.name)
    MSG = 'Device({:s},{:s})/Endpoint({:s}) not found'
    raise Exception(MSG.format(device_uuid, device_name, str(endpoint_uuid)))
