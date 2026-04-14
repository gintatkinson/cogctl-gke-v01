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

"""
P4 driver exceptions.
"""


class UserError(Exception):
    """
    User error exception.
    """
    def __init__(self, info=""):
        super().__init__()
        self.info = info

    def __str__(self):
        return self.info

    # TODO: find better way to get a custom traceback  # pylint: disable=W0511
    def _render_traceback_(self):
        return [str(self)]


class InvalidP4InfoError(Exception):
    """
    Invalid P4 info exception.
    """
    def __init__(self, info=""):
        super().__init__()
        self.info = info

    def __str__(self):
        return f"Invalid P4Info message: {self.info}"

    def _render_traceback_(self):
        return [str(self)]


class UnknownOptionName(UserError):
    """
    Unknown option name exception.
    """
    def __init__(self, option_name):
        super().__init__()
        self.option_name = option_name

    def __str__(self):
        return f"Unknown option name: {self.option_name}"


class InvalidOptionValueType(UserError):
    """
    Invalid option value type exception.
    """
    def __init__(self, option, value):
        super().__init__()
        self.option = option
        self.value = value

    def __str__(self):
        return f"Invalid value type for option {self.option.name}. "\
               "Expected {self.option.value.__name__} but got "\
               "value {self.value} with type {type(self.value).__name__}"


class UserBadIPv4Error(UserError):
    """
    Invalid IPv4 address value exception.
    """
    def __init__(self, addr):
        super().__init__()
        self.addr = addr

    def __str__(self):
        return f"{self.addr}' is not a valid IPv4 address"

    def _render_traceback_(self):
        return [str(self)]


class UserBadIPv6Error(UserError):
    """
    Invalid IPv6 address value exception.
    """
    def __init__(self, addr):
        super().__init__()
        self.addr = addr

    def __str__(self):
        return f"'{self.addr}' is not a valid IPv6 address"

    def _render_traceback_(self):
        return [str(self)]


class UserBadMacError(UserError):
    """
    Invalid MAC address value exception.
    """
    def __init__(self, addr):
        super().__init__()
        self.addr = addr

    def __str__(self):
        return f"'{self.addr}' is not a valid MAC address"

    def _render_traceback_(self):
        return [str(self)]


class UserBadValueError(UserError):
    """
    Invalid value exception.
    """
    def __init__(self, info=""):
        super().__init__()
        self.info = info

    def __str__(self):
        return self.info

    def _render_traceback_(self):
        return [str(self)]
