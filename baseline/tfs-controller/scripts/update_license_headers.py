#!/bin/bash
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

# Run from ~/tfs-ctrl as:
# python scripts/update_license_headers.py

import logging, os, re, sys
from io import TextIOWrapper

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

ROOT_PATH = '.'
FILE_PATH_SKIPPED    = 'out-skipped.txt'
FILE_PATH_NO_HEADER  = 'out-no-header.txt'
FILE_PATH_UPDATED    = 'out-updated.txt'

STR_NEW_COPYRIGHT = 'Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)'

RE_OLD_COPYRIGHTS = [
    r'Copyright\ 2021\-202[0-9]\ H2020\ TeraFlow\ \(https\:\/\/www\.teraflow\-h2020\.eu\/\)',
    r'Copyright\ 2022\-202[0-9]\ ETSI\ TeraFlowSDN\ \-\ TFS\ OSG\ \(https\:\/\/tfs\.etsi\.org\/\)',
    r'Copyright\ 2022\-202[0-9]\ ETSI\ TeraFlowSDN\ \-\ TFS\ OSG\/SDG\ \(https\:\/\/tfs\.etsi\.org\/\)',
    r'Copyright\ 2022\-202[0-9]\ ETSI\ OSG\/SDG\ TeraFlowSDN\ \(TFS\)\ \(https\:\/\/tfs\.etsi\.org\/\)',
    r'Copyright\ 2022\-202[0-4]\ ETSI\ SDG\ TeraFlowSDN\ \(TFS\)\ \(https\:\/\/tfs\.etsi\.org\/\)',
]
RE_OLD_COPYRIGHTS = [
    (re.compile(r'.*{}.*'.format(re_old_copyright)), re.compile(re_old_copyright))
    for re_old_copyright in RE_OLD_COPYRIGHTS
]

def skip_file(file_path : str) -> bool:
    if os.path.islink(file_path): return True
    if file_path.endswith('.pyc'): return True
    if file_path.endswith('_pb2_grpc.py'): return True
    if file_path.endswith('_pb2.py'): return True
    if file_path.endswith('.class'): return True
    if file_path.endswith('.md'): return True
    if file_path.endswith('.png'): return True
    if file_path.endswith('.json'): return True
    if file_path.endswith('.csv'): return True
    if file_path.endswith('.zip'): return True
    if file_path.endswith('.zip'): return True
    if file_path.endswith('.tgz'): return True
    if file_path.endswith('.jar'): return True
    if file_path.endswith('.onnx'): return True
    if file_path.endswith('/tstat'): return True
    if file_path.endswith('/coverage/.coverage'): return True
    if file_path.endswith('/grpc/grpcurl/grpcurl'): return True
    if file_path.endswith('/probe/probe-tfs/target/x86_64-unknown-linux-musl/release/tfsagent'): return True
    if file_path.endswith('/probe/probe-tfs/target/x86_64-unknown-linux-musl/release/tfsping'): return True
    if file_path.startswith('./libyang/'): return True
    if file_path.startswith('./netconf_openconfig/'): return True
    if file_path.startswith('./tmp/'): return True
    if '/manifests/cttc-ols/' in file_path: return True
    if '/hackfest/netconf-oc/openconfig/' in file_path: return True
    if '/hackfest/tapi/server/tapi_server/' in file_path: return True
    if '/hackfest/kafka/kafka_2.13-2.8.0/' in file_path: return True
    if '/hackfest5/clab-hackfest5/' in file_path: return True
    if '/.git/' in file_path: return True
    if '/.vscode/' in file_path: return True
    if '/.pytest_cache/' in file_path: return True
    if '/__pycache__/' in file_path: return True
    if '/.mvn/' in file_path: return True
    if '/bgpls_speaker/service/java/netphony-topology/.settings/' in file_path: return True
    if '/bgpls_speaker/service/java/netphony-topology/' in file_path:
        file_path_parts = file_path.split('/')
        file_name = file_path_parts[-1]
        return file_name in {'LICENSE', 'VERSION'}
    if '/device/service/drivers/gnmi_openconfig/git/' in file_path: return True
    if '/device/service/drivers/gnmi_openconfig/gnmi/gnmi' in file_path: return True
    if '/device/service/drivers/gnmi_openconfig/gnmi/Acknowledgement.txt' in file_path: return True
    if '/device/service/drivers/openconfig/templates/' in file_path:
        if file_path.endswith('.xml'): return True
        file_path_parts = file_path.split('/')
        file_name = file_path_parts[-1]
        if file_name.startswith('openconfig_') and file_name.endswith('.py'): return True
        return False
    if '/device/service/drivers/smartnic/' in file_path:
        if file_path.startswith('openconfig-'): return True
        if file_path.startswith('ietf-'): return True
        if file_path.endswith('references_probes_libraries.txt'): return True
        return False
    if '/nbi/service/ietf_network/bindings/' in file_path: return True
    if '/nbi/service/ietf_network_slice/bindings/' in file_path:
        if file_path.endswith('.py'): return False
        return True
    if '/nbi/service/ietf_l3vpn/yang/' in file_path: return True
    if '/nbi/service/ietf_network/yang/' in file_path: return True
    if '/tests/tools/mock_qkd_nodes/yang/' in file_path: return True
    if '/ztp/target/' in file_path: return True
    if '/policy/target/' in file_path: return True
    if '/dlt/gateway/_legacy' in file_path: return True
    if '/proto/src/python/asyncio/' in file_path: return True
    if FILE_PATH_SKIPPED in file_path: return True
    if FILE_PATH_NO_HEADER in file_path: return True
    if FILE_PATH_UPDATED in file_path: return True
    if file_path in {'./LICENSE', './.python-version', './.env'}: return True
    return False

