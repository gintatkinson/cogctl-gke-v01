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

import ipaddress, re
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Optional, NumberRange, ValidationError, StopValidation

# Custom uuid validator
def validate_uuid_address(form, field):
    if not re.match(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$', field.data):
        raise ValidationError('Invalid uuid format')

# Custom IPv4 address validator
def validate_ipv4_address(form, field):
    try:
        ipaddress.IPv4Address(field.data)
    except ipaddress.AddressValueError:
        raise ValidationError('Invalid IPv4 address format')

# Custom IPv6 address validator
def validate_ipv6_address(form, field):
    try:
        ipaddress.IPv6Address(field.data)
    except ipaddress.AddressValueError:
        raise ValidationError('Invalid IPv6 address format')
    
# Custom Mac address validator
def validate_mac_address(form, field):             
    if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', field.data):
        raise ValidationError('Invalid MAC address format')

# Custom route distinguisher validator
def validate_route_distinguisher(form,field):
    pattern = r'^([0-9]|[1-9][0-9]{1,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5]):([0-9]|[1-9][0-9]{1,8}|[1-3][0-9]{9}|4[01][0-9]{8}|42[0-8][0-9]{7}|429[0-3][0-9]{6}|4294[0-8][0-9]{5}|42949[0-5][0-9]{4}|429496[0-6][0-9]{3}|4294967[01][0-9]{2}|42949672[0-8][0-9]|429496729[0-5])$'
    if not re.match(pattern, field.data):
        raise ValidationError('Invalid Route Distinguisher')

# Custom integer validator
def validate_uint32(form, field):
    if not 0 <= field.data <= 2**32-1:
        raise ValidationError('Value must be a positive integer within the range of uint32')

# Custom  BGP AS validator
def validate_NI_as(form, field):
    if form.NI_protocol.data == 'BGP' and field.data == None:
        raise StopValidation('AS field is required if the BGP protocol is selected.')
        
class CustomInputRequired():
    def __init__(self, message=None):
        self.message = message or "This field is required." 
    def __call__(self, form, field):
        if field.data is None or field.data == '':
            raise StopValidation(self.message)
        
class AddServiceForm_1(FlaskForm):
    service_type = SelectField('Type of service', choices=[('', 'Select a type of service to add'), ('ACL_L2', 'ACL_L2'), ('ACL_IPV4', 'ACL_IPV4'), ('ACL_IPV6', 'ACL_IPV6'), ('L2VPN', 'L2VPN'), ('L3VPN', 'L3VPN'), ('QKD', 'QKD')], validators=[InputRequired()])

class AddServiceForm_QKD(FlaskForm):
    #GENERIC SERVICE PARAMETERS (COMMON & MANDATORY)
    service_name       = StringField('Service Name', validators=[CustomInputRequired()])
    service_type       = SelectField('Service Type', choices=[(6, '6 (QKD)')], validators=[CustomInputRequired()])
    service_device_1   = SelectField('Device_1', choices=[('', 'Select a device (Mandatory)')], validators=[CustomInputRequired()])
    service_device_2   = SelectField('Device_2', choices=[('', 'Select a device (Mandatory)')], validators=[CustomInputRequired()])
    service_endpoint_1 = StringField('Device_1 Endpoint', validators=[CustomInputRequired()])
    service_endpoint_2 = StringField('Device_2 Endpoint', validators=[CustomInputRequired()])
    
    #GENERIC SERVICE CONSTRAINT PARAMETERS (ALL OPTIONAL)
    service_capacity    = DecimalField('Service Capacity', places=2, default=10.00, validators=[Optional(), NumberRange(min=0)])
    service_latency     = DecimalField('Service Latency', places=2, default=15.20, validators=[Optional(), NumberRange(min=0)])
    service_availability= DecimalField('Service Availability', places=2, validators=[Optional(), NumberRange(min=0)])
    service_isolation   = SelectField('Service Isolation', choices=[('', 'Select (Optional)'), ('NO_ISOLATION', 'NO_ISOLATION'), ('PHYSICAL_ISOLATION', 'PHYSICAL_ISOLATION'), 
                                                                    ('LOGICAL_ISOLATION', 'LOGICAL_ISOLATION'), ('PROCESS_ISOLATION', 'PROCESS_ISOLATION'), ('PHYSICAL_MEMORY_ISOLATION', 'PHYSICAL_MEMORY_ISOLATION'), 
                                                                    ('PHYSICAL_NETWORK_ISOLATION', 'PHYSICAL_NETWORK_ISOLATION'), ('VIRTUAL_RESOURCE_ISOLATION', 'VIRTUAL_RESOURCE_ISOLATION'), 
                                                                    ('NETWORK_FUNCTIONS_ISOLATION', 'NETWORK_FUNCTIONS_ISOLATION'), ('SERVICE_ISOLATION', 'SERVICE_ISOLATION')], validators=[Optional()])

class AddServiceForm_ACL_L2(FlaskForm):
    #GENERIC SERVICE PARAMETERS (COMMON & MANDATORY)
    service_name       = StringField('Service Name', validators=[CustomInputRequired()])
    service_type       = SelectField('Service Type', choices=[(2, '2 (L2NM)')], validators=[CustomInputRequired()])
    service_device_1   = SelectField('Device_1', choices=[('', 'Select a device (Mandatory)')], validators=[CustomInputRequired()])
    service_device_2   = SelectField('Device_2', choices=[('', 'Select a device (Mandatory)')], validators=[CustomInputRequired()])
    service_endpoint_1 = StringField('Device_1 Endpoint', validators=[CustomInputRequired()])
    service_endpoint_2 = StringField('Device_2 Endpoint', validators=[CustomInputRequired()])
    
    #GENERIC SERVICE CONSTRAINT PARAMETERS (ALL OPTIONAL)
    service_capacity    = DecimalField('Service Capacity', places=2, default=10.00, validators=[Optional(), NumberRange(min=0)])
    service_latency     = DecimalField('Service Latency', places=2, default=15.20, validators=[Optional(), NumberRange(min=0)])
    service_availability= DecimalField('Service Availability', places=2, validators=[Optional(), NumberRange(min=0)])
    service_isolation   = SelectField('Service Isolation', choices=[('', 'Select (Optional)'), ('NO_ISOLATION', 'NO_ISOLATION'), ('PHYSICAL_ISOLATION', 'PHYSICAL_ISOLATION'), 
                                                                    ('LOGICAL_ISOLATION', 'LOGICAL_ISOLATION'), ('PROCESS_ISOLATION', 'PROCESS_ISOLATION'), ('PHYSICAL_MEMORY_ISOLATION', 'PHYSICAL_MEMORY_ISOLATION'), 
                                                                    ('PHYSICAL_NETWORK_ISOLATION', 'PHYSICAL_NETWORK_ISOLATION'), ('VIRTUAL_RESOURCE_ISOLATION', 'VIRTUAL_RESOURCE_ISOLATION'), 
                                                                    ('NETWORK_FUNCTIONS_ISOLATION', 'NETWORK_FUNCTIONS_ISOLATION'), ('SERVICE_ISOLATION', 'SERVICE_ISOLATION')], validators=[Optional()])
    
    #MANDATORY_PARAMETERS
    name                = StringField('ACL Name', validators=[CustomInputRequired("The name of the ACL is a mandatory parameter")])
    type                = SelectField('ACL Type', choices=[('ACL_L2', 'ACL_L2')], validators=[CustomInputRequired("The type of the ACL is a mandatory parameter")])
    sequence_id         = IntegerField('ACL Sequence ID', validators=[CustomInputRequired("The name of the Sequence ID of the ACL is a mandatory parameter"), validate_uint32])
    forwarding_action   = SelectField('ACL Fowarding Action', choices=[('', 'Select an action (Mandatory)'), ('ACCEPT', 'Accept'), ('DROP','Drop'),('REJECT','Reject')], validators=[CustomInputRequired("The Forwarding Action of the ACL is a mandatory parameter")])  
    log_action          = SelectField('ACL Log Action', choices=[(None, 'Select a log action (Optional)'), ('LOG_SYSLOG', 'Syslog'), ('LOG_NONE','None')], validators=[Optional()]) 

    #PARAMETERS FOR Associating ACL to IF 
    interface           = StringField('Interface Name', validators=[CustomInputRequired("The name of the Interface is a mandatory parameter")])
    subinterface        = StringField('Subinterface Index', validators=[Optional()])
    traffic_flow        = SelectField('ACL Traffic Flow Direction', choices=[('', 'Select a direction (Mandatory)'), ('Ingress', 'Ingress'), ('Egress','Egress')], validators=[CustomInputRequired("The direction of the traffic flow is a mandatory parameter")])

    #SPECIFIC PARAMETERS - Creating ACL Entry [ACL_L2]
    source_mac          = StringField('Source MAC Address', validators=[Optional(), validate_mac_address])  
    destination_mac     = StringField('Destination MAC Address', validators=[Optional(), validate_mac_address]) 

class AddServiceForm_ACL_IPV4(FlaskForm):
    #GENERIC SERVICE PARAMETERS (COMMON & MANDATORY)
    service_name        = StringField('Service Name', validators=[CustomInputRequired()])
    service_type        = SelectField('Service Type', choices=[(1, '1 (L3NM)')], validators=[CustomInputRequired()])
    service_device_1    = SelectField('Device_1', choices=[('', 'Select a device (Mandatory)')], validators=[CustomInputRequired()])
    service_device_2    = SelectField('Device_2', choices=[('', 'Select a device (Mandatory)')], validators=[CustomInputRequired()])
    service_endpoint_1  = StringField('Device_1 Endpoint', validators=[CustomInputRequired()])
    service_endpoint_2  = StringField('Device_2 Endpoint', validators=[CustomInputRequired()])
    
    #GENERIC SERVICE CONSTRAINT PARAMETERS (ALL OPTIONAL)
    service_capacity    = DecimalField('Service Capacity', places=2, default=10.00, validators=[Optional(), NumberRange(min=0)])
    service_latency     = DecimalField('Service Latency', places=2, default=15.20, validators=[Optional(), NumberRange(min=0)])
    service_availability= DecimalField('Service Availability', places=2, validators=[Optional(), NumberRange(min=0)])
    service_isolation   = SelectField('Service Isolation', choices=[('', 'Select (Optional)'), ('NO_ISOLATION', 'NO_ISOLATION'), ('PHYSICAL_ISOLATION', 'PHYSICAL_ISOLATION'), 
                                                                    ('LOGICAL_ISOLATION', 'LOGICAL_ISOLATION'), ('PROCESS_ISOLATION', 'PROCESS_ISOLATION'), ('PHYSICAL_MEMORY_ISOLATION', 'PHYSICAL_MEMORY_ISOLATION'), 
                                                                    ('PHYSICAL_NETWORK_ISOLATION', 'PHYSICAL_NETWORK_ISOLATION'), ('VIRTUAL_RESOURCE_ISOLATION', 'VIRTUAL_RESOURCE_ISOLATION'), 
                                                                    ('NETWORK_FUNCTIONS_ISOLATION', 'NETWORK_FUNCTIONS_ISOLATION'), ('SERVICE_ISOLATION', 'SERVICE_ISOLATION')], validators=[Optional()])
    
    #MANDATORY_PARAMETERS
    name                = StringField('ACL Name', validators=[CustomInputRequired("The name of the ACL is a mandatory parameter")])
    type                = SelectField('ACL Type', choices=[('ACL_IPV4', 'ACL_IPV4')], validators=[CustomInputRequired("The type of the ACL is a mandatory parameter")])
    sequence_id         = IntegerField('ACL Sequence ID', validators=[InputRequired(), NumberRange(min=1, message="Sequence ID must be greater than 0")])
    forwarding_action   = SelectField('ACL Fowarding Action', choices=[(None, 'Select an action (Mandatory)'), ('ACCEPT', 'Accept'), ('DROP','Drop'),('REJECT','Reject')], validators=[InputRequired()])  
    log_action          = SelectField('ACL Log Action', choices=[(None, 'Select a log action (Optional)'), ('LOG_SYSLOG', 'Syslog'), ('LOG_NONE','None')], validators=[Optional()]) 

    #PARAMETERS FOR Associating ACL to IF 
    interface           = StringField('Interface Name', validators=[InputRequired()])
    subinterface        = StringField('Subinterface Index', validators=[Optional()])
    traffic_flow        = SelectField('ACL Traffic Flow Direction', choices=[('', 'Select a direction (Mandatory)'), ('Ingress', 'Ingress'), ('Egress','Egress')], validators=[InputRequired()])

    #OPTIONAL_PARAMETERS - Creating ACL Entry [ACL_IPV4]
    source_address      = StringField('Source Address', validators=[Optional(), validate_ipv4_address])
    destination_address = StringField('Destination Address', validators=[Optional(), validate_ipv4_address]) 
    protocol            = IntegerField('Protocol',  validators=[Optional(),NumberRange(min=1, max=255, message="Protocol number is between 1 and 255 as defined by IANA")])
    hop_limit           = IntegerField('Hop Limit', validators=[Optional(),NumberRange(min=1, max=255, message="The Hop limit value has to be between 0 and 255")])
    dscp                = IntegerField('DSCP', validators=[Optional(),NumberRange(min=1, max=255, message="The DSCP value has to be between 0 and 63")])
    source_port         = IntegerField('Source Port', validators=[Optional(),NumberRange(min=0, max=65535, message="The Port value has to be between 0 and 655535")])
    destination_port    = IntegerField('Destination Port', validators=[Optional(),NumberRange(min=0, max=65535, message="The Port value has to be between 0 and 655535")])
    tcp_flags           = SelectField('TCP Flags', choices=[(None, 'Select a TCP Flag (Optional)'),('TCP_SYN', 'TCP_SYN'),('TCP_ACK', 'TCP_ACK'),('TCP_RST', 'TCP_RST'),('TCP_FIN', 'TCP_FIN'),
                                                            ('TCP_PSH', 'TCP_PSH'),('TCP_URG', 'TCP_URG') ,('TCP_ECE', 'TCP_ECE'),('TCP_CWR', 'TCP_CWR')], validators=[Optional()]) 

class AddServiceForm_ACL_IPV6(FlaskForm):
    #GENERIC SERVICE PARAMETERS (COMMON & MANDATORY)
    service_name       = StringField('Service Name', validators=[CustomInputRequired()])
    service_type       = SelectField('Service Type', choices=[(1, '1 (L3NM)')], validators=[CustomInputRequired()])
    service_device_1   = SelectField('Device_1', choices=[('', 'Select a device (Mandatory)')], validators=[CustomInputRequired()])
    service_device_2   = SelectField('Device_2', choices=[('', 'Select a device (Mandatory)')], validators=[CustomInputRequired()])
    service_endpoint_1 = StringField('Device_1 Endpoint', validators=[CustomInputRequired()])
    service_endpoint_2 = StringField('Device_2 Endpoint', validators=[CustomInputRequired()])
    
    #GENERIC SERVICE CONSTRAINT PARAMETERS (ALL OPTIONAL)
    service_capacity    = DecimalField('Service Capacity', places=2, default=10.00, validators=[Optional(), NumberRange(min=0)])
    service_latency     = DecimalField('Service Latency', places=2, default=15.20, validators=[Optional(), NumberRange(min=0)])
    service_availability= DecimalField('Service Availability', places=2, validators=[Optional(), NumberRange(min=0)])
    service_isolation   = SelectField('Service Isolation', choices=[('', 'Select (Optional)'), ('NO_ISOLATION', 'NO_ISOLATION'), ('PHYSICAL_ISOLATION', 'PHYSICAL_ISOLATION'), 
                                                                    ('LOGICAL_ISOLATION', 'LOGICAL_ISOLATION'), ('PROCESS_ISOLATION', 'PROCESS_ISOLATION'), ('PHYSICAL_MEMORY_ISOLATION', 'PHYSICAL_MEMORY_ISOLATION'), 
                                                                    ('PHYSICAL_NETWORK_ISOLATION', 'PHYSICAL_NETWORK_ISOLATION'), ('VIRTUAL_RESOURCE_ISOLATION', 'VIRTUAL_RESOURCE_ISOLATION'), 
                                                                    ('NETWORK_FUNCTIONS_ISOLATION', 'NETWORK_FUNCTIONS_ISOLATION'), ('SERVICE_ISOLATION', 'SERVICE_ISOLATION')], validators=[Optional()])
    
    #MANDATORY_PARAMETERS
    name                = StringField('ACL Name', validators=[InputRequired()])
    type                = SelectField('ACL Type', choices=[('ACL_IPV6', 'ACL_IPV6')], validators=[InputRequired()])
    sequence_id         = IntegerField('ACL Sequence ID', validators=[InputRequired(), NumberRange(min=1, message="Sequence ID must be greater than 0")])
    forwarding_action   = SelectField('ACL Fowarding Action', choices=[(None, 'Select an action (Mandatory)'), ('ACCEPT', 'Accept'), ('DROP','Drop'),('REJECT','Reject')], validators=[InputRequired()])  
    log_action          = SelectField('ACL Log Action', choices=[(None, 'Select a log action (Optional)'), ('LOG_SYSLOG', 'Syslog'), ('LOG_NONE','None')], validators=[Optional()]) 

    #PARAMETERS FOR Associating ACL to IF 
    interface           = StringField('Interface Name', validators=[InputRequired()])
    subinterface        = StringField('Subinterface Index', validators=[Optional()])
    traffic_flow        = SelectField('ACL Traffic Flow Direction', choices=[('', 'Select a direction (Mandatory)'), ('Ingress', 'Ingress'), ('Egress','Egress')], validators=[InputRequired()])

    #SPECIFIC PARAMETERS - Creating ACL Entry [ACL_IPV6]
    source_address      = StringField('Source Address', validators=[Optional(), validate_ipv6_address])
    destination_address = StringField('Destination Address', validators=[Optional(), validate_ipv6_address])
    protocol            = IntegerField('Protocol',  validators=[Optional(),NumberRange(min=1, max=255, message="Protocol number is between 1 and 255 as defined by IANA")])
    hop_limit           = IntegerField('Hop Limit', validators=[Optional(),NumberRange(min=1, max=255, message="The Hop limit value has to be between 0 and 255")])
    dscp                = IntegerField('DSCP', validators=[Optional(),NumberRange(min=1, max=255, message="The DSCP value has to be between 0 and 63")])

class AddServiceForm_L2VPN(FlaskForm):
    #GENERIC SERVICE PARAMETERS (COMMON & MANDATORY)
    service_name       = StringField('Service Name', validators=[CustomInputRequired()])
    service_type       = SelectField('Service Type', choices=[(2, '2 (L2NM)')], validators=[CustomInputRequired()])
    service_device_1   = SelectField('Device_1', choices=[('', 'Select a device (Mandatory)')], validators=[CustomInputRequired()])
    service_device_2   = SelectField('Device_2', choices=[('', 'Select a device (Mandatory)')], validators=[CustomInputRequired()])
    service_endpoint_1 = StringField('Device_1 Endpoint', validators=[CustomInputRequired()])
    service_endpoint_2 = StringField('Device_2 Endpoint', validators=[CustomInputRequired()])
    
    #GENERIC SERVICE CONSTRAINT PARAMETERS (ALL OPTIONAL)
    service_capacity    = DecimalField('Service Capacity', places=2, default=10.00, validators=[Optional(), NumberRange(min=0)])
    service_latency     = DecimalField('Service Latency', places=2, default=15.20, validators=[Optional(), NumberRange(min=0)])
    service_availability= DecimalField('Service Availability', places=2, validators=[Optional(), NumberRange(min=0)])
    service_isolation   = SelectField('Service Isolation', choices=[('', 'Select (Optional)'), ('NO_ISOLATION', 'NO_ISOLATION'), ('PHYSICAL_ISOLATION', 'PHYSICAL_ISOLATION'), 
                                                                    ('LOGICAL_ISOLATION', 'LOGICAL_ISOLATION'), ('PROCESS_ISOLATION', 'PROCESS_ISOLATION'), ('PHYSICAL_MEMORY_ISOLATION', 'PHYSICAL_MEMORY_ISOLATION'), 
                                                                    ('PHYSICAL_NETWORK_ISOLATION', 'PHYSICAL_NETWORK_ISOLATION'), ('VIRTUAL_RESOURCE_ISOLATION', 'VIRTUAL_RESOURCE_ISOLATION'), 
                                                                    ('NETWORK_FUNCTIONS_ISOLATION', 'NETWORK_FUNCTIONS_ISOLATION'), ('SERVICE_ISOLATION', 'SERVICE_ISOLATION')], validators=[Optional()])
    
    
    NI_name                      = StringField('NI Name', validators=[CustomInputRequired()])
    NI_mtu                       = IntegerField('NI MTU', default=1500, validators=[CustomInputRequired(), NumberRange(min=0, message="MTU value can't be negative")])
    NI_description               = StringField('NI Description', validators=[Optional()])
    #Device_1 specific
    Device_1_NI_remote_system    = StringField('Device_1 NI Remote System', validators=[CustomInputRequired(),validate_ipv4_address])
    Device_1_NI_VC_ID            = IntegerField('Device_1 NI VC ID', validators=[CustomInputRequired(), NumberRange(min=0, message="VC can't be negative")])
    Device_1_NI_connection_point = StringField('Device_1 NI Conection Point', validators=[CustomInputRequired()])
    #Device_2 specific
    Device_2_NI_remote_system    = StringField ('Device_2 NI Remote System', validators=[CustomInputRequired(),validate_ipv4_address])
    Device_2_NI_VC_ID            = IntegerField('Device_2 NI VC ID', validators=[CustomInputRequired(), NumberRange(min=0, message="VC can't be negative")])
    Device_2_NI_connection_point = StringField ('Device_2 NI Conection Point', validators=[CustomInputRequired()])
     
    #Interface parameters (DEVICE SPECIFIC)
    Device_1_IF_index       = IntegerField('Device_1 SubIF Index', validators=[CustomInputRequired(), NumberRange(min=0, message="SubIf index can't be negative")])
    Device_1_IF_vlan_id     = IntegerField('Device_1 VLAN ID', validators=[CustomInputRequired(), NumberRange(min=0, message="VlanID can't be negative")])
    Device_1_IF_mtu         = IntegerField('Device_1 Interface MTU', validators=[Optional(), NumberRange(min=0, message="MTU value can't be negative")])
    Device_1_IF_description = StringField ('Device_1 SubIF Description', validators=[Optional()])
    
    Device_2_IF_index       = IntegerField('Device_2 SubIF Index', validators=[CustomInputRequired(), NumberRange(min=0, message="SubIf index can't be negative")])
    Device_2_IF_vlan_id     = IntegerField('Device_2 VLAN ID', validators=[CustomInputRequired(), NumberRange(min=0, message="VlanID can't be negative")])
    Device_2_IF_mtu         = IntegerField('Device_2 Interface MTU', validators=[Optional(), NumberRange(min=0, message="MTU value can't be negative")])
    Device_2_IF_description = StringField ('Device_2 SubIF Description', validators=[Optional()])

class AddServiceForm_L3VPN(FlaskForm):
    #GENERIC SERVICE PARAMETERS (COMMON & MANDATORY)
    service_name     = StringField('Service Name', validators=[CustomInputRequired()])
    service_type     = SelectField('Service Type', choices=[(1, '1 (L3NM)')], validators=[CustomInputRequired()])
    service_device_1   = SelectField('Device_1', choices=[('', 'Select a device (Mandatory)')], validators=[CustomInputRequired()])
    service_device_2   = SelectField('Device_2', choices=[('', 'Select a device (Mandatory)')], validators=[CustomInputRequired()])
    service_endpoint_1 = StringField('Device_1 Endpoint', validators=[CustomInputRequired()])
    service_endpoint_2 = StringField('Device_2 Endpoint', validators=[CustomInputRequired()])
    
    #GENERIC SERVICE CONSTRAINT PARAMETERS (ALL OPTIONAL)
    service_capacity    = DecimalField('Service Capacity', places=2, default=10.00, validators=[Optional(), NumberRange(min=0)])
    service_latency     = DecimalField('Service Latency', places=2, default=15.20, validators=[Optional(), NumberRange(min=0)])
    service_availability= DecimalField('Service Availability', places=2, validators=[Optional(), NumberRange(min=0)])
    service_isolation   = SelectField('Service Isolation', choices=[('', 'Select (Optional)'), ('NO_ISOLATION', 'NO_ISOLATION'), ('PHYSICAL_ISOLATION', 'PHYSICAL_ISOLATION'), 
                                                                    ('LOGICAL_ISOLATION', 'LOGICAL_ISOLATION'), ('PROCESS_ISOLATION', 'PROCESS_ISOLATION'), ('PHYSICAL_MEMORY_ISOLATION', 'PHYSICAL_MEMORY_ISOLATION'), 
                                                                    ('PHYSICAL_NETWORK_ISOLATION', 'PHYSICAL_NETWORK_ISOLATION'), ('VIRTUAL_RESOURCE_ISOLATION', 'VIRTUAL_RESOURCE_ISOLATION'), 
                                                                    ('NETWORK_FUNCTIONS_ISOLATION', 'NETWORK_FUNCTIONS_ISOLATION'), ('SERVICE_ISOLATION', 'SERVICE_ISOLATION')], validators=[Optional()])
     
    NI_name           = StringField('Name', validators=[InputRequired()])
    NI_route_distinguisher = StringField('Route Distinguisher', validators=[InputRequired(),validate_route_distinguisher])
    NI_router_id      = StringField('Router ID', validators=[Optional(), validate_ipv4_address])
    NI_description    = StringField('Description', validators=[Optional()])
    NI_protocol       = SelectField('Protocol', choices=[('', 'Select a type (Mandatory)'),('STATIC', 'STATIC'),('DIRECTLY_CONNECTED', 'DIRECTLY_CONNECTED'),('BGP', 'BGP')], validators=[InputRequired()])  
    NI_as             = IntegerField('AS', default=None, validators=[validate_NI_as, Optional(), validate_uint32])                      
    NI_address_family = SelectField('Protocol Address Family', choices=[('', 'Select a type (Mandatory)'),('IPV4', 'IPV4'),('IPV6', 'IPV6')], validators=[InputRequired()])        
    NI_default_import_policy = SelectField('Default Network Instance Import Policy', choices=[('', 'Select a policy (Mandatory)'),('ACCEPT_ROUTE', 'ACCEPT_ROUTE'),('REJECT_ROUTE', 'REJECT_ROUTE')], validators=[Optional()])                                 
    NI_import_policy  = StringField('Name of the Network Instance Import Policy', validators=[Optional()])
    NI_export_policy  = StringField('Name of the Network Instance Export Policy', validators=[Optional()])

    ## Interface (IF) PARAMS
    Device_1_IF_index       = IntegerField('Device_1 SubIF Index', validators=[CustomInputRequired(), NumberRange(min=0, message="SubIf index can't be negative")])
    Device_1_IF_vlan_id     = IntegerField('Device_1 VLAN ID', validators=[CustomInputRequired(), NumberRange(min=0, message="VlanID can't be negative")])
    Device_1_IF_mtu         = IntegerField('Device_1 Interface MTU', validators=[Optional(), NumberRange(min=0, message="MTU value can't be negative")])
    Device_1_IF_address_ip  = StringField('Device_1 IP Address', validators=[CustomInputRequired(), validate_ipv4_address])
    Device_1_IF_address_prefix = IntegerField('Device_1 IP Prefix length', validators=[CustomInputRequired(), validate_uint32])
    Device_1_IF_description = StringField ('Device_1 SubIF Description', validators=[Optional()])
    
    Device_2_IF_index       = IntegerField('Device_2 SubIF Index', validators=[CustomInputRequired(), NumberRange(min=0, message="SubIf index can't be negative")])
    Device_2_IF_vlan_id     = IntegerField('Device_2 VLAN ID', validators=[CustomInputRequired(), NumberRange(min=0, message="VlanID can't be negative")])
    Device_2_IF_mtu         = IntegerField('Device_2 Interface MTU', validators=[Optional(), NumberRange(min=0, message="MTU value can't be negative")])
    Device_2_IF_address_ip  = StringField('Device_2 IP Address', validators=[CustomInputRequired(), validate_ipv4_address])
    Device_2_IF_address_prefix = IntegerField('Device_2 IP Prefix length', validators=[CustomInputRequired(), validate_uint32])
    Device_2_IF_description = StringField ('Device_2 SubIF Description', validators=[Optional()])
    
