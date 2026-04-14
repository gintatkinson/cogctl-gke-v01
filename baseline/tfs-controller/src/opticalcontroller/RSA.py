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

import logging
from opticalcontroller.dijkstra import *
from opticalcontroller.tools import *
from opticalcontroller.variables import *

LOGGER = logging.getLogger(__name__)

def print(*args) -> None:
    LOGGER.info(' '.join([str(a) for a in args]))

class RSA():
    def __init__(self, nodes, links):
        self.nodes_dict = nodes
        self.links_dict = links
        self.g = None

        self.flow_id = 0
        self.opt_band_id = 0
        self.db_flows = {}
        self.initGraph2()
        self.c_slot_number = 0
        self.l_slot_number = 0
        self.s_slot_number = 0
        self.optical_bands = {}
       
        
    def init_link_slots(self, testing):
        if full_links:
            for l in self.links_dict["optical_links"]:
                for fib in l["optical_link"]["details"]["fibers"]:
                    #fib = self.links_dict[l]["fibers"][f]
                    if len(fib["c_slots"]) > 0:
                        fib["c_slots"] = list(range(0, Nc))
                    if len(fib["l_slots"]) > 0:
                        fib["l_slots"] = list(range(0, Nl))
                    if len(fib["s_slots"]) > 0:
                        fib["s_slots"] = list(range(0, Ns))
                    if debug:
                        print(fib)
        for l1 in self.links_dict["optical_links"]:

            for fib1 in l1["optical_link"]["details"]["fibers"]:
                #fib1 = self.links_dict[l1]["details"]["fibers"][f1]

                self.c_slot_number = len(fib1["c_slots"])
                self.l_slot_number = len(fib1["l_slots"])
                self.s_slot_number = len(fib1["s_slots"])

                break
            break
        return "{},{},{}".format(self.c_slot_number, self.l_slot_number, self.s_slot_number)

    def init_link_slots2(self):
        if full_links:
            for l in self.links_dict["optical_links"]:
                fib = l["optical_details"]
                #fib = self.links_dict[l]["fibers"][f]
                if len(fib["c_slots"]) > 0:
                    for c in range(0, Nc):
                        fib["c_slots"][c] = 1
                if len(fib["l_slots"]) > 0:
                    for c in range(0, Nl):
                        fib["l_slots"][c] = 1
                if len(fib["s_slots"]) > 0:
                    for c in range(0, Ns):
                        fib["s_slots"][c] = 1
                if debug:
                    print(fib)
        for l1 in self.links_dict["optical_links"]:
            fib1 = l1["optical_details"]
            self.c_slot_number = len(fib1["c_slots"].keys())
            self.l_slot_number = len(fib1["l_slots"].keys())
            self.s_slot_number = len(fib1["s_slots"].keys())
            break
        return "{},{},{}".format(self.c_slot_number, self.l_slot_number, self.s_slot_number)

    def initGraph(self):
        self.g = Graph()
        for n in self.nodes_dict:
            self.g.add_vertex(n)
        for l in self.links_dict["optical_links"]:
            if debug:
                print(l)
            [s, d] = l["optical_link"]["name"].split('-')
            ps = l["optical_link"]["details"]["source"]
            pd = l["optical_link"]["details"]["target"]
            self.g.add_edge(s, d, ps, pd, 1)

        print("INFO: Graph initiated.")
        if debug:
            self.g.printGraph()

    def initGraph2(self):
     
        self.g = Graph()
     
        for n in self.nodes_dict:
            self.g.add_vertex(n)
        for l in self.links_dict["optical_links"]:
            if debug:
                print(l)
            [s, d] = l["name"].split('-')
            ps = l["optical_details"]["src_port"]
            pd = l["optical_details"]["dst_port"]
            self.g.add_edge(s, d, ps, pd, 1)

        print("INFO: Graph initiated.2")
        if debug:
            self.g.printGraph()

    def compute_path(self, src, dst):
        path = shortest_path(self.g, self.g.get_vertex(src), self.g.get_vertex(dst))
        print("INFO: Path from {} to {} with distance: {}".format(src, dst, self.g.get_vertex(dst).get_distance()))
        if debug:
            print(f"compute_path shortest_path {path}")
        links = []
        for i in range(0, len(path) - 1):
            s = path[i]
            if debug:
                print(s)
            if i < len(path) - 1:
                d = path[i + 1]
                link_id = "{}-{}".format(s, d)
                if debug:
                    #print(link_id, self.links_dict[link_id])
                    print(link_id, self.get_link_by_name(link_id))

                links.append(link_id)
        self.g.reset_graph()
        return links, path

    def get_slots(self, links, slots, optical_band_id=None):

        if isinstance(slots, int):
            val_c = slots
            val_s = slots
            val_l = slots
        else:
            val_c = self.c_slot_number
            val_l = self.l_slot_number
            val_s = self.s_slot_number

        c_sts = []
        l_sts = []
        s_sts = []
        c_slots = {}
        l_slots = {}
        s_slots = {}
        add = ""
        drop = ""
        src_1, dst_1 = links[0].split('-')
        src_2, dst_2 = links[-1].split('-')
        if self.nodes_dict[src_1]["type"] == "OC-TP":
            add = links[0]
        if self.nodes_dict[dst_2]["type"] == "OC-TP":
            drop = links[-1]
        found = 0
        for l in links:
            c_slots[l] = []
            l_slots[l] = []
            s_slots[l] = []

            link = self.get_link_by_name(l)
            fib = link["optical_details"]
            if l == add:
                if 'used' in fib:
                    if fib["used"]:
                        #if debug:
                        print("WARNING!!!: link {}, is already in use".format(l))
                        return [], [], []
            if l == drop:
                if 'used' in fib:
                    if fib["used"]:
                        #if debug:
                        print("WARNING!!!: link {} is already in use".format(l))
                        return [], [], []
            c_found = l_found = s_found = 0
            if len(fib["c_slots"].keys()) > 0:
                #c_slots[l] = combine(c_slots[l], consecutives(fib["c_slots"], val_c))
                c_slots[l] = combine(c_slots[l], consecutives(fib["c_slots"], val_c))
                c_found = 1
            if len(fib["l_slots"].keys()) > 0:
                l_slots[l] = combine(l_slots[l], consecutives(fib["l_slots"], val_l))
                l_found = 1
            if len(fib["s_slots"].keys()) > 0:
                s_slots[l] = combine(s_slots[l], consecutives(fib["s_slots"], val_s))
                s_found = 1
            if debug:
                print(l, c_slots[l])
            if c_found == 0 and l_found == 0 and s_found == 0:
                return [], [], []

        keys = list(c_slots.keys())
        if debug:
            print(len(keys))
        if debug:
            print(keys[0])
        # intersection among the slots over all links
        if len(keys) == 1:
            c_sts = c_slots[keys[0]]
            l_sts = l_slots[keys[0]]
            s_sts = s_slots[keys[0]]
        else:
            for i in range(1, len(keys)):
                if debug:
                    print(keys[i])
                # set a for the intersection
                if i == 1:
                    a_c = c_slots[keys[i - 1]]
                    a_l = l_slots[keys[i - 1]]
                    a_s = s_slots[keys[i - 1]]
                else:
                    a_c = c_sts
                    a_l = l_sts
                    a_s = s_sts
                # set b for the intersection
                b_c = c_slots[keys[i]]
                b_l = l_slots[keys[i]]
                b_s = s_slots[keys[i]]

                c_sts = common_slots(a_c, b_c)
                l_sts = common_slots(a_l, b_l)
                s_sts = common_slots(a_s, b_s)
                '''
             if len(fib["l_slots"]) > 0:
                l_slots[l] = combine(l_slots[l], consecutives(fib["l_slots"], val_l))
                l_found = 1'''
        if optical_band_id is not None:
            if "c_slots" in self.optical_bands[optical_band_id].keys():
                if len(self.optical_bands[optical_band_id]["c_slots"]) > 0:
                    a_c = c_sts
                    #MOD
                    b_c = consecutives(self.optical_bands[optical_band_id]["c_slots"], val_c)
                    #b_c = self.optical_bands[optical_band_id]["c_slots"]
                    c_sts = common_slots(a_c, b_c)
            else:
                c_sts = []
            if "l_slots" in self.optical_bands[optical_band_id].keys():
                if len(self.optical_bands[optical_band_id]["l_slots"]) > 0:
                    a_l = l_sts
                    b_l = consecutives(self.optical_bands[optical_band_id]["l_slots"], val_c)
                    l_sts = common_slots(a_l, b_l)
            else:
                l_sts = []
            if "s_slots" in self.optical_bands[optical_band_id].keys():
                if len(self.optical_bands[optical_band_id]["s_slots"]) > 0:
                    a_s = s_sts
                    b_s = consecutives(str_list_to_int(self.optical_bands[optical_band_id]["s_slots"].keys()), val_c)
                    s_sts = common_slots(a_s, b_s)
            else:
                s_sts = []

        return c_sts, l_sts, s_sts

    def update_link(self, fib, slots, band):
        #print(fib)
        for i in slots:
            fib[band][str(i)] = 0
        if 'used' in fib:
            fib['used'] = True
        print(f"fib updated {fib}")    
        #print(fib)
        
    def update_link_2(self, fib, slots, band,link):
        #print(fib)
        for i in slots:
            fib[band][str(i)] = 0
        if 'used' in fib:
            fib['used'] = True
      
        set_link_update(fib,link)  
        #print(fib)    

    def update_optical_band(self, optical_band_id, slots, band):
        for i in slots:
            self.optical_bands[optical_band_id][band][str(i)] = 0

    def augment_optical_band(self, optical_band_id, slots, band):
        for i in slots:
            self.optical_bands[optical_band_id][band][str(i)] = 1

    def restore_link(self, fib, slots, band):
        for i in slots:
            fib[band][str(i)] = 1
        if 'used' in fib:
            fib['used'] = False
        #fib[band].sort()
        
    # def restore_link_2(self, fib, slots, band, link):
    #     print("start restoring link")
    #     for i in slots:
    #         fib[band][str(i)] = 1
    #     if 'used' in fib:
    #         fib['used'] = False
    #     #fib[band].keys().sort()    
    #    #set_link_update(fib,link,test="restoration")     

    def restore_optical_band(self, optical_band_id, slots, band):

        for i in slots:
            self.optical_bands[optical_band_id][band][str(i)] = 1
            
            #self.optical_bands[optical_band_id][band].append(int(i))
            #self.optical_bands[optical_band_id][band].sort()
        
    def restore_optical_band_2(self, optical_band_id, slots, band ,links):
        print(f"example of  band { band}")
        print(f"example of slots {slots}")
        print(f"example of self.optical_bands_before { self.optical_bands}")
        for i in slots:
            self.optical_bands[optical_band_id][band][str(i)] = 1
        print(f"example of self.optical_bands_after { self.optical_bands}")    
       
        #link_name=    self.optical_bands[optical_band_id]['links'][0] 
        #link = self.get_link_by_name(link_name)    
        #update_optical_band(optical_bands=self.optical_bands,optical_band_id=optical_band_id,band=band,link=link)
        
            
    def del_flow(self, flow,flow_id, o_b_id = None):
        flows = flow["flows"]
        band = flow["band_type"]
        slots = flow["slots"]
        fiber_f = flow["fiber_forward"]
        fiber_b = flow["fiber_backward"]
        op = flow["op-mode"]
        n_slots = flow["n_slots"]
        path = flow["path"]
        links = flow["links"]
        bidir = flow["bidir"]
        flow_id = flow["flow_id"]


        for l in links:
            if debug:
                print(l)
            #link = self.links_dict[l]
            #f = fiber_f[l]
            #fib = link['fibers'][f]
            link = self.get_link_by_name(l)
            fib = link["optical_details"]
            #self.restore_link(fib, slots, band)
            self.restore_link(fib, slots, band)
            if debug:
                print(f"fib[band] {fib[band]}")
        if o_b_id is not None: 
            if debug:
                print("restoring OB")
            print(f"invoking restore_optical_band o_b_id: {o_b_id} , slots {slots} , band {band} ")    
            self.restore_optical_band(o_b_id, slots, band)
            if flow_id in self.optical_bands[o_b_id]["served_lightpaths"]:
                if flow_id in self.optical_bands[o_b_id]["served_lightpaths"]:
                    self.optical_bands[o_b_id]["served_lightpaths"].remove(flow_id)

            #self.restore_optical_band_2(o_b_id, slots, band,links)
        if bidir:
            for l in links:
                r_l = reverse_link(l)
                if debug:
                    print(f"reverse_link {r_l}")
                rlink = self.get_link_by_name(r_l)
                fib = rlink["optical_details"]
                #fib = self.get_link_by_name(r_l)["optical_details"]
                if list_in_list(slots, str_list_to_int(fib[band].keys())):
                    #self.restore_link(fib, slots, band, link=l)
                    self.restore_link(fib, slots, band)
                    if debug:
                        print(fib[band])
            '''
            for rl in fiber_b.keys():
                if debug:
                    print(rl)
                    print(fiber_b[rl])
                #rlink = self.links_dict[rl]
                #rf = fiber_b[rl]
                #rfib = rlink['fibers'][rf]
                rfib = self.get_fiber_details(rl, fiber_b[rl])
                if not list_in_list(slots, rfib[band]):
                    self.restore_link(rfib, slots, band)
                    if debug:
                        print(rfib[band])
            '''
            #changed according to TFS development
            #if o_b_id is not None:
            #    rev_o_band_id = self.optical_bands[o_b_id]["reverse_optical_band_id"]
            #    self.restore_optical_band(rev_o_band_id, slots, band)
        return True
    
    
    def del_band(self, flow, o_b_id = None):
        
        print(f"delete band {flow} ")
        flows = flow["flows"]
        band = None
        #slots = flow["slots"]
        fiber_f = flow["fiber_forward"]
        fiber_b = flow["fiber_backward"]
        op = flow["op-mode"]
        n_slots = 0
        path = flow["path"]
        bidir = flow["bidir"]
        links =  []
        slots = []
        if o_b_id is not None:
            links= self.optical_bands[o_b_id]["links"]
            band = self.optical_bands[o_b_id]["band_type"]
            n_slots =self.optical_bands[o_b_id]["n_slots"]
            if isinstance(n_slots, str):
                if n_slots == "full_band":
                    for key in self.optical_bands[o_b_id][band].keys():
                        slots.append(int(key))
                    slots.sort()
            elif isinstance(n_slots, int):
                if n_slots > 0:
                    #slots=[i+1 for i in range(n_slots)]
                    for key in self.optical_bands[o_b_id][band].keys():
                        slots.append(int(key))
                        slots.sort()  
            for l in links:
                if debug:
                    print(l)
                #fib = self.get_link_by_name(l)["optical_details"]
                link = self.get_link_by_name(l)
                fib = link["optical_details"]
                print(f"del_flow_fib {fib } and band {band}")
                print(f"del_flow { str_list_to_int(fib[band].keys())}")
            
                print(f"invoking restore_link_2 fib: {fib} , slots {slots} , band {band} ")
                #self.restore_link(fib, slots, band)
                self.restore_link_2(fib, slots, band, link = link)
                
                self.optical_bands[o_b_id]["is_active"]=False
            
                if debug:
                    print(fib[band])          
            if debug:
                print("restoring OB")
            print(f"invoking restore_optical_band o_b_id: {o_b_id} , slots {slots} , band {band} ")    
            self.restore_optical_band(o_b_id, slots, band)
            #self.restore_optical_band_2(o_b_id, slots, band,links)
            if bidir:
                for l in links:
                    r_l = reverse_link(l)
                    if debug:
                        print(r_l)
                    rlink = self.get_link_by_name(r_l)
                    fib = rlink["optical_details"]
                    #fib = self.get_link_by_name(r_l)["optical_details"]
                    if list_in_list(slots, str_list_to_int(fib[band].keys())):
                        self.restore_link_2(fib, slots, band, link=rlink)
                        if debug:
                            print(fib[band])
                #changed according to TFS development
                #if o_b_id is not None:
                #    rev_o_band_id = self.optical_bands[o_b_id]["reverse_optical_band_id"]
                #    self.restore_optical_band(rev_o_band_id, slots, band)
        return True
    
    
    def del_handler(self, flow,flow_id, o_b_id = None,delete_band=0):
        print(f" del_handler flow {flow} flow_id {flow_id}  o_b_id {o_b_id} delete_band {delete_band}")
        if delete_band != 0:
            print(f"delete band del_band")
            self.del_band(flow,flow_id,o_b_id=o_b_id)
        else :
            self.del_flow(flow,flow_id=flow_id,o_b_id=o_b_id)   
            
            
             
    def get_fibers_forward(self, links, slots, band):
        fiber_list = {}
        add = links[0]
        drop = links[-1]
        #print(links)
        '''
        for link in self.links_dict["links"]:
            if link["optical_link"]["name"] == l:
                # for f in self.links_dict[l]['fibers'].keys():
                for fib in link["optical_link"]["details"]["fibers"]:

        '''
        for l in links:
            for link in self.links_dict["optical_links"]:
                print(f"tracking link info {link}")    
                if link["name"] == l:
                    fib = link["optical_details"]
                    #for f in self.links_dict[l]['fibers'].keys():
                    #for fib in l["optical_link"]["details"]["fibers"]:
                    #fib = self.links_dict[l]['fibers'][f]
                    if l == add:
                        if 'used' in fib:
                            if fib["used"]:
                                if debug:
                                    print("link {} is already in use".format(l))
                                continue
                    if l == drop:
                        if 'used' in fib:
                            if fib["used"]:
                                if debug:
                                    print("link {} is already in use".format(l))
                                continue
                    if list_in_list(slots, str_list_to_int(fib[band].keys())):
                        #fiber_list[l] = fib["ID"]
                        #self.update_link(fib, slots, band)
                        self.update_link_2(fib,slots,band,link)
                        break
        print("INFO: Path forward computation completed")
        return fiber_list

    def get_link_by_name (self, key):
        for link in self.links_dict["optical_links"]:
            if link["name"] == key:
                if debug:
                    print(link)
                break
        return link

    def get_fiber_details(self, link_key, fiber_id):
        for link in self.links_dict["optical_links"]:
            if link["name"] == link_key:
                if debug:
                    print(link)
                for fib in link["optical_details"]:
                    if fib["ID"] == fiber_id:
                        return fib
        return None

    def get_fibers_backward(self, links, slots, band):
        fiber_list = {}
        #r_drop = reverse_link(links[0])
        #r_add = reverse_link(links[-1])
        for l in links:
            fib = self.get_link_by_name(l)["optical_details"]
            '''
            link = self.get_link_by_name(l)
            #port = self.links_dict[l]["fibers"][fibers[l]]["src_port"]
            for fib in link["optical_link"]["details"]["fibers"]:
                if fib["ID"] == fibers[l]:
            '''
            s_port = fib["src_port"]
            d_port = fib["dst_port"]

            if debug:
                print(l, s_port, d_port)

            r_l = reverse_link(l)
            r_link = self.get_link_by_name(r_l)
            if debug:
                print(r_l)

            #for f in r_link["fibers"].keys():
            r_fib = r_link["optical_details"]
            if r_fib["remote_peer_port"] == s_port and r_fib["local_peer_port"] == d_port:
                if list_in_list(slots, str_list_to_int(r_fib[band].keys())):
                    #fiber_list[r_l] = r_fib["ID"]
                    self.update_link(r_fib, slots, band)
        print("INFO: Path backward computation completed")
        return fiber_list

    #function invoked for lightpaths and OB
    def select_slots_and_ports(self, links, n_slots, c, l, s, bidir):
        if debug:
            print (links, n_slots, c, l, s, bidir, self.c_slot_number, self.l_slot_number, self.s_slot_number)
        band, slots = slot_selection(c, l, s, n_slots, self.c_slot_number, self.l_slot_number, self.s_slot_number)
        if debug:
            print (band, slots)
        if band is None:
            print("No slots available in the three bands")
            #return None, None, None, {}, {}
            return None, None, None, {}, {}
        
        self.get_fibers_forward(links, slots, band)
        if bidir:
            self.get_fibers_backward(links, slots, band)
        add = links[0]
        drop = links[-1]
        inport = "0"
        outport = "0"
        r_inport = "0"
        r_outport = "0"
        t_flows = {}
        #if len(links) == 1:

        for llx in links:
            if llx == add:
                inport = "0"
                r_outport = "0"
            if llx == drop:
                outport = "0"
                r_inport = "0"
            '''
            f = fibers_f[lx]
            
            fibx = self.get_fiber_details(lx, f)
            '''
            src, dst = llx.split("-")
            #outport = self.links_dict[lx]['fibers'][f]["src_port"]
            lx = self.get_link_by_name(llx)["optical_details"]
            outport = lx["src_port"]

            t_flows[src] = {}
            t_flows[src]["f"] = {}
            t_flows[src]["b"] = {}
            t_flows[src]["f"] = {"in": inport, "out": outport}

            if bidir:
                #r_inport = self.links_dict[lx]['fibers'][f]["local_peer_port"]
                r_inport = lx["local_peer_port"]
                t_flows[src]["b"] = {"in": r_inport, "out": r_outport}

            #inport = self.links_dict[lx]['fibers'][f]["dst_port"]
            inport = lx["dst_port"]
            if bidir:
                #r_outport = self.links_dict[lx]['fibers'][f]["remote_peer_port"]
                r_outport = lx["remote_peer_port"]
            t_flows[dst] = {}
            t_flows[dst]["f"] = {}
            t_flows[dst]["b"] = {}
            t_flows[dst]["f"] = {"in": inport, "out": "0"}
            if bidir:
                t_flows[dst]["b"] = {"in": "0", "out": r_outport}

        if debug:
            print(self.links_dict)

        if debug:
            print(t_flows)
        print("INFO: Flow matrix computed")

        return t_flows, band, slots, {}, {}

    #function ivoked for fs lightpaths only
    def select_slots_and_ports_fs(self, links, n_slots, c, l, s, bidir, o_band_id):
        if debug:
            print(self.links_dict)
        band, slots = slot_selection(c, l, s, n_slots, self.c_slot_number, self.l_slot_number, self.s_slot_number)
        if band is None:
            print("No slots available in the three bands")
            return None, None, None, None, None
        if debug:
            print(band, slots)
        self.get_fibers_forward(links, slots, band)
        if bidir:
            self.get_fibers_backward(links, slots, band)

        #fibers_f = self.get_fibers_forward(links, slots, band)
        self.update_optical_band(o_band_id, slots, band)
        #fibers_b = []
        #if bidir:
        #    fibers_b = self.get_fibers_backward(links, fibers_f, slots, band)
        '''

            rev_o_band_id = self.optical_bands[o_band_id]["reverse_optical_band_id"]
            self.update_optical_band(rev_o_band_id, slots, band)
        '''
        add = links[0]
        drop = links[-1]
        port_0 = "0"

        t_flows = {}

        #flows_add_side
        src, dst = add.split("-")
        lx = self.get_link_by_name(add)["optical_details"]
        #outport = self.links_dict[add]['fibers'][f]["src_port"]
        outport = lx["src_port"]
        #T1 rules
        t_flows[src] = {}
        t_flows[src]["f"] = {}
        t_flows[src]["b"] = {}
        t_flows[src]["f"] = {"in": port_0, "out": outport}
        if bidir:
            #r_inport = self.links_dict[add]['fibers'][f]["local_peer_port"]
            r_inport = lx["local_peer_port"]
            t_flows[src]["b"] = {"in": r_inport, "out": port_0}

        #R1 rules
        t_flows[dst] = {}
        t_flows[dst]["f"] = {}
        t_flows[dst]["b"] = {}
        #inport = self.links_dict[add]['fibers'][f]["dst_port"]
        inport = lx["dst_port"]
        opt_band_src_port = self.optical_bands[o_band_id]["src_port"]
        t_flows[dst]["f"] = {"in": inport, "out": opt_band_src_port}
        #to modify to peer ports
        if bidir:
            #r_inport = self.links_dict[add]['fibers'][f]["local_peer_port"]
            r_inport = lx["local_peer_port"]
            t_flows[src]["b"] = {"in": r_inport, "out": port_0}
        if bidir:
            rev_opt_band_dst_port = self.optical_bands[o_band_id]["rev_dst_port"]
            #r_outport = self.links_dict[add]['fibers'][f]["remote_peer_port"]
            r_outport = lx["remote_peer_port"]
            t_flows[dst]["b"] = {"in": rev_opt_band_dst_port, "out": r_outport}

        #flows_drop_side
        # R2 rules
        ly = self.get_link_by_name(drop)["optical_details"]
        src, dst = drop.split("-")
        #outport = self.links_dict[drop]['fibers'][f]["src_port"]
        outport = ly["src_port"]

        t_flows[src] = {}
        t_flows[src]["f"] = {}
        t_flows[src]["b"] = {}
        opt_band_dst_port = self.optical_bands[o_band_id]["dst_port"]
        t_flows[src]["f"] = {"in": opt_band_dst_port, "out": outport}
        if bidir:
            rev_opt_band_src_port = self.optical_bands[o_band_id]["rev_src_port"]
            #r_inport = self.links_dict[drop]['fibers'][f]["local_peer_port"]
            r_inport = ly["local_peer_port"]
            t_flows[src]["b"] = {"in": r_inport, "out": rev_opt_band_src_port}
        t_flows[dst] = {}
        t_flows[dst]["f"] = {}
        t_flows[dst]["b"] = {}
        #inport = self.links_dict[drop]['fibers'][f]["dst_port"]
        inport = ly["dst_port"]
        t_flows[dst]["f"] = {"in": inport, "out": port_0}
        if bidir:
            #r_inport = self.links_dict[drop]['fibers'][f]["remote_peer_port"]
            r_inport = ly["remote_peer_port"]
            t_flows[dst]["b"] = {"in": port_0, "out": r_inport}

        if debug:
            print(self.links_dict)

        if debug:
            print(t_flows)
        print("INFO: Flow matrix computed for Flex Lightpath")

        return t_flows, band, slots, {}, {}

    def rsa_computation(self, src, dst, rate, bidir):
        if self.flow_id == 0:
            self.flow_id += 1
        else:
            if (self.db_flows[self.flow_id]["bidir"] == 1):
                self.flow_id += 2
            else:
                self.flow_id += 1
        self.db_flows[self.flow_id] = {}
        self.db_flows[self.flow_id]["flow_id"] = self.flow_id
        self.db_flows[self.flow_id]["src"] = src
        self.db_flows[self.flow_id]["dst"] = dst
        self.db_flows[self.flow_id]["bitrate"] = rate
        self.db_flows[self.flow_id]["bidir"] = bidir

        links, path = self.compute_path(src, dst)

        if len(path) < 1:
            self.null_values(self.flow_id)
            return self.flow_id
        op, num_slots = map_rate_to_slot(rate)
        c_slots, l_slots, s_slots = self.get_slots(links, num_slots)
        if debug:
            print(c_slots)
            print(l_slots)
            print(s_slots)
        if len(c_slots) > 0 or len(l_slots) > 0 or len(s_slots) > 0:
            flow_list, band_range, slots, fiber_f, fiber_b = self.select_slots_and_ports(links, num_slots, c_slots,
                                                                                         l_slots, s_slots, bidir)
            f0, band = frequency_converter(band_range, slots)
            if debug:
                print(f0, band)
            print("INFO: RSA completed for normal wavelenght connection")
            if flow_list is None:
                self.null_values(self.flow_id)
                return self.flow_id
            slots_i = []
            for i in slots:
                slots_i.append(int(i))
            # return links, path, flow_list, band_range, slots, fiber_f, fiber_b, op, num_slots, f0, band
            #        links, path, flows, bx, slots, fiber_f, fiber_b, op, n_slots, f0, band
            self.db_flows[self.flow_id]["flows"] = flow_list
            self.db_flows[self.flow_id]["band_type"] = band_range
            self.db_flows[self.flow_id]["slots"] = slots_i
            self.db_flows[self.flow_id]["fiber_forward"] = fiber_f
            self.db_flows[self.flow_id]["fiber_backward"] = fiber_b
            self.db_flows[self.flow_id]["op-mode"] = op
            self.db_flows[self.flow_id]["n_slots"] = num_slots
            self.db_flows[self.flow_id]["links"] = links
            self.db_flows[self.flow_id]["path"] = path
            self.db_flows[self.flow_id]["band"] = band
            self.db_flows[self.flow_id]["freq"] = f0
            self.db_flows[self.flow_id]["is_active"] = True
        return self.flow_id

    def null_values(self, flow_id):
        self.db_flows[flow_id]["flows"] = {}
        self.db_flows[flow_id]["band_type"] = ""
        self.db_flows[flow_id]["slots"] = []
        self.db_flows[flow_id]["fiber_forward"] = []
        self.db_flows[flow_id]["fiber_backward"] = []
        self.db_flows[flow_id]["op-mode"] = 0
        self.db_flows[flow_id]["n_slots"] = 0
        self.db_flows[flow_id]["links"] = {}
        self.db_flows[flow_id]["path"] = []
        self.db_flows[flow_id]["band"] = 0
        self.db_flows[flow_id]["freq"] = 0
        self.db_flows[flow_id]["is_active"] = False

    def null_values_ob(self, ob_id):
        self.optical_bands[ob_id]["flows"] = {}
        self.optical_bands[ob_id]["band_type"] = ""
        #self.optical_bands[ob_id]["slots"] = []
        self.optical_bands[ob_id]["fiber_forward"] = []
        self.optical_bands[ob_id]["n_slots"] = 0
        self.optical_bands[ob_id]["links"] = {}
        self.optical_bands[ob_id]["path"] = []
        self.optical_bands[ob_id]["band"] = 0
        self.optical_bands[ob_id]["freq"] = 0
        self.optical_bands[ob_id]["is_active"] = False
        self.optical_bands[ob_id]["c_slots"] = []
        self.optical_bands[ob_id]["l_slots"] = []
        self.optical_bands[ob_id]["s_slots"] = []
        self.optical_bands[ob_id]["served_lightpaths"] = []
        self.optical_bands[ob_id]["reverse_optical_band_id"] = 0
        self.db_flows[self.flow_id]["parent_opt_band"] = 0
        self.db_flows[self.flow_id]["new_optical_band"] = 0

    def create_optical_band(self, links, path, bidir, num_slots):
        print("INFO: Creating optical-band of {} slots".format(num_slots))
        if self.opt_band_id == 0:
            self.opt_band_id += 1
        else:
            if (self.optical_bands[self.opt_band_id]["bidir"] == 1):
                self.opt_band_id += 2
            else:
                self.opt_band_id += 1
        forw_opt_band_id = self.opt_band_id
        self.optical_bands[forw_opt_band_id] = {}
        self.optical_bands[forw_opt_band_id]["optical_band_id"] = forw_opt_band_id
        self.optical_bands[forw_opt_band_id]["bidir"] = bidir
        '''
        back_opt_band_id = 0
        if bidir:
            self.opt_band_id += 1
            back_opt_band_id = self.opt_band_id
            self.optical_bands[back_opt_band_id] = {}
            self.optical_bands[back_opt_band_id]["optical_band_id"] = back_opt_band_id
            self.optical_bands[back_opt_band_id]["bidir"] = bidir
            self.optical_bands[back_opt_band_id]["reverse_optical_band_id"] = forw_opt_band_id
            self.optical_bands[forw_opt_band_id]["reverse_optical_band_id"] = back_opt_band_id
        else:
            self.optical_bands[forw_opt_band_id]["reverse_optical_band_id"] = 0
        '''
        op = 0
        temp_links = []
        #num_slots = "all"
        if self.nodes_dict[path[0]]["type"] == "OC-TP":
            add_link = links[0]
            temp_links.append(add_link)
            links.remove(add_link)
            path.remove(path[0])
        self.optical_bands[forw_opt_band_id]["src"] = path[0]
        '''
        if bidir:
            self.optical_bands[back_opt_band_id]["dst"] = path[0]
        '''
        if self.nodes_dict[path[-1]]["type"] == "OC-TP":
            drop_link = links[-1]
            temp_links.append(drop_link)
            links.remove(drop_link)
            path.remove(path[-1])
        self.optical_bands[forw_opt_band_id]["dst"] = path[-1]
        '''
        if bidir:
            self.optical_bands[back_opt_band_id]["src"] = path[-1]
        '''

        c_slots, l_slots, s_slots = self.get_slots(links, num_slots)
        if debug:
            print(c_slots)
            print(l_slots)
            print(s_slots)
        if len(c_slots) > 0 or len(l_slots) > 0 or len(s_slots) > 0:
            flow_list, band_range, slots, fiber_f, fiber_b = self.select_slots_and_ports(links, num_slots, c_slots, l_slots, s_slots, bidir)
            if debug:
                print(flow_list, band_range, slots, fiber_f, fiber_b)
            f0, band = frequency_converter(band_range, slots)
            if debug:
                print(f0, band)
            print("INFO: RSA completed for optical band")
            if flow_list is None:
                self.null_values(self.flow_id)
                return self.flow_id, []
            #slots_i = []
            #for i in slots:
            #    slots_i.append(int(i))
            slots_i = {}
            for i in slots:
                slots_i[str(i)] = 1

            # return links, path, flow_list, band_range, slots, fiber_f, fiber_b, op, num_slots, f0, band
            #        links, path, flows, bx, slots, fiber_f, fiber_b, op, n_slots, f0, band
            if debug:
                print(links)
            if len(flow_list) > 0:
                src_port = flow_list[path[0]]['f']['out']
                dst_port = flow_list[path[-1]]['f']['in']
                if debug:
                    print(flow_list)
            if len(links) == 1:
                #fib_x = fiber_f[link_x]
                #rev_dst_port = self.links_dict[link_x]['fibers'][fib_x]["local_peer_port"]
                #rev_src_port = self.links_dict[link_x]['fibers'][fib_x]["remote_peer_port"]
                fibx = self.get_link_by_name(links[0])["optical_details"]
                rev_dst_port = fibx["local_peer_port"]
                rev_src_port = fibx["remote_peer_port"]
            else:
                link_in = links[0]
                link_out = links[-1]
                fib_inx = self.get_link_by_name(link_in)["optical_details"]
                fib_outx = self.get_link_by_name(link_out)["optical_details"]
                rev_dst_port = fib_inx["local_peer_port"]
                rev_src_port = fib_outx["remote_peer_port"]

                #fib_in = fiber_f[link_in]
                #fib_out = fiber_f[link_out]
                #rev_dst_port = self.links_dict[link_in]['fibers'][fib_in]["local_peer_port"]
                #rev_src_port = self.links_dict[link_out]['fibers'][fib_out]["remote_peer_port"]

            self.optical_bands[forw_opt_band_id]["flows"] = flow_list
            self.optical_bands[forw_opt_band_id]["band_type"] = band_range
            self.optical_bands[forw_opt_band_id]["fiber_forward"] = fiber_f
            self.optical_bands[forw_opt_band_id]["fiber_backward"] = fiber_b
            self.optical_bands[forw_opt_band_id]["op-mode"] = op
            self.optical_bands[forw_opt_band_id]["n_slots"] = num_slots
            self.optical_bands[forw_opt_band_id]["links"] = links
            self.optical_bands[forw_opt_band_id]["path"] = path
            self.optical_bands[forw_opt_band_id]["band"] = band
            self.optical_bands[forw_opt_band_id]["freq"] = f0
            self.optical_bands[forw_opt_band_id]["is_active"] = True
            self.optical_bands[forw_opt_band_id]["src_port"] = src_port
            self.optical_bands[forw_opt_band_id]["dst_port"] = dst_port
            self.optical_bands[forw_opt_band_id]["rev_dst_port"] = rev_dst_port
            self.optical_bands[forw_opt_band_id]["rev_src_port"] = rev_src_port
            self.optical_bands[forw_opt_band_id][band_range] = slots_i
            self.optical_bands[forw_opt_band_id]["served_lightpaths"] = []
            '''
            if bidir:
                self.optical_bands[back_opt_band_id]["flows"] = flow_list_b
                self.optical_bands[back_opt_band_id]["band_type"] = band_range
                self.optical_bands[back_opt_band_id]["fiber_forward"] = fiber_b
                # self.optical_bands[back_opt_band_id]["fiber_backward"] = fiber_b
                self.optical_bands[back_opt_band_id]["op-mode"] = op
                self.optical_bands[back_opt_band_id]["n_slots"] = num_slots
                self.optical_bands[back_opt_band_id]["links"] = rev_links
                self.optical_bands[back_opt_band_id]["path"] = rev_path
                self.optical_bands[back_opt_band_id]["band"] = band
                self.optical_bands[back_opt_band_id]["freq"] = f0
                self.optical_bands[back_opt_band_id]["is_active"] = True
                self.optical_bands[back_opt_band_id]["src_port"] = rev_src_port
                self.optical_bands[back_opt_band_id]["dst_port"] = rev_dst_port
                self.optical_bands[back_opt_band_id][band_range] = slots_i.copy()
                self.optical_bands[back_opt_band_id]["served_lightpaths"] = []
            '''

        return forw_opt_band_id, temp_links

    def get_optical_bands(self, r_src, r_dst):
        result = []
        for ob_id in self.optical_bands:
            ob = self.optical_bands[ob_id]
            if debug:
                print(r_src, ob["src"])
                print(r_dst, ob["dst"])
                print(ob)
            if ob["src"] == r_src and ob["dst"] == r_dst:
                result.append(ob_id)
        return result

    def rsa_fs_computation(self, src, dst, rate, bidir, band):
        num_slots_ob = "full_band"
        if band is not None:
            num_slots_ob = map_band_to_slot(band)
            print(band, num_slots_ob)
        if self.nodes_dict[src]["type"] == "OC-ROADM" and self.nodes_dict[dst]["type"] == "OC-ROADM":
            print("INFO: ROADM to ROADM connection")
            links, path = self.compute_path(src, dst)
            if len(path) < 1:
                self.null_values_ob(self.opt_band_id)
                return self.flow_id, []
            optical_band_id, temp_links = self.create_optical_band(links, path, bidir, num_slots_ob)
            return None, optical_band_id
        print("INFO: TP to TP connection")
        if self.flow_id == 0:
            self.flow_id += 1
        else:
            if (self.db_flows[self.flow_id]["bidir"] == 1):
                self.flow_id += 2
            else:
                self.flow_id += 1
        self.db_flows[self.flow_id] = {}
        self.db_flows[self.flow_id]["flow_id"] = self.flow_id
        self.db_flows[self.flow_id]["src"] = src
        self.db_flows[self.flow_id]["dst"] = dst
        self.db_flows[self.flow_id]["bitrate"] = rate
        self.db_flows[self.flow_id]["bidir"] = bidir

        if band is None:
            temp_links2 = []
            temp_path = []
            src_links = get_links_from_node(self.links_dict, src)
            dst_links = get_links_to_node(self.links_dict, dst)
            if len(src_links.keys()) >= 1:
                temp_links2.append(list(src_links.keys())[0])
            if len(dst_links.keys()) >= 1:
                temp_links2.append(list(dst_links.keys())[0])

            if len(temp_links2) == 2:
                [t_src, roadm_src] = temp_links2[0].split('-')
                [roadm_dst, t_dst] = temp_links2[1].split('-')
                temp_path.append(t_src)
                temp_path.append(roadm_src)
                temp_path.append(roadm_dst)
                temp_path.append(t_dst)
                existing_ob = self.get_optical_bands(roadm_src, roadm_dst)

                if len(existing_ob) > 0:
                    print("INFO: Evaluating existing OB  {}".format(existing_ob))
                    #first checking in existing OB
                    ob_found = 0
                    for ob_id in existing_ob:
                        if "is_active" in self.optical_bands[ob_id].keys():
                            is_active = self.optical_bands[ob_id]["is_active"]
                            if not is_active:
                                continue
                        op, num_slots = map_rate_to_slot(rate)
                        if debug:
                            print(temp_links2)
                        c_slots, l_slots, s_slots = self.get_slots(temp_links2, num_slots, ob_id)
                        if debug:
                            print(c_slots)
                            print(l_slots)
                            print(s_slots)
                        if len(c_slots) >= num_slots or len(l_slots) >= num_slots or len(s_slots) >= num_slots:
                            flow_list, band_range, slots, fiber_f, fiber_b = self.select_slots_and_ports_fs(temp_links2, num_slots,
                                                                                                            c_slots,
                                                                                                            l_slots, s_slots, bidir,
                                                                                                            ob_id)
                            f0, band = frequency_converter(band_range, slots)
                            if debug:
                                print(f0, band)
                            print("INFO: RSA completed for Flex Lightpath with OB already in place")
                            if flow_list is None:
                                self.null_values(self.flow_id)
                                continue
                            slots_i = []
                            for i in slots:
                                slots_i.append(int(i))
                            # return links, path, flow_list, band_range, slots, fiber_f, fiber_b, op, num_slots, f0, band
                            #        links, path, flows, bx, slots, fiber_f, fiber_b, op, n_slots, f0, band
                            self.db_flows[self.flow_id]["flows"] = flow_list
                            self.db_flows[self.flow_id]["band_type"] = band_range
                            self.db_flows[self.flow_id]["slots"] = slots_i
                            self.db_flows[self.flow_id]["fiber_forward"] = fiber_f
                            self.db_flows[self.flow_id]["fiber_backward"] = fiber_b
                            self.db_flows[self.flow_id]["op-mode"] = op
                            self.db_flows[self.flow_id]["n_slots"] = num_slots
                            self.db_flows[self.flow_id]["links"] = temp_links2
                            self.db_flows[self.flow_id]["path"] = temp_path
                            self.db_flows[self.flow_id]["band"] = band
                            self.db_flows[self.flow_id]["freq"] = f0
                            self.db_flows[self.flow_id]["is_active"] = True
                            self.db_flows[self.flow_id]["parent_opt_band"] = ob_id
                            self.db_flows[self.flow_id]["new_optical_band"] = 0
                            self.optical_bands[ob_id]["served_lightpaths"].append(self.flow_id)
                            '''
                            if bidir:
                                rev_ob_id = self.optical_bands[ob_id]["reverse_optical_band_id"]
                                self.optical_bands[rev_ob_id]["served_lightpaths"].append(self.flow_id)
                            '''
                            return self.flow_id, ob_id
                        else:
                            print("not enough slots")
                            print("trying to extend OB {}".format(ob_id))
                            new_slots = self.extend_optical_band(ob_id, band=None)

                            if len(new_slots) > 0:
                                band_type = self.optical_bands[ob_id]["band_type"]
                                c_slots = []
                                l_slots = []
                                s_slots = []
                                if band_type == "c_slots":
                                    c_slots = new_slots
                                elif band_type == "l_slots":
                                    l_slots = new_slots
                                else:
                                    s_slots = new_slots
                                op, num_slots = map_rate_to_slot(rate)
                                if debug:
                                    print(temp_links2)
                                c_slots, l_slots, s_slots = self.get_slots(temp_links2, num_slots, ob_id)
                                if debug:
                                    print(c_slots)
                                    print(l_slots)
                                    print(s_slots)
                                #print(c_slots)
                                #print(l_slots)
                                #print(s_slots)
                                if len(c_slots) >= num_slots or len(l_slots) >= num_slots or len(s_slots) >= num_slots:
                                    flow_list, band_range, slots, fiber_f, fiber_b = self.select_slots_and_ports_fs(
                                        temp_links2, num_slots,
                                        c_slots,
                                        l_slots, s_slots, bidir,
                                        ob_id)
                                    f0, band = frequency_converter(band_range, slots)
                                    if debug:
                                        print(f0, band)
                                    print("INFO: RSA completed for Flex Lightpath with OB already in place")
                                    if flow_list is None:
                                        self.null_values(self.flow_id)
                                        continue
                                    slots_i = []
                                    for i in slots:
                                        slots_i.append(int(i))
                                    # return links, path, flow_list, band_range, slots, fiber_f, fiber_b, op, num_slots, f0, band
                                    #        links, path, flows, bx, slots, fiber_f, fiber_b, op, n_slots, f0, band
                                    self.db_flows[self.flow_id]["flows"] = flow_list
                                    self.db_flows[self.flow_id]["band_type"] = band_range
                                    self.db_flows[self.flow_id]["slots"] = slots_i
                                    self.db_flows[self.flow_id]["fiber_forward"] = fiber_f
                                    self.db_flows[self.flow_id]["fiber_backward"] = fiber_b
                                    self.db_flows[self.flow_id]["op-mode"] = op
                                    self.db_flows[self.flow_id]["n_slots"] = num_slots
                                    self.db_flows[self.flow_id]["links"] = temp_links2
                                    self.db_flows[self.flow_id]["path"] = temp_path
                                    self.db_flows[self.flow_id]["band"] = band
                                    self.db_flows[self.flow_id]["freq"] = f0
                                    self.db_flows[self.flow_id]["is_active"] = True
                                    self.db_flows[self.flow_id]["parent_opt_band"] = ob_id
                                    #self.db_flows[self.flow_id]["new_optical_band"] = 1
                                    self.db_flows[self.flow_id]["new_optical_band"] = 2
                                    self.optical_bands[ob_id]["served_lightpaths"].append(self.flow_id)
                                    '''
                                    if bidir:
                                        rev_ob_id = self.optical_bands[ob_id]["reverse_optical_band_id"]
                                        self.optical_bands[rev_ob_id]["served_lightpaths"].append(self.flow_id)
                                    '''
                                    return self.flow_id, ob_id
                                else:
                                    print("it is not possible to allocate connection in extended OB {}".format(ob_id))
                                    

        if band is None:
            print("INFO: Not existing optical-band meeting the requirements")
        else:
            print("INFO: optical-band width specified")
        #if no OB I create a new one
        links, path = self.compute_path(src, dst)
        optical_band_id, temp_links = self.create_optical_band(links, path, bidir, num_slots_ob)
        op, num_slots = map_rate_to_slot(rate)
        if debug:
            print(temp_links)
        c_slots, l_slots, s_slots = self.get_slots(temp_links, num_slots, optical_band_id)
        if debug:
            print(c_slots)
            print(l_slots)
            print(s_slots)
        if len(c_slots) > 0 or len(l_slots) > 0 or len(s_slots) > 0:
            flow_list, band_range, slots, fiber_f, fiber_b = self.select_slots_and_ports_fs(temp_links, num_slots, c_slots,
                                                                                            l_slots, s_slots, bidir, optical_band_id)
            f0, band = frequency_converter(band_range, slots)
            if debug:
                print(f0, band)
            print("INFO: RSA completed for FLex Lightpath with new OB")
            if flow_list is None:
                self.null_values(self.flow_id)
                return self.flow_id, optical_band_id
            slots_i = []
            for i in slots:
                slots_i.append(int(i))

            self.db_flows[self.flow_id]["flows"] = flow_list
            self.db_flows[self.flow_id]["band_type"] = band_range
            self.db_flows[self.flow_id]["slots"] = slots_i
            self.db_flows[self.flow_id]["fiber_forward"] = fiber_f
            self.db_flows[self.flow_id]["fiber_backward"] = fiber_b
            self.db_flows[self.flow_id]["op-mode"] = op
            self.db_flows[self.flow_id]["n_slots"] = num_slots
            self.db_flows[self.flow_id]["links"] = temp_links
            self.db_flows[self.flow_id]["path"] = path
            self.db_flows[self.flow_id]["band"] = band
            self.db_flows[self.flow_id]["freq"] = f0
            self.db_flows[self.flow_id]["is_active"] = True
            self.db_flows[self.flow_id]["parent_opt_band"] = optical_band_id
            self.db_flows[self.flow_id]["new_optical_band"] = 1
            self.optical_bands[optical_band_id]["served_lightpaths"].append(self.flow_id)
            '''
            if bidir:
                rev_ob_id = self.optical_bands[optical_band_id]["reverse_optical_band_id"]
                self.optical_bands[rev_ob_id]["served_lightpaths"].append(self.flow_id)
            '''
            
        return self.flow_id, optical_band_id

    def extend_optical_band(self, ob_id, band=None):
        ob = self.optical_bands[ob_id]
        links = ob["links"]
        old_band = ob["band"]
        band_type = ob["band_type"]
        f0 = ob["freq"]
        slots = ob[band_type]
        if band is None:
            num_slots_ob = map_band_to_slot(old_band/1000.0)
        else:
            num_slots_ob = map_band_to_slot(band)
        new_slots = []
        for l in links:
            link = self.get_link_by_name(l)
            fib = link["optical_details"][band_type]
            #s_slots = get_side_slots_on_link(link, band_type, num_slots_ob, slots)
            s_slots, s_num = get_side_slots_on_link(fib, num_slots_ob, slots)
            print("NEW SLOTS {}".format(s_slots))
            if len(new_slots) == 0:
                new_slots = s_slots
            else:
                if len(new_slots) < s_num:
                    new_slots = list_in_list(new_slots, s_slots)
        print("NEW SLOTS {}".format(new_slots))
        self.augment_optical_band(ob_id, new_slots, band_type)
        new_band = int(len(new_slots)*12.5*1000)
        print("{}, {},{},{} ".format(old_band, f0, len(new_slots), new_band))
        final_band = old_band + new_band
        final_f0 = int(f0 + new_band/2)
        print("{}, {}".format(final_band, final_f0))
        ob["band"] = final_band
        ob["freq"] = final_f0
        for link_x in links:
            link = self.get_link_by_name(link_x)
            fib = link["optical_details"]
            self.update_link(fib, new_slots, band_type)
           
        return new_slots
