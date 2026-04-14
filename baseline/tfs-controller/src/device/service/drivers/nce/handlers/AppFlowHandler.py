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
from typing import Dict
from common.tools.rest_conf.client.RestConfClient import RestConfClient


LOGGER = logging.getLogger(__name__)


class AppFlowHandler:
    def __init__(self, rest_conf_client : RestConfClient) -> None:
        self._rest_conf_client = rest_conf_client

        self._url_qos_profile = '/huawei-nce-app-flow:qos-profiles'
        self._url_qos_profile_item = self._url_qos_profile + '/qos-profile={:s}'

        self._url_application = '/huawei-nce-app-flow:applications'
        self._url_application_item = self._url_application + '/application={:s}'

        self._url_app_flow = '/huawei-nce-app-flow:app-flows'
        self._url_app_flow_item = self._url_app_flow + '/app-flow={:s}'


    def create(self, data : Dict) -> None:
        MSG = '[create] data={:s}'
        LOGGER.debug(MSG.format(str(data)))

        try:
            qos_profiles = (
                data
                .get('huawei-nce-app-flow:app-flows', dict())
                .get('qos-profiles', dict())
                .get('qos-profile', list())
            )
            for qos_profile in qos_profiles:
                request = {'huawei-nce-app-flow:qos-profiles': {'qos-profile': [qos_profile]}}
                qos_profile_name = qos_profile['name']
                LOGGER.info('Creating QoS Profile: {:s}'.format(str(request)))
                url = self._url_qos_profile_item.format(qos_profile_name)
                self._rest_conf_client.put(url, body=request)

            applications = (
                data
                .get('huawei-nce-app-flow:app-flows', dict())
                .get('applications', dict())
                .get('application', list())
            )
            for application in applications:
                request = {'huawei-nce-app-flow:applications': {'application': [application]}}
                application_name = application['name']
                LOGGER.info('Creating Application: {:s}'.format(str(request)))
                url = self._url_application_item.format(application_name)
                self._rest_conf_client.put(url, body=request)

            app_flows = (
                data
                .get('huawei-nce-app-flow:app-flows', dict())
                .get('app-flow', list())
            )
            for app_flow in app_flows:
                request = {'huawei-nce-app-flow:app-flows': {'app-flow': [app_flow]}}
                app_flow_name = app_flow['name']
                LOGGER.info('Creating App Flow: {:s}'.format(str(request)))
                url = self._url_app_flow_item.format(app_flow_name)
                self._rest_conf_client.put(url, body=request)

        except requests.exceptions.ConnectionError as e:
            MSG = 'Failed to send PUT requests to NCE FAN NBI'
            raise Exception(MSG) from e


    def retrieve(self) -> Dict:
        try:
            LOGGER.info('Retrieving QoS Profiles')
            qos_profiles = self._rest_conf_client.get(self._url_qos_profile)

            LOGGER.info('Retrieving Applications')
            applications = self._rest_conf_client.get(self._url_application)

            LOGGER.info('Retrieving App Flows')
            app_flows = self._rest_conf_client.get(self._url_app_flow)
        except requests.exceptions.ConnectionError as e:
            MSG = 'Failed to send GET requests to NCE FAN NBI'
            raise Exception(MSG) from e

        qos_profiles = (
            qos_profiles
            .get('huawei-nce-app-flow:qos-profiles', dict())
            .get('qos-profile', list())
        )

        applications = (
            applications
            .get('huawei-nce-app-flow:applications', dict())
            .get('application', list())
        )

        app_flows = (
            app_flows
            .get('huawei-nce-app-flow:app-flows', dict())
            .get('app-flow', list())
        )

        return {'huawei-nce-app-flow:app-flows': {
            'qos-profiles': {'qos-profile': qos_profiles},
            'applications': {'application': applications},
            'app-flow': app_flows,
        }}


    def delete(self, data : Dict) -> None:
        MSG = '[delete] data={:s}'
        LOGGER.debug(MSG.format(str(data)))

        try:
            app_flows = (
                data
                .get('huawei-nce-app-flow:app-flows', dict())
                .get('app-flow', list())
            )
            for app_flow in app_flows:
                app_flow_name = app_flow['name']
                LOGGER.info('Deleting App Flow: {:s}'.format(str(app_flow_name)))
                app_flow_url = self._url_app_flow_item.format(app_flow_name)
                self._rest_conf_client.delete(app_flow_url)

            applications = (
                data
                .get('huawei-nce-app-flow:app-flows', dict())
                .get('applications', dict())
                .get('application', list())
            )
            for application in applications:
                application_name = application['name']
                LOGGER.info('Deleting Application: {:s}'.format(str(application_name)))
                application_url = self._url_application_item.format(application_name)
                self._rest_conf_client.delete(application_url)

            qos_profiles = (
                data
                .get('huawei-nce-app-flow:app-flows', dict())
                .get('qos-profiles', dict())
                .get('qos-profile', list())
            )
            for qos_profile in qos_profiles:
                qos_profile_name = qos_profile['name']
                LOGGER.info('Deleting QoS Profile: {:s}'.format(str(qos_profile_name)))
                qos_profile_url = self._url_qos_profile_item.format(qos_profile_name)
                self._rest_conf_client.delete(qos_profile_url)

        except requests.exceptions.ConnectionError as e:
            MSG = 'Failed to send POST requests to NCE FAN NBI'
            raise Exception(MSG) from e
