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

# RFC 8795 - YANG Data Model for Traffic Engineering (TE) Topologies
# Ref: https://datatracker.ietf.org/doc/html/rfc8795

# RFC 8776 - Common YANG Data Types for Traffic Engineering
# Ref: https://datatracker.ietf.org/doc/html/rfc8776

# RFC 8345 - A YANG Data Model for Network Topologies
# Ref: https://datatracker.ietf.org/doc/html/rfc8345

# RFC 6991 - Common YANG Data Types
# Ref: https://datatracker.ietf.org/doc/html/rfc6991

# RFC draft-ietf-ccamp-eth-client-te-topo-yang-05 - A YANG Data Model for Ethernet TE Topology
# Ref: https://datatracker.ietf.org/doc/draft-ietf-ccamp-eth-client-te-topo-yang/

# RFC draft-ietf-ccamp-client-signal-yang-10 - A YANG Data Model for Transport Network Client Signals
# Ref: https://datatracker.ietf.org/doc/draft-ietf-ccamp-client-signal-yang/


from nbi.service.NbiApplication import NbiApplication
from .Networks import Networks

URL_PREFIX = '/restconf/data/ietf-network:networks'

def register_ietf_network(nbi_app : NbiApplication):
    nbi_app.add_rest_api_resource(Networks, URL_PREFIX + '/')
