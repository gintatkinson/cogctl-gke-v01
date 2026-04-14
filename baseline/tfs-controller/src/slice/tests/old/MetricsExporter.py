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

import datetime, logging, os, requests
from typing import Any, Literal, Union
from questdb.ingress import Sender, IngressError # pylint: disable=no-name-in-module

LOGGER = logging.getLogger(__name__)

MAX_RETRIES = 10
DELAY_RETRIES = 0.5

MSG_EXPORT_EXECUTED   = '[rest_request] Export(timestamp={:s}, symbols={:s}, columns={:s}) executed'
MSG_EXPORT_FAILED     = '[rest_request] Export(timestamp={:s}, symbols={:s}, columns={:s}) failed, retry={:d}/{:d}...'
MSG_REST_BAD_STATUS   = '[rest_request] Bad Reply url="{:s}" params="{:s}": status_code={:d} content={:s}'
MSG_REST_EXECUTED     = '[rest_request] Query({:s}) executed, result: {:s}'
MSG_REST_FAILED       = '[rest_request] Query({:s}) failed, retry={:d}/{:d}...'
MSG_ERROR_MAX_RETRIES = 'Maximum number of retries achieved: {:d}'

METRICSDB_HOSTNAME  = os.environ.get('METRICSDB_HOSTNAME')
METRICSDB_ILP_PORT  = int(os.environ.get('METRICSDB_ILP_PORT'))
METRICSDB_REST_PORT = int(os.environ.get('METRICSDB_REST_PORT'))
METRICSDB_TABLE_SLICE_GROUPS = 'slice_groups'

COLORS = {
    'platinum': '#E5E4E2',
    'gold'    : '#FFD700',
    'silver'  : '#808080',
    'bronze'  : '#CD7F32',
}
DEFAULT_COLOR = '#000000' # black

class MetricsExporter():
    def __init__(self) -> None:
        pass

    def create_table(self) -> None:
        sql_query = ' '.join([
            'CREATE TABLE IF NOT EXISTS {:s} ('.format(str(METRICSDB_TABLE_SLICE_GROUPS)),
            ','.join([
                'timestamp TIMESTAMP',
                'slice_uuid SYMBOL',
                'slice_group SYMBOL',
                'slice_color SYMBOL',
                'slice_availability DOUBLE',
                'slice_capacity_center DOUBLE',
                'slice_capacity DOUBLE',
            ]),
            ') TIMESTAMP(timestamp);'
        ])
        try:
            result = self.rest_request(sql_query)
            if not result: raise Exception
            LOGGER.info('Table {:s} created'.format(str(METRICSDB_TABLE_SLICE_GROUPS)))
        except Exception as e:
            LOGGER.warning('Table {:s} cannot be created. {:s}'.format(str(METRICSDB_TABLE_SLICE_GROUPS), str(e)))
            raise

    def export_point(
        self, slice_uuid : str, slice_group : str, slice_availability : float, slice_capacity : float,
        is_center : bool = False
    ) -> None:
        dt_timestamp = datetime.datetime.utcnow()
        slice_color = COLORS.get(slice_group, DEFAULT_COLOR)
        symbols = dict(slice_uuid=slice_uuid, slice_group=slice_group, slice_color=slice_color)
        columns = dict(slice_availability=slice_availability)
        columns['slice_capacity_center' if is_center else 'slice_capacity'] = slice_capacity

        for retry in range(MAX_RETRIES):
            try:
                with Sender(METRICSDB_HOSTNAME, METRICSDB_ILP_PORT) as sender:
                    sender.row(METRICSDB_TABLE_SLICE_GROUPS, symbols=symbols, columns=columns, at=dt_timestamp)
                    sender.flush()
                LOGGER.info(MSG_EXPORT_EXECUTED.format(str(dt_timestamp), str(symbols), str(columns)))
                return
            except (Exception, IngressError): # pylint: disable=broad-except
                LOGGER.exception(MSG_EXPORT_FAILED.format(
                    str(dt_timestamp), str(symbols), str(columns), retry+1, MAX_RETRIES))

        raise Exception(MSG_ERROR_MAX_RETRIES.format(MAX_RETRIES))

    def rest_request(self, rest_query : str) -> Union[Any, Literal[True]]:
        url = 'http://{:s}:{:d}/exec'.format(METRICSDB_HOSTNAME, METRICSDB_REST_PORT)
        params = {'query': rest_query, 'fmt': 'json'}

        for retry in range(MAX_RETRIES):
            try:
                response = requests.get(url, params=params)
                status_code = response.status_code
                if status_code not in {200}:
                    str_content = response.content.decode('UTF-8')
                    raise Exception(MSG_REST_BAD_STATUS.format(str(url), str(params), status_code, str_content))

                json_response = response.json()
                if 'ddl' in json_response:
                    LOGGER.info(MSG_REST_EXECUTED.format(str(rest_query), str(json_response['ddl'])))
                    return True
                elif 'dataset' in json_response:
                    LOGGER.info(MSG_REST_EXECUTED.format(str(rest_query), str(json_response['dataset'])))
                    return json_response['dataset']

            except Exception: # pylint: disable=broad-except
                LOGGER.exception(MSG_REST_FAILED.format(str(rest_query), retry+1, MAX_RETRIES))

        raise Exception(MSG_ERROR_MAX_RETRIES.format(MAX_RETRIES))
