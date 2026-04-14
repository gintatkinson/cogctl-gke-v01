import connexion
import six

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
from tapi_server import util

from tapi_server.models.tapi_connectivity_connection import TapiConnectivityConnection
from tapi_server.models.tapi_connectivity_connection_end_point_ref import TapiConnectivityConnectionEndPointRef
from tapi_server.models.tapi_connectivity_connection_ref import TapiConnectivityConnectionRef
from tapi_server.models.tapi_connectivity_connectivity_context import TapiConnectivityConnectivityContext
from tapi_server.models.tapi_connectivity_getconnectiondetails_output import TapiConnectivityGetconnectiondetailsOutput
from tapi_server.models.tapi_connectivity_getconnectionendpointdetails_output import TapiConnectivityGetconnectionendpointdetailsOutput
from tapi_server.models.tapi_connectivity_getconnectivityservicedetails_output import TapiConnectivityGetconnectivityservicedetailsOutput
from tapi_server.models.tapi_connectivity_getconnectivityservicelist_output import TapiConnectivityGetconnectivityservicelistOutput
from tapi_server import database


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_connection_end_pointtopology_uuidnode_uuidnode_edge_point_uuidconnection_end_point_uuid_get(uuid, topology_uuid, node_uuid, node_edge_point_uuid, connection_end_point_uuid):  # noqa: E501
    """returns tapi.connectivity.ConnectionEndPointRef

    none # noqa: E501

    :param uuid: Id of connection
    :type uuid: str
    :param topology_uuid: Id of connection-end-point
    :type topology_uuid: str
    :param node_uuid: Id of connection-end-point
    :type node_uuid: str
    :param node_edge_point_uuid: Id of connection-end-point
    :type node_edge_point_uuid: str
    :param connection_end_point_uuid: Id of connection-end-point
    :type connection_end_point_uuid: str

    :rtype: TapiConnectivityConnectionEndPointRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_connection_spec_reference_get(uuid):  # noqa: E501
    """returns tapi.connectivity.ConnectionSpecReference

    Provides the reference to the spec that defines the connection type and cepRoles. # noqa: E501

    :param uuid: Id of connection
    :type uuid: str

    :rtype: TapiConnectivityConnectionSpecReferenceWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_get(uuid):  # noqa: E501
    """returns tapi.connectivity.Connection

    none # noqa: E501

    :param uuid: Id of connection
    :type uuid: str

    :rtype: TapiConnectivityConnectionWrapper
    """
    return database.connection(uuid)


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_lower_connectionconnection_uuid_get(uuid, connection_uuid):  # noqa: E501
    """returns tapi.connectivity.ConnectionRef

    An Connection object supports a recursive aggregation relationship such that the internal construction of an Connection can be exposed as multiple lower level Connection objects (partitioning).                  Aggregation is used as for the Node/Topology  to allow changes in hierarchy.                   Connection aggregation reflects Node/Topology aggregation.                   The FC represents a Cross-Connection in an NE. The Cross-Connection in an NE is not necessarily the lowest level of FC partitioning. # noqa: E501

    :param uuid: Id of connection
    :type uuid: str
    :param connection_uuid: Id of lower-connection
    :type connection_uuid: str

    :rtype: TapiConnectivityConnectionRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_namevalue_name_get(uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of connection
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_routelocal_id_connection_end_pointtopology_uuidnode_uuidnode_edge_point_uuidconnection_end_point_uuid_get(uuid, local_id, topology_uuid, node_uuid, node_edge_point_uuid, connection_end_point_uuid):  # noqa: E501
    """returns tapi.connectivity.ConnectionEndPointRef

    none # noqa: E501

    :param uuid: Id of connection
    :type uuid: str
    :param local_id: Id of route
    :type local_id: str
    :param topology_uuid: Id of connection-end-point
    :type topology_uuid: str
    :param node_uuid: Id of connection-end-point
    :type node_uuid: str
    :param node_edge_point_uuid: Id of connection-end-point
    :type node_edge_point_uuid: str
    :param connection_end_point_uuid: Id of connection-end-point
    :type connection_end_point_uuid: str

    :rtype: TapiConnectivityConnectionEndPointRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_routelocal_id_get(uuid, local_id):  # noqa: E501
    """returns tapi.connectivity.Route

    none # noqa: E501

    :param uuid: Id of connection
    :type uuid: str
    :param local_id: Id of route
    :type local_id: str

    :rtype: TapiConnectivityRouteWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_routelocal_id_namevalue_name_get(uuid, local_id, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of connection
    :type uuid: str
    :param local_id: Id of route
    :type local_id: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_routelocal_id_resilience_route_pac_get(uuid, local_id):  # noqa: E501
    """returns tapi.connectivity.ResilienceRoute

    Provides optional resilience and state attributes to the Route. # noqa: E501

    :param uuid: Id of connection
    :type uuid: str
    :param local_id: Id of route
    :type local_id: str

    :rtype: TapiConnectivityResilienceRouteWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_routelocal_id_resilience_route_pac_namevalue_name_get(uuid, local_id, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of connection
    :type uuid: str
    :param local_id: Id of route
    :type local_id: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_supported_client_linktopology_uuidlink_uuid_get(uuid, topology_uuid, link_uuid):  # noqa: E501
    """returns tapi.topology.LinkRef

    none # noqa: E501

    :param uuid: Id of connection
    :type uuid: str
    :param topology_uuid: Id of supported-client-link
    :type topology_uuid: str
    :param link_uuid: Id of supported-client-link
    :type link_uuid: str

    :rtype: TapiTopologyLinkRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_get(uuid, switch_control_uuid):  # noqa: E501
    """returns tapi.connectivity.SwitchControl

    none # noqa: E501

    :param uuid: Id of connection
    :type uuid: str
    :param switch_control_uuid: Id of switch-control
    :type switch_control_uuid: str

    :rtype: TapiConnectivitySwitchControlWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_namevalue_name_get(uuid, switch_control_uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of connection
    :type uuid: str
    :param switch_control_uuid: Id of switch-control
    :type switch_control_uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_resilience_type_get(uuid, switch_control_uuid):  # noqa: E501
    """returns tapi.topology.ResilienceType

    none # noqa: E501

    :param uuid: Id of connection
    :type uuid: str
    :param switch_control_uuid: Id of switch-control
    :type switch_control_uuid: str

    :rtype: TapiTopologyResilienceTypeWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_sub_switch_controlconnection_uuidsub_switch_control_switch_control_uuid_get(uuid, switch_control_uuid, connection_uuid, sub_switch_control_switch_control_uuid):  # noqa: E501
    """returns tapi.connectivity.SwitchControlRef

    none # noqa: E501

    :param uuid: Id of connection
    :type uuid: str
    :param switch_control_uuid: Id of switch-control
    :type switch_control_uuid: str
    :param connection_uuid: Id of sub-switch-control
    :type connection_uuid: str
    :param sub_switch_control_switch_control_uuid: Id of sub-switch-control
    :type sub_switch_control_switch_control_uuid: str

    :rtype: TapiConnectivitySwitchControlRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_switchlocal_id_get(uuid, switch_control_uuid, local_id):  # noqa: E501
    """returns tapi.connectivity.Switch

    none # noqa: E501

    :param uuid: Id of connection
    :type uuid: str
    :param switch_control_uuid: Id of switch-control
    :type switch_control_uuid: str
    :param local_id: Id of switch
    :type local_id: str

    :rtype: TapiConnectivitySwitchWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_switchlocal_id_namevalue_name_get(uuid, switch_control_uuid, local_id, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of connection
    :type uuid: str
    :param switch_control_uuid: Id of switch-control
    :type switch_control_uuid: str
    :param local_id: Id of switch
    :type local_id: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_switchlocal_id_selected_connection_end_pointtopology_uuidnode_uuidnode_edge_point_uuidconnection_end_point_uuid_get(uuid, switch_control_uuid, local_id, topology_uuid, node_uuid, node_edge_point_uuid, connection_end_point_uuid):  # noqa: E501
    """returns tapi.connectivity.ConnectionEndPointRef

    none # noqa: E501

    :param uuid: Id of connection
    :type uuid: str
    :param switch_control_uuid: Id of switch-control
    :type switch_control_uuid: str
    :param local_id: Id of switch
    :type local_id: str
    :param topology_uuid: Id of selected-connection-end-point
    :type topology_uuid: str
    :param node_uuid: Id of selected-connection-end-point
    :type node_uuid: str
    :param node_edge_point_uuid: Id of selected-connection-end-point
    :type node_edge_point_uuid: str
    :param connection_end_point_uuid: Id of selected-connection-end-point
    :type connection_end_point_uuid: str

    :rtype: TapiConnectivityConnectionEndPointRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectionuuid_switch_controlswitch_control_uuid_switchlocal_id_selected_routeconnection_uuidroute_local_id_get(uuid, switch_control_uuid, local_id, connection_uuid, route_local_id):  # noqa: E501
    """returns tapi.connectivity.RouteRef

    none # noqa: E501

    :param uuid: Id of connection
    :type uuid: str
    :param switch_control_uuid: Id of switch-control
    :type switch_control_uuid: str
    :param local_id: Id of switch
    :type local_id: str
    :param connection_uuid: Id of selected-route
    :type connection_uuid: str
    :param route_local_id: Id of selected-route
    :type route_local_id: str

    :rtype: TapiConnectivityRouteRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_service_post(body=None):  # noqa: E501
    """creates tapi.connectivity.ConnectivityService

    none # noqa: E501

    :param body: tapi.connectivity.ConnectivityService to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        raw_body = connexion.request.get_json()
        if "tapi-connectivity:connectivity-service" in raw_body:
            raw_body["connectivity-service"] = raw_body.pop("tapi-connectivity:connectivity-service")
        if isinstance(raw_body["connectivity-service"], list) and len(raw_body["connectivity-service"]) > 0:
            raw_body["connectivity-service"] = raw_body["connectivity-service"][0]
        body = TapiConnectivityConnectivityServiceWrapper.from_dict(raw_body)  # noqa: E501

    connection = TapiConnectivityConnection(
        uuid=body.connectivity_service.uuid,
        connection_end_point=[
            TapiConnectivityConnectionEndPointRef(
                node_edge_point_uuid="node-1-port-3", connection_end_point_uuid="cep13"),
            TapiConnectivityConnectionEndPointRef(
                node_edge_point_uuid="node-3-port-2", connection_end_point_uuid="cep32"),
        ]
    )
    connection_ref = TapiConnectivityConnectionRef(connection.uuid)
    body.connectivity_service.connection = [ connection_ref ]

    if database.context.connectivity_context is None:
        database.context.connectivity_context = TapiConnectivityConnectivityContext(
            connectivity_service=[], connection=[]
        )

    database.context.connectivity_context.connection.append(connection)
    database.context.connectivity_context.connectivity_service.append(body.connectivity_service)


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_connectionconnection_uuid_get(uuid, connection_uuid):  # noqa: E501
    """returns tapi.connectivity.ConnectionRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param connection_uuid: Id of connection
    :type connection_uuid: str

    :rtype: TapiConnectivityConnectionRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_coroute_inclusion_delete(uuid):  # noqa: E501
    """removes tapi.connectivity.ConnectivityServiceRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_coroute_inclusion_get(uuid):  # noqa: E501
    """returns tapi.connectivity.ConnectivityServiceRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: TapiConnectivityConnectivityServiceRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_coroute_inclusion_post(uuid, body=None):  # noqa: E501
    """creates tapi.connectivity.ConnectivityServiceRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.connectivity.ConnectivityServiceRef to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiConnectivityConnectivityServiceRefWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_coroute_inclusion_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.connectivity.ConnectivityServiceRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.connectivity.ConnectivityServiceRef to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiConnectivityConnectivityServiceRefWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_cost_characteristic_post(uuid, body=None):  # noqa: E501
    """creates tapi.topology.CostCharacteristic

    The list of costs where each cost relates to some aspect of the TopologicalEntity. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.topology.CostCharacteristic to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiTopologyCostCharacteristicWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_cost_characteristiccost_name_delete(uuid, cost_name):  # noqa: E501
    """removes tapi.topology.CostCharacteristic

    The list of costs where each cost relates to some aspect of the TopologicalEntity. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param cost_name: Id of cost-characteristic
    :type cost_name: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_cost_characteristiccost_name_get(uuid, cost_name):  # noqa: E501
    """returns tapi.topology.CostCharacteristic

    The list of costs where each cost relates to some aspect of the TopologicalEntity. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param cost_name: Id of cost-characteristic
    :type cost_name: str

    :rtype: TapiTopologyCostCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_cost_characteristiccost_name_put(uuid, cost_name, body=None):  # noqa: E501
    """creates or updates tapi.topology.CostCharacteristic

    The list of costs where each cost relates to some aspect of the TopologicalEntity. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param cost_name: Id of cost-characteristic
    :type cost_name: str
    :param body: tapi.topology.CostCharacteristic to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiTopologyCostCharacteristicWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_delete(uuid):  # noqa: E501
    """removes tapi.connectivity.ConnectivityService

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: None
    """
    if database.context.connectivity_context is None:
        database.context.connectivity_context = TapiConnectivityConnectivityContext(
            connectivity_service=[], connection=[]
        )

    database.context.connectivity_context.connectivity_service = [
        connectivity_service
        for connectivity_service in database.context.connectivity_context.connectivity_service
        if connectivity_service.uuid != uuid # keep items with different uuid
    ]
    database.context.connectivity_context.connection = [
        connection
        for connection in database.context.connectivity_context.connection
        if connection.uuid != uuid # keep items with different uuid
    ]


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_diversity_exclusion_post(uuid, body=None):  # noqa: E501
    """creates tapi.connectivity.ConnectivityServiceRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.connectivity.ConnectivityServiceRef to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiConnectivityConnectivityServiceRefWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_diversity_exclusionconnectivity_service_uuid_delete(uuid, connectivity_service_uuid):  # noqa: E501
    """removes tapi.connectivity.ConnectivityServiceRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param connectivity_service_uuid: Id of diversity-exclusion
    :type connectivity_service_uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_diversity_exclusionconnectivity_service_uuid_get(uuid, connectivity_service_uuid):  # noqa: E501
    """returns tapi.connectivity.ConnectivityServiceRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param connectivity_service_uuid: Id of diversity-exclusion
    :type connectivity_service_uuid: str

    :rtype: TapiConnectivityConnectivityServiceRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_diversity_exclusionconnectivity_service_uuid_put(uuid, connectivity_service_uuid, body=None):  # noqa: E501
    """creates or updates tapi.connectivity.ConnectivityServiceRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param connectivity_service_uuid: Id of diversity-exclusion
    :type connectivity_service_uuid: str
    :param body: tapi.connectivity.ConnectivityServiceRef to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiConnectivityConnectivityServiceRefWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_point_post(uuid, body=None):  # noqa: E501
    """creates tapi.connectivity.ConnectivityServiceEndPoint

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.connectivity.ConnectivityServiceEndPoint to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiConnectivityConnectivityServiceEndPointWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_delete(uuid, local_id):  # noqa: E501
    """removes tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_get(uuid, local_id):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.common.CapacityValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.common.CapacityValue to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_delete(uuid, local_id):  # noqa: E501
    """removes tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_get(uuid, local_id):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.common.CapacityValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.common.CapacityValue to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_delete(uuid, local_id):  # noqa: E501
    """removes tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_get(uuid, local_id):  # noqa: E501
    """returns tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiCommonBandwidthProfileWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_delete(uuid, local_id):  # noqa: E501
    """removes tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_get(uuid, local_id):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.common.CapacityValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.common.CapacityValue to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_delete(uuid, local_id):  # noqa: E501
    """removes tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_get(uuid, local_id):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.common.CapacityValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.common.CapacityValue to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.common.BandwidthProfile to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonBandwidthProfileWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.common.BandwidthProfile to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonBandwidthProfileWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_delete(uuid, local_id):  # noqa: E501
    """removes tapi.common.Capacity

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_get(uuid, local_id):  # noqa: E501
    """returns tapi.common.Capacity

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiCommonCapacityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.common.Capacity

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.common.Capacity to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.common.Capacity

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.common.Capacity to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_total_size_delete(uuid, local_id):  # noqa: E501
    """removes tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_total_size_get(uuid, local_id):  # noqa: E501
    """returns tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_total_size_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.common.CapacityValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_capacity_total_size_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.common.CapacityValue to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_connection_end_pointtopology_uuidnode_uuidnode_edge_point_uuidconnection_end_point_uuid_get(uuid, local_id, topology_uuid, node_uuid, node_edge_point_uuid, connection_end_point_uuid):  # noqa: E501
    """returns tapi.connectivity.ConnectionEndPointRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param topology_uuid: Id of connection-end-point
    :type topology_uuid: str
    :param node_uuid: Id of connection-end-point
    :type node_uuid: str
    :param node_edge_point_uuid: Id of connection-end-point
    :type node_edge_point_uuid: str
    :param connection_end_point_uuid: Id of connection-end-point
    :type connection_end_point_uuid: str

    :rtype: TapiConnectivityConnectionEndPointRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_delete(uuid, local_id):  # noqa: E501
    """removes tapi.connectivity.ConnectivityServiceEndPoint

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_get(uuid, local_id):  # noqa: E501
    """returns tapi.connectivity.ConnectivityServiceEndPoint

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiConnectivityConnectivityServiceEndPointWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_name_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.common.NameAndValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonNameAndValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_namevalue_name_delete(uuid, local_id, value_name):  # noqa: E501
    """removes tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_namevalue_name_get(uuid, local_id, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_namevalue_name_put(uuid, local_id, value_name, body=None):  # noqa: E501
    """creates or updates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param value_name: Id of name
    :type value_name: str
    :param body: tapi.common.NameAndValue to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonNameAndValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_peer_fwd_connectivity_service_end_point_delete(uuid, local_id):  # noqa: E501
    """removes tapi.connectivity.ConnectivityServiceEndPointRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_peer_fwd_connectivity_service_end_point_get(uuid, local_id):  # noqa: E501
    """returns tapi.connectivity.ConnectivityServiceEndPointRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiConnectivityConnectivityServiceEndPointRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_peer_fwd_connectivity_service_end_point_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.connectivity.ConnectivityServiceEndPointRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.connectivity.ConnectivityServiceEndPointRef to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiConnectivityConnectivityServiceEndPointRefWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_peer_fwd_connectivity_service_end_point_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.connectivity.ConnectivityServiceEndPointRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.connectivity.ConnectivityServiceEndPointRef to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiConnectivityConnectivityServiceEndPointRefWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_protecting_connectivity_service_end_point_delete(uuid, local_id):  # noqa: E501
    """removes tapi.connectivity.ConnectivityServiceEndPointRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_protecting_connectivity_service_end_point_get(uuid, local_id):  # noqa: E501
    """returns tapi.connectivity.ConnectivityServiceEndPointRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiConnectivityConnectivityServiceEndPointRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_protecting_connectivity_service_end_point_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.connectivity.ConnectivityServiceEndPointRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.connectivity.ConnectivityServiceEndPointRef to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiConnectivityConnectivityServiceEndPointRefWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_protecting_connectivity_service_end_point_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.connectivity.ConnectivityServiceEndPointRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.connectivity.ConnectivityServiceEndPointRef to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiConnectivityConnectivityServiceEndPointRefWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.connectivity.ConnectivityServiceEndPoint

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.connectivity.ConnectivityServiceEndPoint to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiConnectivityConnectivityServiceEndPointWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_server_connectivity_service_end_point_delete(uuid, local_id):  # noqa: E501
    """removes tapi.connectivity.ConnectivityServiceEndPointRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_server_connectivity_service_end_point_get(uuid, local_id):  # noqa: E501
    """returns tapi.connectivity.ConnectivityServiceEndPointRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiConnectivityConnectivityServiceEndPointRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_server_connectivity_service_end_point_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.connectivity.ConnectivityServiceEndPointRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.connectivity.ConnectivityServiceEndPointRef to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiConnectivityConnectivityServiceEndPointRefWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_server_connectivity_service_end_point_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.connectivity.ConnectivityServiceEndPointRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.connectivity.ConnectivityServiceEndPointRef to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiConnectivityConnectivityServiceEndPointRefWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_service_interface_point_delete(uuid, local_id):  # noqa: E501
    """removes tapi.common.ServiceInterfacePointRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_service_interface_point_get(uuid, local_id):  # noqa: E501
    """returns tapi.common.ServiceInterfacePointRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiCommonServiceInterfacePointRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_service_interface_point_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.common.ServiceInterfacePointRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.common.ServiceInterfacePointRef to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonServiceInterfacePointRefWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_end_pointlocal_id_service_interface_point_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.common.ServiceInterfacePointRef

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.common.ServiceInterfacePointRef to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonServiceInterfacePointRefWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_get(uuid):  # noqa: E501
    """returns tapi.connectivity.ConnectivityService

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: TapiConnectivityConnectivityServiceWrapper
    """
    if database.context.connectivity_context is None:
        database.context.connectivity_context = TapiConnectivityConnectivityContext(
            connectivity_service=[], connection=[]
        )
    return database.connectivity_service(uuid)


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_latency_characteristic_post(uuid, body=None):  # noqa: E501
    """creates tapi.topology.LatencyCharacteristic

    The effect on the latency of a queuing process. This only has significant effect for packet based systems and has a complex characteristic. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.topology.LatencyCharacteristic to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiTopologyLatencyCharacteristicWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_latency_characteristictraffic_property_name_delete(uuid, traffic_property_name):  # noqa: E501
    """removes tapi.topology.LatencyCharacteristic

    The effect on the latency of a queuing process. This only has significant effect for packet based systems and has a complex characteristic. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param traffic_property_name: Id of latency-characteristic
    :type traffic_property_name: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_latency_characteristictraffic_property_name_get(uuid, traffic_property_name):  # noqa: E501
    """returns tapi.topology.LatencyCharacteristic

    The effect on the latency of a queuing process. This only has significant effect for packet based systems and has a complex characteristic. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param traffic_property_name: Id of latency-characteristic
    :type traffic_property_name: str

    :rtype: TapiTopologyLatencyCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_latency_characteristictraffic_property_name_put(uuid, traffic_property_name, body=None):  # noqa: E501
    """creates or updates tapi.topology.LatencyCharacteristic

    The effect on the latency of a queuing process. This only has significant effect for packet based systems and has a complex characteristic. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param traffic_property_name: Id of latency-characteristic
    :type traffic_property_name: str
    :param body: tapi.topology.LatencyCharacteristic to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiTopologyLatencyCharacteristicWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_cost_delete(uuid):  # noqa: E501
    """removes tapi.path.computation.ValueOrPriority

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_cost_get(uuid):  # noqa: E501
    """returns tapi.path.computation.ValueOrPriority

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: TapiPathComputationValueOrPriorityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_cost_post(uuid, body=None):  # noqa: E501
    """creates tapi.path.computation.ValueOrPriority

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.path.computation.ValueOrPriority to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationValueOrPriorityWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_cost_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.path.computation.ValueOrPriority

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.path.computation.ValueOrPriority to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationValueOrPriorityWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_delay_delete(uuid):  # noqa: E501
    """removes tapi.path.computation.ValueOrPriority

    Delay unit is microseconds. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_delay_get(uuid):  # noqa: E501
    """returns tapi.path.computation.ValueOrPriority

    Delay unit is microseconds. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: TapiPathComputationValueOrPriorityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_delay_post(uuid, body=None):  # noqa: E501
    """creates tapi.path.computation.ValueOrPriority

    Delay unit is microseconds. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.path.computation.ValueOrPriority to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationValueOrPriorityWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_delay_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.path.computation.ValueOrPriority

    Delay unit is microseconds. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.path.computation.ValueOrPriority to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationValueOrPriorityWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_hops_delete(uuid):  # noqa: E501
    """removes tapi.path.computation.ValueOrPriority

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_hops_get(uuid):  # noqa: E501
    """returns tapi.path.computation.ValueOrPriority

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: TapiPathComputationValueOrPriorityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_hops_post(uuid, body=None):  # noqa: E501
    """creates tapi.path.computation.ValueOrPriority

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.path.computation.ValueOrPriority to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationValueOrPriorityWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_max_allowed_hops_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.path.computation.ValueOrPriority

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.path.computation.ValueOrPriority to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationValueOrPriorityWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_name_post(uuid, body=None):  # noqa: E501
    """creates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.common.NameAndValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonNameAndValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_namevalue_name_delete(uuid, value_name):  # noqa: E501
    """removes tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_namevalue_name_get(uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_namevalue_name_put(uuid, value_name, body=None):  # noqa: E501
    """creates or updates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str
    :param body: tapi.common.NameAndValue to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonNameAndValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.connectivity.ConnectivityService

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.connectivity.ConnectivityService to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiConnectivityConnectivityServiceWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_burst_size_delete(uuid):  # noqa: E501
    """removes tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_burst_size_get(uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_burst_size_post(uuid, body=None):  # noqa: E501
    """creates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.common.CapacityValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_burst_size_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.common.CapacityValue to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_information_rate_delete(uuid):  # noqa: E501
    """removes tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_information_rate_get(uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_information_rate_post(uuid, body=None):  # noqa: E501
    """creates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.common.CapacityValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_committed_information_rate_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.common.CapacityValue to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_delete(uuid):  # noqa: E501
    """removes tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_get(uuid):  # noqa: E501
    """returns tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: TapiCommonBandwidthProfileWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_burst_size_delete(uuid):  # noqa: E501
    """removes tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_burst_size_get(uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_burst_size_post(uuid, body=None):  # noqa: E501
    """creates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.common.CapacityValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_burst_size_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.common.CapacityValue to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_information_rate_delete(uuid):  # noqa: E501
    """removes tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_information_rate_get(uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_information_rate_post(uuid, body=None):  # noqa: E501
    """creates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.common.CapacityValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_peak_information_rate_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.common.CapacityValue to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_post(uuid, body=None):  # noqa: E501
    """creates tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.common.BandwidthProfile to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonBandwidthProfileWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_bandwidth_profile_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.common.BandwidthProfile to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonBandwidthProfileWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_delete(uuid):  # noqa: E501
    """removes tapi.common.Capacity

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_get(uuid):  # noqa: E501
    """returns tapi.common.Capacity

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: TapiCommonCapacityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_post(uuid, body=None):  # noqa: E501
    """creates tapi.common.Capacity

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.common.Capacity to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.common.Capacity

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.common.Capacity to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_total_size_delete(uuid):  # noqa: E501
    """removes tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_total_size_get(uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_total_size_post(uuid, body=None):  # noqa: E501
    """creates tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.common.CapacityValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_requested_capacity_total_size_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.common.CapacityValue to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonCapacityValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_resilience_type_delete(uuid):  # noqa: E501
    """removes tapi.topology.ResilienceType

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_resilience_type_get(uuid):  # noqa: E501
    """returns tapi.topology.ResilienceType

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: TapiTopologyResilienceTypeWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_resilience_type_post(uuid, body=None):  # noqa: E501
    """creates tapi.topology.ResilienceType

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.topology.ResilienceType to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiTopologyResilienceTypeWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_resilience_type_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.topology.ResilienceType

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.topology.ResilienceType to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiTopologyResilienceTypeWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_risk_diversity_characteristic_post(uuid, body=None):  # noqa: E501
    """creates tapi.topology.RiskCharacteristic

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.topology.RiskCharacteristic to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiTopologyRiskCharacteristicWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_risk_diversity_characteristicrisk_characteristic_name_delete(uuid, risk_characteristic_name):  # noqa: E501
    """removes tapi.topology.RiskCharacteristic

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param risk_characteristic_name: Id of risk-diversity-characteristic
    :type risk_characteristic_name: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_risk_diversity_characteristicrisk_characteristic_name_get(uuid, risk_characteristic_name):  # noqa: E501
    """returns tapi.topology.RiskCharacteristic

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param risk_characteristic_name: Id of risk-diversity-characteristic
    :type risk_characteristic_name: str

    :rtype: TapiTopologyRiskCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_risk_diversity_characteristicrisk_characteristic_name_put(uuid, risk_characteristic_name, body=None):  # noqa: E501
    """creates or updates tapi.topology.RiskCharacteristic

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param risk_characteristic_name: Id of risk-diversity-characteristic
    :type risk_characteristic_name: str
    :param body: tapi.topology.RiskCharacteristic to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiTopologyRiskCharacteristicWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_schedule_delete(uuid):  # noqa: E501
    """removes tapi.common.TimeRange

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_schedule_get(uuid):  # noqa: E501
    """returns tapi.common.TimeRange

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str

    :rtype: TapiCommonTimeRangeWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_schedule_post(uuid, body=None):  # noqa: E501
    """creates tapi.common.TimeRange

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.common.TimeRange to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonTimeRangeWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_connectivity_serviceuuid_schedule_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.common.TimeRange

    none # noqa: E501

    :param uuid: Id of connectivity-service
    :type uuid: str
    :param body: tapi.common.TimeRange to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonTimeRangeWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_delete():  # noqa: E501
    """removes tapi.connectivity.ConnectivityContext

    Augments the base TAPI Context with ConnectivityService information # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_get():  # noqa: E501
    """returns tapi.connectivity.ConnectivityContext

    Augments the base TAPI Context with ConnectivityService information # noqa: E501


    :rtype: TapiConnectivityConnectivityContextWrapper
    """
    if database.context.connectivity_context is None:
        database.context.connectivity_context = TapiConnectivityConnectivityContext(
            connectivity_service=[], connection=[]
        )
    return database.connectivity_context()


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_post(body=None):  # noqa: E501
    """creates tapi.connectivity.ConnectivityContext

    Augments the base TAPI Context with ConnectivityService information # noqa: E501

    :param body: tapi.connectivity.ConnectivityContext to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        #body = TapiConnectivityConnectivityContextWrapper.from_dict(connexion.request.get_json())  # noqa: E501
        raw_body = connexion.request.get_json()
        if "tapi-connectivity:connectivity-service" in raw_body:
            raw_body["connectivity-service"] = raw_body.pop("tapi-connectivity:connectivity-service")
        if isinstance(raw_body["connectivity-service"], list) and len(raw_body["connectivity-service"]) > 0:
            raw_body["connectivity-service"] = raw_body["connectivity-service"][0]
        
        connectivity_service = raw_body["connectivity-service"]
        if "connectivity-constraint" in connectivity_service:
            connectivity_constraint = connectivity_service.pop("connectivity-constraint")
            if "requested-capacity" in connectivity_constraint:
                connectivity_service["requested-capacity"] = connectivity_constraint.pop("requested-capacity")
            if "connectivity-direction" in connectivity_constraint:
                connectivity_service["connectivity-direction"] = connectivity_constraint.pop("connectivity-direction")

        body = TapiConnectivityConnectivityServiceWrapper.from_dict(raw_body)  # noqa: E501

    connection = TapiConnectivityConnection(
        uuid=body.connectivity_service.uuid,
        connection_end_point=[
            TapiConnectivityConnectionEndPointRef(
                node_edge_point_uuid="node-1-port-3", connection_end_point_uuid="cep13"),
            TapiConnectivityConnectionEndPointRef(
                node_edge_point_uuid="node-3-port-2", connection_end_point_uuid="cep32"),
        ]
    )
    connection_ref = TapiConnectivityConnectionRef(connection.uuid)
    body.connectivity_service.connection = [ connection_ref ]

    if database.context.connectivity_context is None:
        database.context.connectivity_context = TapiConnectivityConnectivityContext(
            connectivity_service=[], connection=[]
        )

    database.context.connectivity_context.connection.append(connection)
    database.context.connectivity_context.connectivity_service.append(body.connectivity_service)


def data_tapi_commoncontext_tapi_connectivityconnectivity_context_put(body=None):  # noqa: E501
    """creates or updates tapi.connectivity.ConnectivityContext

    Augments the base TAPI Context with ConnectivityService information # noqa: E501

    :param body: tapi.connectivity.ConnectivityContext to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiConnectivityConnectivityContextWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_aggregated_connection_end_pointtopology_uuidaggregated_connection_end_point_node_uuidnode_edge_point_uuidaggregated_connection_end_point_connection_end_point_uuid_get(uuid, node_uuid, owned_node_edge_point_uuid, connection_end_point_uuid, topology_uuid, aggregated_connection_end_point_node_uuid, node_edge_point_uuid, aggregated_connection_end_point_connection_end_point_uuid):  # noqa: E501
    """returns tapi.connectivity.ConnectionEndPointRef

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str
    :param connection_end_point_uuid: Id of connection-end-point
    :type connection_end_point_uuid: str
    :param topology_uuid: Id of aggregated-connection-end-point
    :type topology_uuid: str
    :param aggregated_connection_end_point_node_uuid: Id of aggregated-connection-end-point
    :type aggregated_connection_end_point_node_uuid: str
    :param node_edge_point_uuid: Id of aggregated-connection-end-point
    :type node_edge_point_uuid: str
    :param aggregated_connection_end_point_connection_end_point_uuid: Id of aggregated-connection-end-point
    :type aggregated_connection_end_point_connection_end_point_uuid: str

    :rtype: TapiConnectivityConnectionEndPointRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_cep_role_connection_spec_reference_get(uuid, node_uuid, owned_node_edge_point_uuid, connection_end_point_uuid):  # noqa: E501
    """returns tapi.connectivity.ConnectionSpecReference

    The reference to the spec that defines the cep role. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str
    :param connection_end_point_uuid: Id of connection-end-point
    :type connection_end_point_uuid: str

    :rtype: TapiConnectivityConnectionSpecReferenceWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_cep_role_get(uuid, node_uuid, owned_node_edge_point_uuid, connection_end_point_uuid):  # noqa: E501
    """returns tapi.connectivity.CepRole

    Defines the role of the CEP in the context of the connection spec.                  There may be many cep role - connection spec combinations for a particular CEP where each corresponds to a specific connection associated with the CEP. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str
    :param connection_end_point_uuid: Id of connection-end-point
    :type connection_end_point_uuid: str

    :rtype: TapiConnectivityCepRoleWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_client_node_edge_pointtopology_uuidclient_node_edge_point_node_uuidnode_edge_point_uuid_get(uuid, node_uuid, owned_node_edge_point_uuid, connection_end_point_uuid, topology_uuid, client_node_edge_point_node_uuid, node_edge_point_uuid):  # noqa: E501
    """returns tapi.topology.NodeEdgePointRef

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str
    :param connection_end_point_uuid: Id of connection-end-point
    :type connection_end_point_uuid: str
    :param topology_uuid: Id of client-node-edge-point
    :type topology_uuid: str
    :param client_node_edge_point_node_uuid: Id of client-node-edge-point
    :type client_node_edge_point_node_uuid: str
    :param node_edge_point_uuid: Id of client-node-edge-point
    :type node_edge_point_uuid: str

    :rtype: TapiTopologyNodeEdgePointRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_get(uuid, node_uuid, owned_node_edge_point_uuid, connection_end_point_uuid):  # noqa: E501
    """returns tapi.connectivity.ConnectionEndPoint

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str
    :param connection_end_point_uuid: Id of connection-end-point
    :type connection_end_point_uuid: str

    :rtype: TapiConnectivityConnectionEndPointWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_namevalue_name_get(uuid, node_uuid, owned_node_edge_point_uuid, connection_end_point_uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str
    :param connection_end_point_uuid: Id of connection-end-point
    :type connection_end_point_uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_connection_end_pointconnection_end_point_uuid_parent_node_edge_point_get(uuid, node_uuid, owned_node_edge_point_uuid, connection_end_point_uuid):  # noqa: E501
    """returns tapi.topology.NodeEdgePointRef

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str
    :param connection_end_point_uuid: Id of connection-end-point
    :type connection_end_point_uuid: str

    :rtype: TapiTopologyNodeEdgePointRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_topologytopology_context_topologyuuid_nodenode_uuid_owned_node_edge_pointowned_node_edge_point_uuid_tapi_connectivitycep_list_get(uuid, node_uuid, owned_node_edge_point_uuid):  # noqa: E501
    """returns tapi.connectivity.CepList

    none # noqa: E501

    :param uuid: Id of topology
    :type uuid: str
    :param node_uuid: Id of node
    :type node_uuid: str
    :param owned_node_edge_point_uuid: Id of owned-node-edge-point
    :type owned_node_edge_point_uuid: str

    :rtype: TapiConnectivityCepListWrapper
    """
    return database.connection_end_point_list(uuid, node_uuid, owned_node_edge_point_uuid)


def operations_tapi_connectivitycreate_connectivity_service_post(body=None):  # noqa: E501
    """operates on tapi.connectivity.CreateConnectivityService

    operates on tapi.connectivity.CreateConnectivityService # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TapiConnectivityCreateConnectivityService
    """
    if connexion.request.is_json:
        body = OperationsTapiconnectivitycreateconnectivityserviceBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def operations_tapi_connectivitydelete_connectivity_service_post(body=None):  # noqa: E501
    """operates on tapi.connectivity.DeleteConnectivityService

    operates on tapi.connectivity.DeleteConnectivityService # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = OperationsTapiconnectivitydeleteconnectivityserviceBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def operations_tapi_connectivityget_connection_details_post(body=None):  # noqa: E501
    """operates on tapi.connectivity.GetConnectionDetails

    operates on tapi.connectivity.GetConnectionDetails # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TapiConnectivityGetConnectionDetails
    """
    if connexion.request.is_json:
        body = OperationsTapiconnectivitygetconnectiondetailsBody.from_dict(connexion.request.get_json())  # noqa: E501
    return TapiConnectivityGetConnectionDetails(TapiConnectivityGetconnectiondetailsOutput(
        database.connection(body.input.connection_id_or_name)))


def operations_tapi_connectivityget_connection_end_point_details_post(body=None):  # noqa: E501
    """operates on tapi.connectivity.GetConnectionEndPointDetails

    operates on tapi.connectivity.GetConnectionEndPointDetails # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TapiConnectivityGetConnectionEndPointDetails
    """
    if connexion.request.is_json:
        body = OperationsTapiconnectivitygetconnectionendpointdetailsBody.from_dict(connexion.request.get_json())  # noqa: E501
    return TapiConnectivityGetConnectionEndPointDetails(TapiConnectivityGetconnectionendpointdetailsOutput(
        database.connection_end_point(body.input.topology_id_or_name, 
                                      body.input.node_id_or_name,
                                      body.input.nep_id_or_name,
                                      body.input.cep_id_or_name)))


def operations_tapi_connectivityget_connectivity_service_details_post(body=None):  # noqa: E501
    """operates on tapi.connectivity.GetConnectivityServiceDetails

    operates on tapi.connectivity.GetConnectivityServiceDetails # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TapiConnectivityGetConnectivityServiceDetails
    """
    if connexion.request.is_json:
        body = OperationsTapiconnectivitygetconnectivityservicedetailsBody.from_dict(connexion.request.get_json())  # noqa: E501
    return TapiConnectivityGetConnectivityServiceDetails(TapiConnectivityGetconnectivityservicedetailsOutput(
        database.connectivity_service(body.input.service_id_or_name)))


def operations_tapi_connectivityget_connectivity_service_list_post():  # noqa: E501
    """operations_tapi_connectivityget_connectivity_service_list_post

     # noqa: E501


    :rtype: TapiConnectivityGetConnectivityServiceList
    """
    return TapiConnectivityGetConnectivityServiceList(TapiConnectivityGetconnectivityservicelistOutput(
        database.connectivity_service_list()))


def operations_tapi_connectivityupdate_connectivity_service_post(body=None):  # noqa: E501
    """operates on tapi.connectivity.UpdateConnectivityService

    operates on tapi.connectivity.UpdateConnectivityService # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TapiConnectivityUpdateConnectivityService
    """
    if connexion.request.is_json:
        body = OperationsTapiconnectivityupdateconnectivityserviceBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
