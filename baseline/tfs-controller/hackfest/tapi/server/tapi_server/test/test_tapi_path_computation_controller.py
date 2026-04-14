# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

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
from tapi_server.test import BaseTestCase


class TestTapiPathComputationController(BaseTestCase):
    """TapiPathComputationController integration test stubs"""

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_delete

        removes tapi.path.computation.PathComputationContext
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/',
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_get

        returns tapi.path.computation.PathComputationContext
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_service_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_service_post

        creates tapi.path.computation.PathComputationService
        """
        body = TapiPathComputationPathComputationServiceWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_delete

        removes tapi.path.computation.PathComputationService
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_point_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_point_post

        creates tapi.path.computation.PathServiceEndPoint
        """
        body = TapiPathComputationPathServiceEndPointWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_delete

        removes tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_post

        creates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_burst_size_put

        creates or updates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_delete

        removes tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_post

        creates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_committed_information_rate_put

        creates or updates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_delete

        removes tapi.common.BandwidthProfile
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_get

        returns tapi.common.BandwidthProfile
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_delete

        removes tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_post

        creates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_burst_size_put

        creates or updates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_delete

        removes tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_post

        creates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_peak_information_rate_put

        creates or updates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_post

        creates tapi.common.BandwidthProfile
        """
        body = TapiCommonBandwidthProfileWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_bandwidth_profile_put

        creates or updates tapi.common.BandwidthProfile
        """
        body = TapiCommonBandwidthProfileWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/bandwidth-profile/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_delete

        removes tapi.common.Capacity
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_get

        returns tapi.common.Capacity
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_post

        creates tapi.common.Capacity
        """
        body = TapiCommonCapacityWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_put

        creates or updates tapi.common.Capacity
        """
        body = TapiCommonCapacityWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_total_size_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_total_size_delete

        removes tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/total-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_total_size_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_total_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/total-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_total_size_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_total_size_post

        creates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/total-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_total_size_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_capacity_total_size_put

        creates or updates tapi.common.CapacityValue
        """
        body = TapiCommonCapacityValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/capacity/total-size/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_delete

        removes tapi.path.computation.PathServiceEndPoint
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_get

        returns tapi.path.computation.PathServiceEndPoint
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_name_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_name_post

        creates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/name/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_namevalue_name_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_namevalue_name_delete

        removes tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/name={value-name}/'.format(uuid='uuid_example', local_id='local_id_example', value_name='value_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/name={value-name}/'.format(uuid='uuid_example', local_id='local_id_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_namevalue_name_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_namevalue_name_put

        creates or updates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/name={value-name}/'.format(uuid='uuid_example', local_id='local_id_example', value_name='value_name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_put

        creates or updates tapi.path.computation.PathServiceEndPoint
        """
        body = TapiPathComputationPathServiceEndPointWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_service_interface_point_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_service_interface_point_delete

        removes tapi.common.ServiceInterfacePointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/service-interface-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_service_interface_point_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_service_interface_point_get

        returns tapi.common.ServiceInterfacePointRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/service-interface-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_service_interface_point_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_service_interface_point_post

        creates tapi.common.ServiceInterfacePointRef
        """
        body = TapiCommonServiceInterfacePointRefWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/service-interface-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_service_interface_point_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_end_pointlocal_id_service_interface_point_put

        creates or updates tapi.common.ServiceInterfacePointRef
        """
        body = TapiCommonServiceInterfacePointRefWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/end-point={local-id}/service-interface-point/'.format(uuid='uuid_example', local_id='local_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_get

        returns tapi.path.computation.PathComputationService
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_name_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_name_post

        creates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/name/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_namevalue_name_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_namevalue_name_delete

        removes tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_namevalue_name_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_namevalue_name_put

        creates or updates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_delete

        removes tapi.path.computation.PathObjectiveFunction
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/objective-function/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_get

        returns tapi.path.computation.PathObjectiveFunction
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/objective-function/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_name_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_name_post

        creates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/objective-function/name/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_namevalue_name_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_namevalue_name_delete

        removes tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/objective-function/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/objective-function/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_namevalue_name_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_namevalue_name_put

        creates or updates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/objective-function/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_post

        creates tapi.path.computation.PathObjectiveFunction
        """
        body = TapiPathComputationPathObjectiveFunctionWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/objective-function/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_objective_function_put

        creates or updates tapi.path.computation.PathObjectiveFunction
        """
        body = TapiPathComputationPathObjectiveFunctionWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/objective-function/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_delete

        removes tapi.path.computation.PathOptimizationConstraint
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/optimization-constraint/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_get

        returns tapi.path.computation.PathOptimizationConstraint
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/optimization-constraint/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_name_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_name_post

        creates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/optimization-constraint/name/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_namevalue_name_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_namevalue_name_delete

        removes tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/optimization-constraint/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/optimization-constraint/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_namevalue_name_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_namevalue_name_put

        creates or updates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/optimization-constraint/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_post

        creates tapi.path.computation.PathOptimizationConstraint
        """
        body = TapiPathComputationPathOptimizationConstraintWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/optimization-constraint/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_optimization_constraint_put

        creates or updates tapi.path.computation.PathOptimizationConstraint
        """
        body = TapiPathComputationPathOptimizationConstraintWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/optimization-constraint/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_pathpath_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_pathpath_uuid_get

        returns tapi.path.computation.PathRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/path={path-uuid}/'.format(uuid='uuid_example', path_uuid='path_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_put

        creates or updates tapi.path.computation.PathComputationService
        """
        body = TapiPathComputationPathComputationServiceWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_cost_characteristic_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_cost_characteristic_post

        creates tapi.topology.CostCharacteristic
        """
        body = TapiTopologyCostCharacteristicWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/cost-characteristic/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_cost_characteristiccost_name_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_cost_characteristiccost_name_delete

        removes tapi.topology.CostCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/cost-characteristic={cost-name}/'.format(uuid='uuid_example', cost_name='cost_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_cost_characteristiccost_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_cost_characteristiccost_name_get

        returns tapi.topology.CostCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/cost-characteristic={cost-name}/'.format(uuid='uuid_example', cost_name='cost_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_cost_characteristiccost_name_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_cost_characteristiccost_name_put

        creates or updates tapi.topology.CostCharacteristic
        """
        body = TapiTopologyCostCharacteristicWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/cost-characteristic={cost-name}/'.format(uuid='uuid_example', cost_name='cost_name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_delete

        removes tapi.path.computation.RoutingConstraint
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_get

        returns tapi.path.computation.RoutingConstraint
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_latency_characteristic_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_latency_characteristic_post

        creates tapi.topology.LatencyCharacteristic
        """
        body = TapiTopologyLatencyCharacteristicWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/latency-characteristic/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_latency_characteristictraffic_property_name_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_latency_characteristictraffic_property_name_delete

        removes tapi.topology.LatencyCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/latency-characteristic={traffic-property-name}/'.format(uuid='uuid_example', traffic_property_name='traffic_property_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_latency_characteristictraffic_property_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_latency_characteristictraffic_property_name_get

        returns tapi.topology.LatencyCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/latency-characteristic={traffic-property-name}/'.format(uuid='uuid_example', traffic_property_name='traffic_property_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_latency_characteristictraffic_property_name_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_latency_characteristictraffic_property_name_put

        creates or updates tapi.topology.LatencyCharacteristic
        """
        body = TapiTopologyLatencyCharacteristicWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/latency-characteristic={traffic-property-name}/'.format(uuid='uuid_example', traffic_property_name='traffic_property_name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_cost_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_cost_delete

        removes tapi.path.computation.ValueOrPriority
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/max-allowed-cost/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_cost_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_cost_get

        returns tapi.path.computation.ValueOrPriority
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/max-allowed-cost/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_cost_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_cost_post

        creates tapi.path.computation.ValueOrPriority
        """
        body = TapiPathComputationValueOrPriorityWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/max-allowed-cost/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_cost_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_cost_put

        creates or updates tapi.path.computation.ValueOrPriority
        """
        body = TapiPathComputationValueOrPriorityWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/max-allowed-cost/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_delay_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_delay_delete

        removes tapi.path.computation.ValueOrPriority
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/max-allowed-delay/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_delay_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_delay_get

        returns tapi.path.computation.ValueOrPriority
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/max-allowed-delay/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_delay_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_delay_post

        creates tapi.path.computation.ValueOrPriority
        """
        body = TapiPathComputationValueOrPriorityWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/max-allowed-delay/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_delay_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_delay_put

        creates or updates tapi.path.computation.ValueOrPriority
        """
        body = TapiPathComputationValueOrPriorityWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/max-allowed-delay/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_hops_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_hops_delete

        removes tapi.path.computation.ValueOrPriority
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/max-allowed-hops/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_hops_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_hops_get

        returns tapi.path.computation.ValueOrPriority
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/max-allowed-hops/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_hops_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_hops_post

        creates tapi.path.computation.ValueOrPriority
        """
        body = TapiPathComputationValueOrPriorityWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/max-allowed-hops/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_hops_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_max_allowed_hops_put

        creates or updates tapi.path.computation.ValueOrPriority
        """
        body = TapiPathComputationValueOrPriorityWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/max-allowed-hops/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_post

        creates tapi.path.computation.RoutingConstraint
        """
        body = TapiPathComputationRoutingConstraintWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_put

        creates or updates tapi.path.computation.RoutingConstraint
        """
        body = TapiPathComputationRoutingConstraintWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_risk_diversity_characteristic_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_risk_diversity_characteristic_post

        creates tapi.topology.RiskCharacteristic
        """
        body = TapiTopologyRiskCharacteristicWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/risk-diversity-characteristic/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_risk_diversity_characteristicrisk_characteristic_name_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_risk_diversity_characteristicrisk_characteristic_name_delete

        removes tapi.topology.RiskCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/risk-diversity-characteristic={risk-characteristic-name}/'.format(uuid='uuid_example', risk_characteristic_name='risk_characteristic_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_risk_diversity_characteristicrisk_characteristic_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_risk_diversity_characteristicrisk_characteristic_name_get

        returns tapi.topology.RiskCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/risk-diversity-characteristic={risk-characteristic-name}/'.format(uuid='uuid_example', risk_characteristic_name='risk_characteristic_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_risk_diversity_characteristicrisk_characteristic_name_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_routing_constraint_risk_diversity_characteristicrisk_characteristic_name_put

        creates or updates tapi.topology.RiskCharacteristic
        """
        body = TapiTopologyRiskCharacteristicWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/routing-constraint/risk-diversity-characteristic={risk-characteristic-name}/'.format(uuid='uuid_example', risk_characteristic_name='risk_characteristic_name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_topology_constraint_delete(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_topology_constraint_delete

        removes tapi.path.computation.TopologyConstraint
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/topology-constraint/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_topology_constraint_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_topology_constraint_get

        returns tapi.path.computation.TopologyConstraint
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/topology-constraint/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_topology_constraint_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_topology_constraint_post

        creates tapi.path.computation.TopologyConstraint
        """
        body = TapiPathComputationTopologyConstraintWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/topology-constraint/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_topology_constraint_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_path_comp_serviceuuid_topology_constraint_put

        creates or updates tapi.path.computation.TopologyConstraint
        """
        body = TapiPathComputationTopologyConstraintWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path-comp-service={uuid}/topology-constraint/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_get

        returns tapi.path.computation.Path
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path={uuid}/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_linktopology_uuidlink_uuid_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_linktopology_uuidlink_uuid_get

        returns tapi.topology.LinkRef
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path={uuid}/link={topology-uuid},{link-uuid}/'.format(uuid='uuid_example', topology_uuid='topology_uuid_example', link_uuid='link_uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path={uuid}/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_cost_characteristiccost_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_cost_characteristiccost_name_get

        returns tapi.topology.CostCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path={uuid}/routing-constraint/cost-characteristic={cost-name}/'.format(uuid='uuid_example', cost_name='cost_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_get

        returns tapi.path.computation.RoutingConstraint
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path={uuid}/routing-constraint/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_latency_characteristictraffic_property_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_latency_characteristictraffic_property_name_get

        returns tapi.topology.LatencyCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path={uuid}/routing-constraint/latency-characteristic={traffic-property-name}/'.format(uuid='uuid_example', traffic_property_name='traffic_property_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_max_allowed_cost_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_max_allowed_cost_get

        returns tapi.path.computation.ValueOrPriority
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path={uuid}/routing-constraint/max-allowed-cost/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_max_allowed_delay_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_max_allowed_delay_get

        returns tapi.path.computation.ValueOrPriority
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path={uuid}/routing-constraint/max-allowed-delay/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_max_allowed_hops_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_max_allowed_hops_get

        returns tapi.path.computation.ValueOrPriority
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path={uuid}/routing-constraint/max-allowed-hops/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_risk_diversity_characteristicrisk_characteristic_name_get(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_pathuuid_routing_constraint_risk_diversity_characteristicrisk_characteristic_name_get

        returns tapi.topology.RiskCharacteristic
        """
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/path={uuid}/routing-constraint/risk-diversity-characteristic={risk-characteristic-name}/'.format(uuid='uuid_example', risk_characteristic_name='risk_characteristic_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_post(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_post

        creates tapi.path.computation.PathComputationContext
        """
        body = TapiPathComputationPathComputationContextWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_tapi_path_computationpath_computation_context_put(self):
        """Test case for data_tapi_commoncontext_tapi_path_computationpath_computation_context_put

        creates or updates tapi.path.computation.PathComputationContext
        """
        body = TapiPathComputationPathComputationContextWrapper()
        response = self.client.open(
            '/data/tapi-common:context/tapi-path-computation:path-computation-context/',
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_path_computationcompute_p2_p_path_post(self):
        """Test case for operations_tapi_path_computationcompute_p2_p_path_post

        operates on tapi.path.computation.ComputeP2PPath
        """
        body = OperationsTapipathcomputationcomputep2ppathBody()
        response = self.client.open(
            '/operations/tapi-path-computation:compute-p-2-p-path/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_path_computationdelete_p2_p_path_post(self):
        """Test case for operations_tapi_path_computationdelete_p2_p_path_post

        operates on tapi.path.computation.DeleteP2PPath
        """
        body = OperationsTapipathcomputationdeletep2ppathBody()
        response = self.client.open(
            '/operations/tapi-path-computation:delete-p-2-p-path/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_path_computationoptimize_p2_ppath_post(self):
        """Test case for operations_tapi_path_computationoptimize_p2_ppath_post

        operates on tapi.path.computation.OptimizeP2Ppath
        """
        body = OperationsTapipathcomputationoptimizep2ppathBody()
        response = self.client.open(
            '/operations/tapi-path-computation:optimize-p-2-ppath/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
