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


import logging, re
from typing import Dict, List, Optional, Union


LOGGER = logging.getLogger(__name__)


class _Callback:
    def __init__(self, path_pattern : Union[str, re.Pattern]) -> None:
        '''
        Initialize a Callback
        @param path_pattern: A regular expression (string or compiled `re.Pattern`)
        '''
        if isinstance(path_pattern, str):
            path_pattern = re.compile('^{:s}/?$'.format(path_pattern))
        self._path_pattern = path_pattern

    def match(self, path : str) -> Optional[re.Match]:
        '''
        Match method used to check if this callback should be executed.
        @param path: A RESTCONF request path to test
        @returns `re.Match` object if pattern fully matches `path`, otherwise `None`
        '''
        return self._path_pattern.fullmatch(path)

    def execute_data_pre_get(
        self, match : re.Match, path : str, old_data : Optional[Dict]
    ) -> bool:
        '''
        Execute the callback action for a matched data path.
        This method should be implemented for each specific callback.
        @param match: `re.Match` object returned by `match()`.
        @param path: Original request path that was matched.
        @param old_data: Resource representation before retrieval, if applicable, otherwise `None`
        @returns boolean indicating whether additional callbacks should be executed, defaults to False
        '''
        MSG = 'match={:s}, path={:s}, old_data={:s}'
        msg = MSG.format(match.groupdict(), path, old_data)
        raise NotImplementedError(msg)

    def execute_data_update(
        self, match : re.Match, path : str, old_data : Optional[Dict],
        new_data : Optional[Dict]
    ) -> bool:
        '''
        Execute the callback action for a matched data path.
        This method should be implemented for each specific callback.
        @param match: `re.Match` object returned by `match()`.
        @param path: Original request path that was matched.
        @param old_data: Resource representation before change, if applicable, otherwise `None`
        @param new_data: Resource representation after change, if applicable, otherwise `None`
        @returns boolean indicating whether additional callbacks should be executed, defaults to False
        '''
        MSG = 'match={:s}, path={:s}, old_data={:s}, new_data={:s}'
        msg = MSG.format(match.groupdict(), path, old_data, new_data)
        raise NotImplementedError(msg)

    def execute_operation(
        self, match : re.Match, path : str, input_data : Optional[Dict]
    ) -> Optional[Dict]:
        '''
        Execute the callback action for a matched operation path.
        This method should be implemented for each specific callback.
        @param match: `re.Match` object returned by `match()`.
        @param path: Original request path that was matched.
        @param input_data: Input data, if applicable, otherwise `None`
        @returns Optional[Dict] containing output data, defaults to None
        '''
        MSG = 'match={:s}, path={:s}, input_data={:s}'
        msg = MSG.format(match.groupdict(), path, input_data)
        raise NotImplementedError(msg)


class CallbackDispatcher:
    def __init__(self):
        self._callbacks : List[_Callback] = list()

    def register(self, callback : _Callback) -> None:
        self._callbacks.append(callback)

    def dispatch_data_pre_get(
        self, path : str, old_data : Optional[Dict] = None
    ) -> None:
        LOGGER.warning('[dispatch_data_pre_get] Checking Callbacks for path={:s}'.format(str(path)))
        for callback in self._callbacks:
            match = callback.match(path)
            if match is None: continue
            keep_running_callbacks = callback.execute_data_pre_get(match, path, old_data)
            if not keep_running_callbacks: break

    def dispatch_data_update(
        self, path : str, old_data : Optional[Dict] = None, new_data : Optional[Dict] = None
    ) -> None:
        LOGGER.warning('[dispatch_data_update] Checking Callbacks for path={:s}'.format(str(path)))
        for callback in self._callbacks:
            match = callback.match(path)
            if match is None: continue
            keep_running_callbacks = callback.execute_data_update(match, path, old_data, new_data)
            if not keep_running_callbacks: break

    def dispatch_operation(
        self, path : str, input_data : Optional[Dict] = None
    ) -> Optional[Dict]:
        LOGGER.warning('[dispatch_operation] Checking Callbacks for path={:s}'.format(str(path)))

        # First matching callback is executed, and its output returned.
        for callback in self._callbacks:
            match = callback.match(path)
            if match is None: continue
            output_data = callback.execute_operation(match, path, input_data)
            return output_data

        # If no callback found, raise NotImplemented exception
        MSG = 'Callback for operation ({:s}) not defined'
        raise NotImplementedError(MSG.format(str(path)))


# ===== EXAMPLE ==========================================================================================

class CallbackOnNetwork(_Callback):
    def __init__(self) -> None:
        pattern = r'/restconf/data'
        pattern += r'/ietf-network:networks/network=(?P<network_id>[^/]+)'
        super().__init__(pattern)

    def execute_data_update(
        self, match : re.Match, path : str, old_data : Optional[Dict],
        new_data : Optional[Dict]
    ) -> bool:
        print('[on_network]', match.groupdict(), path, old_data, new_data)
        return False

class CallbackOnNode(_Callback):
    def __init__(self) -> None:
        pattern = r'/restconf/data'
        pattern += r'/ietf-network:networks/network=(?P<network_id>[^/]+)'
        pattern += r'/node=(?P<node_id>[^/]+)'
        super().__init__(pattern)

    def execute_data_update(
        self, match : re.Match, path : str, old_data : Optional[Dict],
        new_data : Optional[Dict]
    ) -> bool:
        print('[on_node]', match.groupdict(), path, old_data, new_data)
        return False

class CallbackOnLink(_Callback):
    def __init__(self) -> None:
        pattern = r'/restconf/data'
        pattern += r'/ietf-network:networks/network=(?P<network_id>[^/]+)'
        pattern += r'/ietf-network-topology:link=(?P<link_id>[^/]+)'
        super().__init__(pattern)

    def execute_data_update(
        self, match : re.Match, path : str, old_data : Optional[Dict],
        new_data : Optional[Dict]
    ) -> bool:
        print('[on_link]', match.groupdict(), path, old_data, new_data)
        return False

class CallbackShutdown(_Callback):
    def __init__(self) -> None:
        pattern = r'/restconf/operations'
        pattern += r'/shutdown'
        super().__init__(pattern)

    def execute_operation(
        self, match : re.Match, path : str, input_data : Optional[Dict]
    ) -> bool:
        print('[shutdown]', match.groupdict(), path, input_data)
        return {'state': 'processing'}

def main() -> None:
    callbacks = CallbackDispatcher()
    callbacks.register(CallbackOnNetwork())
    callbacks.register(CallbackOnNode())
    callbacks.register(CallbackOnLink())
    callbacks.register(CallbackShutdown())

    callbacks.dispatch_data_update('/restconf/data/ietf-network:networks/network=admin')
    callbacks.dispatch_data_update('/restconf/data/ietf-network:networks/network=admin/node=P-PE2')
    callbacks.dispatch_data_update('/restconf/data/ietf-network:networks/network=admin/ietf-network-topology:link=L6')
    callbacks.dispatch_data_update('/restconf/data/ietf-network:networks/network=admin/')
    callbacks.dispatch_data_update('/restconf/data/ietf-network:networks/network=admin/node=P-PE1/')
    callbacks.dispatch_data_update('/restconf/data/ietf-network:networks/network=admin/ietf-network-topology:link=L4/')
    callbacks.dispatch_operation('/restconf/operations/shutdown/')

if __name__ == '__main__':
    main()
