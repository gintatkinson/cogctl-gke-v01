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
P4Runtime global options.
"""

import enum
try:
    from .p4_exception import UnknownOptionName, InvalidOptionValueType
except ImportError:
    from p4_exception import UnknownOptionName, InvalidOptionValueType


@enum.unique
class Options(enum.Enum):
    """
    P4 options.
    """
    canonical_bytestrings = bool


class GlobalOptions:
    """
    P4 global options.
    """
    option_defaults = {
        Options.canonical_bytestrings: True,
    }

    option_helpstrings = {
        Options.canonical_bytestrings: """
Use byte-padded legacy format for binary strings sent to the P4Runtime server,
instead of the canonical representation. See P4Runtime specification for
details.
"""
    }

    def __init__(self):
        self._values = {}
        self.reset()
        self._option_names = [option.name for option in Options]
        self._set_docstring()

    def reset(self):
        """
        Reset all options to their defaults.

        :return: void
        """
        for option in Options:
            assert option in GlobalOptions.option_defaults
            self._values[option] = GlobalOptions.option_defaults[option]

    def _supported_options_as_str(self):
        """
        Return a comma-separated string of supported options.

        :return: string of supported options
        """
        return ", ".join([f"{o.name} ({o.value.__name__})" for o in Options])

    def _supported_options_as_str_verbose(self):
        """
        Return a detailed comma-separated string of supported options.

        :return: string of supported options
        """
        opt_str = ""
        for option in Options:
            opt_str += f"Option name: {option.name}\n"
            opt_str += f"Type: {option.value.__name__}\n"
            opt_str += f"Default value: " \
                       f"{GlobalOptions.option_defaults[option]}\n"
            opt_str += f"Description: " \
                   f"{GlobalOptions.option_helpstrings.get(option, 'N/A')}\n"
            opt_str += "\n"
        return opt_str[:-1]

    def _set_docstring(self):
        """
        Set the documentation for this object.

        :return: void
        """
        self.__doc__ = f"""
Manage global options for the P4Runtime shell.
Supported options are: {self._supported_options_as_str()}
To set the value of a global option, use GLOBAL_OPTIONS["<option name>"] = <option value>
To access the current value of a global option, use GLOBAL_OPTIONS.["<option name>"]
To reset all options to their default value, use GLOBAL_OPTIONS.reset

{self._supported_options_as_str_verbose()}
"""

    def __dir__(self):
        """
        Return all names in this scope.

        :return: list of names in scope
        """
        return ["reset", "set", "get"]

    def set_option(self, option, value):
        """
        Set an option's value.

        :param option: option to set
        :param value: option value
        :return: void
        """
        self._values[option] = value

    def get_option(self, option):
        """
        Get an option's value.

        :param option: option to get
        :return: option value
        """
        return self._values[option]

    def set(self, name, value):
        """
        Create an option and set its value.

        :param name: option name
        :param value: option value
        :return: void
        """
        try:
            option = Options[name]
        except KeyError as ex:
            raise UnknownOptionName(name) from ex
        if not isinstance(value, option.value):
            raise InvalidOptionValueType(option, value)
        self.set_option(option, value)

    def get(self, name):
        """
        Get option by name.

        :param name: option name
        :return: option
        """
        try:
            option = Options[name]
        except KeyError as ex:
            raise UnknownOptionName(name) from ex
        return self.get_option(option)

    def __setitem__(self, name, value):
        self.set(name, value)

    def __getitem__(self, name):
        return self.get(name)

    def __str__(self):
        return '\n'.join([f"{o.name}: {v}" for o, v in self._values.items()])


GLOBAL_OPTIONS = GlobalOptions()


def to_canonical_bytes(bytes_):
    """
    Convert to canonical bytes.

    :param bytes_: byte stream
    :return: canonical bytes
    """
    if len(bytes_) == 0:
        return bytes_
    num_zeros = 0
    for byte in bytes_:
        if byte != 0:
            break
        num_zeros += 1
    if num_zeros == len(bytes_):
        return bytes_[:1]
    return bytes_[num_zeros:]


def make_canonical_if_option_set(bytes_):
    """
    Convert to canonical bytes if option is set.

    :param bytes_: byte stream
    :return: canonical bytes
    """

    # TODO: Fix canonical representation issue
    # if GLOBAL_OPTIONS.get_option(Options.canonical_bytestrings):
    #     return to_canonical_bytes(bytes_)
    return bytes_
