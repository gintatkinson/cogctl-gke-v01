import connexion
import six

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
from tapi_server import util

from tapi_server.models.tapi_topology_getlinkdetails_output import TapiTopologyGetlinkdetailsOutput
from tapi_server.models.tapi_topology_getnodeedgepointdetails_output import TapiTopologyGetnodeedgepointdetailsOutput
from tapi_server.models.tapi_topology_getnodedetails_output import TapiTopologyGetnodedetailsOutput
from tapi_server.models.tapi_topology_gettopologylist_output import TapiTopologyGettopologylistOutput
from tapi_server.models.tapi_topology_gettopologydetails_output import TapiTopologyGettopologydetailsOutput
from tapi_server import database


def data_tapi_commoncontext_tapi_topologytopology_context_delete():  # noqa: E501
    """removes tapi.topology.context.TopologyContext

    Augments the base TAPI Context with TopologyService information # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_get():  # noqa: E501
    """returns tapi.topology.context.TopologyContext

    Augments the base TAPI Context with TopologyService information # noqa: E501


    :rtype: TapiTopologyTopologyContextWrapper
    """
    return database.context.topology_context


def data_tapi_commoncontext_tapi_topologytopology_context_nw_topology_service_get():  # noqa: E501
    """returns tapi.topology.NetworkTopologyService

    none # noqa: E501


    :rtype: TapiTopologyNetworkTopologyServiceWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_nw_topology_service_namevalue_name_get(value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_nw_topology_service_topologytopology_uuid_get(topology_uuid):  # noqa: E501
    """returns tapi.topology.TopologyRef

    none # noqa: E501

    :param topology_uuid: Id of topology
    :type topology_uuid: str

    :rtype: TapiTopologyTopologyRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_post(body=None):  # noqa: E501
    """creates tapi.topology.context.TopologyContext

    Augments the base TAPI Context with TopologyService information # noqa: E501

    :param body: tapi.topology.TopologyContext to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiTopologyTopologyContextWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_put(body=None):  # noqa: E501
    """creates or updates tapi.topology.context.TopologyContext

    Augments the base TAPI Context with TopologyService information # noqa: E501

    :param body: tapi.topology.TopologyContext to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiTopologyTopologyContextWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_get(uuid):  # noqa: E501
    """returns tapi.topology.topologycontext.Topology

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str

    :rtype: TapiTopologyTopologyWrapper
    """
    return database.topology(uuid)


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_bandwidth_profile_committed_burst_size_get(uuid, link_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_bandwidth_profile_committed_information_rate_get(uuid, link_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_bandwidth_profile_get(uuid, link_uuid):  # noqa: E501
    """returns tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str

    :rtype: TapiCommonBandwidthProfileWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_bandwidth_profile_peak_burst_size_get(uuid, link_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_bandwidth_profile_peak_information_rate_get(uuid, link_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_get(uuid, link_uuid):  # noqa: E501
    """returns tapi.common.Capacity

    Capacity available to be assigned. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str

    :rtype: TapiCommonCapacityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_available_capacity_total_size_get(uuid, link_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_cost_characteristiccost_name_get(uuid, link_uuid, cost_name):  # noqa: E501
    """returns tapi.topology.CostCharacteristic

    The list of costs where each cost relates to some aspect of the TopologicalEntity. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str
    :param cost_name: Id of cost-characteristic
    :type cost_name: str

    :rtype: TapiTopologyCostCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_get(uuid, link_uuid):  # noqa: E501
    """returns tapi.topology.Link

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str

    :rtype: TapiTopologyLinkWrapper
    """
    return database.link(uuid, link_uuid)


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_latency_characteristictraffic_property_name_get(uuid, link_uuid, traffic_property_name):  # noqa: E501
    """returns tapi.topology.LatencyCharacteristic

    The effect on the latency of a queuing process. This only has significant effect for packet based systems and has a complex characteristic. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str
    :param traffic_property_name: Id of latency-characteristic
    :type traffic_property_name: str

    :rtype: TapiTopologyLatencyCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_namevalue_name_get(uuid, link_uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_node_edge_pointtopology_uuidnode_uuidnode_edge_point_uuid_get(uuid, link_uuid, topology_uuid, node_uuid, node_edge_point_uuid):  # noqa: E501
    """returns tapi.topology.NodeEdgePointRef

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str
    :param topology_uuid: Id of node-edge-point
    :type topology_uuid: str
    :param node_uuid: Id of node-edge-point
    :type node_uuid: str
    :param node_edge_point_uuid: Id of node-edge-point
    :type node_edge_point_uuid: str

    :rtype: TapiTopologyNodeEdgePointRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_resilience_type_get(uuid, link_uuid):  # noqa: E501
    """returns tapi.topology.ResilienceType

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str

    :rtype: TapiTopologyResilienceTypeWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_risk_characteristicrisk_characteristic_name_get(uuid, link_uuid, risk_characteristic_name):  # noqa: E501
    """returns tapi.topology.RiskCharacteristic

    A list of risk characteristics for consideration in an analysis of shared risk. Each element of the list represents a specific risk consideration. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str
    :param risk_characteristic_name: Id of risk-characteristic
    :type risk_characteristic_name: str

    :rtype: TapiTopologyRiskCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_bandwidth_profile_committed_burst_size_get(uuid, link_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_bandwidth_profile_committed_information_rate_get(uuid, link_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_bandwidth_profile_get(uuid, link_uuid):  # noqa: E501
    """returns tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str

    :rtype: TapiCommonBandwidthProfileWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_bandwidth_profile_peak_burst_size_get(uuid, link_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_bandwidth_profile_peak_information_rate_get(uuid, link_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_get(uuid, link_uuid):  # noqa: E501
    """returns tapi.common.Capacity

    An optimistic view of the capacity of the TopologicalEntity assuming that any shared capacity is available to be taken. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str

    :rtype: TapiCommonCapacityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_total_potential_capacity_total_size_get(uuid, link_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_linklink_uuid_validation_mechanismvalidation_mechanism_get(uuid, link_uuid, validation_mechanism):  # noqa: E501
    """returns tapi.topology.ValidationMechanism

    Provides details of the specific validation mechanism(s) used to confirm the presence of an intended topologicalEntity. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str
    :param validation_mechanism: Id of validation-mechanism
    :type validation_mechanism: str

    :rtype: TapiTopologyValidationMechanismWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_namevalue_name_get(uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_aggregated_node_edge_pointtopology_uuidaggregated_node_edge_point_node_uuidnode_edge_point_uuid_get(uuid, node_uuid, topology_uuid, aggregated_node_edge_point_node_uuid, node_edge_point_uuid):  # noqa: E501
    """returns tapi.topology.NodeEdgePointRef

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param topology_uuid: Id of aggregated-node-edge-point
    :type topology_uuid: str
    :param aggregated_node_edge_point_node_uuid: Id of aggregated-node-edge-point
    :type aggregated_node_edge_point_node_uuid: str
    :param node_edge_point_uuid: Id of aggregated-node-edge-point
    :type node_edge_point_uuid: str

    :rtype: TapiTopologyNodeEdgePointRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_bandwidth_profile_committed_burst_size_get(uuid, node_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_bandwidth_profile_committed_information_rate_get(uuid, node_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_bandwidth_profile_get(uuid, node_uuid):  # noqa: E501
    """returns tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str

    :rtype: TapiCommonBandwidthProfileWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_bandwidth_profile_peak_burst_size_get(uuid, node_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_bandwidth_profile_peak_information_rate_get(uuid, node_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_get(uuid, node_uuid):  # noqa: E501
    """returns tapi.common.Capacity

    Capacity available to be assigned. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str

    :rtype: TapiCommonCapacityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_available_capacity_total_size_get(uuid, node_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_cost_characteristiccost_name_get(uuid, node_uuid, cost_name):  # noqa: E501
    """returns tapi.topology.CostCharacteristic

    The list of costs where each cost relates to some aspect of the TopologicalEntity. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param cost_name: Id of cost-characteristic
    :type cost_name: str

    :rtype: TapiTopologyCostCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_encap_topology_get(uuid, node_uuid):  # noqa: E501
    """returns tapi.topology.TopologyRef

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str

    :rtype: TapiTopologyTopologyRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_get(uuid, node_uuid):  # noqa: E501
    """returns tapi.topology.topology.Node

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str

    :rtype: TapiTopologyTopologyNodeWrapper
    """
    return database.node(uuid, node_uuid)


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_latency_characteristictraffic_property_name_get(uuid, node_uuid, traffic_property_name):  # noqa: E501
    """returns tapi.topology.LatencyCharacteristic

    The effect on the latency of a queuing process. This only has significant effect for packet based systems and has a complex characteristic. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param traffic_property_name: Id of latency-characteristic
    :type traffic_property_name: str

    :rtype: TapiTopologyLatencyCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_namevalue_name_get(uuid, node_uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_bandwidth_profile_committed_burst_size_get(uuid, node_uuid, node_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_bandwidth_profile_committed_information_rate_get(uuid, node_uuid, node_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_bandwidth_profile_get(uuid, node_uuid, node_rule_group_uuid):  # noqa: E501
    """returns tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str

    :rtype: TapiCommonBandwidthProfileWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_bandwidth_profile_peak_burst_size_get(uuid, node_uuid, node_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_bandwidth_profile_peak_information_rate_get(uuid, node_uuid, node_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_get(uuid, node_uuid, node_rule_group_uuid):  # noqa: E501
    """returns tapi.common.Capacity

    Capacity available to be assigned. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str

    :rtype: TapiCommonCapacityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_available_capacity_total_size_get(uuid, node_uuid, node_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_cost_characteristiccost_name_get(uuid, node_uuid, node_rule_group_uuid, cost_name):  # noqa: E501
    """returns tapi.topology.CostCharacteristic

    The list of costs where each cost relates to some aspect of the TopologicalEntity. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param cost_name: Id of cost-characteristic
    :type cost_name: str

    :rtype: TapiTopologyCostCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_get(uuid, node_uuid, node_rule_group_uuid):  # noqa: E501
    """returns tapi.topology.NodeRuleGroup

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str

    :rtype: TapiTopologyNodeRuleGroupWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_associated_node_rule_grouptopology_uuidassociated_node_rule_group_node_uuidassociated_node_rule_group_node_rule_group_uuid_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid, topology_uuid, associated_node_rule_group_node_uuid, associated_node_rule_group_node_rule_group_uuid):  # noqa: E501
    """returns tapi.topology.NodeRuleGroupRef

    The NodeRuleGroups that the InterRuleGroup constrains interconnection between.                  The CEPs of the NEPs of a referenced NodeRuleGroup can interconnect to the CEPs of the NEPs of another referenced NodeRuleGroup constrained by the rules of the InterRuleGroup. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str
    :param topology_uuid: Id of associated-node-rule-group
    :type topology_uuid: str
    :param associated_node_rule_group_node_uuid: Id of associated-node-rule-group
    :type associated_node_rule_group_node_uuid: str
    :param associated_node_rule_group_node_rule_group_uuid: Id of associated-node-rule-group
    :type associated_node_rule_group_node_rule_group_uuid: str

    :rtype: TapiTopologyNodeRuleGroupRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_bandwidth_profile_committed_burst_size_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_bandwidth_profile_committed_information_rate_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_bandwidth_profile_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid):  # noqa: E501
    """returns tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str

    :rtype: TapiCommonBandwidthProfileWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_bandwidth_profile_peak_burst_size_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_bandwidth_profile_peak_information_rate_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid):  # noqa: E501
    """returns tapi.common.Capacity

    Capacity available to be assigned. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str

    :rtype: TapiCommonCapacityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_available_capacity_total_size_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_cost_characteristiccost_name_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid, cost_name):  # noqa: E501
    """returns tapi.topology.CostCharacteristic

    The list of costs where each cost relates to some aspect of the TopologicalEntity. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str
    :param cost_name: Id of cost-characteristic
    :type cost_name: str

    :rtype: TapiTopologyCostCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid):  # noqa: E501
    """returns tapi.topology.InterRuleGroup

    Nested NodeRuleGroups may have InterRuleGroups. The Superior NodeRuleGroup contains the nested NodeRuleGroups and their associated InterRuleGroups.                  This is equivalent to the Node-Topology hierarchy. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str

    :rtype: TapiTopologyInterRuleGroupWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_latency_characteristictraffic_property_name_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid, traffic_property_name):  # noqa: E501
    """returns tapi.topology.LatencyCharacteristic

    The effect on the latency of a queuing process. This only has significant effect for packet based systems and has a complex characteristic. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str
    :param traffic_property_name: Id of latency-characteristic
    :type traffic_property_name: str

    :rtype: TapiTopologyLatencyCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_namevalue_name_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_risk_characteristicrisk_characteristic_name_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid, risk_characteristic_name):  # noqa: E501
    """returns tapi.topology.RiskCharacteristic

    A list of risk characteristics for consideration in an analysis of shared risk. Each element of the list represents a specific risk consideration. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str
    :param risk_characteristic_name: Id of risk-characteristic
    :type risk_characteristic_name: str

    :rtype: TapiTopologyRiskCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_rulelocal_id_cep_port_role_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid, local_id):  # noqa: E501
    """returns tapi.topology.PortRoleRule

    Indicates the port role to which the rule applies.                   The port role is interpreted in the context of the connection type which is identified by the connection spec.                   The port role is not meaningful in the absence of a connection spec reference.                  If a node rule group carries a port role, that role applies also to the associated inter rule where the combination of the roles in the node rule groups at the ends of the inter group rule define the connection orientation.                  For example a root-and-leaf connection may be used in a node where a node rule group collects one set of NEPs has the port role &#x27;root&#x27; and another node rule group collects another set of NEPs has the port role &#x27;leaf&#x27; where these are joined by an inter rule group. This combination specifies an allowed orientation of the root-and-leaf connection.                  No port role statement means all port roles are allowed. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str
    :param local_id: Id of rule
    :type local_id: str

    :rtype: TapiTopologyPortRoleRuleWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_rulelocal_id_connection_spec_reference_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid, local_id):  # noqa: E501
    """returns tapi.topology.ConnectionSpecReference

    Identifies the type of connection that the rule applies to.                   If the attribute is not present then the rule applies to all types of connection supported by the device. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str
    :param local_id: Id of rule
    :type local_id: str

    :rtype: TapiTopologyConnectionSpecReferenceWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_rulelocal_id_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid, local_id):  # noqa: E501
    """returns tapi.topology.Rule

    The list of rules of the InterRuleGroup. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str
    :param local_id: Id of rule
    :type local_id: str

    :rtype: TapiTopologyRuleWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_rulelocal_id_namevalue_name_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid, local_id, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str
    :param local_id: Id of rule
    :type local_id: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_rulelocal_id_signal_property_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid, local_id):  # noqa: E501
    """returns tapi.topology.SignalPropertyRule

    The rule only applies to signals with the properties listed.                   If the attribute is not present then the rule applies to all signals. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str
    :param local_id: Id of rule
    :type local_id: str

    :rtype: TapiTopologySignalPropertyRuleWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_bandwidth_profile_committed_burst_size_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_bandwidth_profile_committed_information_rate_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_bandwidth_profile_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid):  # noqa: E501
    """returns tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str

    :rtype: TapiCommonBandwidthProfileWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_bandwidth_profile_peak_burst_size_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_bandwidth_profile_peak_information_rate_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid):  # noqa: E501
    """returns tapi.common.Capacity

    An optimistic view of the capacity of the TopologicalEntity assuming that any shared capacity is available to be taken. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str

    :rtype: TapiCommonCapacityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_inter_rule_groupinter_rule_group_uuid_total_potential_capacity_total_size_get(uuid, node_uuid, node_rule_group_uuid, inter_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param inter_rule_group_uuid: Id of inter-rule-group
    :type inter_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_latency_characteristictraffic_property_name_get(uuid, node_uuid, node_rule_group_uuid, traffic_property_name):  # noqa: E501
    """returns tapi.topology.LatencyCharacteristic

    The effect on the latency of a queuing process. This only has significant effect for packet based systems and has a complex characteristic. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param traffic_property_name: Id of latency-characteristic
    :type traffic_property_name: str

    :rtype: TapiTopologyLatencyCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_namevalue_name_get(uuid, node_uuid, node_rule_group_uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_node_edge_pointtopology_uuidnode_edge_point_node_uuidnode_edge_point_uuid_get(uuid, node_uuid, node_rule_group_uuid, topology_uuid, node_edge_point_node_uuid, node_edge_point_uuid):  # noqa: E501
    """returns tapi.topology.NodeEdgePointRef

    NEPs and their client CEPs that the rules apply to. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param topology_uuid: Id of node-edge-point
    :type topology_uuid: str
    :param node_edge_point_node_uuid: Id of node-edge-point
    :type node_edge_point_node_uuid: str
    :param node_edge_point_uuid: Id of node-edge-point
    :type node_edge_point_uuid: str

    :rtype: TapiTopologyNodeEdgePointRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_node_rule_grouptopology_uuidnode_rule_group_node_uuidnode_rule_group_node_rule_group_uuid_get(uuid, node_uuid, node_rule_group_uuid, topology_uuid, node_rule_group_node_uuid, node_rule_group_node_rule_group_uuid):  # noqa: E501
    """returns tapi.topology.NodeRuleGroupRef

    NodeRuleGroups may be nested such that finer grained rules may be applied.                  A nested rule group should have a subset of the NEPs of the superior rule group. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param topology_uuid: Id of node-rule-group
    :type topology_uuid: str
    :param node_rule_group_node_uuid: Id of node-rule-group
    :type node_rule_group_node_uuid: str
    :param node_rule_group_node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_node_rule_group_uuid: str

    :rtype: TapiTopologyNodeRuleGroupRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_risk_characteristicrisk_characteristic_name_get(uuid, node_uuid, node_rule_group_uuid, risk_characteristic_name):  # noqa: E501
    """returns tapi.topology.RiskCharacteristic

    A list of risk characteristics for consideration in an analysis of shared risk. Each element of the list represents a specific risk consideration. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param risk_characteristic_name: Id of risk-characteristic
    :type risk_characteristic_name: str

    :rtype: TapiTopologyRiskCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_rulelocal_id_cep_port_role_get(uuid, node_uuid, node_rule_group_uuid, local_id):  # noqa: E501
    """returns tapi.topology.PortRoleRule

    Indicates the port role to which the rule applies.                   The port role is interpreted in the context of the connection type which is identified by the connection spec.                   The port role is not meaningful in the absence of a connection spec reference.                  If a node rule group carries a port role, that role applies also to the associated inter rule where the combination of the roles in the node rule groups at the ends of the inter group rule define the connection orientation.                  For example a root-and-leaf connection may be used in a node where a node rule group collects one set of NEPs has the port role &#x27;root&#x27; and another node rule group collects another set of NEPs has the port role &#x27;leaf&#x27; where these are joined by an inter rule group. This combination specifies an allowed orientation of the root-and-leaf connection.                  No port role statement means all port roles are allowed. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param local_id: Id of rule
    :type local_id: str

    :rtype: TapiTopologyPortRoleRuleWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_rulelocal_id_connection_spec_reference_get(uuid, node_uuid, node_rule_group_uuid, local_id):  # noqa: E501
    """returns tapi.topology.ConnectionSpecReference

    Identifies the type of connection that the rule applies to.                   If the attribute is not present then the rule applies to all types of connection supported by the device. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param local_id: Id of rule
    :type local_id: str

    :rtype: TapiTopologyConnectionSpecReferenceWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_rulelocal_id_get(uuid, node_uuid, node_rule_group_uuid, local_id):  # noqa: E501
    """returns tapi.topology.Rule

    The list of rules of the NodeRuleGroup. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param local_id: Id of rule
    :type local_id: str

    :rtype: TapiTopologyRuleWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_rulelocal_id_namevalue_name_get(uuid, node_uuid, node_rule_group_uuid, local_id, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param local_id: Id of rule
    :type local_id: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_rulelocal_id_signal_property_get(uuid, node_uuid, node_rule_group_uuid, local_id):  # noqa: E501
    """returns tapi.topology.SignalPropertyRule

    The rule only applies to signals with the properties listed.                   If the attribute is not present then the rule applies to all signals. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str
    :param local_id: Id of rule
    :type local_id: str

    :rtype: TapiTopologySignalPropertyRuleWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_bandwidth_profile_committed_burst_size_get(uuid, node_uuid, node_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_bandwidth_profile_committed_information_rate_get(uuid, node_uuid, node_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_bandwidth_profile_get(uuid, node_uuid, node_rule_group_uuid):  # noqa: E501
    """returns tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str

    :rtype: TapiCommonBandwidthProfileWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_bandwidth_profile_peak_burst_size_get(uuid, node_uuid, node_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_bandwidth_profile_peak_information_rate_get(uuid, node_uuid, node_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_get(uuid, node_uuid, node_rule_group_uuid):  # noqa: E501
    """returns tapi.common.Capacity

    An optimistic view of the capacity of the TopologicalEntity assuming that any shared capacity is available to be taken. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str

    :rtype: TapiCommonCapacityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_node_rule_groupnode_rule_group_uuid_total_potential_capacity_total_size_get(uuid, node_uuid, node_rule_group_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param node_rule_group_uuid: Id of node-rule-group
    :type node_rule_group_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_aggregated_node_edge_pointtopology_uuidaggregated_node_edge_point_node_uuidnode_edge_point_uuid_get(uuid, node_uuid, owned_node_edge_point_uuid, topology_uuid, aggregated_node_edge_point_node_uuid, node_edge_point_uuid):  # noqa: E501
    """returns tapi.topology.NodeEdgePointRef

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str
    :param topology_uuid: Id of aggregated-node-edge-point
    :type topology_uuid: str
    :param aggregated_node_edge_point_node_uuid: Id of aggregated-node-edge-point
    :type aggregated_node_edge_point_node_uuid: str
    :param node_edge_point_uuid: Id of aggregated-node-edge-point
    :type node_edge_point_uuid: str

    :rtype: TapiTopologyNodeEdgePointRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_bandwidth_profile_committed_burst_size_get(uuid, node_uuid, owned_node_edge_point_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_bandwidth_profile_committed_information_rate_get(uuid, node_uuid, owned_node_edge_point_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_bandwidth_profile_get(uuid, node_uuid, owned_node_edge_point_uuid):  # noqa: E501
    """returns tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str

    :rtype: TapiCommonBandwidthProfileWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_bandwidth_profile_peak_burst_size_get(uuid, node_uuid, owned_node_edge_point_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_bandwidth_profile_peak_information_rate_get(uuid, node_uuid, owned_node_edge_point_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_get(uuid, node_uuid, owned_node_edge_point_uuid):  # noqa: E501
    """returns tapi.common.Capacity

    Capacity available to be assigned. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str

    :rtype: TapiCommonCapacityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_available_capacity_total_size_get(uuid, node_uuid, owned_node_edge_point_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_get(uuid, node_uuid, owned_node_edge_point_uuid):  # noqa: E501
    """returns tapi.topology.node.OwnedNodeEdgePoint

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str

    :rtype: TapiTopologyNodeOwnedNodeEdgePointWrapper
    """
    return database.node_edge_point(uuid, node_uuid, owned_node_edge_point_uuid)


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_mapped_service_interface_pointservice_interface_point_uuid_get(uuid, node_uuid, owned_node_edge_point_uuid, service_interface_point_uuid):  # noqa: E501
    """returns tapi.common.ServiceInterfacePointRef

    NodeEdgePoint mapped to more than ServiceInterfacePoint (slicing/virtualizing) or a ServiceInterfacePoint mapped to more than one NodeEdgePoint (load balancing/Resilience) should be considered experimental # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str
    :param service_interface_point_uuid: Id of mapped-service-interface-point
    :type service_interface_point_uuid: str

    :rtype: TapiCommonServiceInterfacePointRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_namevalue_name_get(uuid, node_uuid, owned_node_edge_point_uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_bandwidth_profile_committed_burst_size_get(uuid, node_uuid, owned_node_edge_point_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_bandwidth_profile_committed_information_rate_get(uuid, node_uuid, owned_node_edge_point_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_bandwidth_profile_get(uuid, node_uuid, owned_node_edge_point_uuid):  # noqa: E501
    """returns tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str

    :rtype: TapiCommonBandwidthProfileWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_bandwidth_profile_peak_burst_size_get(uuid, node_uuid, owned_node_edge_point_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_bandwidth_profile_peak_information_rate_get(uuid, node_uuid, owned_node_edge_point_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_get(uuid, node_uuid, owned_node_edge_point_uuid):  # noqa: E501
    """returns tapi.common.Capacity

    An optimistic view of the capacity of the TopologicalEntity assuming that any shared capacity is available to be taken. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str

    :rtype: TapiCommonCapacityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_total_potential_capacity_total_size_get(uuid, node_uuid, owned_node_edge_point_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_bandwidth_profile_committed_burst_size_get(uuid, node_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_bandwidth_profile_committed_information_rate_get(uuid, node_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_bandwidth_profile_get(uuid, node_uuid):  # noqa: E501
    """returns tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str

    :rtype: TapiCommonBandwidthProfileWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_bandwidth_profile_peak_burst_size_get(uuid, node_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_bandwidth_profile_peak_information_rate_get(uuid, node_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_get(uuid, node_uuid):  # noqa: E501
    """returns tapi.common.Capacity

    An optimistic view of the capacity of the TopologicalEntity assuming that any shared capacity is available to be taken. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str

    :rtype: TapiCommonCapacityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_total_potential_capacity_total_size_get(uuid, node_uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def operations_tapi_topologyget_link_details_post(body=None):  # noqa: E501
    """operates on tapi.topology.GetLinkDetails

    operates on tapi.topology.GetLinkDetails # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TapiTopologyGetLinkDetails
    """
    if connexion.request.is_json:
        body = OperationsTapitopologygetlinkdetailsBody.from_dict(connexion.request.get_json())  # noqa: E501

    return TapiTopologyGetLinkDetails(TapiTopologyGetlinkdetailsOutput(
        database.link(body.input.topology_id_or_name, body.input.link_id_or_name)))


def operations_tapi_topologyget_node_details_post(body=None):  # noqa: E501
    """operates on tapi.topology.GetNodeDetails

    operates on tapi.topology.GetNodeDetails # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TapiTopologyGetNodeDetails
    """
    if connexion.request.is_json:
        body = OperationsTapitopologygetnodedetailsBody.from_dict(connexion.request.get_json())  # noqa: E501
    return TapiTopologyGetNodeDetails(TapiTopologyGetnodedetailsOutput(
        database.node(body.input.topology_id_or_name,
                      body.input.node_id_or_name)))


def operations_tapi_topologyget_node_edge_point_details_post(body=None):  # noqa: E501
    """operates on tapi.topology.GetNodeEdgePointDetails

    operates on tapi.topology.GetNodeEdgePointDetails # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TapiTopologyGetNodeEdgePointDetails
    """
    if connexion.request.is_json:
        body = OperationsTapitopologygetnodeedgepointdetailsBody.from_dict(connexion.request.get_json())  # noqa: E501

    return TapiTopologyGetNodeEdgePointDetails(TapiTopologyGetnodeedgepointdetailsOutput(
        database.node_edge_point(body.input.topology_id_or_name,
                                 body.input.node_id_or_name,
                                 body.input.nep_id_or_name)))


def operations_tapi_topologyget_topology_details_post(body=None):  # noqa: E501
    """operates on tapi.topology.GetTopologyDetails

    operates on tapi.topology.GetTopologyDetails # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TapiTopologyGetTopologyDetails
    """
    if connexion.request.is_json:
        body = OperationsTapitopologygettopologydetailsBody.from_dict(connexion.request.get_json())  # noqa: E501

    return TapiTopologyGetTopologyDetails(TapiTopologyGettopologydetailsOutput(
        database.topology(body.input.topology_id_or_name)))


def operations_tapi_topologyget_topology_list_post():  # noqa: E501
    """operations_tapi_topologyget_topology_list_post

     # noqa: E501


    :rtype: TapiTopologyGetTopologyList
    """
    return TapiTopologyGetTopologyList(TapiTopologyGettopologylistOutput(
        database.topology_list()))
