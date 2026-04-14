# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from tapi_server.models.operations_tapitopologygetlinkdetails_body import OperationsTapitopologygetlinkdetailsBody  # noqa: E501
from tapi_server.models.operations_tapitopologygetnodedetails_body import OperationsTapitopologygetnodedetailsBody  # noqa: E501
from tapi_server.models.operations_tapitopologygetnodeedgepointdetails_body import OperationsTapitopologygetnodeedgepointdetailsBody  # noqa: E501
from tapi_server.models.operations_tapitopologygettopologydetails_body import OperationsTapitopologygettopologydetailsBody  # noqa: E501
from tapi_server.models.tapi_common_bandwidth_profile_wrapper import TapiCommonBandwidthProfileWrapper  # noqa: E501
from tapi_server.models.tapi_common_capacity_value_wrapper import TapiCommonCapacityValueWrapper  # noqa: E501
from tapi_server.models.tapi_common_capacity_wrapper import TapiCommonCapacityWrapper  # noqa: E501
from tapi_server.models.tapi_common_name_and_value_wrapper import TapiCommonNameAndValueWrapper  # noqa: E501
from tapi_server.models.tapi_common_service_interface_point_ref_wrapper import TapiCommonServiceInterfacePointRefWrapper  # noqa: E501
from tapi_server.models.tapi_topology_connection_spec_reference_wrapper import TapiTopologyConnectionSpecReferenceWrapper  # noqa: E501
from tapi_server.models.tapi_topology_cost_characteristic_wrapper import TapiTopologyCostCharacteristicWrapper  # noqa: E501
from tapi_server.models.tapi_topology_get_link_details import TapiTopologyGetLinkDetails  # noqa: E501
from tapi_server.models.tapi_topology_get_node_details import TapiTopologyGetNodeDetails  # noqa: E501
from tapi_server.models.tapi_topology_get_node_edge_point_details import TapiTopologyGetNodeEdgePointDetails  # noqa: E501
from tapi_server.models.tapi_topology_get_topology_details import TapiTopologyGetTopologyDetails  # noqa: E501
from tapi_server.models.tapi_topology_get_topology_list import TapiTopologyGetTopologyList  # noqa: E501
from tapi_server.models.tapi_topology_inter_rule_group_wrapper import TapiTopologyInterRuleGroupWrapper  # noqa: E501
from tapi_server.models.tapi_topology_latency_characteristic_wrapper import TapiTopologyLatencyCharacteristicWrapper  # noqa: E501
from tapi_server.models.tapi_topology_link_wrapper import TapiTopologyLinkWrapper  # noqa: E501
from tapi_server.models.tapi_topology_network_topology_service_wrapper import TapiTopologyNetworkTopologyServiceWrapper  # noqa: E501
from tapi_server.models.tapi_topology_node_edge_point_ref_wrapper import TapiTopologyNodeEdgePointRefWrapper  # noqa: E501
from tapi_server.models.tapi_topology_node_owned_node_edge_point_wrapper import TapiTopologyNodeOwnedNodeEdgePointWrapper  # noqa: E501
from tapi_server.models.tapi_topology_node_rule_group_ref_wrapper import TapiTopologyNodeRuleGroupRefWrapper  # noqa: E501
from tapi_server.models.tapi_topology_node_rule_group_wrapper import TapiTopologyNodeRuleGroupWrapper  # noqa: E501
from tapi_server.models.tapi_topology_port_role_rule_wrapper import TapiTopologyPortRoleRuleWrapper  # noqa: E501
from tapi_server.models.tapi_topology_resilience_type_wrapper import TapiTopologyResilienceTypeWrapper  # noqa: E501
from tapi_server.models.tapi_topology_risk_characteristic_wrapper import TapiTopologyRiskCharacteristicWrapper  # noqa: E501
from tapi_server.models.tapi_topology_rule_wrapper import TapiTopologyRuleWrapper  # noqa: E501
from tapi_server.models.tapi_topology_signal_property_rule_wrapper import TapiTopologySignalPropertyRuleWrapper  # noqa: E501
from tapi_server.models.tapi_topology_topology_context_wrapper import TapiTopologyTopologyContextWrapper  # noqa: E501
from tapi_server.models.tapi_topology_topology_node_wrapper import TapiTopologyTopologyNodeWrapper  # noqa: E501
from tapi_server.models.tapi_topology_topology_ref_wrapper import TapiTopologyTopologyRefWrapper  # noqa: E501
from tapi_server.models.tapi_topology_topology_wrapper import TapiTopologyTopologyWrapper  # noqa: E501
from tapi_server.models.tapi_topology_validation_mechanism_wrapper import TapiTopologyValidationMechanismWrapper  # noqa: E501
from tapi_server.test import BaseTestCase


