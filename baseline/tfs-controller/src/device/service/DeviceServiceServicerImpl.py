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

import grpc, logging, os, time
from typing import Dict, List
from prometheus_client import Histogram
from common.Constants import ServiceNameEnum
from common.Settings import ENVVAR_SUFIX_SERVICE_HOST, get_env_var_name
from common.method_wrappers.Decorator import MetricTypeEnum, MetricsPool, safe_and_metered_rpc_method
from common.method_wrappers.ServiceExceptions import NotFoundException, OperationFailedException
from common.proto.context_pb2 import (
    Device, DeviceConfig, DeviceDriverEnum, DeviceId, DeviceOperationalStatusEnum, Empty, Link,
    OpticalConfig, OpticalConfigId
)
from common.proto.device_pb2 import MonitoringSettings
from common.proto.device_pb2_grpc import DeviceServiceServicer
from common.proto.monitoring_pb2 import SSEMonitoringSubscriptionConfig, SSEMonitoringSubscriptionResponse
from common.tools.context_queries.Device import get_device
from common.tools.mutex_queues.MutexQueues import MutexQueues
from context.client.ContextClient import ContextClient
from .driver_api._Driver import _Driver
from .driver_api.DriverInstanceCache import DriverInstanceCache, get_driver
from .monitoring.MonitoringLoops import MonitoringLoops
from .ErrorMessages import ERROR_MISSING_DRIVER, ERROR_MISSING_KPI
from .Tools import (
    check_connect_rules, check_no_endpoints, compute_rules_to_add_delete, configure_rules,
    deconfigure_rules, get_device_controller_uuid, populate_config_rules,
    populate_endpoint_monitoring_resources, populate_endpoints, populate_initial_config_rules,
    subscribe_kpi, unsubscribe_kpi, update_endpoints
)

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('Device', 'RPC')

METRICS_POOL_DETAILS = MetricsPool('Device', 'execution', labels={
    'driver': '', 'operation': '', 'step': '',
})

