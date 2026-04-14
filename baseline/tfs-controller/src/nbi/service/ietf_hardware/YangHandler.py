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
from typing import Dict, Optional
import datetime
import json
import logging
import libyang
import os
import re

LOGGER = logging.getLogger(__name__)
YANG_DIR = os.path.join(os.path.dirname(__file__), 'yang')
YANG_MODULES = [
    'iana-hardware',
    'ietf-hardware',
    'ietf-network-hardware-inventory'
]

class YangHandler:
    def __init__(self) -> None:
        self._yang_context = libyang.Context(YANG_DIR)
        for yang_module_name in YANG_MODULES:
            LOGGER.info('Loading module: {:s}'.format(str(yang_module_name)))
            self._yang_context.load_module(yang_module_name).feature_enable_all()

    def parse_to_dict(self, message : Dict) -> Dict:
        yang_module = self._yang_context.get_module('ietf-network-hardware-inventory')
        dnode : Optional[libyang.DNode] = yang_module.parse_data_dict(
            message, validate_present=True, validate=True, strict=True
        )
        if dnode is None: raise Exception('Unable to parse Message({:s})'.format(str(message)))
        message = dnode.print_dict()
        dnode.free()
        return message

    @staticmethod
    def convert_to_iso_date(date_str: str) -> Optional[str]:
        date_str = date_str.strip('"')
        pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[\+\-]\d{2}:\d{2})"
        if re.match(pattern, date_str):
            return date_str 
        else:
            try:
                datetime_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                iso_date = datetime_obj.isoformat() + "Z"
                return iso_date
            except ValueError:
                return None  

    def compose(self, device : Device) -> Dict:
        hardware = self._yang_context.create_data_path('/ietf-network-hardware-inventory:network-hardware-inventory')
        network_elements = hardware.create_path('network-elements')

        network_element = network_elements.create_path('network-element[uuid="{:s}"]'.format(device.device_id.device_uuid.uuid))
        network_element.create_path('uuid', device.device_id.device_uuid.uuid)
        network_element.create_path('name', device.name)
        components = network_element.create_path('components')
        physical_index = 1

        for component in device.components:
            attributes = component.attributes
            component_new = components.create_path('component[uuid="{:s}"]'.format(component.component_uuid.uuid))
            component_new.create_path('name', component.name)
            component_type = component.type
            if component_type == "TRANSCEIVER" :
                component_type = "module"
            if component_type == "FRU" :
                component_type = "slack"

            component_type = component_type.replace("_", "-").lower()
            component_type = 'iana-hardware:' + component_type
            component_new.create_path('class', component_type)
            physical_index += 1
            component_new.create_path('description', attributes["description"].replace('/"',""))
            if "CHASSIS" not in component.type:
                parent_component_references = component_new.create_path('parent-component-references')
                parent = parent_component_references.create_path('component-reference[index="{:d}"]'.format(physical_index))
                for component_parent in device.components:
                    if component.parent == component_parent.name : 
                      parent.create_path('uuid', component_parent.component_uuid.uuid)
                      break
            if attributes["mfg-date"] != "":
                mfg_date = self.convert_to_iso_date(attributes["mfg-date"])
                component_new.create_path('mfg-date', mfg_date)

            component_new.create_path('hardware-rev', attributes["hardware-rev"])
            component_new.create_path('software-rev', attributes["software-rev"])
            component_new.create_path('firmware-rev', attributes["firmware-version"])
            component_new.create_path('serial-num', attributes["serial-num"])
            component_new.create_path('mfg-name', attributes["mfg-name"])
            if attributes["removable"]:
                removable = attributes["removable"].lower()
                if 'true' in removable:
                    component_new.create_path('is-fru', True)
                elif 'false' in removable:
                    component_new.create_path('is-fru', False)

            if attributes["id"]:
                try:
                    if  "CHASSIS" in component.type :  
                        component_new.create_path('parent-rel-pos', 0)
                    else:                        
                        parent_rel_pos = int(attributes["id"].replace("\"", ""))
                        component_new.create_path('parent-rel-pos', parent_rel_pos)
                except ValueError:
                    LOGGER.info('ERROR:{:s} '.format(component.name ))
                    continue

            component_new.create_path('uri', component.name)
            component_new.create_path('uuid', component.component_uuid.uuid)
            for child in device.components:
                if component.name == child.parent : 
                    component_new.create_path('contained-child', child.component_uuid.uuid)

        return json.loads(hardware.print_mem('json'))

    def destroy(self) -> None:
        self._yang_context.destroy()
