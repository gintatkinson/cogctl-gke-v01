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

import numpy as np
from opticalcontroller.variables import  *
import json , logging
from context.client.ContextClient import ContextClient
from common.proto.context_pb2 import TopologyId , LinkId , OpticalLink , OpticalLinkDetails
from common.tools.object_factory.OpticalLink import correct_slot


def common_slots(a, b):
    return list(np.intersect1d(a, b))


def map_modulation_to_op(mod, rate):
    if mod == "DP-QPSK":
        return 1
    elif mod == "DP-8QAM":
        return 2
    elif mod == "DP-16QAM":
        if rate == 400:
            return 4
        elif rate == 800:
            return 8
        else:
            return 18
    elif mod == "DP-32QAM":
        return 10


def map_band_to_slot(band):
    return int(band/12.5)


def map_rate_to_slot(rate):
    if rate == 100:
        mod = "DP-QPSK"
        slots = 4
        op = map_modulation_to_op(mod, rate)
        return op, slots
    elif rate == 400:
        mod = "DP-8QAM"
        slots = 8 #100GHz
        op = map_modulation_to_op(mod, rate)
        return op, slots
    elif rate == 800:
        mod = "DP-16QAM"
        slots = 12 #150GHz
        op = map_modulation_to_op(mod, rate)
        return op, slots
    elif rate == 1000:
        mod = "DP-32QAM"
        slots = 18
        op = map_modulation_to_op(mod, rate)
        return op, slots
    else:
        return 2, 5


def consecutives(link, val):
    res = []
    temp = []
    x1 = list(link.keys())
    x = str_list_to_int(x1)
    x.sort()
    y = 0
    if debug:
        print("BLACK")
        print(link)
        print(x)
        print(x[0])
    if link[str(x[0])] == 1:
        temp.append(int(x[0]))
        y = 1
    for i in range(1, len(x)):
        if (int(x[i]) == int(x[i - 1]) + 1) and link[str(x[i])] == 1:
            y += 1
            temp.append(int(x[i]))
        else:
            if y >= val:
                res.extend(temp)
            if link[str(x[i])] == 1:
                temp = [int(x[i])]
                y = 1
            else:
                temp = []
                y = 0
        if i == len(x) - 1 and y >= val:
            res.extend(temp)
    return res


def combine(ls1, ls2):
    temp = ls1
    for i in ls2:
        if i not in ls1:
            temp.append(i)
    temp.sort()
    return temp


def str_list_to_int(str_list):
    int_list = []
    for i in str_list:
        int_list.append(int(i))
    int_list.sort()
    return int_list


def list_in_list(a, b):
    # convert list A to numpy array
    a_arr = np.array(a)
    # convert list B to numpy array
    b_arr = np.array(b)

    for i in range(len(b_arr)):
        if np.array_equal(a_arr, b_arr[i:i + len(a_arr)]):
            return True
    return False


def reverse_link(link):
    s, d = link.split('-')
    r_link = "{}-{}".format(d, s)
    return r_link


def get_slot_frequency(b, n):
    if debug:
        print(n)
    if b == "c_slots":
        return Fc + n * 12.5
    if b == "s_slots":
        return Fs + n * 12.5
    if b == "l_slots":
        return Fl + n * 12.5


def get_side_slots_on_link(link, val, old_slots):
    #link = l["optical_details"][band]
    x = list(old_slots.keys())
    y = list(link.keys())
    keys = str_list_to_int(x)
    keys.sort()
    #print("AAAA")
    #print(link, val, old_slots, keys)
    #print(x)
    starting_slot = keys[-1]
    num = 0
    res = []
    #print(starting_slot)
    for slot_id in range(starting_slot, len(y)):
        if link[y[slot_id]] == 1:
            num += 1
            res.append(int(y[slot_id]))
        else:
            return res, 0
        if num == val or slot_id == len(y) - 1:
            return res, num


def frequency_converter(b, slots):
    l = len(slots)
    if debug:
        print(slots)
    if l % 2 == 0:
        if debug:
            print("pari {}".format(l))
        fx = get_slot_frequency(b, slots[int(l / 2)-1])
        if debug:
            print(fx)
        #GHz
        # #f0 = fx + 6.25
        #MHz
        f0 = int((fx + 6.25) * 1000)
    else:
        f0 = get_slot_frequency(b, slots[int((l + 1) / 2) - 1])
    #GHz
    # #return f0, 12.5 * l
    # MHz
    return f0, int((12.5 * l) * 1000)


