import connexion
import six

from tapi_server.models.operations_tapinotificationcreatenotificationsubscriptionservice_body import OperationsTapinotificationcreatenotificationsubscriptionserviceBody  # noqa: E501
from tapi_server.models.operations_tapinotificationdeletenotificationsubscriptionservice_body import OperationsTapinotificationdeletenotificationsubscriptionserviceBody  # noqa: E501
from tapi_server.models.operations_tapinotificationgetnotificationlist_body import OperationsTapinotificationgetnotificationlistBody  # noqa: E501
from tapi_server.models.operations_tapinotificationgetnotificationsubscriptionservicedetails_body import OperationsTapinotificationgetnotificationsubscriptionservicedetailsBody  # noqa: E501
from tapi_server.models.operations_tapinotificationupdatenotificationsubscriptionservice_body import OperationsTapinotificationupdatenotificationsubscriptionserviceBody  # noqa: E501
from tapi_server.models.tapi_common_name_and_value_wrapper import TapiCommonNameAndValueWrapper  # noqa: E501
from tapi_server.models.tapi_notification_alarm_info_wrapper import TapiNotificationAlarmInfoWrapper  # noqa: E501
from tapi_server.models.tapi_notification_create_notification_subscription_service import TapiNotificationCreateNotificationSubscriptionService  # noqa: E501
from tapi_server.models.tapi_notification_delete_notification_subscription_service import TapiNotificationDeleteNotificationSubscriptionService  # noqa: E501
from tapi_server.models.tapi_notification_get_notification_list import TapiNotificationGetNotificationList  # noqa: E501
from tapi_server.models.tapi_notification_get_notification_subscription_service_details import TapiNotificationGetNotificationSubscriptionServiceDetails  # noqa: E501
from tapi_server.models.tapi_notification_get_notification_subscription_service_list import TapiNotificationGetNotificationSubscriptionServiceList  # noqa: E501
from tapi_server.models.tapi_notification_get_supported_notification_types import TapiNotificationGetSupportedNotificationTypes  # noqa: E501
from tapi_server.models.tapi_notification_name_and_value_change_wrapper import TapiNotificationNameAndValueChangeWrapper  # noqa: E501
from tapi_server.models.tapi_notification_notification_channel_wrapper import TapiNotificationNotificationChannelWrapper  # noqa: E501
from tapi_server.models.tapi_notification_notification_context_wrapper import TapiNotificationNotificationContextWrapper  # noqa: E501
from tapi_server.models.tapi_notification_notification_subscription_service_wrapper import TapiNotificationNotificationSubscriptionServiceWrapper  # noqa: E501
from tapi_server.models.tapi_notification_notification_wrapper import TapiNotificationNotificationWrapper  # noqa: E501
from tapi_server.models.tapi_notification_subscription_filter_wrapper import TapiNotificationSubscriptionFilterWrapper  # noqa: E501
from tapi_server.models.tapi_notification_tca_info_wrapper import TapiNotificationTcaInfoWrapper  # noqa: E501
from tapi_server.models.tapi_notification_update_notification_subscription_service import TapiNotificationUpdateNotificationSubscriptionService  # noqa: E501
from tapi_server import util


