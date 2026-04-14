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

class UnsatisfiedFilterException(Exception):
    def __init__(self, filter_fields):
        msg = 'No Driver satisfies FilterFields({:s})'
        super().__init__(msg.format(str(filter_fields)))

class AmbiguousFilterException(Exception):
    def __init__(self, filter_fields, compatible_drivers):
        msg = 'Multiple Drivers satisfy FilterFields({:s}): {:s}'
        super().__init__(msg.format(str(filter_fields), str(compatible_drivers)))

class UnsupportedDriverClassException(Exception):
    def __init__(self, driver_class_name):
        msg = 'Class({:s}) is not a subclass of _Driver'
        super().__init__(msg.format(str(driver_class_name)))

class EmptyFilterFieldException(Exception):
    def __init__(self, filter_fields, driver_class_name=None):
        if driver_class_name:
            msg = 'Empty FilterField({:s}) specified by Driver({:s}) is not supported'
            msg = msg.format(str(filter_fields), str(driver_class_name))
        else:
            msg = 'Empty FilterField({:s}) is not supported'
            msg = msg.format(str(filter_fields))
        super().__init__(msg)

class UnsupportedFilterFieldException(Exception):
    def __init__(self, unsupported_filter_fields, driver_class_name=None):
        if driver_class_name:
            msg = 'FilterFields({:s}) specified by Driver({:s}) are not supported'
            msg = msg.format(str(unsupported_filter_fields), str(driver_class_name))
        else:
            msg = 'FilterFields({:s}) specified in Filter are not supported'
            msg = msg.format(str(unsupported_filter_fields))
        super().__init__(msg)

class UnsupportedFilterFieldValueException(Exception):
    def __init__(self, filter_field_name, filter_field_value, allowed_filter_field_values, driver_class_name=None):
        if driver_class_name:
            msg = 'FilterField({:s}={:s}) specified by Driver({:s}) is not supported. Allowed values are {:s}'
            msg = msg.format(
                str(filter_field_name), str(filter_field_value), str(driver_class_name),
                str(allowed_filter_field_values))
        else:
            msg = 'FilterField({:s}={:s}) specified in Filter is not supported. Allowed values are {:s}'
            msg = msg.format(str(filter_field_name), str(filter_field_value), str(allowed_filter_field_values))
        super().__init__(msg)

class DriverInstanceCacheTerminatedException(Exception):
    def __init__(self):
        msg = 'DriverInstanceCache is terminated. No new instances can be processed.'
        super().__init__(msg)

class UnsupportedResourceKeyException(Exception):
    def __init__(self, resource_key):
        msg = 'ResourceKey({:s}) not supported'
        msg = msg.format(str(resource_key))
        super().__init__(msg)

class ConfigFieldNotFoundException(Exception):
    def __init__(self, config_field_name):
        msg = 'ConfigField({:s}) not specified in resource'
        msg = msg.format(str(config_field_name))
        super().__init__(msg)

class ConfigFieldsNotSupportedException(Exception):
    def __init__(self, config_fields):
        msg = 'ConfigFields({:s}) not supported in resource'
        msg = msg.format(str(config_fields))
        super().__init__(msg)
