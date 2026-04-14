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

from __future__ import print_function

import grpc
import logging
import time

from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.proto.acl_pb2 import AclForwardActionEnum, AclLogActionEnum, AclRuleTypeEnum
from common.proto.context_pb2 import ConfigActionEnum, Empty, Service, ServiceId
from common.proto.l3_attackmitigator_pb2 import ACLRules, L3AttackmitigatorOutput
from common.proto.l3_attackmitigator_pb2_grpc import L3AttackmitigatorServicer
from common.proto.l3_centralizedattackdetector_pb2 import StatusMessage
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from service.client.ServiceClient import ServiceClient


LOGGER = logging.getLogger(__name__)
METRICS_POOL = MetricsPool("l3_attackmitigator", "RPC")


class l3_attackmitigatorServiceServicerImpl(L3AttackmitigatorServicer):
    def __init__(self):
        """
        Initializes the Attack Mitigator service.

        Args:
            None.

        Returns:
            None.
        """

        LOGGER.info("Creating Attack Mitigator service")

        self.last_value = -1
        self.last_tag = 0
        self.sequence_id = 0

        self.context_client = ContextClient()
        self.service_client = ServiceClient()
        self.configured_acl_config_rules = []

    def configure_acl_rule(
        self,
        context_uuid: str,
        service_uuid: str,
        device_uuid: str,
        endpoint_uuid: str,
        src_ip: str,
        dst_ip: str,
        src_port: str,
        dst_port: str,
    ) -> None:
        """
        Configures an ACL rule to block undesired TCP traffic.

        Args:
            context_uuid (str): The UUID of the context.
            service_uuid (str): The UUID of the service.
            device_uuid (str): The UUID of the device.
            endpoint_uuid (str): The UUID of the endpoint.
            src_ip (str): The source IP address.
            dst_ip (str): The destination IP address.
            src_port (str): The source port.
            dst_port (str): The destination port.

        Returns:
            None.
        """

        # Create ServiceId
        service_id = ServiceId()
        service_id.context_id.context_uuid.uuid = context_uuid
        service_id.service_uuid.uuid = service_uuid

        try:
            _service: Service = self.context_client.GetService(service_id)
        except:
            raise Exception("Service({:s}) not found".format(grpc_message_to_json_string(service_id)))

        # _service is read-only; copy it to have an updatable service message
        service_request = Service()
        service_request.CopyFrom(_service)

        # Add ACL ConfigRule into the service service_request
        acl_config_rule = service_request.service_config.config_rules.add()
        acl_config_rule.action = ConfigActionEnum.CONFIGACTION_SET

        # Set EndpointId associated to the ACLRuleSet
        acl_endpoint_id = acl_config_rule.acl.endpoint_id
        acl_endpoint_id.device_id.device_uuid.uuid = device_uuid
        acl_endpoint_id.endpoint_uuid.uuid = endpoint_uuid

        # Set RuleSet for this ACL ConfigRule
        acl_rule_set = acl_config_rule.acl.rule_set

        acl_rule_set.name = "DROP-TCP"
        acl_rule_set.type = AclRuleTypeEnum.ACLRULETYPE_IPV4
        acl_rule_set.description = "DROP undesired TCP traffic"

        # Add ACLEntry to the ACLRuleSet
        acl_entry = acl_rule_set.entries.add()
        acl_entry.sequence_id = self.sequence_id
        acl_entry.description = "DROP-{src_ip}:{src_port}-{dst_ip}:{dst_port}".format(
            src_ip=src_ip, src_port=src_port, dst_ip=dst_ip, dst_port=dst_port
        )
        acl_entry.match.protocol = (
            6  # TCP according to https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
        )
        acl_entry.match.src_address = "{}/32".format(src_ip)
        acl_entry.match.dst_address = "{}/32".format(dst_ip)
        acl_entry.match.src_port = int(src_port)
        acl_entry.match.dst_port = int(dst_port)

        acl_entry.action.forward_action = AclForwardActionEnum.ACLFORWARDINGACTION_DROP
        acl_entry.action.log_action = AclLogActionEnum.ACLLOGACTION_NOLOG

        LOGGER.info(f"ACL Rule Set: {grpc_message_to_json_string(acl_rule_set)}")
        LOGGER.info(f"ACL Config Rule: {grpc_message_to_json_string(acl_config_rule)}")

        # Add the ACLRuleSet to the list of configured ACLRuleSets
        self.configured_acl_config_rules.append(acl_config_rule)
        
        LOGGER.info(service_request)

        # Update the Service with the new ACL RuleSet
        service_reply = self.service_client.UpdateService(service_request)

        LOGGER.info(f"Service reply: {grpc_message_to_json_string(service_reply)}")

        if service_reply != service_request.service_id:  # pylint: disable=no-member
            raise Exception("Service update failed. Wrong ServiceId was returned")

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def PerformMitigation(self, request : L3AttackmitigatorOutput, context : grpc.ServicerContext) -> StatusMessage:
        """
        Performs mitigation on an attack by configuring an ACL rule to block undesired TCP traffic.

        Args:
            request (L3AttackmitigatorOutput): The request message containing the attack mitigation information.
            context (Empty): The context of the request.

        Returns:
            StatusMessage: A response with a message indicating that the attack mitigation information
                was received and processed.
        """

        last_value = request.confidence
        last_tag = request.tag

        LOGGER.info(
            f"Attack Mitigator received attack mitigation information. Prediction confidence: {last_value}, Predicted class: {last_tag}"
        )

        ip_o = request.ip_o
        ip_d = request.ip_d
        port_o = request.port_o
        port_d = request.port_d

        sentinel = True
        counter = 0
        service_id = request.service_id

        LOGGER.info(f"Service Id.: {grpc_message_to_json_string(service_id)}")
        LOGGER.info("Retrieving service from Context")

        while sentinel:
            try:
                service = self.context_client.GetService(service_id)
                sentinel = False
            except Exception as e:
                counter = counter + 1
                LOGGER.debug(f"Waiting 2 seconds for service to be available (attempt: {counter})")
                time.sleep(2)

        LOGGER.info(
            f"Service with Service Id.: {grpc_message_to_json_string(service_id)}\n{grpc_message_to_json_string(service)}"
        )
        LOGGER.info("Adding new rule to the service to block the attack")

        self.configure_acl_rule(
            context_uuid=service_id.context_id.context_uuid.uuid,
            service_uuid=service_id.service_uuid.uuid,
            device_uuid=request.endpoint_id.device_id.device_uuid.uuid,
            endpoint_uuid=request.endpoint_id.endpoint_uuid.uuid,
            src_ip=ip_o,
            dst_ip=ip_d,
            src_port=port_o,
            dst_port=port_d,
        )
        LOGGER.info("Service with new rule:\n{}".format(grpc_message_to_json_string(service)))
        LOGGER.info("Updating service with the new rule")

        self.service_client.UpdateService(service)
        service = self.context_client.GetService(service_id)

        LOGGER.info(
            "Service obtained from Context after updating with the new rule:\n{}".format(
                grpc_message_to_json_string(service)
            )
        )

        return StatusMessage(message=f"OK, received values: {last_tag} with confidence {last_value}.")

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetConfiguredACLRules(self, request : Empty, context : grpc.ServicerContext) -> ACLRules:
        """
        Returns the configured ACL rules.

        Args:
            request (Empty): The request message.
            context (Empty): The context of the RPC call.

        Returns:
            acl_rules (ACLRules): The configured ACL rules.
        """

        acl_rules = ACLRules()

        for acl_config_rule in self.configured_acl_config_rules:
            acl_rules.acl_rules.append(acl_config_rule)

        return acl_rules
