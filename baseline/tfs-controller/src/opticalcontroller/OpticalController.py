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

import logging, time
from flask import Flask
from flask import render_template
from common.DeviceTypes import DeviceTypeEnum
from flask_restplus import Resource, Api
from opticalcontroller.tools import *
from opticalcontroller.variables import *
from opticalcontroller.RSA import RSA
from common.proto.context_pb2 import TopologyId , OpticalLink
import json
from google.protobuf.message import Message
from google.protobuf.json_format import MessageToDict
from common.tools.object_factory.OpticalLink import order_dict
global rsa
global links_dict
rsa = None


app = Flask(__name__)
api = Api(app, version='1.0', title='Optical controller API',
          description='Rest API to configure OC Optical devices in TFS')
# app.config.from_object('config')
# appbuilder = AppBuilder(app, indexview=MyIndexView)
optical = api.namespace('OpticalTFS', description='TFS Optical APIs')


@app.route('/index')
def index():
    return render_template('index.html')


#@optical.route('/AddLightpath/<string:src>/<string:dst>/<int:bitrate>')
@optical.route('/AddLightpath/<string:src>/<string:dst>/<int:bitrate>/<int:bidir>')
@optical.response(200, 'Success')
@optical.response(404, 'Error, not found')
class AddLightpath(Resource):
    @staticmethod
    def put(src, dst, bitrate, bidir=1):

        print("INFO: New Lightpath request from {} to {} with rate {} ".format(src, dst, bitrate))
        t0 = time.time()*1000.0
        if debug:
            rsa.g.printGraph()

        if rsa is not None:
            flow_id = rsa.rsa_computation(src, dst, bitrate, bidir)
            if rsa.db_flows[flow_id]["op-mode"] == 0:
                return 'No path found', 404
            t1 = time.time() * 1000.0
            elapsed = t1 - t0
            print("INFO: time elapsed = {} ms".format(elapsed))
            return rsa.db_flows[flow_id], 200
        else:
            return "Error", 404


#@optical.route('/AddFlexLightpath/<string:src>/<string:dst>/<int:bitrate>')
@optical.route('/AddFlexLightpath/<string:src>/<string:dst>/<int:bitrate>',
               defaults={"bidir": 1, "band": None})
@optical.route('/AddFlexLightpath/<string:src>/<string:dst>/<int:bitrate>/<int:bidir>',
               defaults={"band": None})
@optical.route('/AddFlexLightpath/<string:src>/<string:dst>/<int:bitrate>/<int:bidir>/<int:band>',)
@optical.response(200, 'Success')
@optical.response(404, 'Error, not found')
class AddFlexLightpath(Resource):
    @staticmethod
    def put(src, dst, bitrate, bidir=1, band=None):

        print("INFO: New FlexLightpath request from {} to {} with rate {} ".format(src, dst, bitrate))
        t0 = time.time()*1000.0
        if debug:
            rsa.g.printGraph()

        if rsa is not None:
            flow_id, optical_band_id = rsa.rsa_fs_computation(src, dst, bitrate, bidir, band)
            if flow_id is not None:
                if rsa.db_flows[flow_id]["op-mode"] == 0:
                    return 'No path found', 404
                t1 = time.time() * 1000.0
                elapsed = t1 - t0
                print("INFO: time elapsed = {} ms".format(elapsed))

                return rsa.db_flows[flow_id], 200
            else:
                if len(rsa.optical_bands[optical_band_id]["flows"]) == 0:
                    return 'No path found', 404
                else:
                    t1 = time.time() * 1000.0
                    elapsed = t1 - t0
                    print("INFO: time elapsed = {} ms".format(elapsed))

                    return rsa.optical_bands[optical_band_id], 200
        else:
            return "Error", 404
