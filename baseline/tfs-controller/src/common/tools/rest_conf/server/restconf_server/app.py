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
from .RestConfServerApplication import RestConfServerApplication


logging.basicConfig(
    level=logging.INFO,
    format='[Worker-%(process)d][%(asctime)s] %(levelname)s:%(name)s:%(message)s',
)
LOGGER = logging.getLogger(__name__)

LOGGER.info('Starting...')
rcs_app = RestConfServerApplication()
rcs_app.register_host_meta()
rcs_app.register_restconf()
LOGGER.info('All connectors registered')

rcs_app.dump_configuration()
app = rcs_app.get_flask_app()

LOGGER.info('Initialization completed!')
