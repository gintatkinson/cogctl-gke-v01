# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from tapi_server.models.operations_tapiconnectivitycreateconnectivityservice_body import OperationsTapiconnectivitycreateconnectivityserviceBody  # noqa: E501
from tapi_server.models.operations_tapiconnectivitydeleteconnectivityservice_body import OperationsTapiconnectivitydeleteconnectivityserviceBody  # noqa: E501
from tapi_server.models.operations_tapiconnectivitygetconnectiondetails_body import OperationsTapiconnectivitygetconnectiondetailsBody  # noqa: E501
from tapi_server.models.operations_tapiconnectivitygetconnectionendpointdetails_body import OperationsTapiconnectivitygetconnectionendpointdetailsBody  # noqa: E501
from tapi_server.models.operations_tapiconnectivitygetconnectivityservicedetails_body import OperationsTapiconnectivitygetconnectivityservicedetailsBody  # noqa: E501
from tapi_server.models.operations_tapiconnectivityupdateconnectivityservice_body import OperationsTapiconnectivityupdateconnectivityserviceBody  # noqa: E501
from tapi_server.models.tapi_common_bandwidth_profile_wrapper import TapiCommonBandwidthProfileWrapper  # noqa: E501
from tapi_server.models.tapi_common_capacity_value_wrapper import TapiCommonCapacityValueWrapper  # noqa: E501
from tapi_server.models.tapi_common_capacity_wrapper import TapiCommonCapacityWrapper  # noqa: E501
from tapi_server.models.tapi_common_name_and_value_wrapper import TapiCommonNameAndValueWrapper  # noqa: E501
from tapi_server.models.tapi_common_service_interface_point_ref_wrapper import TapiCommonServiceInterfacePointRefWrapper  # noqa: E501
from tapi_server.models.tapi_common_time_range_wrapper import TapiCommonTimeRangeWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_cep_list_wrapper import TapiConnectivityCepListWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_cep_role_wrapper import TapiConnectivityCepRoleWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_connection_end_point_ref_wrapper import TapiConnectivityConnectionEndPointRefWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_connection_end_point_wrapper import TapiConnectivityConnectionEndPointWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_connection_ref_wrapper import TapiConnectivityConnectionRefWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_connection_spec_reference_wrapper import TapiConnectivityConnectionSpecReferenceWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_connection_wrapper import TapiConnectivityConnectionWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_connectivity_context_wrapper import TapiConnectivityConnectivityContextWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_connectivity_service_end_point_ref_wrapper import TapiConnectivityConnectivityServiceEndPointRefWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_connectivity_service_end_point_wrapper import TapiConnectivityConnectivityServiceEndPointWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_connectivity_service_ref_wrapper import TapiConnectivityConnectivityServiceRefWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_connectivity_service_wrapper import TapiConnectivityConnectivityServiceWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_create_connectivity_service import TapiConnectivityCreateConnectivityService  # noqa: E501
from tapi_server.models.tapi_connectivity_get_connection_details import TapiConnectivityGetConnectionDetails  # noqa: E501
from tapi_server.models.tapi_connectivity_get_connection_end_point_details import TapiConnectivityGetConnectionEndPointDetails  # noqa: E501
from tapi_server.models.tapi_connectivity_get_connectivity_service_details import TapiConnectivityGetConnectivityServiceDetails  # noqa: E501
from tapi_server.models.tapi_connectivity_get_connectivity_service_list import TapiConnectivityGetConnectivityServiceList  # noqa: E501
from tapi_server.models.tapi_connectivity_resilience_route_wrapper import TapiConnectivityResilienceRouteWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_route_ref_wrapper import TapiConnectivityRouteRefWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_route_wrapper import TapiConnectivityRouteWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_switch_control_ref_wrapper import TapiConnectivitySwitchControlRefWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_switch_control_wrapper import TapiConnectivitySwitchControlWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_switch_wrapper import TapiConnectivitySwitchWrapper  # noqa: E501
from tapi_server.models.tapi_connectivity_update_connectivity_service import TapiConnectivityUpdateConnectivityService  # noqa: E501
from tapi_server.models.tapi_path_computation_value_or_priority_wrapper import TapiPathComputationValueOrPriorityWrapper  # noqa: E501
from tapi_server.models.tapi_topology_cost_characteristic_wrapper import TapiTopologyCostCharacteristicWrapper  # noqa: E501
from tapi_server.models.tapi_topology_latency_characteristic_wrapper import TapiTopologyLatencyCharacteristicWrapper  # noqa: E501
from tapi_server.models.tapi_topology_link_ref_wrapper import TapiTopologyLinkRefWrapper  # noqa: E501
from tapi_server.models.tapi_topology_node_edge_point_ref_wrapper import TapiTopologyNodeEdgePointRefWrapper  # noqa: E501
from tapi_server.models.tapi_topology_resilience_type_wrapper import TapiTopologyResilienceTypeWrapper  # noqa: E501
from tapi_server.models.tapi_topology_risk_characteristic_wrapper import TapiTopologyRiskCharacteristicWrapper  # noqa: E501
from tapi_server.test import BaseTestCase