# @optical.route('/DelFlexLightpath/<string:src>/<string:dst>/<int:bitrate>/<int:o_band_id>')
@optical.route('/DelFlexLightpath/<string:src>/<string:dst>/<int:bitrate>/<int:flow_id>')
@optical.route('/DelFlexLightpath/<string:src>/<string:dst>/<int:bitrate>/<int:flow_id>/<int:o_band_id>')
@optical.response(200, 'Success')
@optical.response(404, 'Error, not found')
class DelFLightpath(Resource):
    @staticmethod
    def delete( src, dst, bitrate, o_band_id=None, flow_id=None):
            flow = None
            match1=False
            ob_id=None
            if flow_id is not None:
     
                if flow_id in rsa.db_flows.keys():
                   flow = rsa.db_flows[flow_id]
                   match1 = flow["src"] == src and flow["dst"] == dst and flow["bitrate"] == bitrate
                   ob_id = flow["parent_opt_band"] if 'parent_opt_band' in flow else None
                   flow['is_active']=False
            if flow is not None:
                bidir = flow["bidir"]
                if bidir:
                    match2 = flow["src"] == dst and flow["dst"] == src and flow["bitrate"] == bitrate
                    if match1 or match2:
                        ob_id = flow["parent_opt_band"] if 'parent_opt_band' in flow else None
                        rsa.db_flows[flow_id]["is_active"] = False
                        if ob_id:
                           rsa.del_flow(flow, flow_id, ob_id)
                           if flow_id in rsa.optical_bands[ob_id]["served_lightpaths"]:
                               rsa.optical_bands[ob_id]["served_lightpaths"].remove(flow_id)
                        
                        #if rsa.optical_bands[ob_id]["reverse_optical_band_id"] != 0:
                        #    rev_ob_id = rsa.optical_bands[ob_id]["reverse_optical_band_id"]
                        #    rsa.optical_bands[rev_ob_id]["served_lightpaths"].remove(flow_id)

                        if debug:
                            print(rsa.links_dict)
                        return "flow {} deleted".format(flow_id), 200
                    else:
                        return "flow {} not matching".format(flow_id), 404
                else:
                    if match1:
                      
                        # if delete_band !=0 and ob_id is not None:
                        #     print(f"delete_lightpath {delete_band} and ob_id {ob_id}")
                        #     if len( rsa.optical_bands[ob_id]["served_lightpaths"]) != 0:
                        #         return "DELETE_NOT_ALLOWED" ,400
                            
                        ob_id = flow["parent_opt_band"] if 'parent_opt_band' in flow else None
                        if ob_id:
                           rsa.del_flow(flow,flow_id,ob_id)                  
                    
                        if debug:
                           print(f"rsa.links_dict {rsa.links_dict}")
                           if ob_id: 
                               print(f"vor ob_id {ob_id} rsa.optical_bands  {rsa.optical_bands[ob_id]}")
                            
                        return "flow {} deleted".format(flow_id), 200
                    else:
                        return "flow {} not matching".format(flow_id), 404
            else:
                return "flow id {} does not exist".format(flow_id), 404
   
            
         


@optical.route('/DelOpticalBand/<string:src>/<string:dst>/<int:o_band_id>',methods=['DELETE'])
@optical.response(200, 'Success')
@optical.response(404, 'Error, not found')
class DelOpticalBand(Resource):
    @staticmethod
    def delete( src, dst, o_band_id):
            flow = None

            ob_id=None
            if o_band_id is not None:            
            
                if o_band_id in  rsa.optical_bands.keys():
                    flow=rsa.optical_bands[o_band_id]
                    #match1 = flow["src"] == src and flow["dst"] == dst 
                    ob_id=o_band_id 
              
                if flow is not None:
                    bidir = flow["bidir"]
                    if bidir:
                        match1 = flow["src"] == src and flow["dst"] == dst and flow["bitrate"]
                        match2 = flow["src"] == dst and flow["dst"] == src and flow["bitrate"] 
                        if match1 or match2:
                            ob_id = flow["parent_opt_band"]
                            #rsa.del_flow(flow, ob_id)
                            rsa.optical_bands[ob_id]["is_active"] = False
                            # if flow_id in rsa.optical_bands[ob_id]["served_lightpaths"].remove:
                            #    rsa.optical_bands[ob_id]["served_lightpaths"].remove(flow_id)
                            #if rsa.optical_bands[ob_id]["reverse_optical_band_id"] != 0:
                            #    rev_ob_id = rsa.optical_bands[ob_id]["reverse_optical_band_id"]
                            #    rsa.optical_bands[rev_ob_id]["served_lightpaths"].remove(flow_id)

                            if debug:
                                print(rsa.links_dict)
                            return "ob_id {} deleted".format(ob_id), 200
                        else:
                            return "ob_id {} not matching".format(ob_id), 404
                    else:
                        if ob_id is not None:
                        
                            if len( rsa.optical_bands[ob_id]["served_lightpaths"]) != 0:
                                return "DELETE_NOT_ALLOWED" ,400

                        rsa.del_band(flow,ob_id)
                        if debug:
                            print(f"vor ob_id {ob_id} rsa.optical_bands  {rsa.optical_bands[ob_id]}")
                            print(f"rsa.links_dict {rsa.links_dict}")
                        return "ob_id {} deleted".format(ob_id), 200
                       
                else :
                    return "flow for ob_id {} not found".format(ob_id),400        
            else:
                return "ob_id  {} does not exist".format(ob_id), 404
   
            
         
