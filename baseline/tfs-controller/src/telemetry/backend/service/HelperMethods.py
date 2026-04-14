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

import uuid
import logging
from .collector_api._Collector               import _Collector
from .collector_api.DriverInstanceCache      import get_driver
from common.proto.kpi_manager_pb2            import KpiId
from common.tools.context_queries.Device     import get_device
from common.tools.context_queries.EndPoint   import get_endpoint_names
from typing import List, Tuple, Optional

LOGGER = logging.getLogger(__name__)

def get_subscription_parameters(
        kpi_id : str, kpi_manager_client, context_client, duration, interval
        ) -> Optional[List[Tuple]]:
    """
    Method to get subscription parameters based on KPI ID.
    Returns a list of tuples with subscription parameters.
    Each tuple contains:
        - Subscription ID (str)
        - Dictionary with:
            - "kpi" (str): KPI ID
            - "endpoint" (str): Endpoint name (e.g., 'eth0')
            - "resource" (str): Resource type (e.g., 'interface')
        - Sample interval (float)
        - Report interval (float)
    If the KPI ID is not found or the device is not available, returns None.
    Preconditions:
        - A KPI Descriptor must be added in KPI DB with correct device_id.
        - The device must be available in the context.
    """
    kpi_id_obj = KpiId()
    kpi_id_obj.kpi_id.uuid = kpi_id              # pyright: ignore[reportAttributeAccessIssue]
    kpi_descriptor = kpi_manager_client.GetKpiDescriptor(kpi_id_obj)
    if not kpi_descriptor:
        LOGGER.warning(f"KPI ID: {kpi_id} - Descriptor not found. Skipping...")
        return None

    kpi_sample_type = kpi_descriptor.kpi_sample_type
    LOGGER.info(f"KPI Descriptor (KPI Sample Type): {kpi_sample_type}")

    device = get_device( context_client       = context_client,
                         device_uuid          = kpi_descriptor.device_id.device_uuid.uuid,
                         include_config_rules = False,
                         include_components   = False
                         )
    if not device:
        raise Exception(f"KPI ID: {kpi_id} - Device not found for KPI descriptor.")
    endpoints = device.device_endpoints

    # LOGGER.info(f"Device for KPI ID: {kpi_id} - {endpoints}")
    # LOGGER.info(f"--------------------")
    endpointsIds = [endpoint_id.endpoint_id for endpoint_id in endpoints]
    # for endpoint_id in endpoints:
    #     LOGGER.info(f"Endpoint UUID: {endpoint_id.endpoint_id}")
        
    # Getting endpoint names
    device_names, endpoint_data = get_endpoint_names(
        context_client = context_client,
        endpoint_ids   = endpointsIds
    )
    # LOGGER.info(f"Device names: {device_names}")
    # LOGGER.info(f"Endpoint data: {endpoint_data}")

    subscriptions = []
    sub_id = None
    for endpoint in endpointsIds:
        sub_id = str(uuid.uuid4())  # Generate a unique subscription ID
        LOGGER.info(f"Endpoint names only: {endpoint_data[endpoint.endpoint_uuid.uuid][0]}") 
        subscriptions.append(
            (
                sub_id,  # Example subscription ID
                {
                    "kpi"      : kpi_sample_type,   # As request is based on the single KPI so it should have only one endpoint
                    "endpoint" : endpoint_data[endpoint.endpoint_uuid.uuid][0],  # Endpoint name
                    "resource" : 'interface',  # Example resource type
                },
                float(duration),
                float(interval),
            )
        )
    return subscriptions


def get_collector_by_kpi_id(kpi_id: str, kpi_manager_client, context_client, driver_instance_cache
                            ) -> Optional[_Collector]:
    """
    Method to get a collector instance based on KPI ID.
    Preconditions:
        - A KPI Descriptor must be added in KPI DB with correct device_id.
        - The device must be available in the context.
    Returns:
        - Collector instance if found, otherwise None.
    Raises:
        - Exception if the KPI ID is not found or the collector cannot be created.
    """
    LOGGER.info(f"Getting collector for KPI ID: {kpi_id}")
    kpi_id_obj = KpiId()
    kpi_id_obj.kpi_id.uuid = kpi_id              # pyright: ignore[reportAttributeAccessIssue]
    kpi_descriptor     = kpi_manager_client.GetKpiDescriptor(kpi_id_obj)
    # LOGGER.info(f"KPI Descriptor: {kpi_descriptor}")
    if not kpi_descriptor:
        raise Exception(f"KPI ID: {kpi_id} - Descriptor not found.")
    
    # device_uuid       = kpi_descriptor.device_id.device_uuid.uuid
    device = get_device( context_client       = context_client,
                         device_uuid          = kpi_descriptor.device_id.device_uuid.uuid,
                         include_config_rules = True,
                         include_components   = False,
                         )

    # Getting device collector (testing)
    collector : _Collector = get_driver(driver_instance_cache, device)
    if collector is None:
        raise Exception(f"KPI ID: {kpi_id} - Collector not found for device {device.device_uuid.uuid}.")
    # LOGGER.info(f"Collector for KPI ID: {kpi_id} - {collector.__class__.__name__}")
    return collector
