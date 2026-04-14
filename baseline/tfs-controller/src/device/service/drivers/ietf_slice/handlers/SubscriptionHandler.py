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

import logging, requests
from typing_extensions import TypedDict
from common.tools.rest_conf.client.RestConfClient import RestConfClient


LOGGER = logging.getLogger(__name__)


Periodic = TypedDict('Periodic', {'ietf-yang-push:period': str})

Input = TypedDict(
    'Input',
    {
        'datastore': str,
        'ietf-yang-push:datastore-xpath-filter': str,
        'ietf-yang-push:periodic': Periodic,
    },
)

SubscribedNotificationsSchema = TypedDict(
    'SubscribedNotificationsSchema', {'ietf-subscribed-notifications:input': Input}
)

SubscriptionSchema = TypedDict('SubscriptionSchema', {'id': str})

UnsubscribedNotificationsSchema = TypedDict(
    'UnsubscribedNotificationsSchema', {'ietf-subscribed-notifications:input': SubscriptionSchema}
)


class SubscriptionId(TypedDict):
    identifier: str
    uri: str


class SubscriptionHandler:
    def __init__(self, rest_conf_client : RestConfClient) -> None:
        self._rest_conf_client = rest_conf_client

    def subscribe(
        self, subscription_data : SubscribedNotificationsSchema
    ) -> SubscriptionId:
        MSG = '[subscribe] subscription_data={:s}'
        LOGGER.debug(MSG.format(str(subscription_data)))
        try:
            url = '/subscriptions:establish-subscription'
            LOGGER.debug('Subscribing to telemetry: {:s}'.format(str(subscription_data)))
            reply = self._rest_conf_client.rpc(url, body=subscription_data)
            LOGGER.debug('Subscription reply: {:s}'.format(str(reply)))
            return reply
        except requests.exceptions.ConnectionError as e:
            MSG = 'Failed to send RPC request'
            raise Exception(MSG) from e

    def unsubscribe(
        self, unsubscription_data : UnsubscribedNotificationsSchema
    ) -> SubscriptionId:
        MSG = '[unsubscribe] unsubscription_data={:s}'
        LOGGER.debug(MSG.format(str(unsubscription_data)))
        try:
            url = '/subscriptions:delete-subscription'
            LOGGER.debug('Unsubscribing from telemetry: {:s}'.format(str(unsubscription_data)))
            reply = self._rest_conf_client.rpc(url, body=unsubscription_data)
            LOGGER.debug('Unsubscription reply: {:s}'.format(str(reply)))
            return reply
        except requests.exceptions.ConnectionError as e:
            MSG = 'Failed to send RPC request'
            raise Exception(MSG) from e
