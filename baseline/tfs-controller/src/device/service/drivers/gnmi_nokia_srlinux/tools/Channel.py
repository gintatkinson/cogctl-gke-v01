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

import grpc, logging, ssl

def get_grpc_channel(address : str, port : int, use_tls : bool, logger : logging.Logger) -> grpc.Channel:
    endpoint = str(address) + ':' + str(port)
    logger.info('Connecting gNMI {:s}...'.format(endpoint))
    if use_tls:
        logger.debug('Getting server certificate...')
        str_server_certificate = ssl.get_server_certificate((str(address), int(port)))
        bytes_server_certificate = str_server_certificate.encode('UTF-8')
        logger.debug('Using secure SSL channel...')
        credentials = grpc.ssl_channel_credentials(
            root_certificates=bytes_server_certificate, private_key=None, certificate_chain=None)
        options = [
            #('grpc.ssl_target_name_override', options.altName,)
        ]
        channel = grpc.secure_channel(endpoint, credentials, options)
    else:
        logger.debug('Using insecure channel...')
        channel = grpc.insecure_channel(endpoint)
    return channel
