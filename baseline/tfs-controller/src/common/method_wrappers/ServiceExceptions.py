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

import grpc
from typing import Iterable, List, Tuple, Union

class ServiceException(Exception):
    def __init__(
        self, code : grpc.StatusCode, details : str, extra_details : Union[str, Iterable[str]] = []
    ) -> None:
        self.code = code
        if isinstance(extra_details, str): extra_details = [extra_details]
        self.details = '; '.join([str(item) for item in ([details] + extra_details)])
        super().__init__(self.details)

class NotFoundException(ServiceException):
    def __init__(
        self, object_name : str, object_uuid: str, extra_details : Union[str, Iterable[str]] = []
    ) -> None:
        details = '{:s}({:s}) not found'.format(str(object_name), str(object_uuid))
        super().__init__(grpc.StatusCode.NOT_FOUND, details, extra_details=extra_details)

class AlreadyExistsException(ServiceException):
    def __init__(
        self, object_name : str, object_uuid: str, extra_details : Union[str, Iterable[str]] = []
    ) -> None:
        details = '{:s}({:s}) already exists'.format(str(object_name), str(object_uuid))
        super().__init__(grpc.StatusCode.ALREADY_EXISTS, details, extra_details=extra_details)

class InvalidArgumentException(ServiceException):
    def __init__(
        self, argument_name : str, argument_value: str, extra_details : Union[str, Iterable[str]] = []
    ) -> None:
        details = '{:s}({:s}) is invalid'.format(str(argument_name), str(argument_value))
        super().__init__(grpc.StatusCode.INVALID_ARGUMENT, details, extra_details=extra_details)

class InvalidArgumentsException(ServiceException):
    def __init__(
        self, arguments : List[Tuple[str, str]], extra_details : Union[str, Iterable[str]] = []
    ) -> None:
        str_arguments = ', '.join(['{:s}({:s})'.format(name, value) for name,value in arguments])
        details = 'Arguments {:s} are invalid'.format(str_arguments)
        super().__init__(grpc.StatusCode.INVALID_ARGUMENT, details, extra_details=extra_details)

class OperationFailedException(ServiceException):
    def __init__(
        self, operation : str, extra_details : Union[str, Iterable[str]] = []
    ) -> None:
        details = 'Operation({:s}) failed'.format(str(operation))
        super().__init__(grpc.StatusCode.INTERNAL, details, extra_details=extra_details)

class NotImplementedException(ServiceException):
    def __init__(
        self, operation : str, extra_details : Union[str, Iterable[str]] = []
    ) -> None:
        details = 'Operation({:s}) not implemented'.format(str(operation))
        super().__init__(grpc.StatusCode.UNIMPLEMENTED, details, extra_details=extra_details)
