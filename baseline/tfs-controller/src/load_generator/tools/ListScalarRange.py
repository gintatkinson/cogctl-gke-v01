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

import random
from typing import List, Optional, Tuple, Union

from common.proto.load_generator_pb2 import ScalarOrRange

# RegEx to validate strings formatted as: '1, 2.3, 4.5  .. 6.7 , .8...9, 10., .11'
# IMPORTANT: this regex just validates data, it does not extract the pieces of data!
RE_FLOAT = r'[\ ]*[0-9]*[\.]?[0-9]*[\ ]*'
RE_RANGE = RE_FLOAT + r'(\.\.' + RE_FLOAT + r')?'
RE_SCALAR_RANGE_LIST  = RE_RANGE + r'(\,' + RE_RANGE + r')*'

Type_ListScalarRange = List[Union[float, Tuple[float, float]]]

def parse_list_scalar_range(value : str) -> Type_ListScalarRange:
    str_value = str(value).replace(' ', '')
    ranges = [[float(value) for value in item.split('..')] for item in str_value.split(',')]
    return ranges

def list_scalar_range__list_to_grpc(list_scalar_range : Type_ListScalarRange, obj : List[ScalarOrRange]) -> None:
    for i,scalar_or_range in enumerate(list_scalar_range):
        if isinstance(scalar_or_range, (float, str)):
            _scalar = obj.add()
            _scalar.scalar = float(scalar_or_range)
        elif isinstance(scalar_or_range, (list, tuple)):
            if len(scalar_or_range) == 1:
                _scalar = obj.add()
                _scalar.scalar = float(scalar_or_range[0])
            elif len(scalar_or_range) == 2:
                _range = obj.add()
                _range.range.minimum = float(scalar_or_range[0])
                _range.range.maximum = float(scalar_or_range[1])
            else:
                MSG = 'List/tuple with {:d} items in item(#{:d}, {:s})'
                raise NotImplementedError(MSG.format(len(scalar_or_range), i, str(scalar_or_range)))
        else:
            MSG = 'Type({:s}) in item(#{:d}, {:s})'
            raise NotImplementedError(MSG.format(str(type(scalar_or_range), i, str(scalar_or_range))))

def list_scalar_range__grpc_to_str(obj : List[ScalarOrRange]) -> str:
    str_items = list()
    for item in obj:
        item_kind = item.WhichOneof('value')
        if item_kind == 'scalar':
            str_items.append(str(item.scalar))
        elif item_kind == 'range':
            str_items.append('{:s}..{:s}'.format(str(item.range.minimum), str(item.range.maximum)))
        else:
            raise NotImplementedError('Unsupported ScalarOrRange kind({:s})'.format(str(item_kind)))
    return ','.join(str_items)

def list_scalar_range__grpc_to_list(obj : List[ScalarOrRange]) -> Type_ListScalarRange:
    list_scalar_range = list()
    for item in obj:
        item_kind = item.WhichOneof('value')
        if item_kind == 'scalar':
            scalar_or_range = float(item.scalar)
        elif item_kind == 'range':
            scalar_or_range = (float(item.range.minimum), float(item.range.maximum))
        else:
            raise NotImplementedError('Unsupported ScalarOrRange kind({:s})'.format(str(item_kind)))
        list_scalar_range.append(scalar_or_range)
    return list_scalar_range

def generate_value(
    list_scalar_range : Type_ListScalarRange, ndigits : Optional[int] = None
) -> float:
    scalar_or_range = random.choice(list_scalar_range)
    if isinstance(scalar_or_range, (float, str)):
        value = float(scalar_or_range)
    elif isinstance(scalar_or_range, (list, tuple)):
        if len(scalar_or_range) == 1:
            value = float(scalar_or_range[0])
        elif len(scalar_or_range) == 2:
            minimum = float(scalar_or_range[0])
            maximum = float(scalar_or_range[1])
            value = random.uniform(minimum, maximum)
        else:
            MSG = 'List/tuple with {:d} items in item({:s})'
            raise NotImplementedError(MSG.format(len(scalar_or_range), str(scalar_or_range)))
    else:
        MSG = 'Type({:s}) in item({:s})'
        raise NotImplementedError(MSG.format(str(type(scalar_or_range), str(scalar_or_range))))

    if ndigits is None: return value
    return round(value, ndigits=ndigits)
