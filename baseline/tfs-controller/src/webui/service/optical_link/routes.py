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


from flask import current_app, render_template, Blueprint, flash, session, redirect, url_for
from common.proto.context_pb2 import Empty, OpticalLink, LinkId, OpticalLinkList , Service
from common.tools.context_queries.EndPoint import get_endpoint_names
from common.tools.context_queries.Topology import get_topology
from context.client.ContextClient import ContextClient
import functools ,requests ,logging
from common.Constants import ServiceNameEnum
from common.tools.context_queries.OpticalConfig import find_optical_band
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_BASEURL_HTTP, ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC,
    find_environment_variables, get_env_var_name
)

get_optical_controller_setting = functools.partial(get_env_var_name, ServiceNameEnum.OPTICALCONTROLLER)
VAR_NAME_OPTICAL_CTRL_HOST         = get_optical_controller_setting(ENVVAR_SUFIX_SERVICE_HOST)
VAR_NAME_OPTICAL_CTRL_PORT         = get_optical_controller_setting(ENVVAR_SUFIX_SERVICE_PORT_GRPC)
VAR_NAME_OPTICAL_CTRL_BASEURL_HTTP = get_optical_controller_setting(ENVVAR_SUFIX_SERVICE_BASEURL_HTTP)
VAR_NAME_OPTICAL_CTRL_SCHEMA       = get_optical_controller_setting('SCHEMA')

settings = find_environment_variables([
        VAR_NAME_OPTICAL_CTRL_BASEURL_HTTP,
        VAR_NAME_OPTICAL_CTRL_SCHEMA,
        VAR_NAME_OPTICAL_CTRL_HOST,
        VAR_NAME_OPTICAL_CTRL_PORT,
    ])

host = settings.get(VAR_NAME_OPTICAL_CTRL_HOST)
port = settings.get(VAR_NAME_OPTICAL_CTRL_PORT, 80)

optical_link = Blueprint('optical_link', __name__, url_prefix='/optical_link')
context_client = ContextClient()

@optical_link.get('/')
def home():
    if 'context_uuid' not in session or 'topology_uuid' not in session:
        flash("Please select a context!", "warning")
        return redirect(url_for("main.home"))

    context_uuid = session['context_uuid']
    topology_uuid = session['topology_uuid']

    links, endpoint_ids = list(), list()
    device_names, endpoints_data = dict(), dict()

    context_client.connect()
    grpc_topology = get_topology(context_client, topology_uuid, context_uuid=context_uuid, rw_copy=False)
    if grpc_topology is None:
        flash('Context({:s})/Topology({:s}) not found'.format(str(context_uuid), str(topology_uuid)), 'danger')
    else:
        grpc_links : OpticalLinkList = context_client.GetOpticalLinkList(Empty())
        for link_ in grpc_links.optical_links:
            links.append(link_)
            endpoint_ids.extend(link_.link_endpoint_ids)
        device_names, endpoints_data = get_endpoint_names(context_client, endpoint_ids)
    context_client.close()

    return render_template(
        'optical_link/home.html', links=links, device_names=device_names,
        endpoints_data=endpoints_data
    )


@optical_link.route('detail/<path:link_uuid>', methods=('GET', 'POST'))
def detail(link_uuid: str):
    context_client.connect()
    # pylint: disable=no-member
    link_id = LinkId()
    link_id.link_uuid.uuid = link_uuid
    link_obj = context_client.GetOpticalLink(link_id)
    c_slots=s_slots=l_slots=None
    if link_obj is None:
        flash('Optical Link({:s}) not found'.format(str(link_uuid)), 'danger')
        link_obj = OpticalLink()
        device_names, endpoints_data = dict(), dict()
    else:
        device_names, endpoints_data = get_endpoint_names(context_client, link_obj.link_endpoint_ids)
        c_slots = link_obj.optical_details.c_slots
        l_slots = link_obj.optical_details.l_slots
        s_slots = link_obj.optical_details.s_slots

    context_client.close()

    return render_template(
        'optical_link/detail.html', link=link_obj, device_names=device_names,
        endpoints_data=endpoints_data, c_slots=c_slots, l_slots=l_slots, s_slots=s_slots
    )


