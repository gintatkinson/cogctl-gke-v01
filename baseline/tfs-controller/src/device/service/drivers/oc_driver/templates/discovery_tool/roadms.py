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

import re
import lxml.etree as ET

def extract_channel_xmlns (data_xml:str,is_opticalband:bool):
    xml_bytes = data_xml.encode("utf-8")
    root = ET.fromstring(xml_bytes) 
 
    namespace=None
    channels=None
  
    if (not is_opticalband) :
      
        optical_channel_namespaces = {
        'ns': 'urn:ietf:params:xml:ns:netconf:base:1.0',
          'oc': 'http://openconfig.net/yang/platform',
        }
       
        channels= root.find('.//{*}optical-channel',optical_channel_namespaces)
        if channels is not None :
          optical_channel_namespace = channels.tag.replace("optical-channel", "")
          namespace=optical_channel_namespace.replace("{", "").replace("}", "")
    else :       
        optical_band_namespaces= {
          'oc':'http://openconfig.net/yang/wavelength-router'
        }
        
        channels= root.find('.//{*}optical-bands',optical_band_namespaces)
        if channels is not None: 
          optical_channel_namespace = channels.tag.replace("optical-bands", "")
          namespace=optical_channel_namespace.replace("{", "").replace("}", "")
    return namespace

def extract_optical_bands (data_xml:str,namespace:str):
    namespaces={"oc":namespace}
    xml_bytes = data_xml.encode("utf-8")
    root = ET.fromstring(xml_bytes) 
    op_bands=[]
    optical_bands= root.find('.//oc:optical-bands',namespaces)

    if optical_bands is not None :
        optical_bands_ele= optical_bands.findall('.//oc:optical-band',namespaces)

        for optical_band in optical_bands_ele:
            band_ele=optical_band.find('.//oc:name',namespaces)
            lower_freq_ele=optical_band.find('.//oc:lower-frequency',namespaces)
            upper_freq_ele=optical_band.find('.//oc:upper-frequency',namespaces)
            admin_status_ele=optical_band.find('.//oc:admin-status',namespaces)
            source_ele=optical_band.find('.//oc:source/oc:config/oc:port-name',namespaces)
            dest_ele=optical_band.find('.//oc:dest/oc:config/oc:port-name',namespaces)
            channel_index= optical_band.find('.//oc:index',namespaces)
            op_band_obj={
                'band_name':band_ele.text if band_ele is not None else None,
                'lower_frequency':lower_freq_ele.text if lower_freq_ele is not None else None,
                'upper_frequency':upper_freq_ele.text if upper_freq_ele is not None else None,
                'status':admin_status_ele.text if admin_status_ele is not None else None,
                'src_port':source_ele.text if source_ele is not None else None,
                'dest_port':dest_ele.text if dest_ele is not None else None,
                "channel_index":channel_index.text if channel_index is not None else None
            }
            op_bands.append(op_band_obj)
        
    return op_bands
        
def extract_media_channels (data_xml:str):
    optical_band_namespaces="http://flex-scale-project.eu/yang/flex-scale-mg-on"
    namespaces={"oc":"http://openconfig.net/yang/wavelength-router",'ob_parent':optical_band_namespaces}
    xml_bytes = data_xml.encode("utf-8")
    root = ET.fromstring(xml_bytes) 
    media_channels= root.find(f'.//oc:media-channels',namespaces)
    op_bands=[]
    if media_channels is not None :
        media_channels_ele= media_channels.findall('.//oc:channel',namespaces)
        for optical_band in media_channels_ele:
            band_ele=optical_band.find('.//oc:name',namespaces)
            lower_freq_ele=optical_band.find('.//oc:lower-frequency',namespaces)
            upper_freq_ele=optical_band.find('.//oc:upper-frequency',namespaces)
            admin_status_ele=optical_band.find('.//oc:admin-status',namespaces)
            source_ele=optical_band.find('.//oc:source/oc:config/oc:port-name',namespaces)
            dest_ele=optical_band.find('.//oc:dest/oc:config/oc:port-name',namespaces)
            ob_parent=optical_band.find('.//ob_parent:optical-band-parent',namespaces)
            channel_index= optical_band.find('.//oc:index',namespaces)
            op_band_obj={
                'band_name':band_ele.text if band_ele is not None else None,
                'lower_frequency':lower_freq_ele.text if lower_freq_ele is not None else None,
                'upper_frequency':upper_freq_ele.text if upper_freq_ele is not None else None,
                'status':admin_status_ele.text if admin_status_ele is not None else None,
                'src_port':source_ele.text if source_ele is not None else None,
                'dest_port':dest_ele.text if dest_ele is not None else None,
                'optical_band_parent':ob_parent.text if ob_parent is not None else None,
                'channel_index':channel_index.text if channel_index is not None else None
            }
            op_bands.append(op_band_obj)

    return op_bands

def extract_roadm_ports_old (xml_data:str):
    ports =[]
    pattern = r'\bMG_ON_OPTICAL_PORT_WAVEBAND\b'
    xml_bytes = xml_data.encode("utf-8")
    root = ET.fromstring(xml_bytes)
    with open('xml.log', 'w') as f:
         print(xml_bytes, file=f)

    namespace = {'oc': 'http://openconfig.net/yang/platform'}
    ports = []
    components = root.findall('.//oc:component',namespace)
    print(f"component {components}")

    for component  in components:
        properties = component.find(".//oc:properties",namespace)
        if (properties is not None):
            for property in properties :
                value = property.find(".//oc:value",namespace)
                if (re.search(pattern,value.text)):
                    name_element= component.find(".//oc:name",namespace)
                    ports.append(name_element.text)
    return ports     

def extract_roadm_ports (xml_data:str):
    ports =[]
    pattern2=r'\bMG_ON_PORT_TYPE'
    pattern = r'\bMG_ON_OPTICAL_PORT_WAVEBAND\b'
    xml_bytes = xml_data.encode("utf-8")
    root = ET.fromstring(xml_bytes)

    namespace = {'oc': 'http://openconfig.net/yang/platform'}
    ports = []
    components = root.findall('.//oc:component',namespace)
    #print(f"component {components}")

    for component  in components:
        properties = component.find(".//oc:properties",namespace)
        if (properties is not None):
            for property in properties :
                value = property.find(".//oc:value",namespace)
                name= property.find('.//oc:name',namespace)
                if (re.search(pattern2,name.text)):
                   value = property.find(".//oc:value",namespace)
                   name_element= component.find(".//oc:name",namespace)
                   print('value',value.text)
                   ports.append((name_element.text,value.text))
    return ports                

def roadm_values_extractor (data_xml:str,resource_keys:list,dic:dict):
    ports_result=[]
    ports = extract_roadm_ports(data_xml)
    namespcae= extract_channel_xmlns(data_xml,True)
    optical_bands=extract_optical_bands(data_xml=data_xml,namespace=namespcae)
    media_cahannels=extract_media_channels(data_xml)

    if len(ports)>0 :
        for port in ports :
            name,type=port
            resource_key = '/endpoints/endpoint[{:s}]'.format(name)
            resource_value = {'uuid': name, 'type':type}
            ports_result.append((resource_key, resource_value))
    return [ports_result,optical_bands,media_cahannels]   