class TestTapiTopologyController(BaseTestCase):
    """TapiTopologyController integration test stubs"""

    def test_data_tapi_commoncontext_tapi_topologytopology_context_delete(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_delete

        removes tapi.topology.context.TopologyContext
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/',
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_get

        returns tapi.topology.context.TopologyContext
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_nw_topology_service_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_nw_topology_service_get

        returns tapi.topology.NetworkTopologyService
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/nw-topology-service/',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_nw_topology_service_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_nw_topology_service_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/nw-topology-service/name={value-name}/'.format(value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_nw_topology_service_topologytopology_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_nw_topology_service_topologytopology_uuid_get

        returns tapi.topology.TopologyRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/nw-topology-service/topology={topology-uuid}/'.format(topology_uuid='topology_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_post(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_post

        creates tapi.topology.context.TopologyContext
        """
        body = TapiTopologyTopologyContextWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_put(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_put

        creates or updates tapi.topology.context.TopologyContext
        """
        body = TapiTopologyTopologyContextWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/',
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_get

        returns tapi.topology.topologycontext.Topology
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_bandwidth_profile_committed_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_bandwidth_profile_committed_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/available-capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example', link_uuid='link_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_bandwidth_profile_committed_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_bandwidth_profile_committed_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/available-capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example', link_uuid='link_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_bandwidth_profile_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_bandwidth_profile_get

        returns tapi.common.BandwidthProfile
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/available-capacity/bandwidth-profile/'.format(uuid='uuid_example', link_uuid='link_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_bandwidth_profile_peak_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_bandwidth_profile_peak_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/available-capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example', link_uuid='link_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_bandwidth_profile_peak_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_bandwidth_profile_peak_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/available-capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example', link_uuid='link_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_get

        returns tapi.common.Capacity
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/available-capacity/'.format(uuid='uuid_example', link_uuid='link_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_total_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_total_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/available-capacity/total-size/'.format(uuid='uuid_example', link_uuid='link_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_cost_characteristiccost_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_cost_characteristiccost_name_get

        returns tapi.topology.CostCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/cost-characteristic={cost-name}/'.format(uuid='uuid_example', link_uuid='link_uuid_example', cost_name='cost_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_get

        returns tapi.topology.Link
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/'.format(uuid='uuid_example', link_uuid='link_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_latency_characteristictraffic_property_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_latency_characteristictraffic_property_name_get

        returns tapi.topology.LatencyCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/latency-characteristic={traffic-property-name}/'.format(uuid='uuid_example', link_uuid='link_uuid_example', traffic_property_name='traffic_property_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/name={value-name}/'.format(uuid='uuid_example', link_uuid='link_uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_node_edge_pointtopology_uuidnode_uuidnode_edge_point_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_node_edge_pointtopology_uuidnode_uuidnode_edge_point_uuid_get

        returns tapi.topology.NodeEdgePointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/node-edge-point={topology-uuid},{node-uuid},{node-edge-point-uuid}/'.format(uuid='uuid_example', link_uuid='link_uuid_example', topology_uuid='topology_uuid_example', node_uuid='node_uuid_example', node_edge_point_uuid='node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_resilience_type_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_resilience_type_get

        returns tapi.topology.ResilienceType
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/resilience-type/'.format(uuid='uuid_example', link_uuid='link_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_risk_characteristicrisk_characteristic_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_risk_characteristicrisk_characteristic_name_get

        returns tapi.topology.RiskCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/risk-characteristic={risk-characteristic-name}/'.format(uuid='uuid_example', link_uuid='link_uuid_example', risk_characteristic_name='risk_characteristic_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_bandwidth_profile_committed_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_bandwidth_profile_committed_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/total-potential-capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example', link_uuid='link_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_bandwidth_profile_committed_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_bandwidth_profile_committed_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/total-potential-capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example', link_uuid='link_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_bandwidth_profile_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_bandwidth_profile_get

        returns tapi.common.BandwidthProfile
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/total-potential-capacity/bandwidth-profile/'.format(uuid='uuid_example', link_uuid='link_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_bandwidth_profile_peak_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_bandwidth_profile_peak_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/total-potential-capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example', link_uuid='link_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_bandwidth_profile_peak_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_bandwidth_profile_peak_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/total-potential-capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example', link_uuid='link_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_get

        returns tapi.common.Capacity
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/total-potential-capacity/'.format(uuid='uuid_example', link_uuid='link_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_total_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_total_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/total-potential-capacity/total-size/'.format(uuid='uuid_example', link_uuid='link_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_validation_mechanismvalidation_mechanism_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_validation_mechanismvalidation_mechanism_get

        returns tapi.topology.ValidationMechanism
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/link={link-uuid}/validation-mechanism={validation-mechanism}/'.format(uuid='uuid_example', link_uuid='link_uuid_example', validation_mechanism='validation_mechanism_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_aggregated_node_edge_pointtopology_uuidaggregated_node_edge_point_node_uuidnode_edge_point_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_aggregated_node_edge_pointtopology_uuidaggregated_node_edge_point_node_uuidnode_edge_point_uuid_get

        returns tapi.topology.NodeEdgePointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/aggregated-node-edge-point={topology-uuid},{aggregated-node-edge-point-node-uuid},{node-edge-point-uuid}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', topology_uuid='topology_uuid_example', aggregated_node_edge_point_node_uuid='aggregated_node_edge_point_node_uuid_example', node_edge_point_uuid='node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_bandwidth_profile_committed_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_bandwidth_profile_committed_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/available-capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_bandwidth_profile_committed_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_bandwidth_profile_committed_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/available-capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example', node_uuid='node_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_bandwidth_profile_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_bandwidth_profile_get

        returns tapi.common.BandwidthProfile
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/available-capacity/bandwidth-profile/'.format(uuid='uuid_example', node_uuid='node_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_bandwidth_profile_peak_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_bandwidth_profile_peak_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/available-capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_bandwidth_profile_peak_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_bandwidth_profile_peak_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/available-capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example', node_uuid='node_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_get

        returns tapi.common.Capacity
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/available-capacity/'.format(uuid='uuid_example', node_uuid='node_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_total_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_total_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/available-capacity/total-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_cost_characteristiccost_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_cost_characteristiccost_name_get

        returns tapi.topology.CostCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/cost-characteristic={cost-name}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', cost_name='cost_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_encap_topology_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_encap_topology_get

        returns tapi.topology.TopologyRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/encap-topology/'.format(uuid='uuid_example', node_uuid='node_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_get

        returns tapi.topology.topology.Node
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/'.format(uuid='uuid_example', node_uuid='node_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_latency_characteristictraffic_property_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_latency_characteristictraffic_property_name_get

        returns tapi.topology.LatencyCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/latency-characteristic={traffic-property-name}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', traffic_property_name='traffic_property_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/name={value-name}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_bandwidth_profile_committed_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_bandwidth_profile_committed_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/available-capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_bandwidth_profile_committed_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_bandwidth_profile_committed_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/available-capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_bandwidth_profile_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_bandwidth_profile_get

        returns tapi.common.BandwidthProfile
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/available-capacity/bandwidth-profile/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_bandwidth_profile_peak_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_bandwidth_profile_peak_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/available-capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_bandwidth_profile_peak_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_bandwidth_profile_peak_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/available-capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_get

        returns tapi.common.Capacity
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/available-capacity/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_total_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_total_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/available-capacity/total-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_cost_characteristiccost_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_cost_characteristiccost_name_get

        returns tapi.topology.CostCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/cost-characteristic={cost-name}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', cost_name='cost_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_get

        returns tapi.topology.NodeRuleGroup
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_associated_node_rule_grouptopology_uuidassociated_node_rule_group_node_uuidassociated_node_rule_group_node_rule_group_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_associated_node_rule_grouptopology_uuidassociated_node_rule_group_node_uuidassociated_node_rule_group_node_rule_group_uuid_get

        returns tapi.topology.NodeRuleGroupRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/associated-node-rule-group={topology-uuid},{associated-node-rule-group-node-uuid},{associated-node-rule-group-node-rule-group-uuid}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example', topology_uuid='topology_uuid_example', associated_node_rule_group_node_uuid='associated_node_rule_group_node_uuid_example', associated_node_rule_group_node_rule_group_uuid='associated_node_rule_group_node_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_bandwidth_profile_committed_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_bandwidth_profile_committed_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/available-capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_bandwidth_profile_committed_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_bandwidth_profile_committed_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/available-capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_bandwidth_profile_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_bandwidth_profile_get

        returns tapi.common.BandwidthProfile
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/available-capacity/bandwidth-profile/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_bandwidth_profile_peak_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_bandwidth_profile_peak_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/available-capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_bandwidth_profile_peak_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_bandwidth_profile_peak_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/available-capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_get

        returns tapi.common.Capacity
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/available-capacity/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_total_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_total_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/available-capacity/total-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_cost_characteristiccost_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_cost_characteristiccost_name_get

        returns tapi.topology.CostCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/cost-characteristic={cost-name}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example', cost_name='cost_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_get

        returns tapi.topology.InterRuleGroup
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_latency_characteristictraffic_property_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_latency_characteristictraffic_property_name_get

        returns tapi.topology.LatencyCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/latency-characteristic={traffic-property-name}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example', traffic_property_name='traffic_property_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/name={value-name}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_risk_characteristicrisk_characteristic_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_risk_characteristicrisk_characteristic_name_get

        returns tapi.topology.RiskCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/risk-characteristic={risk-characteristic-name}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example', risk_characteristic_name='risk_characteristic_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_rulelocal_id_cep_port_role_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_rulelocal_id_cep_port_role_get

        returns tapi.topology.PortRoleRule
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/rule={local-id}/cep-port-role/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_rulelocal_id_connection_spec_reference_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_rulelocal_id_connection_spec_reference_get

        returns tapi.topology.ConnectionSpecReference
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/rule={local-id}/connection-spec-reference/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_rulelocal_id_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_rulelocal_id_get

        returns tapi.topology.Rule
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/rule={local-id}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_rulelocal_id_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_rulelocal_id_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/rule={local-id}/name={value-name}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example', local_id='local_id_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_rulelocal_id_signal_property_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_rulelocal_id_signal_property_get

        returns tapi.topology.SignalPropertyRule
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/rule={local-id}/signal-property/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_bandwidth_profile_committed_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_bandwidth_profile_committed_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/total-potential-capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_bandwidth_profile_committed_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_bandwidth_profile_committed_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/total-potential-capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_bandwidth_profile_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_bandwidth_profile_get

        returns tapi.common.BandwidthProfile
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/total-potential-capacity/bandwidth-profile/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_bandwidth_profile_peak_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_bandwidth_profile_peak_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/total-potential-capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_bandwidth_profile_peak_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_bandwidth_profile_peak_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/total-potential-capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_get

        returns tapi.common.Capacity
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/total-potential-capacity/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_total_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_total_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/inter-rule-group={inter-rule-group-uuid}/total-potential-capacity/total-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', inter_rule_group_uuid='inter_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_latency_characteristictraffic_property_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_latency_characteristictraffic_property_name_get

        returns tapi.topology.LatencyCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/latency-characteristic={traffic-property-name}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', traffic_property_name='traffic_property_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/name={value-name}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_node_edge_pointtopology_uuidnode_edge_point_node_uuidnode_edge_point_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_node_edge_pointtopology_uuidnode_edge_point_node_uuidnode_edge_point_uuid_get

        returns tapi.topology.NodeEdgePointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/node-edge-point={topology-uuid},{node-edge-point-node-uuid},{node-edge-point-uuid}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', topology_uuid='topology_uuid_example', node_edge_point_node_uuid='node_edge_point_node_uuid_example', node_edge_point_uuid='node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_node_rule_grouptopology_uuidnode_rule_group_node_uuidnode_rule_group_node_rule_group_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_node_rule_grouptopology_uuidnode_rule_group_node_uuidnode_rule_group_node_rule_group_uuid_get

        returns tapi.topology.NodeRuleGroupRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/node-rule-group={topology-uuid},{node-rule-group-node-uuid},{node-rule-group-node-rule-group-uuid}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', topology_uuid='topology_uuid_example', node_rule_group_node_uuid='node_rule_group_node_uuid_example', node_rule_group_node_rule_group_uuid='node_rule_group_node_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_risk_characteristicrisk_characteristic_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_risk_characteristicrisk_characteristic_name_get

        returns tapi.topology.RiskCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/risk-characteristic={risk-characteristic-name}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', risk_characteristic_name='risk_characteristic_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_rulelocal_id_cep_port_role_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_rulelocal_id_cep_port_role_get

        returns tapi.topology.PortRoleRule
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/rule={local-id}/cep-port-role/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_rulelocal_id_connection_spec_reference_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_rulelocal_id_connection_spec_reference_get

        returns tapi.topology.ConnectionSpecReference
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/rule={local-id}/connection-spec-reference/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_rulelocal_id_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_rulelocal_id_get

        returns tapi.topology.Rule
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/rule={local-id}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_rulelocal_id_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_rulelocal_id_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/rule={local-id}/name={value-name}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', local_id='local_id_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_rulelocal_id_signal_property_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_rulelocal_id_signal_property_get

        returns tapi.topology.SignalPropertyRule
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/rule={local-id}/signal-property/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_bandwidth_profile_committed_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_bandwidth_profile_committed_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/total-potential-capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_bandwidth_profile_committed_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_bandwidth_profile_committed_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/total-potential-capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_bandwidth_profile_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_bandwidth_profile_get

        returns tapi.common.BandwidthProfile
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/total-potential-capacity/bandwidth-profile/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_bandwidth_profile_peak_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_bandwidth_profile_peak_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/total-potential-capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_bandwidth_profile_peak_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_bandwidth_profile_peak_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/total-potential-capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_get

        returns tapi.common.Capacity
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/total-potential-capacity/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_total_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_total_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/node-rule-group={node-rule-group-uuid}/total-potential-capacity/total-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example', node_rule_group_uuid='node_rule_group_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_aggregated_node_edge_pointtopology_uuidaggregated_node_edge_point_node_uuidnode_edge_point_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_aggregated_node_edge_pointtopology_uuidaggregated_node_edge_point_node_uuidnode_edge_point_uuid_get

        returns tapi.topology.NodeEdgePointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/aggregated-node-edge-point={topology-uuid},{aggregated-node-edge-point-node-uuid},{node-edge-point-uuid}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example', topology_uuid='topology_uuid_example', aggregated_node_edge_point_node_uuid='aggregated_node_edge_point_node_uuid_example', node_edge_point_uuid='node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_bandwidth_profile_committed_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_bandwidth_profile_committed_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/available-capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_bandwidth_profile_committed_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_bandwidth_profile_committed_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/available-capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_bandwidth_profile_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_bandwidth_profile_get

        returns tapi.common.BandwidthProfile
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/available-capacity/bandwidth-profile/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_bandwidth_profile_peak_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_bandwidth_profile_peak_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/available-capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_bandwidth_profile_peak_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_bandwidth_profile_peak_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/available-capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_get

        returns tapi.common.Capacity
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/available-capacity/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_total_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_total_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/available-capacity/total-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_get

        returns tapi.topology.node.OwnedNodeEdgePoint
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_mapped_service_interface_pointservice_interface_point_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_mapped_service_interface_pointservice_interface_point_uuid_get

        returns tapi.common.ServiceInterfacePointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/mapped-service-interface-point={service-interface-point-uuid}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example', service_interface_point_uuid='service_interface_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/name={value-name}/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_bandwidth_profile_committed_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_bandwidth_profile_committed_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/total-potential-capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_bandwidth_profile_committed_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_bandwidth_profile_committed_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/total-potential-capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_bandwidth_profile_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_bandwidth_profile_get

        returns tapi.common.BandwidthProfile
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/total-potential-capacity/bandwidth-profile/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_bandwidth_profile_peak_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_bandwidth_profile_peak_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/total-potential-capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_bandwidth_profile_peak_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_bandwidth_profile_peak_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/total-potential-capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_get

        returns tapi.common.Capacity
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/total-potential-capacity/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_total_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_total_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/owned-node-edge-point={owned-node-edge-point-uuid}/total-potential-capacity/total-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example', owned_node_edge_point_uuid='owned_node_edge_point_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_bandwidth_profile_committed_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_bandwidth_profile_committed_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/total-potential-capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_bandwidth_profile_committed_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_bandwidth_profile_committed_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/total-potential-capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example', node_uuid='node_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_bandwidth_profile_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_bandwidth_profile_get

        returns tapi.common.BandwidthProfile
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/total-potential-capacity/bandwidth-profile/'.format(uuid='uuid_example', node_uuid='node_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_bandwidth_profile_peak_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_bandwidth_profile_peak_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/total-potential-capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_bandwidth_profile_peak_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_bandwidth_profile_peak_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/total-potential-capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example', node_uuid='node_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_get

        returns tapi.common.Capacity
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/total-potential-capacity/'.format(uuid='uuid_example', node_uuid='node_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_total_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_total_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-topology:topology-context/topology={uuid}/node={node-uuid}/total-potential-capacity/total-size/'.format(uuid='uuid_example', node_uuid='node_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_topologyget_link_details_post(self):
        """Test case for operations_tapi_topologyget_link_details_post

        operates on tapi.topology.GetLinkDetails
        """
        body = OperationsTapitopologygetlinkdetailsBody()
        response = self.client.open(
            '/operations/tapi-topology:get-link-details/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_topologyget_node_details_post(self):
        """Test case for operations_tapi_topologyget_node_details_post

        operates on tapi.topology.GetNodeDetails
        """
        body = OperationsTapitopologygetnodedetailsBody()
        response = self.client.open(
            '/operations/tapi-topology:get-node-details/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_topologyget_node_edge_point_details_post(self):
        """Test case for operations_tapi_topologyget_node_edge_point_details_post

        operates on tapi.topology.GetNodeEdgePointDetails
        """
        body = OperationsTapitopologygetnodeedgepointdetailsBody()
        response = self.client.open(
            '/operations/tapi-topology:get-node-edge-point-details/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_topologyget_topology_details_post(self):
        """Test case for operations_tapi_topologyget_topology_details_post

        operates on tapi.topology.GetTopologyDetails
        """
        body = OperationsTapitopologygettopologydetailsBody()
        response = self.client.open(
            '/operations/tapi-topology:get-topology-details/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_topologyget_topology_list_post(self):
        """Test case for operations_tapi_topologyget_topology_list_post

        
        """
        response = self.client.open(
            '/operations/tapi-topology:get-topology-list/',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
