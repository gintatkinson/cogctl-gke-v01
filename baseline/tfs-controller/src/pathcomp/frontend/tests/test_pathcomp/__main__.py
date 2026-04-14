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


import logging, sys
from common.proto.context_pb2 import ServiceTypeEnum
from pathcomp.frontend.service.algorithms.tools.ComputeSubServices import convert_explicit_path_hops_to_connections
from .data import path_hops, device_dict

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

def main():
    service_uuid = 'dc-2-dc-svc'
    service_type = ServiceTypeEnum.SERVICETYPE_L2NM
    connections = convert_explicit_path_hops_to_connections(path_hops, device_dict, service_uuid, service_type)
    str_connections = '\n'.join(['  ' + str(connection) for connection in connections])
    LOGGER.debug('connections = [\n{:s}\n]'.format(str_connections))
    return 0

if __name__ == '__main__':
    sys.exit(main())
