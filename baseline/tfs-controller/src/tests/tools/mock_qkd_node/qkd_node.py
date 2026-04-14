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


from freeconf import restconf, source, device, parser, node, source, nodeutil
from threading import Event

YANG_PATH    = './yang'
YANG_MDL     = 'etsi-qkd-sdn-node'
STARTUP_FILE = './startup.json'

def main():
    # specify all the places where you store YANG files
    yang_path = source.any(
        source.path(YANG_PATH),             # director to your local *.yang files
        source.restconf_internal_ypath()    # required for restconf protocol support
    )

    # load and validate your YANG file(s)
    yang_module = parser.load_module_file(yang_path, YANG_MDL)

    # device hosts one or more management "modules" into a single instance that you
    # want to export in the management interface
    _device = device.Device(yang_path)

    # connect your application to your management implementation.
    # there are endless ways to to build your management interface from code generation,
    # to reflection and any combination there of.  A lot more information in docs.
    handler = nodeutil.Node(dict())

    # connect parsed YANG to your management implementation.  Browser is a powerful way
    # to dynamically control your application can can be useful in unit tests or other contexts
    # but here we construct it to serve our management API
    browser = node.Browser(yang_module, handler)

    # register your app management browser in device.  Device can hold any number of browsers
    _device.add_browser(browser)

    # select RESTCONF as management protocol. gNMI is option as well or any custom or
    # future protocols
    restconf.Server(_device)

    # this will apply configuration including starting the RESTCONF web server
    _device.apply_startup_config_file(STARTUP_FILE)

    # simple python trick to wait until ctrl-c shutdown
    Event().wait()

if __name__ == '__main__':
    main()