class DeviceServiceServicerImpl(DeviceServiceServicer):
    def __init__(self, driver_instance_cache : DriverInstanceCache, monitoring_loops : MonitoringLoops) -> None:
        LOGGER.debug('Creating Servicer...')
        self.driver_instance_cache = driver_instance_cache
        self.monitoring_loops = monitoring_loops
        self.mutex_queues = MutexQueues()
        LOGGER.debug('Servicer Created')

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def AddDevice(self, request : Device, context : grpc.ServicerContext) -> DeviceId:
        t0 = time.time()

        device_uuid = request.device_id.device_uuid.uuid

        connection_config_rules = check_connect_rules(request.device_config)
        check_no_endpoints(request.device_endpoints)

        t1 = time.time()

        context_client = ContextClient()
        device = get_device(context_client, device_uuid, rw_copy=True)

        if device is None:
            # not in context, create blank one to get UUID, and populate it below
            device = Device()
            device.device_id.CopyFrom(request.device_id)            # pylint: disable=no-member
            device.name = request.name
            device.device_type = request.device_type
            device.device_operational_status = DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_UNDEFINED
            device.device_drivers.extend(request.device_drivers)    # pylint: disable=no-member
            device.device_config.CopyFrom(request.device_config)    # pylint: disable=no-member

            if request.HasField('controller_id'):
                controller_id = request.controller_id
                if controller_id.HasField('device_uuid'):
                    controller_device_uuid = controller_id.device_uuid.uuid
                    device.controller_id.device_uuid.uuid = controller_device_uuid

            device_id = context_client.SetDevice(device)
            device = get_device(context_client, device_id.device_uuid.uuid, rw_copy=True)

        # update device_uuid to honor UUID provided by Context
        device_uuid = device.device_id.device_uuid.uuid
        device_name = device.name

        t2 = time.time()

        self.mutex_queues.add_alias(device_uuid, device_name)
        self.mutex_queues.wait_my_turn(device_uuid)
        t3 = time.time()
        try:
            driver : _Driver = get_driver(self.driver_instance_cache, device)

            t4 = time.time()

            errors = []

            # Sub-devices and sub-links are exposed by intermediate controllers or represent mgmt links.
            # They are used to assist in path computation algorithms, and/or to identify dependencies
            # (which controller is in charge of which sub-device).
            new_sub_devices : Dict[str, Device] = dict()
            new_sub_links : Dict[str, Link] = dict()
            sorted_sub_device_uuids : List[str] = list()

            #----- Experimental ------------
            new_optical_configs : Dict[str, OpticalConfig] = dict()

            if len(device.device_endpoints) == 0:
                t5 = time.time()
                # created from request, populate endpoints using driver
                errors.extend(populate_endpoints(
                    device, driver, self.monitoring_loops, new_sub_devices, sorted_sub_device_uuids,
                    new_sub_links, new_optical_configs
                ))
                t6 = time.time()
                t_pop_endpoints = t6 - t5
            else:
                t_pop_endpoints = None

            OPTICAL_DRIVERS = {
                DeviceDriverEnum.DEVICEDRIVER_OC,
                DeviceDriverEnum.DEVICEDRIVER_OPENROADM,
            }
            is_optical_device = request.device_drivers[0] in OPTICAL_DRIVERS
            if len(device.device_config.config_rules) == len(connection_config_rules) and not is_optical_device:
                # created from request, populate config rules using driver
                t7 = time.time()
                errors.extend(populate_config_rules(device, driver))
                t8 = time.time()
                t_pop_config_rules = t8 - t7
            else:
                t_pop_config_rules = None

            # TODO: populate components

            if len(errors) > 0:
                for error in errors: LOGGER.error(error)
                raise OperationFailedException('AddDevice', extra_details=errors)

            t9 = time.time()

            ztp_service_host = get_env_var_name(ServiceNameEnum.ZTP, ENVVAR_SUFIX_SERVICE_HOST)
            environment_variables = set(os.environ.keys())
            if ztp_service_host in environment_variables:
                # ZTP component is deployed; leave devices disabled. ZTP will enable them.
                device.device_operational_status = DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_DISABLED
            else:
                # ZTP is not deployed; assume the device is ready while onboarding and set them as enabled.
                device.device_operational_status = DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED

            # temporary line
            if  is_optical_device:
                #for endpoint in request.device_endpoints:
                #    #endpoint.endpoint_id.device_id.CopyFrom(device.device_id)
                #    pass

                if 'new_optical_config' in new_optical_configs and 'opticalconfig' in new_optical_configs["new_optical_config"]:
                    LOGGER.info(f"set optical device config {new_optical_configs}")
                    context_client.SetOpticalConfig(new_optical_configs["new_optical_config"]['opticalconfig'])

            device_id = context_client.SetDevice(device)

            t10 = time.time()

            for sub_device_uuid in sorted_sub_device_uuids:
                sub_device = new_sub_devices[sub_device_uuid]
                context_client.SetDevice(sub_device)

            t11 = time.time()

            for sub_links in new_sub_links.values():
                context_client.SetLink(sub_links)

            t12 = time.time()

            # Update endpoint monitoring resources with UUIDs
            device_with_uuids = get_device(
                context_client, device_id.device_uuid.uuid, rw_copy=False, include_endpoints=True,
                include_components=False, include_config_rules=False)
            populate_endpoint_monitoring_resources(device_with_uuids, self.monitoring_loops)

            t13 = time.time()

            context_client.close()

            t14 = time.time()

            metrics_labels = dict(driver=driver.name, operation='add_device')

            histogram_duration : Histogram = METRICS_POOL_DETAILS.get_or_create(
                'details', MetricTypeEnum.HISTOGRAM_DURATION)
            histogram_duration.labels(step='total'              , **metrics_labels).observe(t14-t0)
            histogram_duration.labels(step='execution'          , **metrics_labels).observe(t14-t3)
            histogram_duration.labels(step='endpoint_checks'    , **metrics_labels).observe(t1-t0)
            histogram_duration.labels(step='get_device'         , **metrics_labels).observe(t2-t1)
            histogram_duration.labels(step='wait_queue'         , **metrics_labels).observe(t3-t2)
            histogram_duration.labels(step='get_driver'         , **metrics_labels).observe(t4-t3)
            histogram_duration.labels(step='set_device'         , **metrics_labels).observe(t10-t9)
            histogram_duration.labels(step='populate_monit_rsrc', **metrics_labels).observe(t13-t12)

            if t_pop_endpoints is not None:
                histogram_duration.labels(step='populate_endpoints', **metrics_labels).observe(t_pop_endpoints)

            if t_pop_config_rules is not None:
                histogram_duration.labels(step='populate_config_rules', **metrics_labels).observe(t_pop_config_rules)

            if len(new_sub_devices) > 0:
                histogram_duration.labels(step='set_sub_devices', **metrics_labels).observe(t11-t10)

            if len(new_sub_links) > 0:
                histogram_duration.labels(step='set_sub_links', **metrics_labels).observe(t12-t11)

            return device_id
        finally:
            self.mutex_queues.signal_done(device_uuid)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ConfigureDevice(self, request : Device, context : grpc.ServicerContext) -> DeviceId:
        t0 = time.time()
        device_id = request.device_id
        device_uuid = device_id.device_uuid.uuid

        self.mutex_queues.wait_my_turn(device_uuid)
        t1 = time.time()
        try:
            context_client = ContextClient()
            t2 = time.time()
            device = get_device(
                context_client, device_uuid, rw_copy=True, include_endpoints=False, include_components=False,
                include_config_rules=True)
            if device is None:
                raise NotFoundException('Device', device_uuid, extra_details='loading in ConfigureDevice')

            t3 = time.time()
            device_controller_uuid = get_device_controller_uuid(device)
            if device_controller_uuid is not None:
                device = get_device(
                    context_client, device_controller_uuid, rw_copy=True, include_endpoints=False,
                    include_components=False, include_config_rules=True)
                if device is None:
                    raise NotFoundException(
                        'Device', device_controller_uuid, extra_details='loading in ConfigureDevice')

            device_uuid = device.device_id.device_uuid.uuid
            driver : _Driver = get_driver(self.driver_instance_cache, device)
            if driver is None:
                msg = ERROR_MISSING_DRIVER.format(device_uuid=str(device_uuid))
                raise OperationFailedException('ConfigureDevice', extra_details=msg)

            if DeviceDriverEnum.DEVICEDRIVER_P4 in device.device_drivers:
                device = get_device(
                    context_client, device_uuid, rw_copy=False, include_endpoints=True, include_components=False,
                    include_config_rules=True)
                # P4 Driver, by now, has no means to retrieve endpoints
                # We allow defining the endpoints manually
                update_endpoints(request, device)

                # Update endpoints to get UUIDs
                device_id = context_client.SetDevice(device)
                device = context_client.GetDevice(device_id)

            ztp_service_host = get_env_var_name(ServiceNameEnum.ZTP, ENVVAR_SUFIX_SERVICE_HOST)
            environment_variables = set(os.environ.keys())
            if ztp_service_host in environment_variables:
                # ZTP component is deployed; accept status updates
                if request.device_operational_status != DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_UNDEFINED:
                    device.device_operational_status = request.device_operational_status
            else:
                # ZTP is not deployed; activated during AddDevice and not modified
                pass

            t4 = time.time()
            # TODO: use of datastores (might be virtual ones) to enable rollbacks
            resources_to_set, resources_to_delete = compute_rules_to_add_delete(device, request)

            t5 = time.time()
            errors = []
            errors.extend(configure_rules(device, driver, resources_to_set))
            t6 = time.time()
            errors.extend(deconfigure_rules(device, driver, resources_to_delete))

            t7 = time.time()
            if len(errors) > 0:
                for error in errors: LOGGER.error(error)
                raise OperationFailedException('ConfigureDevice', extra_details=errors)

            # Context Performance+Scalability enhancement:
            # This method, besides P4 logic, does not add/update/delete endpoints.
            # Remove endpoints to reduce number of inserts done by Context.
            # TODO: Add logic to inspect endpoints and keep only those ones modified with respect to Context.
            del device.device_endpoints[:]

            t8 = time.time()
            # Note: Rules are updated by configure_rules() and deconfigure_rules() methods.
            device_id = context_client.SetDevice(device)

            t9 = time.time()

            metrics_labels = dict(driver=driver.name, operation='configure_device')

            histogram_duration : Histogram = METRICS_POOL_DETAILS.get_or_create(
                'details', MetricTypeEnum.HISTOGRAM_DURATION)
            histogram_duration.labels(step='total'            , **metrics_labels).observe(t9-t0)
            histogram_duration.labels(step='wait_queue'       , **metrics_labels).observe(t1-t0)
            histogram_duration.labels(step='execution'        , **metrics_labels).observe(t9-t1)
            histogram_duration.labels(step='get_device'       , **metrics_labels).observe(t3-t2)
            histogram_duration.labels(step='split_rules'      , **metrics_labels).observe(t5-t4)
            histogram_duration.labels(step='configure_rules'  , **metrics_labels).observe(t6-t5)
            histogram_duration.labels(step='deconfigure_rules', **metrics_labels).observe(t7-t6)
            histogram_duration.labels(step='set_device'       , **metrics_labels).observe(t9-t8)

            return device_id
        finally:
            self.mutex_queues.signal_done(device_uuid)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def DeleteDevice(self, request : DeviceId, context : grpc.ServicerContext) -> Empty:
        device_uuid = request.device_uuid.uuid

        self.mutex_queues.wait_my_turn(device_uuid)
        try:
            context_client = ContextClient()
            device = get_device(
                context_client, device_uuid, rw_copy=False, include_endpoints=False, include_config_rules=False,
                include_components=False)
            if device is None:
                raise NotFoundException('Device', device_uuid, extra_details='loading in DeleteDevice')
            device_uuid = device.device_id.device_uuid.uuid

            self.monitoring_loops.remove_device(device_uuid)
            self.driver_instance_cache.delete(device_uuid)
            context_client.RemoveDevice(request)
            return Empty()
        finally:
            self.mutex_queues.signal_done(device_uuid)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetInitialConfig(self, request : DeviceId, context : grpc.ServicerContext) -> DeviceConfig:
        device_uuid = request.device_uuid.uuid

        self.mutex_queues.wait_my_turn(device_uuid)
        try:
            context_client = ContextClient()
            device = get_device(
                context_client, device_uuid, rw_copy=False, include_endpoints=False, include_components=False,
                include_config_rules=True)
            if device is None:
                raise NotFoundException('Device', device_uuid, extra_details='loading in DeleteDevice')

            driver : _Driver = get_driver(self.driver_instance_cache, device)
            if driver is None:
                msg = ERROR_MISSING_DRIVER.format(device_uuid=str(device_uuid))
                raise OperationFailedException('GetInitialConfig', extra_details=msg)

            device_config = DeviceConfig()
            errors = populate_initial_config_rules(device_uuid, device_config, driver)

            if len(errors) > 0:
                for error in errors: LOGGER.error(error)
                raise OperationFailedException('GetInitialConfig', extra_details=errors)

            return device_config
        finally:
            self.mutex_queues.signal_done(device_uuid)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def MonitorDeviceKpi(self, request : MonitoringSettings, context : grpc.ServicerContext) -> Empty:
        subscribe = (request.sampling_duration_s > 0.0) and (request.sampling_interval_s > 0.0)
        manage_kpi_method = subscribe_kpi if subscribe else unsubscribe_kpi

        if subscribe:
            device_uuid = request.kpi_descriptor.device_id.device_uuid.uuid
        else:
            # unsubscribe only carries kpi_uuid; take device_uuid from recorded KPIs
            kpi_uuid = request.kpi_id.kpi_id.uuid
            kpi_details = self.monitoring_loops.get_kpi_by_uuid(kpi_uuid)
            if kpi_details is None:
                msg = ERROR_MISSING_KPI.format(kpi_uuid=str(kpi_uuid))
                raise OperationFailedException('MonitorDeviceKpi', extra_details=msg)
            device_uuid = kpi_details[0]

        self.mutex_queues.wait_my_turn(device_uuid)
        try:
            context_client = ContextClient()
            device = get_device(
                context_client, device_uuid, rw_copy=False, include_endpoints=False, include_components=False,
                include_config_rules=True)
            if device is None:
                raise NotFoundException('Device', device_uuid, extra_details='loading in DeleteDevice')

            driver : _Driver = get_driver(self.driver_instance_cache, device)
            if driver is None:
                msg = ERROR_MISSING_DRIVER.format(device_uuid=str(device_uuid))
                raise OperationFailedException('MonitorDeviceKpi', extra_details=msg)

            errors = manage_kpi_method(request, driver, self.monitoring_loops)
            if len(errors) > 0: raise OperationFailedException('MonitorDeviceKpi', extra_details=errors)

            return Empty()
        finally:
            self.mutex_queues.signal_done(device_uuid)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SSETelemetrySubscribe(
        self, request: SSEMonitoringSubscriptionConfig, context : grpc.ServicerContext
    ) -> SSEMonitoringSubscriptionResponse:
        device_id = request.device_id.device_uuid.uuid
        config_type = request.config_type
        context_client = ContextClient()
        device = get_device(
            context_client, device_id, rw_copy=True, include_endpoints=False, include_components=False,
            include_config_rules=True)
        if device is None:
            raise NotFoundException('Device', device_id, extra_details='loading in ConfigureDevice')
        driver : _Driver = get_driver(self.driver_instance_cache, device)

        if config_type == SSEMonitoringSubscriptionConfig.Subscribe:
            r = driver.SubscribeState([(request.uri, 0, float(request.sampling_interval))])
            if len(r) != 1:
                raise OperationFailedException(
                    'SSETelemetrySubscribe', extra_details='Driver returned an unexpected number of responses: {:d}'.format(len(r))
                )
            sub_conf: dict = r[0]
            return SSEMonitoringSubscriptionResponse(identifier=str(sub_conf['id']), uri=sub_conf['uri'])

        if config_type == SSEMonitoringSubscriptionConfig.Unsubscribe:
            r = driver.UnsubscribeState([(str(request.identifier), 0, 0)])
            if len(r) != 1:
                raise OperationFailedException(
                    'SSETelemetrySubscribe', extra_details='Driver returned an unexpected number of responses: {:d}'.format(len(r))
                )
            return SSEMonitoringSubscriptionResponse()

