import connexion
import six

from tapi_server.models.operations_tapipathcomputationcomputep2ppath_body import OperationsTapipathcomputationcomputep2ppathBody  # noqa: E501
from tapi_server.models.operations_tapipathcomputationdeletep2ppath_body import OperationsTapipathcomputationdeletep2ppathBody  # noqa: E501
from tapi_server.models.operations_tapipathcomputationoptimizep2ppath_body import OperationsTapipathcomputationoptimizep2ppathBody  # noqa: E501
from tapi_server.models.tapi_common_bandwidth_profile_wrapper import TapiCommonBandwidthProfileWrapper  # noqa: E501
from tapi_server.models.tapi_common_capacity_value_wrapper import TapiCommonCapacityValueWrapper  # noqa: E501
from tapi_server.models.tapi_common_capacity_wrapper import TapiCommonCapacityWrapper  # noqa: E501
from tapi_server.models.tapi_common_name_and_value_wrapper import TapiCommonNameAndValueWrapper  # noqa: E501
from tapi_server.models.tapi_common_service_interface_point_ref_wrapper import TapiCommonServiceInterfacePointRefWrapper  # noqa: E501
from tapi_server.models.tapi_path_computation_compute_p2_p_path import TapiPathComputationComputeP2PPath  # noqa: E501
from tapi_server.models.tapi_path_computation_delete_p2_p_path import TapiPathComputationDeleteP2PPath  # noqa: E501
from tapi_server.models.tapi_path_computation_optimize_p2_ppath import TapiPathComputationOptimizeP2Ppath  # noqa: E501
from tapi_server.models.tapi_path_computation_path_computation_context_wrapper import TapiPathComputationPathComputationContextWrapper  # noqa: E501
from tapi_server.models.tapi_path_computation_path_computation_service_wrapper import TapiPathComputationPathComputationServiceWrapper  # noqa: E501
from tapi_server.models.tapi_path_computation_path_objective_function_wrapper import TapiPathComputationPathObjectiveFunctionWrapper  # noqa: E501
from tapi_server.models.tapi_path_computation_path_optimization_constraint_wrapper import TapiPathComputationPathOptimizationConstraintWrapper  # noqa: E501
from tapi_server.models.tapi_path_computation_path_ref_wrapper import TapiPathComputationPathRefWrapper  # noqa: E501
from tapi_server.models.tapi_path_computation_path_service_end_point_wrapper import TapiPathComputationPathServiceEndPointWrapper  # noqa: E501
from tapi_server.models.tapi_path_computation_path_wrapper import TapiPathComputationPathWrapper  # noqa: E501
from tapi_server.models.tapi_path_computation_routing_constraint_wrapper import TapiPathComputationRoutingConstraintWrapper  # noqa: E501
from tapi_server.models.tapi_path_computation_topology_constraint_wrapper import TapiPathComputationTopologyConstraintWrapper  # noqa: E501
from tapi_server.models.tapi_path_computation_value_or_priority_wrapper import TapiPathComputationValueOrPriorityWrapper  # noqa: E501
from tapi_server.models.tapi_topology_cost_characteristic_wrapper import TapiTopologyCostCharacteristicWrapper  # noqa: E501
from tapi_server.models.tapi_topology_latency_characteristic_wrapper import TapiTopologyLatencyCharacteristicWrapper  # noqa: E501
from tapi_server.models.tapi_topology_link_ref_wrapper import TapiTopologyLinkRefWrapper  # noqa: E501
from tapi_server.models.tapi_topology_risk_characteristic_wrapper import TapiTopologyRiskCharacteristicWrapper  # noqa: E501
from tapi_server import util


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_delete():  # noqa: E501
    """removes tapi.path.computation.PathComputationContext

    Augments the base TAPI Context with PathComputationService information # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_get():  # noqa: E501
    """returns tapi.path.computation.PathComputationContext

    Augments the base TAPI Context with PathComputationService information # noqa: E501


    :rtype: TapiPathComputationPathComputationContextWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_service_post(body=None):  # noqa: E501
    """creates tapi.path.computation.PathComputationService

    none # noqa: E501

    :param body: tapi.path.computation.PathComputationService to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationPathComputationServiceWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_delete(uuid):  # noqa: E501
    """removes tapi.path.computation.PathComputationService

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_point_post(uuid, body=None):  # noqa: E501
    """creates tapi.path.computation.PathServiceEndPoint

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.path.computation.PathServiceEndPoint to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationPathServiceEndPointWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_delete(uuid, local_id):  # noqa: E501
    """removes tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_get(uuid, local_id):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_delete(uuid, local_id):  # noqa: E501
    """removes tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_get(uuid, local_id):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_delete(uuid, local_id):  # noqa: E501
    """removes tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_get(uuid, local_id):  # noqa: E501
    """returns tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiCommonBandwidthProfileWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_delete(uuid, local_id):  # noqa: E501
    """removes tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_get(uuid, local_id):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_delete(uuid, local_id):  # noqa: E501
    """removes tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_get(uuid, local_id):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_delete(uuid, local_id):  # noqa: E501
    """removes tapi.common.Capacity

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_get(uuid, local_id):  # noqa: E501
    """returns tapi.common.Capacity

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiCommonCapacityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.common.Capacity

    none # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.common.Capacity

    none # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_total_size_delete(uuid, local_id):  # noqa: E501
    """removes tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_total_size_get(uuid, local_id):  # noqa: E501
    """returns tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_total_size_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_total_size_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_delete(uuid, local_id):  # noqa: E501
    """removes tapi.path.computation.PathServiceEndPoint

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_get(uuid, local_id):  # noqa: E501
    """returns tapi.path.computation.PathServiceEndPoint

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiPathComputationPathServiceEndPointWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_name_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_namevalue_name_delete(uuid, local_id, value_name):  # noqa: E501
    """removes tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_namevalue_name_get(uuid, local_id, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_namevalue_name_put(uuid, local_id, value_name, body=None):  # noqa: E501
    """creates or updates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.path.computation.PathServiceEndPoint

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str
    :param body: tapi.path.computation.PathServiceEndPoint to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationPathServiceEndPointWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_service_interface_point_delete(uuid, local_id):  # noqa: E501
    """removes tapi.common.ServiceInterfacePointRef

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_service_interface_point_get(uuid, local_id):  # noqa: E501
    """returns tapi.common.ServiceInterfacePointRef

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param local_id: Id of end-point
    :type local_id: str

    :rtype: TapiCommonServiceInterfacePointRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_service_interface_point_post(uuid, local_id, body=None):  # noqa: E501
    """creates tapi.common.ServiceInterfacePointRef

    none # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_service_interface_point_put(uuid, local_id, body=None):  # noqa: E501
    """creates or updates tapi.common.ServiceInterfacePointRef

    none # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_get(uuid):  # noqa: E501
    """returns tapi.path.computation.PathComputationService

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str

    :rtype: TapiPathComputationPathComputationServiceWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_name_post(uuid, body=None):  # noqa: E501
    """creates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.common.NameAndValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonNameAndValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_namevalue_name_delete(uuid, value_name):  # noqa: E501
    """removes tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_namevalue_name_get(uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_namevalue_name_put(uuid, value_name, body=None):  # noqa: E501
    """creates or updates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_delete(uuid):  # noqa: E501
    """removes tapi.path.computation.PathObjectiveFunction

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_get(uuid):  # noqa: E501
    """returns tapi.path.computation.PathObjectiveFunction

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str

    :rtype: TapiPathComputationPathObjectiveFunctionWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_name_post(uuid, body=None):  # noqa: E501
    """creates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.common.NameAndValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonNameAndValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_namevalue_name_delete(uuid, value_name):  # noqa: E501
    """removes tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_namevalue_name_get(uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_namevalue_name_put(uuid, value_name, body=None):  # noqa: E501
    """creates or updates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_post(uuid, body=None):  # noqa: E501
    """creates tapi.path.computation.PathObjectiveFunction

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.path.computation.PathObjectiveFunction to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationPathObjectiveFunctionWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.path.computation.PathObjectiveFunction

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.path.computation.PathObjectiveFunction to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationPathObjectiveFunctionWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_delete(uuid):  # noqa: E501
    """removes tapi.path.computation.PathOptimizationConstraint

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_get(uuid):  # noqa: E501
    """returns tapi.path.computation.PathOptimizationConstraint

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str

    :rtype: TapiPathComputationPathOptimizationConstraintWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_name_post(uuid, body=None):  # noqa: E501
    """creates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.common.NameAndValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonNameAndValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_namevalue_name_delete(uuid, value_name):  # noqa: E501
    """removes tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_namevalue_name_get(uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_namevalue_name_put(uuid, value_name, body=None):  # noqa: E501
    """creates or updates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_post(uuid, body=None):  # noqa: E501
    """creates tapi.path.computation.PathOptimizationConstraint

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.path.computation.PathOptimizationConstraint to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationPathOptimizationConstraintWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.path.computation.PathOptimizationConstraint

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.path.computation.PathOptimizationConstraint to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationPathOptimizationConstraintWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_pathpath_uuid_get(uuid, path_uuid):  # noqa: E501
    """returns tapi.path.computation.PathRef

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param path_uuid: Id of path
    :type path_uuid: str

    :rtype: TapiPathComputationPathRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.path.computation.PathComputationService

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.path.computation.PathComputationService to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationPathComputationServiceWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_cost_characteristic_post(uuid, body=None):  # noqa: E501
    """creates tapi.topology.CostCharacteristic

    The list of costs where each cost relates to some aspect of the TopologicalEntity. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.topology.CostCharacteristic to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiTopologyCostCharacteristicWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_cost_characteristiccost_name_delete(uuid, cost_name):  # noqa: E501
    """removes tapi.topology.CostCharacteristic

    The list of costs where each cost relates to some aspect of the TopologicalEntity. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param cost_name: Id of cost-characteristic
    :type cost_name: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_cost_characteristiccost_name_get(uuid, cost_name):  # noqa: E501
    """returns tapi.topology.CostCharacteristic

    The list of costs where each cost relates to some aspect of the TopologicalEntity. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param cost_name: Id of cost-characteristic
    :type cost_name: str

    :rtype: TapiTopologyCostCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_cost_characteristiccost_name_put(uuid, cost_name, body=None):  # noqa: E501
    """creates or updates tapi.topology.CostCharacteristic

    The list of costs where each cost relates to some aspect of the TopologicalEntity. # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_delete(uuid):  # noqa: E501
    """removes tapi.path.computation.RoutingConstraint

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_get(uuid):  # noqa: E501
    """returns tapi.path.computation.RoutingConstraint

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str

    :rtype: TapiPathComputationRoutingConstraintWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_latency_characteristic_post(uuid, body=None):  # noqa: E501
    """creates tapi.topology.LatencyCharacteristic

    The effect on the latency of a queuing process. This only has significant effect for packet based systems and has a complex characteristic. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.topology.LatencyCharacteristic to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiTopologyLatencyCharacteristicWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_latency_characteristictraffic_property_name_delete(uuid, traffic_property_name):  # noqa: E501
    """removes tapi.topology.LatencyCharacteristic

    The effect on the latency of a queuing process. This only has significant effect for packet based systems and has a complex characteristic. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param traffic_property_name: Id of latency-characteristic
    :type traffic_property_name: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_latency_characteristictraffic_property_name_get(uuid, traffic_property_name):  # noqa: E501
    """returns tapi.topology.LatencyCharacteristic

    The effect on the latency of a queuing process. This only has significant effect for packet based systems and has a complex characteristic. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param traffic_property_name: Id of latency-characteristic
    :type traffic_property_name: str

    :rtype: TapiTopologyLatencyCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_latency_characteristictraffic_property_name_put(uuid, traffic_property_name, body=None):  # noqa: E501
    """creates or updates tapi.topology.LatencyCharacteristic

    The effect on the latency of a queuing process. This only has significant effect for packet based systems and has a complex characteristic. # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_cost_delete(uuid):  # noqa: E501
    """removes tapi.path.computation.ValueOrPriority

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_cost_get(uuid):  # noqa: E501
    """returns tapi.path.computation.ValueOrPriority

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str

    :rtype: TapiPathComputationValueOrPriorityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_cost_post(uuid, body=None):  # noqa: E501
    """creates tapi.path.computation.ValueOrPriority

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.path.computation.ValueOrPriority to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationValueOrPriorityWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_cost_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.path.computation.ValueOrPriority

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.path.computation.ValueOrPriority to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationValueOrPriorityWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_delay_delete(uuid):  # noqa: E501
    """removes tapi.path.computation.ValueOrPriority

    Delay unit is microseconds. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_delay_get(uuid):  # noqa: E501
    """returns tapi.path.computation.ValueOrPriority

    Delay unit is microseconds. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str

    :rtype: TapiPathComputationValueOrPriorityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_delay_post(uuid, body=None):  # noqa: E501
    """creates tapi.path.computation.ValueOrPriority

    Delay unit is microseconds. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.path.computation.ValueOrPriority to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationValueOrPriorityWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_delay_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.path.computation.ValueOrPriority

    Delay unit is microseconds. # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.path.computation.ValueOrPriority to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationValueOrPriorityWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_hops_delete(uuid):  # noqa: E501
    """removes tapi.path.computation.ValueOrPriority

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_hops_get(uuid):  # noqa: E501
    """returns tapi.path.computation.ValueOrPriority

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str

    :rtype: TapiPathComputationValueOrPriorityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_hops_post(uuid, body=None):  # noqa: E501
    """creates tapi.path.computation.ValueOrPriority

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.path.computation.ValueOrPriority to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationValueOrPriorityWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_hops_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.path.computation.ValueOrPriority

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.path.computation.ValueOrPriority to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationValueOrPriorityWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_post(uuid, body=None):  # noqa: E501
    """creates tapi.path.computation.RoutingConstraint

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.path.computation.RoutingConstraint to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationRoutingConstraintWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.path.computation.RoutingConstraint

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.path.computation.RoutingConstraint to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationRoutingConstraintWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_risk_diversity_characteristic_post(uuid, body=None):  # noqa: E501
    """creates tapi.topology.RiskCharacteristic

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.topology.RiskCharacteristic to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiTopologyRiskCharacteristicWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_risk_diversity_characteristicrisk_characteristic_name_delete(uuid, risk_characteristic_name):  # noqa: E501
    """removes tapi.topology.RiskCharacteristic

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param risk_characteristic_name: Id of risk-diversity-characteristic
    :type risk_characteristic_name: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_risk_diversity_characteristicrisk_characteristic_name_get(uuid, risk_characteristic_name):  # noqa: E501
    """returns tapi.topology.RiskCharacteristic

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param risk_characteristic_name: Id of risk-diversity-characteristic
    :type risk_characteristic_name: str

    :rtype: TapiTopologyRiskCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_risk_diversity_characteristicrisk_characteristic_name_put(uuid, risk_characteristic_name, body=None):  # noqa: E501
    """creates or updates tapi.topology.RiskCharacteristic

    none # noqa: E501

    :param uuid: Id of path-comp-service
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


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_topology_constraint_delete(uuid):  # noqa: E501
    """removes tapi.path.computation.TopologyConstraint

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_topology_constraint_get(uuid):  # noqa: E501
    """returns tapi.path.computation.TopologyConstraint

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str

    :rtype: TapiPathComputationTopologyConstraintWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_topology_constraint_post(uuid, body=None):  # noqa: E501
    """creates tapi.path.computation.TopologyConstraint

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.path.computation.TopologyConstraint to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationTopologyConstraintWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_topology_constraint_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.path.computation.TopologyConstraint

    none # noqa: E501

    :param uuid: Id of path-comp-service
    :type uuid: str
    :param body: tapi.path.computation.TopologyConstraint to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationTopologyConstraintWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_get(uuid):  # noqa: E501
    """returns tapi.path.computation.Path

    none # noqa: E501

    :param uuid: Id of path
    :type uuid: str

    :rtype: TapiPathComputationPathWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_linktopology_uuidlink_uuid_get(uuid, topology_uuid, link_uuid):  # noqa: E501
    """returns tapi.topology.LinkRef

    none # noqa: E501

    :param uuid: Id of path
    :type uuid: str
    :param topology_uuid: Id of link
    :type topology_uuid: str
    :param link_uuid: Id of link
    :type link_uuid: str

    :rtype: TapiTopologyLinkRefWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_namevalue_name_get(uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of path
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_cost_characteristiccost_name_get(uuid, cost_name):  # noqa: E501
    """returns tapi.topology.CostCharacteristic

    The list of costs where each cost relates to some aspect of the TopologicalEntity. # noqa: E501

    :param uuid: Id of path
    :type uuid: str
    :param cost_name: Id of cost-characteristic
    :type cost_name: str

    :rtype: TapiTopologyCostCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_get(uuid):  # noqa: E501
    """returns tapi.path.computation.RoutingConstraint

    none # noqa: E501

    :param uuid: Id of path
    :type uuid: str

    :rtype: TapiPathComputationRoutingConstraintWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_latency_characteristictraffic_property_name_get(uuid, traffic_property_name):  # noqa: E501
    """returns tapi.topology.LatencyCharacteristic

    The effect on the latency of a queuing process. This only has significant effect for packet based systems and has a complex characteristic. # noqa: E501

    :param uuid: Id of path
    :type uuid: str
    :param traffic_property_name: Id of latency-characteristic
    :type traffic_property_name: str

    :rtype: TapiTopologyLatencyCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_max_allowed_cost_get(uuid):  # noqa: E501
    """returns tapi.path.computation.ValueOrPriority

    none # noqa: E501

    :param uuid: Id of path
    :type uuid: str

    :rtype: TapiPathComputationValueOrPriorityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_max_allowed_delay_get(uuid):  # noqa: E501
    """returns tapi.path.computation.ValueOrPriority

    Delay unit is microseconds. # noqa: E501

    :param uuid: Id of path
    :type uuid: str

    :rtype: TapiPathComputationValueOrPriorityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_max_allowed_hops_get(uuid):  # noqa: E501
    """returns tapi.path.computation.ValueOrPriority

    none # noqa: E501

    :param uuid: Id of path
    :type uuid: str

    :rtype: TapiPathComputationValueOrPriorityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_risk_diversity_characteristicrisk_characteristic_name_get(uuid, risk_characteristic_name):  # noqa: E501
    """returns tapi.topology.RiskCharacteristic

    none # noqa: E501

    :param uuid: Id of path
    :type uuid: str
    :param risk_characteristic_name: Id of risk-diversity-characteristic
    :type risk_characteristic_name: str

    :rtype: TapiTopologyRiskCharacteristicWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_post(body=None):  # noqa: E501
    """creates tapi.path.computation.PathComputationContext

    Augments the base TAPI Context with PathComputationService information # noqa: E501

    :param body: tapi.path.computation.PathComputationContext to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationPathComputationContextWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_path_computationpath_computation_context_put(body=None):  # noqa: E501
    """creates or updates tapi.path.computation.PathComputationContext

    Augments the base TAPI Context with PathComputationService information # noqa: E501

    :param body: tapi.path.computation.PathComputationContext to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiPathComputationPathComputationContextWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def operations_tapi_path_computationcompute_p_2_p_path_post(body=None):  # noqa: E501
    """operates on tapi.path.computation.ComputeP2PPath

    operates on tapi.path.computation.ComputeP2PPath # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TapiPathComputationComputeP2PPath
    """
    if connexion.request.is_json:
        body = OperationsTapipathcomputationcomputep2ppathBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def operations_tapi_path_computationdelete_p_2_p_path_post(body=None):  # noqa: E501
    """operates on tapi.path.computation.DeleteP2PPath

    operates on tapi.path.computation.DeleteP2PPath # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TapiPathComputationDeleteP2PPath
    """
    if connexion.request.is_json:
        body = OperationsTapipathcomputationdeletep2ppathBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def operations_tapi_path_computationoptimize_p_2_ppath_post(body=None):  # noqa: E501
    """operates on tapi.path.computation.OptimizeP2Ppath

    operates on tapi.path.computation.OptimizeP2Ppath # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TapiPathComputationOptimizeP2Ppath
    """
    if connexion.request.is_json:
        body = OperationsTapipathcomputationoptimizep2ppathBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
