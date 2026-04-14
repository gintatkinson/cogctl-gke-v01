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
from flask import Flask
from flask_restful import Api
from .resources.ACLs import register_restconf_openconfig_acls
from .resources.Components import register_restconf_openconfig_components
from .resources.HostMeta import register_host_meta
from .resources.Interfaces import register_restconf_openconfig_interfaces
from .resources.Root import register_restconf_root


logging.basicConfig(level=logging.INFO)


app = Flask(__name__)
api = Api(app)
register_host_meta(api)
register_restconf_root(api)
register_restconf_openconfig_components(api)
register_restconf_openconfig_interfaces(api)
register_restconf_openconfig_acls(api)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