@optical_link.get('<path:link_uuid>/delete')
def delete(link_uuid):
    try:
        request = LinkId()
        request.link_uuid.uuid = link_uuid # pylint: disable=no-member
        context_client.connect()
        context_client.DeleteOpticalLink(request)
        context_client.close()

        flash(f'Optical Link "{link_uuid}" deleted successfully!', 'success')
    except Exception as e: # pylint: disable=broad-except
        flash(f'Problem deleting link "{link_uuid}": {e.details()}', 'danger')
        current_app.logger.exception(e)
    return redirect(url_for('optical_link.home'))


@optical_link.get("delete_all")
def delete_all():
    try:
        context_client.connect()
        optical_link_list : OpticalLinkList = context_client.GetOpticalLinkList(Empty())
        for optical_link in optical_link_list.optical_links:
            context_client.DeleteOpticalLink(optical_link.link_id)
        context_client.close()
        flash(f"All Optical Link Deleted Successfully",'success')
    except Exception as e:
        flash(f"Problem in delete all optical link  => {e}",'danger')
    return redirect(url_for('optical_link.home'))


@optical_link.route('getopticallinks', methods=(['GET']))
def get_optical_links (): 
    

    urlx = "http://{:s}:{:s}/OpticalTFS/GetLinks".format(host,port)
   
    headers = {"Content-Type": "application/json"}
    optical_links =[]
    try: 
        r = requests.get(urlx, headers=headers)
        reply = r.json()
        if (reply and 'optical_links' in reply): 
            optical_links = reply["optical_links"]
            for link in optical_links : 
                for k,v in link['optical_details'].items():
                    if k == 'c_slots' or k =='l_slots' or k =='s_slots':
                        sorted_keys = sorted(v.keys(), key=lambda x: int(x), reverse=False)
                        sorted_dict = {key: v[key] for key in sorted_keys}
                        link['optical_details'][k] = sorted_dict
            
    except Exception as e : 
        logging.info(f"error {e}")
    finally:
         
       return render_template(
        'opticalconfig/opticallinks.html', optical_links=optical_links
    )
       



@optical_link.route('getopticalbands', methods=(['GET']))
def get_optical_bands(): 
    

    urlx = "http://{:s}:{:s}/OpticalTFS/GetOpticalBands".format(host,port)
   
    headers = {"Content-Type": "application/json"}
    optical_bands ={}
    service_uuid = None
    try: 
        r = requests.get(urlx, headers=headers)
        reply = r.json()
        if (reply and r.status_code == 200):
            optical_bands=reply
            ob_keys = optical_bands.keys()
            for ob_key in ob_keys :
                ob_service = find_optical_band(ob_key)
                if ob_service is not None :
                    service_uuid=ob_service.service.service_id.service_uuid.uuid
                    optical_bands[ob_key]['service_uuid']=service_uuid
        
        logging.info(f"optical bands {optical_bands}")

    except Exception as e : 
        logging.info(f"error {e}")
    finally:
         
       return render_template(
        'opticalconfig/opticalbands.html',optical_bands=optical_bands
    )       
 
@optical_link.route('getlightpath', methods=(['GET']))
def get_lightpath(): 
    

    urlx = "http://{:s}:{:s}/OpticalTFS/GetLightpaths".format(host,port)
   
    headers = {"Content-Type": "application/json"}
    light_paths ={}
    try: 
        r = requests.get(urlx, headers=headers)
        reply = r.json()
        if (reply):light_paths=reply
       
        
        logging.info(f"lightpaths {reply}")
    except Exception as e : 
        logging.info(f"error {e}")
    finally:
         
       return render_template(
        'opticalconfig/lightpaths.html',light_paths=light_paths
    )