def process_line(line_in : str) -> str:
    for re_match, re_sub in RE_OLD_COPYRIGHTS:
        match = re_match.match(line_in)
        if match is None: continue
        line_out = re_sub.sub(STR_NEW_COPYRIGHT, line_in)
        return line_out
    return line_in

def process_file(
    file_path : str, file_no_header : TextIOWrapper, file_skipped : TextIOWrapper, file_updated : TextIOWrapper
) -> None:
    if skip_file(file_path):
        # silent skips
        if file_path.startswith('./.git'): return
        if file_path.startswith('./libyang'): return
        if file_path.startswith('./tmp'): return
        if file_path.startswith('./hackfest/kafka/kafka_2.13-2.8.0/'): return
        if file_path.startswith('./hackfest/tapi/server/tapi_server/'): return
        if '/__pycache__/' in file_path: return
        if '/nbi/service/ietf_network/bindings/' in file_path: return
        if '/target/classes/' in file_path: return
        if '/target/generated-classes/' in file_path: return
        if '/target/generated-sources/' in file_path: return
        if '/target/test-classes/' in file_path: return
        if '/git/openconfig/public/' in file_path: return
        if file_path.endswith('.class'): return
        if file_path.endswith('.csv'): return
        if file_path.endswith('.jar'): return
        if file_path.endswith('.json'): return
        if file_path.endswith('.pyc'): return
        if file_path.endswith('.png'): return
        if file_path.endswith('.zip'): return
        if file_path.endswith('_pb2.py'): return
        if file_path.endswith('_grpc.py'): return

        # verbose skip
        file_skipped.write(file_path + '\n')
        return

    LOGGER.info('  File {:s}...'.format(str(file_path)))

    temp_file_path = file_path + '.temp'
    replaced = False
    file_stat = os.stat(file_path)
    try:
        with open(file_path, encoding='UTF-8', newline='') as source:
            with open(temp_file_path, 'w', encoding='UTF-8', newline='') as target:
                for line_in in source:
                    if STR_NEW_COPYRIGHT in line_in:
                        replaced = True
                        target.write(line_in)
                    else:
                        line_out = process_line(line_in)
                        replaced = replaced or (line_out != line_in)
                        target.write(line_out)
    except: # pylint: disable=bare-except
        replaced = False

    if not replaced:
        file_no_header.write(file_path + '\n')
    else:
        file_updated.write(file_path + '\n')

    os.rename(temp_file_path, file_path)
    os.chmod(file_path, file_stat.st_mode)

def main() -> int:
    with open(FILE_PATH_NO_HEADER, 'w', encoding='UTF-8') as file_no_header:
        with open(FILE_PATH_SKIPPED, 'w', encoding='UTF-8') as file_skipped:
            with open(FILE_PATH_UPDATED, 'w', encoding='UTF-8') as file_updated:
                for dirpath, _, filenames in os.walk(ROOT_PATH):
                    LOGGER.info('Folder {:s}...'.format(str(dirpath)))
                    for filename in filenames:
                        file_path = os.path.join(dirpath, filename)
                        process_file(file_path, file_no_header, file_skipped, file_updated)
    return 0

if __name__ == '__main__':
    sys.exit(main())
