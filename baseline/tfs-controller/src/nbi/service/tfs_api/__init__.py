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

from nbi.service.NbiApplication import NbiApplication
from .Resources import (
    Connection, ConnectionIds, Connections,
    Context, ContextIds, Contexts,
    Device, DeviceIds, Devices,
    DummyContexts,
    Link, LinkIds, Links,
    PolicyRule, PolicyRuleIds, PolicyRules,
    Service, ServiceIds, Services,
    Slice, SliceIds, Slices,
    Topologies, Topology, TopologyDetails, TopologyIds
)

ENDPOINT_PREFIX = 'tfs_api.'
URL_PREFIX = '/tfs-api'

# Use 'path' type since some identifiers might contain char '/' and Flask is unable to recognize them in 'string' type.
_RESOURCES = [
    # (endpoint_name, resource_class, resource_url)
    ('api.context_ids',      ContextIds,      '/context_ids'),
    ('api.contexts',         Contexts,        '/contexts'),
    ('api.dummy_contexts',   DummyContexts,   '/dummy_contexts'),
    ('api.context',          Context,         '/context/<path:context_uuid>'),

    ('api.topology_ids',     TopologyIds,     '/context/<path:context_uuid>/topology_ids'),
    ('api.topologies',       Topologies,      '/context/<path:context_uuid>/topologies'),
    ('api.topology',         Topology,        '/context/<path:context_uuid>/topology/<path:topology_uuid>'),
    ('api.topology_details', TopologyDetails, '/context/<path:context_uuid>/topology_details/<path:topology_uuid>'),

    ('api.service_ids',      ServiceIds,      '/context/<path:context_uuid>/service_ids'),
    ('api.services',         Services,        '/context/<path:context_uuid>/services'),
    ('api.service',          Service,         '/context/<path:context_uuid>/service/<path:service_uuid>'),

    ('api.slice_ids',        SliceIds,        '/context/<path:context_uuid>/slice_ids'),
    ('api.slices',           Slices,          '/context/<path:context_uuid>/slices'),
    ('api.slice',            Slice,           '/context/<path:context_uuid>/slice/<path:slice_uuid>'),

    ('api.device_ids',       DeviceIds,       '/device_ids'),
    ('api.devices',          Devices,         '/devices'),
    ('api.device',           Device,          '/device/<path:device_uuid>'),

    ('api.link_ids',         LinkIds,         '/link_ids'),
    ('api.links',            Links,           '/links'),
    ('api.link',             Link,            '/link/<path:link_uuid>'),

    ('api.connection_ids',   ConnectionIds,   '/context/<path:context_uuid>/service/<path:service_uuid>/connection_ids'),
    ('api.connections',      Connections,     '/context/<path:context_uuid>/service/<path:service_uuid>/connections'),
    ('api.connection',       Connection,      '/connection/<path:connection_uuid>'),

    ('api.policyrule_ids',   PolicyRuleIds,   '/policyrule_ids'),
    ('api.policyrules',      PolicyRules,     '/policyrules'),
    ('api.policyrule',       PolicyRule,      '/policyrule/<path:policyrule_uuid>'),
]
RESOURCES = [
    (ENDPOINT_PREFIX + endpoint_name, resource_class, URL_PREFIX + resource_url)
    for endpoint_name, resource_class, resource_url in _RESOURCES
]

def register_tfs_api(nbi_app : NbiApplication):
    nbi_app.add_rest_api_resources(RESOURCES)
