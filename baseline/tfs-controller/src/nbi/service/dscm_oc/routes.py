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
from .enforce_header                           import require_accept, require_content_type
from .error                                    import _bad_request, _not_found, yang_json
from .json_to_proto_conversion                 import (
    json_to_create_pluggable_request,
    json_to_delete_pluggable_request,
    json_to_get_pluggable_request,
    json_to_list_pluggables_request,
)
from common.method_wrappers.ServiceExceptions  import (
    ServiceException,
    NotFoundException,
    AlreadyExistsException,
    InvalidArgumentException
)
from common.tools.grpc.Tools                   import grpc_message_to_json
from flask                                     import Blueprint, request, Response
from pluggables.client.PluggablesClient        import PluggablesClient


LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

blueprint = Blueprint("testconf_dscm", __name__)

YANG_JSON = "application/yang-data+json"
ERR_JSON  = "application/yang-errors+json"


# Root endpoints (both prefixes) TODO: call list pluggables if device_uuid is given
# @blueprint.route("/device=<device_uuid>/", methods=["GET"])
# @blueprint.route("/", methods=["GET"], defaults={'device_uuid': None})
# @require_accept([YANG_JSON])
# def list_root(device_uuid=None):
#     """List top-level modules/containers available."""
#     # TODO: If device_uuid is given, call ListPluggables gRPC method
#     return 


@blueprint.route("/device=<device_uuid>/<path:rc_path>", methods=["GET"])
@require_accept([YANG_JSON])
def rc_get(rc_path, device_uuid=None):
    LOGGER.info(f"GET request for path: {rc_path} on device UUID: {device_uuid}")
    
    if device_uuid is None:
        return _bad_request("Device UUID must be specified for GET requests.", path=rc_path)
    pluggables_client = PluggablesClient()

    try:
        get_request = json_to_get_pluggable_request(device_uuid)
        pluggable = pluggables_client.GetPluggable(get_request)
        LOGGER.info(f"Successfully retrieved pluggable for device {device_uuid}")
        response_data = grpc_message_to_json(pluggable)
        return yang_json(response_data)
    
    except NotFoundException as e:
        LOGGER.warning(f"Pluggable not found for device {device_uuid}: {e.details}")
        return _not_found(f"Pluggable not found: {e.details}", path=rc_path)
    
    except ServiceException as e:
        LOGGER.error(f"Unexpected error getting pluggable for device {device_uuid}: {str(e)}", exc_info=True)
        return _bad_request(f"Failed to get pluggable: {str(e)}", path=rc_path)
    
    finally:
            pluggables_client.close()

@blueprint.route("/device=<device_uuid>/<path:rc_path>", methods=["POST"])
@require_accept([YANG_JSON])
@require_content_type([YANG_JSON])
def rc_post(rc_path, device_uuid=None):
    if device_uuid is None:
        return _bad_request("Device UUID must be specified for POST requests.", path=rc_path)
    
    payload = request.get_json(force=True, silent=True)
    if payload is None:
        return _bad_request("Invalid or empty JSON payload.", path=rc_path)
    
    try:
        create_request = json_to_create_pluggable_request(
            device_uuid    = device_uuid,
            initial_config = payload,
        )
        
        pluggables_client = PluggablesClient()
        try:
            pluggable = pluggables_client.CreatePluggable(create_request)
            LOGGER.info(f"Successfully created pluggable for device {device_uuid}")
            response_data = grpc_message_to_json(pluggable)
            
            return yang_json(response_data, status=201)
        finally:
            pluggables_client.close()
    
    except AlreadyExistsException as e:
        LOGGER.warning(f"Pluggable already exists for device {device_uuid}: {e.details}")
        return _bad_request(f"Pluggable already exists: {e.details}", path=rc_path)
    
    except InvalidArgumentException as e:
        LOGGER.warning(f"Invalid argument creating pluggable for device {device_uuid}: {e.details}")
        return _bad_request(f"Invalid argument: {e.details}", path=rc_path)
    
    except ServiceException as e:
        LOGGER.error(f"Unexpected error creating pluggable for device {device_uuid}: {str(e)}", exc_info=True)
        return _bad_request(f"Failed to create pluggable: {str(e)}", path=rc_path)

@blueprint.route("/device=<device_uuid>/<path:rc_path>", methods=["DELETE"])
@require_accept([YANG_JSON])
def rc_delete(rc_path, device_uuid=None):
    LOGGER.info(f"DELETE request for path: {rc_path} on device UUID: {device_uuid}")
    
    if device_uuid is None:
        return _bad_request("Device UUID must be specified for DELETE requests.", path=rc_path)
    
    pluggables_client = PluggablesClient()
    try:
        # Delete specific pluggable
        delete_request = json_to_delete_pluggable_request(device_uuid)
        pluggables_client.DeletePluggable(delete_request)
        LOGGER.info(f"Successfully deleted pluggable for device {device_uuid}")
        return Response(status=204)
        
    except NotFoundException as e:
        LOGGER.warning(f"Pluggable not found for device {device_uuid}: {e.details} (already deleted or never existed)")
        return Response(status=204)
    
    except ServiceException as e:
        LOGGER.error(f"Unexpected error deleting pluggable for device {device_uuid}: {str(e)}", exc_info=True)
        return _bad_request(f"Failed to delete pluggable: {str(e)}", path=rc_path)

    finally:
        pluggables_client.close()
