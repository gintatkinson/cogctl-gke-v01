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

import queue
from typing import Any, Iterator, List, Optional, Tuple, Union

# Special resource names to request to the collector to retrieve the specified
# configuration/structural resources.
# These resource names should be used with GetConfig() method.
RESOURCE_ENDPOINTS         = '__endpoints__'
RESOURCE_INTERFACES        = '__interfaces__'
RESOURCE_NETWORK_INSTANCES = '__network_instances__'
RESOURCE_ROUTING_POLICIES  = '__routing_policies__'
RESOURCE_SERVICES          = '__services__'
RESOURCE_ACL               = '__acl__'
RESOURCE_INVENTORY         = '__inventory__'
RESOURCE_RULES             = "__rules__"

class _Collector:
    def __init__(self, name : str, address: str, port: int, **settings) -> None:
        """ Initialize Collector.
            Parameters:
                address : str
                    The address of the device
                port : int
                    The port of the device
                **settings
                    Extra settings required by the collector.
        """
        self._name     = name
        self._address  = address
        self._port     = port
        self._settings = settings

    @property
    def name(self): return self._name

    @property
    def address(self): return self._address

    @property
    def port(self): return self._port

    @property
    def settings(self): return self._settings

    def Connect(self) -> bool:
        """ Connect to the Device.
            Returns:
                succeeded : bool
                    Boolean variable indicating if connection succeeded.
        """
        raise NotImplementedError()

    def Disconnect(self) -> bool:
        """ Disconnect from the Device.
            Returns:
                succeeded : bool
                    Boolean variable indicating if disconnection succeeded.
        """
        raise NotImplementedError()

    # def GetInitialConfig(self) -> List[Tuple[str, Any]]:
    #     """ Retrieve initial configuration of entire device.
    #         Returns:
    #             values : List[Tuple[str, Any]]
    #                 List of tuples (resource key, resource value) for
    #                 resource keys.
    #     """
    #     raise NotImplementedError()

    # def GetConfig(self, resource_keys: List[str] = []) -> \
    #         List[Tuple[str, Union[Any, None, Exception]]]:
    #     """ Retrieve running configuration of entire device or
    #     selected resource keys.
    #         Parameters:
    #             resource_keys : List[str]
    #                 List of keys pointing to the resources to be retrieved.
    #         Returns:
    #             values : List[Tuple[str, Union[Any, None, Exception]]]
    #                 List of tuples (resource key, resource value) for
    #                 resource keys requested. If a resource is found,
    #                 the appropriate value type must be retrieved.
    #                 If a resource is not found, None must be retrieved as
    #                 value for that resource. In case of Exception,
    #                 the Exception must be retrieved as value.
    #     """
    #     raise NotImplementedError()

    # def SetConfig(self, resources: List[Tuple[str, Any]]) -> \
    #         List[Union[bool, Exception]]:
    #     """ Create/Update configuration for a list of resources.
    #         Parameters:
    #             resources : List[Tuple[str, Any]]
    #                 List of tuples, each containing a resource_key pointing the
    #                 resource to be modified, and a resource_value containing
    #                 the new value to be set.
    #         Returns:
    #             results : List[Union[bool, Exception]]
    #                 List of results for resource key changes requested.
    #                 Return values must be in the same order as the
    #                 resource keys requested. If a resource is properly set,
    #                 True must be retrieved; otherwise, the Exception that is
    #                 raised during the processing must be retrieved.
    #     """
    #     raise NotImplementedError()

    # def DeleteConfig(self, resources: List[Tuple[str, Any]]) -> \
    #         List[Union[bool, Exception]]:
    #     """ Delete configuration for a list of resources.
    #         Parameters:
    #             resources : List[Tuple[str, Any]]
    #                 List of tuples, each containing a resource_key pointing the
    #                 resource to be modified, and a resource_value containing
    #                 possible additionally required values to locate
    #                 the value to be removed.
    #         Returns:
    #             results : List[Union[bool, Exception]]
    #                 List of results for resource key deletions requested.
    #                 Return values must be in the same order as the resource keys
    #                 requested. If a resource is properly deleted, True must be
    #                 retrieved; otherwise, the Exception that is raised during
    #                 the processing must be retrieved.
    #     """
    #     raise NotImplementedError()

    def SubscribeState(self, subscriptions: List[Tuple[str, dict, float, float]]) -> \
                List[Union[bool, Exception]]:
        """ Subscribe to state information of the entire device or selected resources. 
            Subscriptions are incremental, and the collector should keep track of requested resources.
                    List of tuples, each containing:
                        - resource_id (str): Identifier pointing to the resource to be subscribed.
                        - resource_dict (dict): Dictionary containing resource name, KPI to be subscribed, and type.
                        - sampling_duration (float): Duration (in seconds) for how long monitoring should last.
                        - sampling_interval (float): Desired monitoring interval (in seconds) for the specified resource.
                    List of results for the requested resource key subscriptions. 
                    The return values are in the same order as the requested resource keys.
                    - True if a resource is successfully subscribed.
                    - Exception if an error occurs during the subscription process.
            List[Union[bool, Exception]]:
        """
        raise NotImplementedError()

    def UnsubscribeState(self, resource_key: str) \
            -> bool:
        """ Unsubscribe from state information of entire device
        or selected resources. Subscriptions are incremental.
            Collector should keep track of requested resources.
            Parameters:
                subscriptions : List[str]
                    List of tuples, each containing a resource_key pointing the
                    resource to be subscribed, a sampling_duration, and a
                    sampling_interval (both in seconds with float
                    representation) defining, respectively, for how long
                    monitoring should last, and the desired monitoring interval
                    for the resource specified.
            Returns:
                results : List[Union[bool, Exception]]
                    List of results for resource key un-subscriptions requested.
                    Return values must be in the same order as the resource keys
                    requested. If a resource is properly unsubscribed,
                    True must be retrieved; otherwise, the Exception that is
                    raised during the processing must be retrieved.
        """
        raise NotImplementedError()

    def GetState(
        self, duration : int, blocking=False, terminate: Optional[queue.Queue] = None
    ) -> Iterator[Tuple[float, str, Any]]:
        """ Retrieve last collected values for subscribed resources.
        Operates as a generator, so this method should be called once and will
        block until values are available. When values are available,
        it should yield each of them and block again until new values are
        available. When the collector is destroyed, GetState() can return instead
        of yield to terminate the loop.
        Terminate enables to request interruption of the generation.
            Examples:
                # keep looping waiting for extra samples (generator loop)
                terminate = threading.Event()
                i = 0
                for timestamp,resource_key,resource_value in my_collector.GetState(blocking=True, terminate=terminate):
                    process(timestamp, resource_key, resource_value)
                    i += 1
                    if i == 10: terminate.set()

                # just retrieve accumulated samples
                samples = my_collector.GetState(blocking=False, terminate=terminate)
                # or (as classical loop)
                i = 0
                for timestamp,resource_key,resource_value in my_collector.GetState(blocking=False, terminate=terminate):
                    process(timestamp, resource_key, resource_value)
                    i += 1
                    if i == 10: terminate.set()
            Parameters:
                blocking : bool
                    Select the collector behaviour. In both cases, the collector will
                    first retrieve the samples accumulated and available in the
                    internal queue. Then, if blocking, the collector does not
                    terminate the loop and waits for additional samples to come,
                    thus behaving as a generator. If non-blocking, the collector
                    terminates the loop and returns. Non-blocking behaviour can
                    be used for periodically polling the collector, while blocking
                    can be used when a separate thread is in charge of
                    collecting the samples produced by the collector.
                terminate : threading.Event
                    Signals the interruption of the GetState method as soon as
                    possible.
            Returns:
                results : Iterator[Tuple[float, str, Any]]
                    Sequences of state sample. Each State sample contains a
                    float Unix-like timestamps of the samples in seconds with up
                    to microsecond resolution, the resource_key of the sample,
                    and its resource_value.
                    Only resources with an active subscription must be
                    retrieved. Interval and duration of the sampling process are
                    specified when creating the subscription using method
                    SubscribeState(). Order of values yielded is arbitrary.
        """
        raise NotImplementedError()
