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

from common.method_wrappers.ServiceExceptions import InvalidArgumentsException
from common.proto.context_pb2 import DeviceId
from ._Builder import get_uuid_from_string, get_uuid_random
import logging

def channel_get_uuid(
    channel_name : str , device_id : str, allow_random : bool = False
) -> str:
    if len(channel_name) > 0:
        return get_uuid_from_string(channel_name) + device_id
    if allow_random: return get_uuid_random()

    raise InvalidArgumentsException([
        ('channel uuid', channel_name),
    ], extra_details=['Channel name is required to produce a channel UUID'])

def interface_get_uuid(
    interface_name :str , allow_random : bool = False
) -> str:
    if len(interface_name) > 0:
        return get_uuid_from_string(interface_name)
    if allow_random: return get_uuid_random()

    raise InvalidArgumentsException([
        ('interface uuid', interface_name),
    ], extra_details=['interface name is required to produce a interface UUID'])

def transponder_get_uuid(
    opticalconfig_id : str, allow_random : bool = False
) -> str:
    if opticalconfig_id is not None:
        return get_uuid_from_string(f"{opticalconfig_id}-transponder")
    if allow_random: return get_uuid_random()

    raise InvalidArgumentsException([
        ('transponder uuid', opticalconfig_id),
       
    ], extra_details=['opticalconfig id is required to produce a transponder UUID'])

def roadm_get_uuid(
    opticalconfig_id : str, allow_random : bool = False
) -> str:
    if opticalconfig_id is not None:
        return get_uuid_from_string(f"{opticalconfig_id}-roadm")
    if allow_random: return get_uuid_random()

    raise InvalidArgumentsException([
        ('roadm uuid', opticalconfig_id),
       
    ], extra_details=['opticalconfig id is required to produce a roadm UUID'])

def opticalconfig_get_uuid(
    device_id : DeviceId, allow_random : bool = False
) -> str:
    device_uuid = device_id.device_uuid.uuid
    if (len(device_uuid)>0):
        return get_uuid_from_string(f"{device_uuid}_opticalconfig")
    if allow_random: return get_uuid_random()

    raise InvalidArgumentsException([
        ('DeviceId ', device_id),
    ], extra_details=['device_id is required to produce a OpticalConfig UUID'])


def ob_get_uuid(
    ob_name:str , allow_random : bool = False
) -> str:
   
    if ( ob_name is not None):
        
        
      result = get_uuid_from_string(f'ob_{ob_name}')
      logging.info(f'get_ob_uuid {result}')
      return result 
    if allow_random: return get_uuid_random()

    raise InvalidArgumentsException([
        ('ob_name ', ob_name),
    ], extra_details=['ob_name is required to produce a Optical band UUID'])



    
def interface_get_uuid(
    interface_name :str , device_id:str, allow_random : bool = False
) -> str:
    

    if len(interface_name) > 0:
        return get_uuid_from_string(interface_name) + device_id
    if allow_random: return get_uuid_random()

    raise InvalidArgumentsException([
        ('interface uuid', interface_name),
       
    ], extra_details=['Interface name is required to produce a interface UUID'])
