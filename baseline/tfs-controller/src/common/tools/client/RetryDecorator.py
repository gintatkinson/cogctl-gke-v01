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

# This decorator re-executes the decorated function when it raises an exception. It enables to control the maximum
# number of retries, the delay between retries, and to set the execution of a preparation method before every retry.
# The delay is specfied by means of user-customizable functions.
#
# Delay functions should return a compute function with a single parameter, the number of retry. For instance:
#   delay_linear(initial=0, increment=0):
#       adds a constant delay of 0 seconds between retries
#   delay_linear(initial=1, increment=0):
#       adds a constant delay of 1 second between retries
#   delay_linear(initial=1, increment=0.5, maximum=10):
#       adds an increasing delay between retries, starting with 1 second, and incresing it linearly by steps of 0.5
#       seconds, up to 10 seconds, every time an exception is caught within the current execution.
#       E.g. 1.0, 1.5, 2.0, 2.5, ..., 10.0, 10.0, 10.0, ...
#   delay_exponential(initial=1, increment=1): adds a constant delay of 1 second between retries
#   delay_exponential(initial=1, increment=2, maximum=10):
#       adds an increasing delay between retries, starting with 1 second, and incresing it exponentially by steps of 2
#       seconds, up to 10 seconds,  every time an exception is caught within the current execution.
#       E.g. 1.0, 2.0, 4.0, 8.0, 10.0, 10.0, 10.0, ...
#
# Arguments:
# - max_retries: defines the maximum number of retries acceptable before giving up. By default, 0 retries are executed.
# - delay_function: defines the delay computation method to be used. By default, delay_linear with a fixed delay of 0.1
#   seconds is used.
# - prepare_method_name: if not None, defines the name of the preparation method within the same class to be executed
#   when an exception in exceptions is caught, and before running the next retry. By default, is None, meaning that no
#   method is executed.
# - prepare_method_args: defines the list of positional arguments to be provided to the preparation method. If no
#   preparation method is specified, the argument is silently ignored. By default, an empty list is defined.
# - prepare_method_kwargs: defines the dictionary of keyword arguments to be provided to the preparation method. If no
#   preparation method is specified, the argument is silently ignored. By default, an empty dictionary is defined.

import grpc, logging, time
from grpc._channel import _InactiveRpcError

LOGGER = logging.getLogger(__name__)

def delay_linear(initial=0, increment=0, maximum=None):
    def compute(num_try):
        delay = initial + (num_try - 1) * increment
        if maximum is not None:
            delay = max(delay, maximum)
        return delay
    return compute

def delay_exponential(initial=1.0, increment=1.0, maximum=None):
    def compute(num_try):
        delay = initial * pow(increment, (num_try - 1))
        if maximum is not None:
            delay = max(delay, maximum)
        return delay
    return compute

# pylint: disable=dangerous-default-value
def retry(
    max_retries=0, delay_function=delay_linear(initial=0, increment=0),
    prepare_method_name=None, prepare_method_args=list(), prepare_method_kwargs=dict()
):
    def _reconnect(func):
        def wrapper(self, *args, **kwargs):
            if prepare_method_name is not None:
                prepare_method = getattr(self, prepare_method_name, None)
                if prepare_method is None:
                    MSG = 'Prepare Method ({:s}) not found'
                    # pylint: disable=broad-exception-raised
                    raise Exception(MSG.format(prepare_method_name))
            num_try, given_up = 0, False
            while not given_up:
                try:
                    return func(self, *args, **kwargs)
                except (grpc.RpcError, _InactiveRpcError) as e:
                    if e.code() not in [grpc.StatusCode.UNAVAILABLE]: raise

                    num_try += 1
                    given_up = num_try > max_retries
                    if given_up:
                        MSG = '[{:s}:{:s}] Giving up... {:d} tries failed'
                        msg = MSG.format(func.__module__, func.__name__, max_retries)
                        # pylint: disable=broad-exception-raised
                        raise Exception(msg) from e
                    if delay_function is not None:
                        delay = delay_function(num_try)
                        time.sleep(delay)
                        MSG = '[{:s}:{:s}] Retry {:d}/{:d} after {:f} seconds...'
                        LOGGER.info(MSG.format(
                            func.__module__, func.__name__, num_try, max_retries, delay
                        ))
                    else:
                        MSG = '[{:s}:{:s}] Retry {:d}/{:d} immediate...'
                        LOGGER.info(MSG.format(
                            func.__module__, func.__name__, num_try, max_retries
                        ))

                    if prepare_method_name is not None:
                        MSG = '[{:s}:{:s}] Running prepare method...'
                        LOGGER.debug(MSG.format(
                            prepare_method.__module__, prepare_method.__name__
                        ))
                        prepare_method(*prepare_method_args, **prepare_method_kwargs)
        return wrapper
    return _reconnect