@optical.route('/DelOpticalBandSimple/<int:o_band_id>',methods=['DELETE'])
@optical.response(200, 'Success')
@optical.response(404, 'Error, not found')
class DelOpticalBandSimple(Resource):
    @staticmethod
    def delete(o_band_id):
        flow = None
        ob_id=None
        if o_band_id is not None:            
            if o_band_id in  rsa.optical_bands.keys():
                flow=rsa.optical_bands[o_band_id]
                ob_id=o_band_id             
            if flow is not None:
                bidir = flow["bidir"]
                if bidir:
                    if len( rsa.optical_bands[ob_id]["served_lightpaths"]) != 0:
                        return "DELETE_NOT_ALLOWED" ,400
                    rsa.optical_bands[ob_id]["is_active"] = False
                    rsa.del_band(flow,ob_id)
                    if debug:
                        print(rsa.links_dict)
                    return "ob_id {} deleted".format(ob_id), 200
                else:
                    if len( rsa.optical_bands[ob_id]["served_lightpaths"]) != 0:
                        return "DELETE_NOT_ALLOWED" ,400
                    rsa.optical_bands[ob_id]["is_active"] = False
                    rsa.del_band(flow,ob_id)
                    if debug:
                        print(f"vor ob_id {ob_id} rsa.optical_bands  {rsa.optical_bands[ob_id]}")
                        print(f"rsa.links_dict {rsa.links_dict}")
                    return "ob_id {} deleted".format(ob_id), 200
                    
            else :
                return "flow for ob_id {} not found".format(ob_id),400        
        else:
            return "ob_id  {} does not exist".format(ob_id), 404
   




@optical.route('/DelLightpath/<string:src>/<string:dst>/<int:bitrate>/<int:flow_id>')
@optical.response(200, 'Success')
@optical.response(404, 'Error, not found')
class DelLightpath(Resource):
    @staticmethod
    def delete(flow_id, src, dst, bitrate):
        if flow_id in rsa.db_flows.keys():
            flow = rsa.db_flows[flow_id]
            match1 = flow["src"] == src and flow["dst"] == dst and flow["bitrate"] == bitrate
            match2 = flow["src"] == dst and flow["dst"] == src and flow["bitrate"] == bitrate
            if match1 or match2:
                rsa.del_flow(flow,flow_id)
                rsa.db_flows[flow_id]["is_active"] = False
                if debug:
                    print(rsa.links_dict)
                return "flow {} deleted".format(flow_id), 200
            else:
                return "flow {} not matching".format(flow_id), 404
        else:
            return "flow id {} does not exist".format(flow_id), 404


@optical.route('/GetLightpaths')
@optical.response(200, 'Success')
@optical.response(404, 'Error, not found')
class GetFlows(Resource):
    @staticmethod
    def get():
        try:
            if debug:
                print(rsa.db_flows)
            return rsa.db_flows, 200
        except:
            return "Error", 404

@optical.route('/GetOpticalBands')
@optical.response(200, 'Success')
@optical.response(404, 'Error, not found')
class GetBands(Resource):
    @staticmethod
    def get():
        try:
            if debug:
                print(rsa.optical_bands)
            return rsa.optical_bands, 200
        except:
            return "Error", 404


@optical.route('/GetOpticalBand/<int:ob_id>')
@optical.response(200, 'Success')
@optical.response(404, 'Error, not found')
class GetBand(Resource):
    @staticmethod
    def get(ob_id):
        for ob_idx in rsa.optical_bands.keys():
            if str(ob_idx) == str(ob_id):
                if debug:
                    print(rsa.optical_bands[ob_id])
                return rsa.optical_bands[ob_idx], 200
        return {}, 404


