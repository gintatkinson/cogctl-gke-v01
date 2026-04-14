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

import json, logging, grpc
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.proto.context_pb2 import Empty, Device, DeviceId
from common.proto.pluggables_pb2_grpc import PluggablesServiceServicer
from common.proto.pluggables_pb2 import (
    Pluggable, CreatePluggableRequest, ListPluggablesRequest, ListPluggablesResponse, 
    GetPluggableRequest, DeletePluggableRequest, ConfigurePluggableRequest)
from common.method_wrappers.ServiceExceptions import (
    NotFoundException, AlreadyExistsException, InvalidArgumentException, OperationFailedException)
from common.tools.object_factory.ConfigRule import json_config_rule_set
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from .config_translator import translate_pluggable_config_to_netconf, create_config_rule_from_dict

LOGGER = logging.getLogger(__name__)
METRICS_POOL = MetricsPool('Pluggables', 'ServicegRPC')

class PluggablesServiceServicerImpl(PluggablesServiceServicer):
    def __init__(self):
        LOGGER.info('Initiate PluggablesService')
        self.pluggables = {}  # In-memory store for pluggables
        self.context_client = ContextClient()
        self.device_client = DeviceClient()

    def _push_config_to_device(self, device_uuid: str, pluggable_index: int, pluggable_config):  # type: ignore
        """
        Push pluggable configuration to the actual device via DeviceClient.
        Args:
            device_uuid: UUID of the target device
            pluggable_index: Index of the pluggable
            pluggable_config: PluggableConfig protobuf message
        """
        LOGGER.info(f"Configuring device {device_uuid}, pluggable index {pluggable_index}")
        
        # Step 1: Get the device from Context service (to extract IP address)
        try:
            device = self.context_client.GetDevice(DeviceId(device_uuid={'uuid': device_uuid}))  # type: ignore
            LOGGER.info(f"Retrieved device from Context: {device.name}")
        except grpc.RpcError as e:
            LOGGER.error(f"Failed to get device {device_uuid} from Context: {e}")
            raise
        
        # Translate pluggable config to NETCONF format
        component_name = f"channel-{pluggable_index}"
        netconf_config = translate_pluggable_config_to_netconf(pluggable_config, component_name=component_name)
        
        LOGGER.info(f"Translated pluggable config to NETCONF format: {netconf_config}")
        
        # Step 2: Create configuration rule with generic pluggable template
        # Use template index 1 for standard pluggable configuration
        template_index = 1
        resource_key = f"/pluggable/{template_index}/config"
        
        # Create config rule dict and convert to protobuf
        config_json = json.dumps(netconf_config)
        config_rule_dict = json_config_rule_set(resource_key, config_json)
        config_rule = create_config_rule_from_dict(config_rule_dict)
        
        # Step 3: Create a minimal Device object with only the DSCM config rule
        config_device = Device()
        config_device.device_id.device_uuid.uuid = device_uuid  # type: ignore
        config_device.device_config.config_rules.append(config_rule)  # type: ignore
        
        LOGGER.info(f"Created minimal device with config rule: resource_key={resource_key}")

        # Step 4: Call ConfigureDevice to push the configuration
        try:
            device_id = self.device_client.ConfigureDevice(config_device)
            LOGGER.info(f"Successfully configured device {device_id.device_uuid.uuid}")  # type: ignore
        except grpc.RpcError as e:
            LOGGER.error(f"Failed to configure device {device_uuid}: {e}")
            raise InvalidArgumentException(
                'Device configuration', f'{device_uuid}:{pluggable_index}', extra_details=str(e))

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def CreatePluggable(
        self, request: CreatePluggableRequest, context: grpc.ServicerContext # type: ignore
    ) -> Pluggable: # type: ignore
        LOGGER.info("Received gRPC message object: {:}".format(request))
        
        device_uuid = request.device.device_uuid.uuid
        
        if request.preferred_pluggable_index >= 0:
            pluggable_index = request.preferred_pluggable_index
        else:
            pluggable_index = -1
        
        pluggable_key = f"{device_uuid}:{pluggable_index}"
        
        if pluggable_key in self.pluggables:
            LOGGER.warning(f"Pluggable already exists at device {device_uuid} index {pluggable_index}")
            raise AlreadyExistsException('Pluggable', pluggable_key)
        
        pluggable = Pluggable()
        
        pluggable.id.device.device_uuid.uuid = device_uuid
        pluggable.id.pluggable_index         = pluggable_index
        
        if request.HasField('initial_config'):
            pluggable.config.CopyFrom(request.initial_config)
            # The below code ensures ID consistency across all levels are maintained
            # User might send incorrect/inconsistent IDs in nested structures
            pluggable.config.id.device.device_uuid.uuid = device_uuid
            pluggable.config.id.pluggable_index         = pluggable_index
            
            for dsc_group in pluggable.config.dsc_groups:
                dsc_group.id.pluggable.device.device_uuid.uuid = device_uuid
                dsc_group.id.pluggable.pluggable_index         = pluggable_index
                
                for subcarrier in dsc_group.subcarriers:
                    subcarrier.id.group.pluggable.device.device_uuid.uuid = device_uuid
                    subcarrier.id.group.pluggable.pluggable_index         = pluggable_index
        
        pluggable.state.id.device.device_uuid.uuid = device_uuid
        pluggable.state.id.pluggable_index         = pluggable_index

        # Verify device exists in Context service
        try:
            device = self.context_client.GetDevice(DeviceId(device_uuid={'uuid': device_uuid}))  # type: ignore
            LOGGER.info(f"Device {device_uuid} found in Context service: {device.name}")
        except grpc.RpcError as e:
            LOGGER.error(f"Device {device_uuid} not found in Context service: {e}")
            raise NotFoundException(
                'Device', device_uuid, extra_details='Device must exist before creating pluggable')
        
        # If initial_config is provided, push configuration to device
        if request.HasField('initial_config') and len(pluggable.config.dsc_groups) > 0:
            LOGGER.info(f"Pushing initial configuration to device {device_uuid}")
            try:
                self._push_config_to_device(device_uuid, pluggable_index, pluggable.config)
            except Exception as e:
                LOGGER.error(f"Failed to push initial config to device: {e}")
                raise OperationFailedException(
                    'Push initial pluggable configuration', extra_details=str(e))
        
        self.pluggables[pluggable_key] = pluggable
        
        LOGGER.info(f"Created pluggable: device={device_uuid}, index={pluggable_index}")
        return pluggable

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetPluggable(
        self, request: GetPluggableRequest, context: grpc.ServicerContext # type: ignore
    ) -> Pluggable: # type: ignore
        LOGGER.info("Received gRPC message object: {:}".format(request))
        
        device_uuid     = request.id.device.device_uuid.uuid
        pluggable_index = request.id.pluggable_index
        pluggable_key   = f"{device_uuid}:{pluggable_index}"
        
        if pluggable_key not in self.pluggables:
            LOGGER.warning(f'No matching pluggable found: device={device_uuid}, index={pluggable_index}')
            raise NotFoundException('Pluggable', pluggable_key)
        
        pluggable = self.pluggables[pluggable_key]
        
        if request.view_level == 1:
            filtered = Pluggable()
            filtered.id.CopyFrom(pluggable.id)
            filtered.config.CopyFrom(pluggable.config)
            return filtered
        elif request.view_level == 2:
            filtered = Pluggable()
            filtered.id.CopyFrom(pluggable.id)
            filtered.state.CopyFrom(pluggable.state)
            return filtered
        else:
            return pluggable
    
    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def DeletePluggable(
        self, request: DeletePluggableRequest, context: grpc.ServicerContext # type: ignore
    ) -> Empty: # type: ignore
        LOGGER.info("Received gRPC message object: {:}".format(request))
        
        device_uuid     = request.id.device.device_uuid.uuid
        pluggable_index = request.id.pluggable_index
        pluggable_key   = f"{device_uuid}:{pluggable_index}"
        
        if pluggable_key not in self.pluggables:
            LOGGER.info(f'No matching pluggable found: device={device_uuid}, index={pluggable_index}')
            raise NotFoundException('Pluggable', pluggable_key)
        
        # Remove pluggable config from device
        # TODO: Verify deletion works with actual hub and leaf devices
        # 
        try:
            pluggable = self.pluggables[pluggable_key]
            # Create empty config to trigger deletion
            from common.proto.pluggables_pb2 import PluggableConfig
            empty_config = PluggableConfig()
            empty_config.id.device.device_uuid.uuid = device_uuid
            empty_config.id.pluggable_index = pluggable_index
            
            LOGGER.info(f"Removing configuration from device {device_uuid}")
            self._push_config_to_device(device_uuid, pluggable_index, empty_config)
        except Exception as e:
            LOGGER.error(f"Failed to remove config from device: {e}")
            # Continue with deletion from memory even if device config removal fails
        
        del self.pluggables[pluggable_key]
        LOGGER.info(f"Deleted pluggable: device={device_uuid}, index={pluggable_index}")
        
        return Empty()
    
    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListPluggables(
        self, request: ListPluggablesRequest, context: grpc.ServicerContext # type: ignore
    ) -> ListPluggablesResponse: # type: ignore
        LOGGER.info("Received gRPC message object: {:}".format(request))
        
        response    = ListPluggablesResponse()
        device_uuid = request.device.device_uuid.uuid if request.HasField('device') else None
        
        for pluggable in self.pluggables.values():
            if device_uuid and pluggable.id.device.device_uuid.uuid != device_uuid:
                continue
            
            if request.view_level == 1:
                filtered = Pluggable()
                filtered.id.CopyFrom(pluggable.id)
                filtered.config.CopyFrom(pluggable.config)
                response.pluggables.append(filtered)
            elif request.view_level == 2:
                filtered = Pluggable()
                filtered.id.CopyFrom(pluggable.id)
                filtered.state.CopyFrom(pluggable.state)
                response.pluggables.append(filtered)
            else:
                response.pluggables.append(pluggable)
        
        LOGGER.info(f"Returning {len(response.pluggables)} pluggable(s)")
        return response
    
    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ConfigurePluggable(
        self, request: ConfigurePluggableRequest, context: grpc.ServicerContext # type: ignore
    ) -> Pluggable: # type: ignore
        LOGGER.info("Received gRPC message object: {:}".format(request))
        
        device_uuid     = request.config.id.device.device_uuid.uuid
        pluggable_index = request.config.id.pluggable_index
        pluggable_key   = f"{device_uuid}:{pluggable_index}"
        
        if pluggable_key not in self.pluggables:
            LOGGER.info(f'No matching pluggable found: device={device_uuid}, index={pluggable_index}')
            raise NotFoundException('Pluggable', pluggable_key)
        
        pluggable = self.pluggables[pluggable_key]
        
        LOGGER.info(f"Applying full configuration to pluggable: device={device_uuid}, index={pluggable_index}")
        pluggable.config.CopyFrom(request.config)

        # To ensure ID consistency across all levels are maintained
        # User might send incorrect/inconsistent IDs in nested structures 
        pluggable.config.id.device.device_uuid.uuid = device_uuid
        pluggable.config.id.pluggable_index         = pluggable_index
        for dsc_group in pluggable.config.dsc_groups:
            dsc_group.id.pluggable.device.device_uuid.uuid = device_uuid
            dsc_group.id.pluggable.pluggable_index         = pluggable_index
            for subcarrier in dsc_group.subcarriers:
                subcarrier.id.group.pluggable.device.device_uuid.uuid = device_uuid
                subcarrier.id.group.pluggable.pluggable_index         = pluggable_index
        
        has_config = len(pluggable.config.dsc_groups) > 0
        
        # Push pluggable config to device via DSCM driver
        if has_config:
            LOGGER.info(f"Pushing configuration to device {device_uuid}")
            try:
                self._push_config_to_device(device_uuid, pluggable_index, pluggable.config)
            except Exception as e:
                LOGGER.error(f"Failed to push config to device: {e}")
                # Continue even if device configuration fails
                # In production, you might want to raise the exception
        else:
            LOGGER.info(f"Empty configuration - removing config from device {device_uuid}")
            try:
                self._push_config_to_device(device_uuid, pluggable_index, pluggable.config)
            except Exception as e:
                LOGGER.error(f"Failed to remove config from device: {e}")
        
        state_msg  = "configured" if has_config else "deconfigured (empty config)"
        LOGGER.info(f"Successfully {state_msg} pluggable: device={device_uuid}, index={pluggable_index}")
        
        if request.view_level == 1:
            filtered = Pluggable()
            filtered.id.CopyFrom(pluggable.id)
            filtered.config.CopyFrom(pluggable.config)
            return filtered
        elif request.view_level == 2:
            filtered = Pluggable()
            filtered.id.CopyFrom(pluggable.id)
            filtered.state.CopyFrom(pluggable.state)
            return filtered
        else:
            return pluggable
