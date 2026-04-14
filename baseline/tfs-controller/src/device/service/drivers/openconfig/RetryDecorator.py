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

import logging, time
from common.tools.client.RetryDecorator import delay_linear

LOGGER = logging.getLogger(__name__)

def retry(max_retries=0, delay_function=delay_linear(initial=0, increment=0),
          prepare_method_name=None, prepare_method_args=[], prepare_method_kwargs={}):
    def _reconnect(func):
        def wrapper(self, *args, **kwargs):
            if prepare_method_name is not None:
                prepare_method = getattr(self, prepare_method_name, None)
                if prepare_method is None: raise Exception('Prepare Method ({}) not found'.format(prepare_method_name))
            num_try, given_up = 0, False
            while not given_up:
                try:
                    return func(self, *args, **kwargs)
                except OSError as e:
                    if str(e) != 'Socket is closed': raise

                    num_try += 1
                    given_up = num_try > max_retries
                    if given_up: raise Exception('Giving up... {:d} tries failed'.format(max_retries)) from e
                    if delay_function is not None:
                        delay = delay_function(num_try)
                        time.sleep(delay)
                        LOGGER.info('Retry {:d}/{:d} after {:f} seconds...'.format(num_try, max_retries, delay))
                    else:
                        LOGGER.info('Retry {:d}/{:d} immediate...'.format(num_try, max_retries))

                    if prepare_method_name is not None: prepare_method(*prepare_method_args, **prepare_method_kwargs)
        return wrapper
    return _reconnect