@optical.route('/GetLinks')
@optical.response(200, 'Success')
@optical.response(404, 'Error, not found')
class GetFlows(Resource):
    @staticmethod
    def get():
        global rsa
        #global links_dict
        links = None
        if rsa is not None :
           links = rsa.links_dict
        try:
            if debug:
                print(links)
            return links, 200
        except:
            return "Error", 404
        
                
@optical.route('/GetTopology/<path:context_id>/<path:topology_id>',methods=['GET'])
@optical.response(200, 'Success')
@optical.response(404, 'Error, not found')
class GetTopology(Resource):
    @staticmethod
    def get(context_id:str,topology_id:str):
        
        global rsa
    
        if (rsa is not None):
          
            return "Opticalcontroller is synchronised" ,200
        topog_id = TopologyId()
        topog_id.topology_uuid.uuid=topology_id
        topog_id.context_id.context_uuid.uuid=context_id
        
        try: 
            links_dict={"optical_links":[]}
            node_dict = {}
            topo , nodes = readTopologyDataFromContext(topog_id)

            OPTICAL_ROADM_TYPES = {
                DeviceTypeEnum.OPTICAL_ROADM.value, DeviceTypeEnum.EMULATED_OPTICAL_ROADM.value
            }
            OPTICAL_OPENROADM_TYPES = {
                DeviceTypeEnum.OPEN_ROADM.value, DeviceTypeEnum.EMULATED_OPEN_ROADM.value
            }
            OPTICAL_TRANSPONDER_TYPES = {
                DeviceTypeEnum.OPTICAL_TRANSPONDER.value, DeviceTypeEnum.EMULATED_OPTICAL_TRANSPONDER.value
            }
            added_device_uuids = set()
            for device in nodes:
                if device.device_type in OPTICAL_ROADM_TYPES:
                    dev_type = "OC-ROADM"
                elif device.device_type in OPTICAL_TRANSPONDER_TYPES:
                    dev_type = "OC-TP"
                elif  device.device_type in OPTICAL_OPENROADM_TYPES:
                    dev_type = "OC-ROADM"
                else:
                    continue

                dev_dic = {
                    "id":device.device_id.device_uuid.uuid,
                    #"ip":f"10.30.2.{207+i}",
                    #"port":"50001",
                    "type": dev_type,
                    "driver": "OpticalOC"
                }
                node_dict[device.name] = dev_dic
                added_device_uuids.add(device.device_id.device_uuid.uuid)
                #i+=1
                #print(f"refresh_optical controller optical_links_dict= {links_dict}")
                #print(f"refresh_optical controller node_dict  {node_dict}")
            
            for link in topo:
                endpoint_id_a = link.link_endpoint_ids[ 0]
                endpoint_id_z = link.link_endpoint_ids[-1]

                device_uuid_a = endpoint_id_a.device_id.device_uuid.uuid
                if device_uuid_a not in added_device_uuids: continue

                device_uuid_z = endpoint_id_z.device_id.device_uuid.uuid
                if device_uuid_z not in added_device_uuids: continue

                link_dict_type = MessageToDict(link, preserving_proto_field_name=True)
                
                if "c_slots" in link_dict_type["optical_details"] : 
                    link_dict_type["optical_details"]["c_slots"]=order_dict(link_dict_type["optical_details"]["c_slots"])
                    
                if "l_slots" in link_dict_type["optical_details"] : 
                    link_dict_type["optical_details"]["l_slots"]=order_dict(link_dict_type["optical_details"]["l_slots"])
                    
                if "s_slots" in link_dict_type["optical_details"] : 
                    link_dict_type["optical_details"]["s_slots"]=order_dict(link_dict_type["optical_details"]["s_slots"])
                    
                links_dict["optical_links"].append(link_dict_type)
    
            rsa = RSA(node_dict, links_dict)
            if debug:
                print(f'rsa.init_link_slots2() {rsa}')
                print(rsa.init_link_slots2())
        
        
            return  "ok" ,200
        except Exception as e:
            print(f"err {e}")
            return "Error", 400
    
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=10060, debug=True)
