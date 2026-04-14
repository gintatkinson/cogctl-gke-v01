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

# import pytest
from flask_unittest import ClientTestCase
from unittest import mock
from flask.testing import FlaskClient
from flask.app import Flask
from flask.helpers import url_for
from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import ContextIdList, Empty, DeviceId, DeviceList, TopologyIdList
# from device.client.DeviceClient import DeviceClient
from webui.service import create_app

class TestWebUI(ClientTestCase):
    app = create_app(use_config={
        'TESTING': True,
        'SERVER_NAME': 'localhost.localdomain',
        'SECRET_KEY': '>s&}24@{]]#k3&^5$f3#?6?h3{W@[}/7z}2pa]>{3&5%RP<)[(',
        'WTF_CSRF_ENABLED': False,
    })

    def setUp(self, client: FlaskClient) -> None:

        self.mocker_delete_device = mock.patch('webui.service.device.routes.device_client.DeleteDevice')
        self.mocker_delete_device.return_value = Empty()
        self.mocker_delete_device.start()
        self.addCleanup(self.mocker_delete_device.stop)

        self.mocker_list_context_ids = mock.patch('webui.service.device.routes.context_client.ListContextIds')
        self.mocker_list_context_ids.return_value = ContextIdList()  # returns an empty list
        self.mocker_list_context_ids.start()
        self.addCleanup(self.mocker_list_context_ids.stop)

        self.mocker_list_devices = mock.patch('webui.service.device.routes.context_client.ListDevices')
        self.mocker_list_devices.return_value = DeviceList()  # returns an empty list
        self.mocker_list_devices.start()
        self.addCleanup(self.mocker_list_devices.stop)

        self.mocker_add_device = mock.patch('webui.service.device.routes.device_client.AddDevice')
        self.mocker_add_device.return_value = DeviceId()
        self.mocker_add_device.start()
        self.addCleanup(self.mocker_add_device.stop)

        self.mocker_list_topology_ids = mock.patch('webui.service.device.routes.context_client.ListTopologyIds')
        self.mocker_list_topology_ids.return_value = TopologyIdList()
        self.mocker_list_topology_ids.start()
        self.addCleanup(self.mocker_list_topology_ids.stop)

        return super().setUp(client)

    def tearDown(self, client: FlaskClient) -> None:
        mock.patch.stopall()
        return super().tearDown(client)

    def test_routes(self, _) -> None:
        with self.app.app_context():
            url_for('main.home')
            url_for('service.home')
            url_for('slice.home')
            url_for('device.home')
            url_for('link.home')
            #url_for('main.debug')
            url_for('main.about')
            url_for('js.topology_js')
            url_for('js.site_js')

    def test_device_add_action_success(self, client) -> None:
        with client.session_transaction() as sess:
            sess['context_uuid'] = 'admin'
        DEVICE_EMU = {
            'device_id': 'EMULATED',
            'device_type': DeviceTypeEnum.EMULATED_PACKET_ROUTER.value,
            'device_config': '',
            'operational_status': 1,
            'device_drivers': 0,
            'device_endpoints': [],
        }
        rv = client.post('/device/add', data=DEVICE_EMU, follow_redirects=True)
        self.assertInResponse(b'success', rv)

    def test_device_delete_action(self, client):
        with client.session_transaction() as sess:
            sess['context_uuid'] = 'admin'

        rv = client.get('/device/EMULATED/delete', follow_redirects=True)
        # mocked_list.assert_called()
        # mocked_delete.assert_called()
        self.assertInResponse(b'success', rv)

    # def test_service_up(self, client):
    #     rw = client.get('/')
    #     assert rw.status_code == 200, 'Service is not up!'

# def test_home_page(client):
#     rw = client.get('/')
#     assert rw.status_code == 200, 'Error in the home page!'
#     assert b'Select the working context' in rw.data

# def test_service_home_page(client):
#     with client.session_transaction() as sess:
#         sess['context_uuid'] = 'admin'
#     rw = client.get('/service/')
#     assert rw.status_code == 200
#     assert b'Services' in rw.data
#     assert b'Add New Service' in rw.data

# def test_device_home_page(client):
#     with client.session_transaction() as sess:
#         sess['context_uuid'] = 'admin'
#     rw = client.get('/device/')
#     assert rw.status_code == 200
#     assert b'Devices' in rw.data
#     assert b'Add New Device' in rw.data

# @pytest.mark.parametrize('device_id', (
#     'DEV1',
#     'DEV2',
#     'DEV3',
# ))
# def test_device_detail_page(client, device_id):
#     with client.session_transaction() as sess:
#         sess['context_uuid'] = 'admin'
#     rw = client.get(f'/device/detail/{device_id}')
#     assert rw.status_code == 200
#     assert b'Device' in rw.data
#     assert device_id in rw.data.decode()
#     assert b'Endpoints' in rw.data, 'Missing endpoint information on the device detail page.'
#     # assert b'Add New Device' in rw.data

# def test_device_add_page(client):
#     with client.session_transaction() as sess:
#         sess['context_uuid'] = 'admin'
#     rw = client.get('/device/add')
#     assert rw.status_code == 200
#     assert b'Add New Device' in rw.data
#     assert b'Operational Status' in rw.data, 'Form is not correctly implemented.'
#     assert b'Type' in rw.data, 'Form is not correctly implemented.'
#     assert b'Configurations' in rw.data, 'Form is not correctly implemented.'
#     assert b'Drivers' in rw.data, 'Form is not correctly implemented.'

# def test_device_add_action(client):
#     with client.session_transaction() as sess:
#         sess['context_uuid'] = 'admin'
#     DEVICE_EMU = {
#         'device_id': 'EMULATED',
#         'device_type': DeviceTypeEnum.EMULATED_PACKET_ROUTER.value,
#         'device_config': '',
#         'operational_status': 1,
#         'device_drivers': 0,
#         'device_endpoints': [],
#     }
#     with mock.patch('webui.service.device.routes.device_client.AddDevice') as mocked_add:
#         mocked_add.return_value = DeviceId()
#         rw = client.post('/device/add', data=DEVICE_EMU, follow_redirects=True)
#     assert b'success' in rw.data

# def test_device_delete_action(client):
#     with client.session_transaction() as sess:
#         sess['context_uuid'] = 'admin'
#     with mock.patch('webui.service.device.routes.device_client.DeleteDevice') as mocked_delete,\
#          mock.patch('webui.service.device.routes.context_client.ListDevices') as mocked_list:
#         mocked_list.return_value = DeviceList()  # returns an empty list
#         rw = client.get('/device/EMULATED/delete', follow_redirects=True)
#         mocked_list.assert_called()
#         mocked_delete.assert_called()
#     assert b'success' in rw.data