def data_tapi_commoncontext_tapi_notificationnotification_context_delete():  # noqa: E501
    """removes tapi.notification.NotificationContext

    Augments the base TAPI Context with NotificationService information # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_get():  # noqa: E501
    """returns tapi.notification.NotificationContext

    Augments the base TAPI Context with NotificationService information # noqa: E501


    :rtype: TapiNotificationNotificationContextWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscription_post(body=None):  # noqa: E501
    """creates tapi.notification.NotificationSubscriptionService

    none # noqa: E501

    :param body: tapi.notification.NotificationSubscriptionService to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiNotificationNotificationSubscriptionServiceWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_delete(uuid):  # noqa: E501
    """removes tapi.notification.NotificationSubscriptionService

    none # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_get(uuid):  # noqa: E501
    """returns tapi.notification.NotificationSubscriptionService

    none # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str

    :rtype: TapiNotificationNotificationSubscriptionServiceWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_name_post(uuid, body=None):  # noqa: E501
    """creates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str
    :param body: tapi.common.NameAndValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonNameAndValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_namevalue_name_delete(uuid, value_name):  # noqa: E501
    """removes tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_namevalue_name_get(uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_namevalue_name_put(uuid, value_name, body=None):  # noqa: E501
    """creates or updates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of notif-subscription
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


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notification_channel_get(uuid):  # noqa: E501
    """returns tapi.notification.NotificationChannel

    none # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str

    :rtype: TapiNotificationNotificationChannelWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notification_channel_namevalue_name_get(uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_additional_infovalue_name_get(uuid, notification_uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    none # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str
    :param notification_uuid: Id of notification
    :type notification_uuid: str
    :param value_name: Id of additional-info
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_alarm_info_get(uuid, notification_uuid):  # noqa: E501
    """returns tapi.notification.AlarmInfo

    none # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str
    :param notification_uuid: Id of notification
    :type notification_uuid: str

    :rtype: TapiNotificationAlarmInfoWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_changed_attributesvalue_name_get(uuid, notification_uuid, value_name):  # noqa: E501
    """returns tapi.notification.NameAndValueChange

    none # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str
    :param notification_uuid: Id of notification
    :type notification_uuid: str
    :param value_name: Id of changed-attributes
    :type value_name: str

    :rtype: TapiNotificationNameAndValueChangeWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_get(uuid, notification_uuid):  # noqa: E501
    """returns tapi.notification.Notification

    none # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str
    :param notification_uuid: Id of notification
    :type notification_uuid: str

    :rtype: TapiNotificationNotificationWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_namevalue_name_get(uuid, notification_uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str
    :param notification_uuid: Id of notification
    :type notification_uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_target_object_namevalue_name_get(uuid, notification_uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    none # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str
    :param notification_uuid: Id of notification
    :type notification_uuid: str
    :param value_name: Id of target-object-name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_tca_info_get(uuid, notification_uuid):  # noqa: E501
    """returns tapi.notification.TcaInfo

    none # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str
    :param notification_uuid: Id of notification
    :type notification_uuid: str

    :rtype: TapiNotificationTcaInfoWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.notification.NotificationSubscriptionService

    none # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str
    :param body: tapi.notification.NotificationSubscriptionService to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiNotificationNotificationSubscriptionServiceWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_delete(uuid):  # noqa: E501
    """removes tapi.notification.SubscriptionFilter

    none # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_get(uuid):  # noqa: E501
    """returns tapi.notification.SubscriptionFilter

    none # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str

    :rtype: TapiNotificationSubscriptionFilterWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_name_post(uuid, body=None):  # noqa: E501
    """creates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str
    :param body: tapi.common.NameAndValue to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiCommonNameAndValueWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_namevalue_name_delete(uuid, value_name):  # noqa: E501
    """removes tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: None
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_namevalue_name_get(uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_namevalue_name_put(uuid, value_name, body=None):  # noqa: E501
    """creates or updates tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of notif-subscription
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


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_post(uuid, body=None):  # noqa: E501
    """creates tapi.notification.SubscriptionFilter

    none # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str
    :param body: tapi.notification.SubscriptionFilter to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiNotificationSubscriptionFilterWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_put(uuid, body=None):  # noqa: E501
    """creates or updates tapi.notification.SubscriptionFilter

    none # noqa: E501

    :param uuid: Id of notif-subscription
    :type uuid: str
    :param body: tapi.notification.SubscriptionFilter to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiNotificationSubscriptionFilterWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_additional_infovalue_name_get(uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    none # noqa: E501

    :param uuid: Id of notification
    :type uuid: str
    :param value_name: Id of additional-info
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_alarm_info_get(uuid):  # noqa: E501
    """returns tapi.notification.AlarmInfo

    none # noqa: E501

    :param uuid: Id of notification
    :type uuid: str

    :rtype: TapiNotificationAlarmInfoWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_changed_attributesvalue_name_get(uuid, value_name):  # noqa: E501
    """returns tapi.notification.NameAndValueChange

    none # noqa: E501

    :param uuid: Id of notification
    :type uuid: str
    :param value_name: Id of changed-attributes
    :type value_name: str

    :rtype: TapiNotificationNameAndValueChangeWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_get(uuid):  # noqa: E501
    """returns tapi.notification.Notification

    none # noqa: E501

    :param uuid: Id of notification
    :type uuid: str

    :rtype: TapiNotificationNotificationWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_namevalue_name_get(uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    List of names. A property of an entity with a value that is unique in some namespace but may change during the life of the entity. A name carries no semantics with respect to the purpose of the entity. # noqa: E501

    :param uuid: Id of notification
    :type uuid: str
    :param value_name: Id of name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_target_object_namevalue_name_get(uuid, value_name):  # noqa: E501
    """returns tapi.common.NameAndValue

    none # noqa: E501

    :param uuid: Id of notification
    :type uuid: str
    :param value_name: Id of target-object-name
    :type value_name: str

    :rtype: TapiCommonNameAndValueWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_tca_info_get(uuid):  # noqa: E501
    """returns tapi.notification.TcaInfo

    none # noqa: E501

    :param uuid: Id of notification
    :type uuid: str

    :rtype: TapiNotificationTcaInfoWrapper
    """
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_post(body=None):  # noqa: E501
    """creates tapi.notification.NotificationContext

    Augments the base TAPI Context with NotificationService information # noqa: E501

    :param body: tapi.notification.NotificationContext to be added to list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiNotificationNotificationContextWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def data_tapi_commoncontext_tapi_notificationnotification_context_put(body=None):  # noqa: E501
    """creates or updates tapi.notification.NotificationContext

    Augments the base TAPI Context with NotificationService information # noqa: E501

    :param body: tapi.notification.NotificationContext to be added or updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TapiNotificationNotificationContextWrapper.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def operations_tapi_notificationcreate_notification_subscription_service_post(body=None):  # noqa: E501
    """operates on tapi.notification.CreateNotificationSubscriptionService

    operates on tapi.notification.CreateNotificationSubscriptionService # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TapiNotificationCreateNotificationSubscriptionService
    """
    if connexion.request.is_json:
        body = OperationsTapinotificationcreatenotificationsubscriptionserviceBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def operations_tapi_notificationdelete_notification_subscription_service_post(body=None):  # noqa: E501
    """operates on tapi.notification.DeleteNotificationSubscriptionService

    operates on tapi.notification.DeleteNotificationSubscriptionService # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TapiNotificationDeleteNotificationSubscriptionService
    """
    if connexion.request.is_json:
        body = OperationsTapinotificationdeletenotificationsubscriptionserviceBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def operations_tapi_notificationget_notification_list_post(body=None):  # noqa: E501
    """operates on tapi.notification.GetNotificationList

    operates on tapi.notification.GetNotificationList # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TapiNotificationGetNotificationList
    """
    if connexion.request.is_json:
        body = OperationsTapinotificationgetnotificationlistBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def operations_tapi_notificationget_notification_subscription_service_details_post(body=None):  # noqa: E501
    """operates on tapi.notification.GetNotificationSubscriptionServiceDetails

    operates on tapi.notification.GetNotificationSubscriptionServiceDetails # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TapiNotificationGetNotificationSubscriptionServiceDetails
    """
    if connexion.request.is_json:
        body = OperationsTapinotificationgetnotificationsubscriptionservicedetailsBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def operations_tapi_notificationget_notification_subscription_service_list_post():  # noqa: E501
    """operations_tapi_notificationget_notification_subscription_service_list_post

     # noqa: E501


    :rtype: TapiNotificationGetNotificationSubscriptionServiceList
    """
    return 'do some magic!'


def operations_tapi_notificationget_supported_notification_types_post():  # noqa: E501
    """operations_tapi_notificationget_supported_notification_types_post

     # noqa: E501


    :rtype: TapiNotificationGetSupportedNotificationTypes
    """
    return 'do some magic!'


def operations_tapi_notificationupdate_notification_subscription_service_post(body=None):  # noqa: E501
    """operates on tapi.notification.UpdateNotificationSubscriptionService

    operates on tapi.notification.UpdateNotificationSubscriptionService # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TapiNotificationUpdateNotificationSubscriptionService
    """
    if connexion.request.is_json:
        body = OperationsTapinotificationupdatenotificationsubscriptionserviceBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
