# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

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
from tapi_server.test import BaseTestCase


class TestTapiNotificationController(BaseTestCase):
    """TapiNotificationController integration test stubs"""

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_delete(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_delete

        removes tapi.notification.NotificationContext
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/',
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_get

        returns tapi.notification.NotificationContext
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscription_post(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscription_post

        creates tapi.notification.NotificationSubscriptionService
        """
        body = TapiNotificationNotificationSubscriptionServiceWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_delete(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_delete

        removes tapi.notification.NotificationSubscriptionService
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_get

        returns tapi.notification.NotificationSubscriptionService
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_name_post(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_name_post

        creates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/name/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_namevalue_name_delete(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_namevalue_name_delete

        removes tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_namevalue_name_put(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_namevalue_name_put

        creates or updates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notification_channel_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notification_channel_get

        returns tapi.notification.NotificationChannel
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/notification-channel/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notification_channel_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notification_channel_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/notification-channel/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_additional_infovalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_additional_infovalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/notification={notification-uuid}/additional-info={value-name}/'.format(uuid='uuid_example', notification_uuid='notification_uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_alarm_info_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_alarm_info_get

        returns tapi.notification.AlarmInfo
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/notification={notification-uuid}/alarm-info/'.format(uuid='uuid_example', notification_uuid='notification_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_changed_attributesvalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_changed_attributesvalue_name_get

        returns tapi.notification.NameAndValueChange
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/notification={notification-uuid}/changed-attributes={value-name}/'.format(uuid='uuid_example', notification_uuid='notification_uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_get

        returns tapi.notification.Notification
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/notification={notification-uuid}/'.format(uuid='uuid_example', notification_uuid='notification_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/notification={notification-uuid}/name={value-name}/'.format(uuid='uuid_example', notification_uuid='notification_uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_target_object_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_target_object_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/notification={notification-uuid}/target-object-name={value-name}/'.format(uuid='uuid_example', notification_uuid='notification_uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_tca_info_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_notificationnotification_uuid_tca_info_get

        returns tapi.notification.TcaInfo
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/notification={notification-uuid}/tca-info/'.format(uuid='uuid_example', notification_uuid='notification_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_put(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_put

        creates or updates tapi.notification.NotificationSubscriptionService
        """
        body = TapiNotificationNotificationSubscriptionServiceWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_delete(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_delete

        removes tapi.notification.SubscriptionFilter
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/subscription-filter/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_get

        returns tapi.notification.SubscriptionFilter
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/subscription-filter/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_name_post(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_name_post

        creates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/subscription-filter/name/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_namevalue_name_delete(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_namevalue_name_delete

        removes tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/subscription-filter/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/subscription-filter/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_namevalue_name_put(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_namevalue_name_put

        creates or updates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/subscription-filter/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_post(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_post

        creates tapi.notification.SubscriptionFilter
        """
        body = TapiNotificationSubscriptionFilterWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/subscription-filter/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_put(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notif_subscriptionuuid_subscription_filter_put

        creates or updates tapi.notification.SubscriptionFilter
        """
        body = TapiNotificationSubscriptionFilterWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notif-subscription={uuid}/subscription-filter/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_additional_infovalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_additional_infovalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notification={uuid}/additional-info={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_alarm_info_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_alarm_info_get

        returns tapi.notification.AlarmInfo
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notification={uuid}/alarm-info/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_changed_attributesvalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_changed_attributesvalue_name_get

        returns tapi.notification.NameAndValueChange
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notification={uuid}/changed-attributes={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_get

        returns tapi.notification.Notification
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notification={uuid}/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notification={uuid}/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_target_object_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_target_object_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notification={uuid}/target-object-name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_tca_info_get(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_notificationuuid_tca_info_get

        returns tapi.notification.TcaInfo
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/notification={uuid}/tca-info/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_post(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_post

        creates tapi.notification.NotificationContext
        """
        body = TapiNotificationNotificationContextWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_notificationnotification_context_put(self):
        """Test case for data_tapi_commoncontext_tapi_notificationnotification_context_put

        creates or updates tapi.notification.NotificationContext
        """
        body = TapiNotificationNotificationContextWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-notification:notification-context/',
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_notificationcreate_notification_subscription_service_post(self):
        """Test case for operations_tapi_notificationcreate_notification_subscription_service_post

        operates on tapi.notification.CreateNotificationSubscriptionService
        """
        body = OperationsTapinotificationcreatenotificationsubscriptionserviceBody()
        response = self.client.open(
            '/operations/tapi-notification:create-notification-subscription-service/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_notificationdelete_notification_subscription_service_post(self):
        """Test case for operations_tapi_notificationdelete_notification_subscription_service_post

        operates on tapi.notification.DeleteNotificationSubscriptionService
        """
        body = OperationsTapinotificationdeletenotificationsubscriptionserviceBody()
        response = self.client.open(
            '/operations/tapi-notification:delete-notification-subscription-service/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_notificationget_notification_list_post(self):
        """Test case for operations_tapi_notificationget_notification_list_post

        operates on tapi.notification.GetNotificationList
        """
        body = OperationsTapinotificationgetnotificationlistBody()
        response = self.client.open(
            '/operations/tapi-notification:get-notification-list/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_notificationget_notification_subscription_service_details_post(self):
        """Test case for operations_tapi_notificationget_notification_subscription_service_details_post

        operates on tapi.notification.GetNotificationSubscriptionServiceDetails
        """
        body = OperationsTapinotificationgetnotificationsubscriptionservicedetailsBody()
        response = self.client.open(
            '/operations/tapi-notification:get-notification-subscription-service-details/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_notificationget_notification_subscription_service_list_post(self):
        """Test case for operations_tapi_notificationget_notification_subscription_service_list_post

        
        """
        response = self.client.open(
            '/operations/tapi-notification:get-notification-subscription-service-list/',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_notificationget_supported_notification_types_post(self):
        """Test case for operations_tapi_notificationget_supported_notification_types_post

        
        """
        response = self.client.open(
            '/operations/tapi-notification:get-supported-notification-types/',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_notificationupdate_notification_subscription_service_post(self):
        """Test case for operations_tapi_notificationupdate_notification_subscription_service_post

        operates on tapi.notification.UpdateNotificationSubscriptionService
        """
        body = OperationsTapinotificationupdatenotificationsubscriptionserviceBody()
        response = self.client.open(
            '/operations/tapi-notification:update-notification-subscription-service/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
