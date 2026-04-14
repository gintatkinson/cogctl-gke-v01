import connexion
import six

from tapi_server.models.operations_tapicommongetserviceinterfacepointdetails_body import OperationsTapicommongetserviceinterfacepointdetailsBody  # noqa: E501
from tapi_server.models.operations_tapicommonupdateserviceinterfacepoint_body import OperationsTapicommonupdateserviceinterfacepointBody  # noqa: E501
from tapi_server.models.tapi_common_bandwidth_profile_wrapper import TapiCommonBandwidthProfileWrapper  # noqa: E501
from tapi_server.models.tapi_common_capacity_value_wrapper import TapiCommonCapacityValueWrapper  # noqa: E501
from tapi_server.models.tapi_common_capacity_wrapper import TapiCommonCapacityWrapper  # noqa: E501
from tapi_server.models.tapi_common_context_wrapper import TapiCommonContextWrapper  # noqa: E501
from tapi_server.models.tapi_common_get_service_interface_point_details import TapiCommonGetServiceInterfacePointDetails  # noqa: E501
from tapi_server.models.tapi_common_get_service_interface_point_list import TapiCommonGetServiceInterfacePointList  # noqa: E501
from tapi_server.models.tapi_common_name_and_value_wrapper import TapiCommonNameAndValueWrapper  # noqa: E501
from tapi_server.models.tapi_common_service_interface_point_wrapper import TapiCommonServiceInterfacePointWrapper  # noqa: E501
from tapi_server import util

from tapi_server.models.tapi_common_getserviceinterfacepointdetails_output import TapiCommonGetserviceinterfacepointdetailsOutput
from tapi_server.models.tapi_common_getserviceinterfacepointlist_output import TapiCommonGetserviceinterfacepointlistOutput
from tapi_server import database


def data_tapi_commoncontext_delete():  # noqa: E501
    """removes tapi.common.Context

    none # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_get():  # noqa: E501
    """returns tapi.common.Context

    none # noqa: E501


    :rtype: TapiCommonContextWrapper
    """
    return database.context


def data_tapi_commoncontext_name_post(body=None):  # noqa: E501
    """creates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param body: tapi.common.NameAndValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonNameAndValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_namevalue_name_delete(value_name):  # noqa: E501
    """removes tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param value_name: Id of name
    :type value_name: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_namevalue_name_get(value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_namevalue_name_put(value_name, body=None):  # noqa: E501
    """creates or updates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param value_name: Id of name
    :type value_name: str
    :param body: tapi.common.NameAndValue to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonNameAndValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_post(body=None):  # noqa: E501
    """creates tapi.common.Context

    none # noqa: E501

    :param body: tapi.common.Context to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonContextWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_put(body=None):  # noqa: E501
    """creates or updates tapi.common.Context

    none # noqa: E501

    :param body: tapi.common.Context to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonContextWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_point_post(body=None):  # noqa: E501
    """creates tapi.common.ServiceInterfacePoint

    none # noqa: E501

    :param body: tapi.common.ServiceInterfacePoint to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonServiceInterfacePointWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_available_capacity_bandwidth_profile_committed_burst_size_get(uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_available_capacity_bandwidth_profile_committed_information_rate_get(uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_available_capacity_bandwidth_profile_get(uuid):  # noqa: E501
    """returns tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str

    :rtype: TapiCommonBandwidthProfileWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_available_capacity_bandwidth_profile_peak_burst_size_get(uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_available_capacity_bandwidth_profile_peak_information_rate_get(uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_available_capacity_get(uuid):  # noqa: E501
    """returns tapi.common.Capacity

    Capacity available to be assigned. # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str

    :rtype: TapiCommonCapacityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_available_capacity_total_size_get(uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_delete(uuid):  # noqa: E501
    """removes tapi.common.ServiceInterfacePoint

    none # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_get(uuid):  # noqa: E501
    """returns tapi.common.ServiceInterfacePoint

    none # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str

    :rtype: TapiCommonServiceInterfacePointWrapper
    """
    return database.service_interface_point(uuid)


def data_tapi_commoncontext_service_interface_pointuuid_name_post(uuid, body=None):  # noqa: E501
    """creates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str
    :param body: tapi.common.NameAndValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonNameAndValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_namevalue_name_delete(uuid, value_name):  # noqa: E501
    """removes tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_namevalue_name_get(uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_namevalue_name_put(uuid, value_name, body=None):  # noqa: E501
    """creates or updates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of service-interface-point
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


def data_tapi_commoncontext_service_interface_pointuuid_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.common.ServiceInterfacePoint

    none # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str
    :param body: tapi.common.ServiceInterfacePoint to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonServiceInterfacePointWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_bandwidth_profile_committed_burst_size_get(uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_bandwidth_profile_committed_information_rate_get(uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_bandwidth_profile_get(uuid):  # noqa: E501
    """returns tapi.common.BandwidthProfile

    none # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str

    :rtype: TapiCommonBandwidthProfileWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_bandwidth_profile_peak_burst_size_get(uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_bandwidth_profile_peak_information_rate_get(uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    none # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_get(uuid):  # noqa: E501
    """returns tapi.common.Capacity

    An optimistic view of the capacity of the TopologicalEntity assuming that any shared capacity is available to be taken. # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str

    :rtype: TapiCommonCapacityWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_total_size_get(uuid):  # noqa: E501
    """returns tapi.common.CapacityValue

    Total capacity of the TopologicalEntity in MB/s. In case of bandwidthProfile, this is expected to same as the committedInformationRate. # noqa: E501

    :param uuid: Id of service-interface-point
    :type uuid: str

    :rtype: TapiCommonCapacityValueWrapper
    """
    return 'do some magic!'


def operations_tapi_commonget_service_interface_point_details_post(body=None):  # noqa: E501
    """operates on tapi.common.GetServiceInterfacePointDetails

    operates on tapi.common.GetServiceInterfacePointDetails # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TapiCommonGetServiceInterfacePointDetails
    """
    if connexion.request.is_json:
        body = OperationsTapicommongetserviceinterfacepointdetailsBody.from_dict(connexion.request.get_json())  # noqa: E501
    return TapiCommonGetServiceInterfacePointDetails(TapiCommonGetserviceinterfacepointdetailsOutput(
        database.service_interface_point(body.input.sip_id_or_name)))


def operations_tapi_commonget_service_interface_point_list_post():  # noqa: E501
    """operations_tapi_commonget_service_interface_point_list_post

     # noqa: E501


    :rtype: TapiCommonGetServiceInterfacePointList
    """
    return TapiCommonGetServiceInterfacePointList(TapiCommonGetserviceinterfacepointlistOutput(
        database.service_interface_point_list()))


def operations_tapi_commonupdate_service_interface_point_post(body=None):  # noqa: E501
    """operates on tapi.common.UpdateServiceInterfacePoint

    operates on tapi.common.UpdateServiceInterfacePoint # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = OperationsTapicommonupdateserviceinterfacepointBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