def readTopologyData(nodes, topology):
        
        
        nodes_file = open(nodes, 'r')
        topo_file = open(topology, 'r')
        nodes = json.load(nodes_file)
        topo = json.load(topo_file)
        #print(topo)
        nodes_file.close()
        topo_file.close()
        return nodes, topo

    
def readTopologyDataFromContext(topology_id:TopologyId): 
    ctx_client = ContextClient()
    ctx_client.connect()
    topo_details = ctx_client.GetTopologyDetails(topology_id)
    topo = topo_details.optical_links
    nodes = topo_details.devices
    ctx_client.close()
    return topo , nodes


def reverse_links(links):
    temp_links = links.copy()
    temp_links.reverse()
    result = []
    for link in temp_links:
        [a, b] = link.split("-")
        result.append("{}-{}".format(b, a))
    return result


def get_links_from_node(topology, node):
    result = {}
    for link in topology["optical_links"]:
        if "{}-".format(node) in link["name"]:
            result[link["name"]] = link
    return result


def get_links_to_node(topology, node):
    result = {}
    for link in topology["optical_links"]:
        if "-{}".format(node) in link["name"]:
            result[link["name"]] = link
    return result


def slot_selection(c, l, s, n_slots, Nc, Nl, Ns):
    # First Fit
    
    if isinstance(n_slots, int):
        slot_c = n_slots
        slot_l = n_slots
        slot_s = n_slots
    else:
        slot_c = Nc
        slot_l = Nl
        slot_s = Ns
    if len(c) >= slot_c:
        return "c_slots", c[0: slot_c]
    elif len(l) >= slot_l:
        return "l_slots", l[0: slot_l]
    elif len(s) >= slot_s:
        return "s_slots", s[0: slot_s]
    else:
        return None, None

def handle_slot (slot_field, slot):
    for key,value in slot.items() :
        slot_field[key]=value


      
def update_optical_band (optical_bands,optical_band_id,band,link):
    key_list = optical_bands[optical_band_id][band].keys()
    corrected_slots=optical_bands[optical_band_id][band]
    if (len(key_list) < 20):
        corrected_slots=correct_slot(optical_bands[optical_band_id][band])
        
    fib={}
    fib['c_slots']=link['optical_details']['c_slots']
    fib['l_slots']=link['optical_details']['l_slots']
    fib['s_slots']=link['optical_details']['s_slots']
      
    fib[band]=corrected_slots
    fib["src_port"]=optical_bands[optical_band_id]['src_port']
    fib["dst_port"]=optical_bands[optical_band_id]['dst_port']
    fib["local_peer_port"]=link["optical_details"]["local_peer_port"]
    fib["remote_peer_port"]=link["optical_details"]["remote_peer_port"]
    set_link_update(fib,link,test=f"restoring_optical_band {link['link_id']}")
    
def set_link_update (fib:dict,link:dict,test="updating"):
    #print(link)
    print(f"invoked from {test}")
    print(f"fib updated {fib}")  
    optical_link = OpticalLink()
    linkId = LinkId()
    #linkId.link_uuid.uuid=link["link_id"]["link_uuid"]["uuid"]
    linkId.link_uuid.uuid=link["link_id"]["link_uuid"]["uuid"]
    optical_details = OpticalLinkDetails()
    optical_link.optical_details.length=0
    if "src_port" in fib :
       optical_link.optical_details.src_port=fib["src_port"]
    if "dst_port" in fib :   
       optical_link.optical_details.dst_port=fib["dst_port"]
    if "local_peer_port" in fib :   
       optical_link.optical_details.local_peer_port=fib['local_peer_port']
    if "remote_peer_port" in fib:   
       optical_link.optical_details.remote_peer_port=fib['remote_peer_port']
       
    optical_link.optical_details.used=fib['used'] if 'used' in fib else False
    if "c_slots" in fib :
        
        handle_slot( optical_link.optical_details.c_slots,fib["c_slots"])
    if "s_slots" in fib :
             
       handle_slot( optical_link.optical_details.s_slots,fib["s_slots"])
    if "l_slots" in fib :
           
       handle_slot( optical_link.optical_details.l_slots,fib["l_slots"])

    
    optical_link.name=link['name']
  
    optical_link.link_id.CopyFrom(linkId)
    
    ctx_client = ContextClient()
    ctx_client.connect()
    try:
        ctx_client.SetOpticalLink(optical_link)
    except Exception as err:
        print (f"setOpticalLink {err}")    