class TestTapiConnectivityController(BaseTestCase):
    """TapiConnectivityController integration test stubs"""

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_connection_end_pointtopology_uuidnode_uuidnode_edge_point_uuidconnection_end_point_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_connection_end_pointtopology_uuidnode_uuidnode_edge_point_uuidconnection_end_point_uuid_get

        returns tapi.connectivity.ConnectionEndPointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/connection-end-point={topology-uuid},{node-uuid},{node-edge-point-uuid},{connection-end-point-uuid}/'.format(uuid='uuid_example', topology_uuid='topology_uuid_example', node_uuid='node_uuid_example', node_edge_point_uuid='node_edge_point_uuid_example', connection_end_point_uuid='connection_end_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_connection_spec_reference_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_connection_spec_reference_get

        returns tapi.connectivity.ConnectionSpecReference
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/connection-spec-reference/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_get

        returns tapi.connectivity.Connection
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_lower_connectionconnection_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_lower_connectionconnection_uuid_get

        returns tapi.connectivity.ConnectionRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/lower-connection={connection-uuid}/'.format(uuid='uuid_example', connection_uuid='connection_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_routelocal_id_connection_end_pointtopology_uuidnode_uuidnode_edge_point_uuidconnection_end_point_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_routelocal_id_connection_end_pointtopology_uuidnode_uuidnode_edge_point_uuidconnection_end_point_uuid_get

        returns tapi.connectivity.ConnectionEndPointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/route={local-id}/connection-end-point={topology-uuid},{node-uuid},{node-edge-point-uuid},{connection-end-point-uuid}/'.format(uuid='uuid_example', local_id='local_id_example', topology_uuid='topology_uuid_example', node_uuid='node_uuid_example', node_edge_point_uuid='node_edge_point_uuid_example', connection_end_point_uuid='connection_end_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_routelocal_id_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_routelocal_id_get

        returns tapi.connectivity.Route
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/route={local-id}/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_routelocal_id_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_routelocal_id_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/route={local-id}/name={value-name}/'.format(uuid='uuid_example', local_id='local_id_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_routelocal_id_resilience_route_pac_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_routelocal_id_resilience_route_pac_get

        returns tapi.connectivity.ResilienceRoute
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/route={local-id}/resilience-route-pac/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_routelocal_id_resilience_route_pac_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_routelocal_id_resilience_route_pac_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/route={local-id}/resilience-route-pac/name={value-name}/'.format(uuid='uuid_example', local_id='local_id_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_supported_client_linktopology_uuidlink_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_supported_client_linktopology_uuidlink_uuid_get

        returns tapi.topology.LinkRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/supported-client-link={topology-uuid},{link-uuid}/'.format(uuid='uuid_example', topology_uuid='topology_uuid_example', link_uuid='link_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_get

        returns tapi.connectivity.SwitchControl
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/switch-control={switch-control-uuid}/'.format(uuid='uuid_example', switch_control_uuid='switch_control_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/switch-control={switch-control-uuid}/name={value-name}/'.format(uuid='uuid_example', switch_control_uuid='switch_control_uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_resilience_type_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_resilience_type_get

        returns tapi.topology.ResilienceType
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/switch-control={switch-control-uuid}/resilience-type/'.format(uuid='uuid_example', switch_control_uuid='switch_control_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_sub_switch_controlconnection_uuidsub_switch_control_switch_control_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_sub_switch_controlconnection_uuidsub_switch_control_switch_control_uuid_get

        returns tapi.connectivity.SwitchControlRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/switch-control={switch-control-uuid}/sub-switch-control={connection-uuid},{sub-switch-control-switch-control-uuid}/'.format(uuid='uuid_example', switch_control_uuid='switch_control_uuid_example', connection_uuid='connection_uuid_example', sub_switch_control_switch_control_uuid='sub_switch_control_switch_control_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_switchlocal_id_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_switchlocal_id_get

        returns tapi.connectivity.Switch
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/switch-control={switch-control-uuid}/switch={local-id}/'.format(uuid='uuid_example', switch_control_uuid='switch_control_uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_switchlocal_id_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_switchlocal_id_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/switch-control={switch-control-uuid}/switch={local-id}/name={value-name}/'.format(uuid='uuid_example', switch_control_uuid='switch_control_uuid_example', local_id='local_id_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_switchlocal_id_selected_connection_end_pointtopology_uuidnode_uuidnode_edge_point_uuidconnection_end_point_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_switchlocal_id_selected_connection_end_pointtopology_uuidnode_uuidnode_edge_point_uuidconnection_end_point_uuid_get

        returns tapi.connectivity.ConnectionEndPointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/switch-control={switch-control-uuid}/switch={local-id}/selected-connection-end-point={topology-uuid},{node-uuid},{node-edge-point-uuid},{connection-end-point-uuid}/'.format(uuid='uuid_example', switch_control_uuid='switch_control_uuid_example', local_id='local_id_example', topology_uuid='topology_uuid_example', node_uuid='node_uuid_example', node_edge_point_uuid='node_edge_point_uuid_example', connection_end_point_uuid='connection_end_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_switchlocal_id_selected_routeconnection_uuidroute_local_id_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_switchlocal_id_selected_routeconnection_uuidroute_local_id_get

        returns tapi.connectivity.RouteRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connection={uuid}/switch-control={switch-control-uuid}/switch={local-id}/selected-route={connection-uuid},{route-local-id}/'.format(uuid='uuid_example', switch_control_uuid='switch_control_uuid_example', local_id='local_id_example', connection_uuid='connection_uuid_example', route_local_id='route_local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_service_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_service_post

        creates tapi.connectivity.ConnectivityService
        """
        body = TapiConnectivityConnectivityServiceWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_connectionconnection_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_connectionconnection_uuid_get

        returns tapi.connectivity.ConnectionRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/connection={connection-uuid}/'.format(uuid='uuid_example', connection_uuid='connection_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_coroute_inclusion_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_coroute_inclusion_delete

        removes tapi.connectivity.ConnectivityServiceRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/coroute-inclusion/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_coroute_inclusion_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_coroute_inclusion_get

        returns tapi.connectivity.ConnectivityServiceRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/coroute-inclusion/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_coroute_inclusion_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_coroute_inclusion_post

        creates tapi.connectivity.ConnectivityServiceRef
        """
        body = TapiConnectivityConnectivityServiceRefWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/coroute-inclusion/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_coroute_inclusion_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_coroute_inclusion_put

        creates or updates tapi.connectivity.ConnectivityServiceRef
        """
        body = TapiConnectivityConnectivityServiceRefWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/coroute-inclusion/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_cost_characteristic_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_cost_characteristic_post

        creates tapi.topology.CostCharacteristic
        """
        body = TapiTopologyCostCharacteristicWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/cost-characteristic/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_cost_characteristiccost_name_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_cost_characteristiccost_name_delete

        removes tapi.topology.CostCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/cost-characteristic={cost-name}/'.format(uuid='uuid_example', cost_name='cost_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_cost_characteristiccost_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_cost_characteristiccost_name_get

        returns tapi.topology.CostCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/cost-characteristic={cost-name}/'.format(uuid='uuid_example', cost_name='cost_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_cost_characteristiccost_name_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_cost_characteristiccost_name_put

        creates or updates tapi.topology.CostCharacteristic
        """
        body = TapiTopologyCostCharacteristicWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/cost-characteristic={cost-name}/'.format(uuid='uuid_example', cost_name='cost_name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_delete

        removes tapi.connectivity.ConnectivityService
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_diversity_exclusion_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_diversity_exclusion_post

        creates tapi.connectivity.ConnectivityServiceRef
        """
        body = TapiConnectivityConnectivityServiceRefWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/diversity-exclusion/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_diversity_exclusionconnectivity_service_uuid_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_diversity_exclusionconnectivity_service_uuid_delete

        removes tapi.connectivity.ConnectivityServiceRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/diversity-exclusion={connectivity-service-uuid}/'.format(uuid='uuid_example', connectivity_service_uuid='connectivity_service_uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_diversity_exclusionconnectivity_service_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_diversity_exclusionconnectivity_service_uuid_get

        returns tapi.connectivity.ConnectivityServiceRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/diversity-exclusion={connectivity-service-uuid}/'.format(uuid='uuid_example', connectivity_service_uuid='connectivity_service_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_diversity_exclusionconnectivity_service_uuid_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_diversity_exclusionconnectivity_service_uuid_put

        creates or updates tapi.connectivity.ConnectivityServiceRef
        """
        body = TapiConnectivityConnectivityServiceRefWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/diversity-exclusion={connectivity-service-uuid}/'.format(uuid='uuid_example', connectivity_service_uuid='connectivity_service_uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_point_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_point_post

        creates tapi.connectivity.ConnectivityServiceEndPoint
        """
        body = TapiConnectivityConnectivityServiceEndPointWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_delete

        removes tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_post

        creates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_put

        creates or updates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_delete

        removes tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_post

        creates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_put

        creates or updates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_delete

        removes tapi.common.BandwidthProfile
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_get

        returns tapi.common.BandwidthProfile
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_delete

        removes tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_post

        creates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_put

        creates or updates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_delete

        removes tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_post

        creates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_put

        creates or updates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_post

        creates tapi.common.BandwidthProfile
        """
        body = TapiCommonBandwidthProfileWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_put

        creates or updates tapi.common.BandwidthProfile
        """
        body = TapiCommonBandwidthProfileWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_delete

        removes tapi.common.Capacity
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_get

        returns tapi.common.Capacity
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_post

        creates tapi.common.Capacity
        """
        body = TapiCommonCapacityWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_put

        creates or updates tapi.common.Capacity
        """
        body = TapiCommonCapacityWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_total_size_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_total_size_delete

        removes tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/total-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_total_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_total_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/total-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_total_size_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_total_size_post

        creates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/total-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_total_size_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_total_size_put

        creates or updates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/capacity/total-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_connection_end_pointtopology_uuidnode_uuidnode_edge_point_uuidconnection_end_point_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_connection_end_pointtopology_uuidnode_uuidnode_edge_point_uuidconnection_end_point_uuid_get

        returns tapi.connectivity.ConnectionEndPointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/connection-end-point={topology-uuid},{node-uuid},{node-edge-point-uuid},{connection-end-point-uuid}/'.format(uuid='uuid_example', local_id='local_id_example', topology_uuid='topology_uuid_example', node_uuid='node_uuid_example', node_edge_point_uuid='node_edge_point_uuid_example', connection_end_point_uuid='connection_end_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_delete

        removes tapi.connectivity.ConnectivityServiceEndPoint
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_get

        returns tapi.connectivity.ConnectivityServiceEndPoint
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_name_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_name_post

        creates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/name/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_namevalue_name_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_namevalue_name_delete

        removes tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/name={value-name}/'.format(uuid='uuid_example', local_id='local_id_example', value_name='value_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/name={value-name}/'.format(uuid='uuid_example', local_id='local_id_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_namevalue_name_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_namevalue_name_put

        creates or updates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/name={value-name}/'.format(uuid='uuid_example', local_id='local_id_example', value_name='value_name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_peer_fwd_connectivity_service_end_point_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_peer_fwd_connectivity_service_end_point_delete

        removes tapi.connectivity.ConnectivityServiceEndPointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/peer-fwd-connectivity-service-end-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_peer_fwd_connectivity_service_end_point_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_peer_fwd_connectivity_service_end_point_get

        returns tapi.connectivity.ConnectivityServiceEndPointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/peer-fwd-connectivity-service-end-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_peer_fwd_connectivity_service_end_point_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_peer_fwd_connectivity_service_end_point_post

        creates tapi.connectivity.ConnectivityServiceEndPointRef
        """
        body = TapiConnectivityConnectivityServiceEndPointRefWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/peer-fwd-connectivity-service-end-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_peer_fwd_connectivity_service_end_point_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_peer_fwd_connectivity_service_end_point_put

        creates or updates tapi.connectivity.ConnectivityServiceEndPointRef
        """
        body = TapiConnectivityConnectivityServiceEndPointRefWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/peer-fwd-connectivity-service-end-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_protecting_connectivity_service_end_point_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_protecting_connectivity_service_end_point_delete

        removes tapi.connectivity.ConnectivityServiceEndPointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/protecting-connectivity-service-end-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_protecting_connectivity_service_end_point_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_protecting_connectivity_service_end_point_get

        returns tapi.connectivity.ConnectivityServiceEndPointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/protecting-connectivity-service-end-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_protecting_connectivity_service_end_point_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_protecting_connectivity_service_end_point_post

        creates tapi.connectivity.ConnectivityServiceEndPointRef
        """
        body = TapiConnectivityConnectivityServiceEndPointRefWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/protecting-connectivity-service-end-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_protecting_connectivity_service_end_point_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_protecting_connectivity_service_end_point_put

        creates or updates tapi.connectivity.ConnectivityServiceEndPointRef
        """
        body = TapiConnectivityConnectivityServiceEndPointRefWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/protecting-connectivity-service-end-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_put

        creates or updates tapi.connectivity.ConnectivityServiceEndPoint
        """
        body = TapiConnectivityConnectivityServiceEndPointWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_server_connectivity_service_end_point_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_server_connectivity_service_end_point_delete

        removes tapi.connectivity.ConnectivityServiceEndPointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/server-connectivity-service-end-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_server_connectivity_service_end_point_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_server_connectivity_service_end_point_get

        returns tapi.connectivity.ConnectivityServiceEndPointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/server-connectivity-service-end-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_server_connectivity_service_end_point_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_server_connectivity_service_end_point_post

        creates tapi.connectivity.ConnectivityServiceEndPointRef
        """
        body = TapiConnectivityConnectivityServiceEndPointRefWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/server-connectivity-service-end-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_server_connectivity_service_end_point_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_server_connectivity_service_end_point_put

        creates or updates tapi.connectivity.ConnectivityServiceEndPointRef
        """
        body = TapiConnectivityConnectivityServiceEndPointRefWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/server-connectivity-service-end-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_service_interface_point_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_service_interface_point_delete

        removes tapi.common.ServiceInterfacePointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/service-interface-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_service_interface_point_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_service_interface_point_get

        returns tapi.common.ServiceInterfacePointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/service-interface-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_service_interface_point_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_service_interface_point_post

        creates tapi.common.ServiceInterfacePointRef
        """
        body = TapiCommonServiceInterfacePointRefWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/service-interface-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_service_interface_point_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_service_interface_point_put

        creates or updates tapi.common.ServiceInterfacePointRef
        """
        body = TapiCommonServiceInterfacePointRefWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/end-point={local-id}/service-interface-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_get

        returns tapi.connectivity.ConnectivityService
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_latency_characteristic_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_latency_characteristic_post

        creates tapi.topology.LatencyCharacteristic
        """
        body = TapiTopologyLatencyCharacteristicWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/latency-characteristic/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_latency_characteristictraffic_property_name_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_latency_characteristictraffic_property_name_delete

        removes tapi.topology.LatencyCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/latency-characteristic={traffic-property-name}/'.format(uuid='uuid_example', traffic_property_name='traffic_property_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_latency_characteristictraffic_property_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_latency_characteristictraffic_property_name_get

        returns tapi.topology.LatencyCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/latency-characteristic={traffic-property-name}/'.format(uuid='uuid_example', traffic_property_name='traffic_property_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_latency_characteristictraffic_property_name_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_latency_characteristictraffic_property_name_put

        creates or updates tapi.topology.LatencyCharacteristic
        """
        body = TapiTopologyLatencyCharacteristicWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/latency-characteristic={traffic-property-name}/'.format(uuid='uuid_example', traffic_property_name='traffic_property_name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_cost_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_cost_delete

        removes tapi.path.computation.ValueOrPriority
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/max-allowed-cost/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_cost_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_cost_get

        returns tapi.path.computation.ValueOrPriority
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/max-allowed-cost/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_cost_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_cost_post

        creates tapi.path.computation.ValueOrPriority
        """
        body = TapiPathComputationValueOrPriorityWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/max-allowed-cost/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_cost_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_cost_put

        creates or updates tapi.path.computation.ValueOrPriority
        """
        body = TapiPathComputationValueOrPriorityWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/max-allowed-cost/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_delay_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_delay_delete

        removes tapi.path.computation.ValueOrPriority
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/max-allowed-delay/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_delay_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_delay_get

        returns tapi.path.computation.ValueOrPriority
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/max-allowed-delay/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_delay_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_delay_post

        creates tapi.path.computation.ValueOrPriority
        """
        body = TapiPathComputationValueOrPriorityWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/max-allowed-delay/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_delay_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_delay_put

        creates or updates tapi.path.computation.ValueOrPriority
        """
        body = TapiPathComputationValueOrPriorityWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/max-allowed-delay/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_hops_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_hops_delete

        removes tapi.path.computation.ValueOrPriority
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/max-allowed-hops/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_hops_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_hops_get

        returns tapi.path.computation.ValueOrPriority
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/max-allowed-hops/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_hops_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_hops_post

        creates tapi.path.computation.ValueOrPriority
        """
        body = TapiPathComputationValueOrPriorityWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/max-allowed-hops/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_hops_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_hops_put

        creates or updates tapi.path.computation.ValueOrPriority
        """
        body = TapiPathComputationValueOrPriorityWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/max-allowed-hops/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_name_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_name_post

        creates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/name/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_namevalue_name_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_namevalue_name_delete

        removes tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_namevalue_name_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_namevalue_name_put

        creates or updates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_put

        creates or updates tapi.connectivity.ConnectivityService
        """
        body = TapiConnectivityConnectivityServiceWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_burst_size_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_burst_size_delete

        removes tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_burst_size_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_burst_size_post

        creates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_burst_size_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_burst_size_put

        creates or updates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_information_rate_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_information_rate_delete

        removes tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_information_rate_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_information_rate_post

        creates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_information_rate_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_information_rate_put

        creates or updates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_delete

        removes tapi.common.BandwidthProfile
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_get

        returns tapi.common.BandwidthProfile
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_burst_size_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_burst_size_delete

        removes tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_burst_size_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_burst_size_post

        creates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_burst_size_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_burst_size_put

        creates or updates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_information_rate_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_information_rate_delete

        removes tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_information_rate_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_information_rate_post

        creates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_information_rate_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_information_rate_put

        creates or updates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_post

        creates tapi.common.BandwidthProfile
        """
        body = TapiCommonBandwidthProfileWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_put

        creates or updates tapi.common.BandwidthProfile
        """
        body = TapiCommonBandwidthProfileWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/bandwidth-profile/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_delete

        removes tapi.common.Capacity
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_get

        returns tapi.common.Capacity
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_post

        creates tapi.common.Capacity
        """
        body = TapiCommonCapacityWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_put

        creates or updates tapi.common.Capacity
        """
        body = TapiCommonCapacityWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_total_size_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_total_size_delete

        removes tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/total-size/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_total_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_total_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/total-size/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_total_size_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_total_size_post

        creates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/total-size/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_total_size_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_total_size_put

        creates or updates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/requested-capacity/total-size/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_resilience_type_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_resilience_type_delete

        removes tapi.topology.ResilienceType
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/resilience-type/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_resilience_type_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_resilience_type_get

        returns tapi.topology.ResilienceType
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/resilience-type/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_resilience_type_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_resilience_type_post

        creates tapi.topology.ResilienceType
        """
        body = TapiTopologyResilienceTypeWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/resilience-type/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_resilience_type_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_resilience_type_put

        creates or updates tapi.topology.ResilienceType
        """
        body = TapiTopologyResilienceTypeWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/resilience-type/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_risk_diversity_characteristic_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_risk_diversity_characteristic_post

        creates tapi.topology.RiskCharacteristic
        """
        body = TapiTopologyRiskCharacteristicWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/risk-diversity-characteristic/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_risk_diversity_characteristicrisk_characteristic_name_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_risk_diversity_characteristicrisk_characteristic_name_delete

        removes tapi.topology.RiskCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/risk-diversity-characteristic={risk-characteristic-name}/'.format(uuid='uuid_example', risk_characteristic_name='risk_characteristic_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_risk_diversity_characteristicrisk_characteristic_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_risk_diversity_characteristicrisk_characteristic_name_get

        returns tapi.topology.RiskCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/risk-diversity-characteristic={risk-characteristic-name}/'.format(uuid='uuid_example', risk_characteristic_name='risk_characteristic_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_risk_diversity_characteristicrisk_characteristic_name_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_risk_diversity_characteristicrisk_characteristic_name_put

        creates or updates tapi.topology.RiskCharacteristic
        """
        body = TapiTopologyRiskCharacteristicWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/risk-diversity-characteristic={risk-characteristic-name}/'.format(uuid='uuid_example', risk_characteristic_name='risk_characteristic_name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_schedule_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_schedule_delete

        removes tapi.common.TimeRange
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/schedule/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_schedule_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_schedule_get

        returns tapi.common.TimeRange
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/schedule/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_schedule_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_schedule_post

        creates tapi.common.TimeRange
        """
        body = TapiCommonTimeRangeWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/schedule/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_schedule_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_schedule_put

        creates or updates tapi.common.TimeRange
        """
        body = TapiCommonTimeRangeWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={uuid}/schedule/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_delete(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_delete

        removes tapi.connectivity.ConnectivityContext
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/',
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_get(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_get

        returns tapi.connectivity.ConnectivityContext
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_post(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_post

        creates tapi.connectivity.ConnectivityContext
        """
        body = TapiConnectivityConnectivityContextWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_connectivityconnectivity_context_put(self):
        """Test case for data_tapi_commoncontext_tapi_connectivityconnectivity_context_put

        creates or updates tapi.connectivity.ConnectivityContext
        """
        body = TapiConnectivityConnectivityContextWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-connectivity:connectivity-context/',
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_aggregated_connection_end_pointtopology_uuidaggregated_connection_end_point_node_uuidnode_edge_point_uuidaggregated_connection_end_point_connection_end_point_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_aggregated_connection_end_pointtopology_uuidaggregated_connection_end_point_node_uuidnode_edge_point_uuidaggregated_connection_end_point_connection_end_point_uuid_get

        returns tapi.connectivity.ConnectionEndPointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/tapi-connectivity:cep-list/connection-end-point={connection-end-point-uuid}/aggregated-connection-end-point={topology-uuid},{aggregated-connection-end-point-node-uuid},{node-edge-point-uuid},{aggregated-connection-end-point-connection-end-point-uuid}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example', connection_end_point_uuid='connection_end_point_uuid_example', topology_uuid='topology_uuid_example', aggregated_connection_end_point_node_uuid='aggregated_connection_end_point_node_uuid_example', node_edge_point_uuid='node_edge_point_uuid_example', aggregated_connection_end_point_connection_end_point_uuid='aggregated_connection_end_point_connection_end_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_cep_role_connection_spec_reference_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_cep_role_connection_spec_reference_get

        returns tapi.connectivity.ConnectionSpecReference
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/tapi-connectivity:cep-list/connection-end-point={connection-end-point-uuid}/cep-role/connection-spec-reference/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example', connection_end_point_uuid='connection_end_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_cep_role_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_cep_role_get

        returns tapi.connectivity.CepRole
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/tapi-connectivity:cep-list/connection-end-point={connection-end-point-uuid}/cep-role/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example', connection_end_point_uuid='connection_end_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_client_node_edge_pointtopology_uuidclient_node_edge_point_node_uuidnode_edge_point_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_client_node_edge_pointtopology_uuidclient_node_edge_point_node_uuidnode_edge_point_uuid_get

        returns tapi.topology.NodeEdgePointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/tapi-connectivity:cep-list/connection-end-point={connection-end-point-uuid}/client-node-edge-point={topology-uuid},{client-node-edge-point-node-uuid},{node-edge-point-uuid}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example', connection_end_point_uuid='connection_end_point_uuid_example', topology_uuid='topology_uuid_example', client_node_edge_point_node_uuid='client_node_edge_point_node_uuid_example', node_edge_point_uuid='node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_get

        returns tapi.connectivity.ConnectionEndPoint
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/tapi-connectivity:cep-list/connection-end-point={connection-end-point-uuid}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example', connection_end_point_uuid='connection_end_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/tapi-connectivity:cep-list/connection-end-point={connection-end-point-uuid}/name={value-name}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example', connection_end_point_uuid='connection_end_point_uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_parent_node_edge_point_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_parent_node_edge_point_get

        returns tapi.topology.NodeEdgePointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/tapi-connectivity:cep-list/connection-end-point={connection-end-point-uuid}/parent-node-edge-point/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example', connection_end_point_uuid='connection_end_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_get

        returns tapi.connectivity.CepList
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/tapi-connectivity:cep-list/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_connectivitycreate_connectivity_service_post(self):
        """Test case for operations_tapi_connectivitycreate_connectivity_service_post

        operates on tapi.connectivity.CreateConnectivityService
        """
        body = OperationsTapiconnectivitycreateconnectivityserviceBody()
        response = self.client.open(
            '/operations/tapi-connectivity:create-connectivity-service/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_connectivitydelete_connectivity_service_post(self):
        """Test case for operations_tapi_connectivitydelete_connectivity_service_post

        operates on tapi.connectivity.DeleteConnectivityService
        """
        body = OperationsTapiconnectivitydeleteconnectivityserviceBody()
        response = self.client.open(
            '/operations/tapi-connectivity:delete-connectivity-service/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_connectivityget_connection_details_post(self):
        """Test case for operations_tapi_connectivityget_connection_details_post

        operates on tapi.connectivity.GetConnectionDetails
        """
        body = OperationsTapiconnectivitygetconnectiondetailsBody()
        response = self.client.open(
            '/operations/tapi-connectivity:get-connection-details/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_connectivityget_connection_end_point_details_post(self):
        """Test case for operations_tapi_connectivityget_connection_end_point_details_post

        operates on tapi.connectivity.GetConnectionEndPointDetails
        """
        body = OperationsTapiconnectivitygetconnectionendpointdetailsBody()
        response = self.client.open(
            '/operations/tapi-connectivity:get-connection-end-point-details/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_connectivityget_connectivity_service_details_post(self):
        """Test case for operations_tapi_connectivityget_connectivity_service_details_post

        operates on tapi.connectivity.GetConnectivityServiceDetails
        """
        body = OperationsTapiconnectivitygetconnectivityservicedetailsBody()
        response = self.client.open(
            '/operations/tapi-connectivity:get-connectivity-service-details/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_connectivityget_connectivity_service_list_post(self):
        """Test case for operations_tapi_connectivityget_connectivity_service_list_post

        
        """
        response = self.client.open(
            '/operations/tapi-connectivity:get-connectivity-service-list/',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_connectivityupdate_connectivity_service_post(self):
        """Test case for operations_tapi_connectivityupdate_connectivity_service_post

        operates on tapi.connectivity.UpdateConnectivityService
        """
        body = OperationsTapiconnectivityupdateconnectivityserviceBody()
        response = self.client.open(
            '/operations/tapi-connectivity:update-connectivity-service/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
