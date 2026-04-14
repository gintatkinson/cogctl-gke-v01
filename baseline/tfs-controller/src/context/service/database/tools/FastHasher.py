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

import hashlib
from typing import List, Tuple, Union

# For some models, it is convenient to produce a string hash for fast comparisons of existence or modification. Method
# fast_hasher computes configurable length (between 1 and 64 byte) hashes and retrieves them in hex representation.

FASTHASHER_ITEM_ACCEPTED_FORMAT = 'Union[bytes, str]'
FASTHASHER_DATA_ACCEPTED_FORMAT = 'Union[{fmt:s}, List[{fmt:s}], Tuple[{fmt:s}]]'.format(
    fmt=FASTHASHER_ITEM_ACCEPTED_FORMAT)

def fast_hasher(data : Union[bytes, str, List[Union[bytes, str]], Tuple[Union[bytes, str]]], digest_size : int = 8):
    hasher = hashlib.blake2b(digest_size=digest_size)
    # Do not accept sets, dicts, or other unordered dats tructures since their order is arbitrary thus producing
    # different hashes depending on the order. Consider adding support for sets or dicts with previous sorting of
    # items by their key.

    if isinstance(data, bytes):
        data = [data]
    elif isinstance(data, str):
        data = [data.encode('UTF-8')]
    elif isinstance(data, (list, tuple)):
        pass
    else:
        msg = 'data({:s}) must be {:s}, found {:s}'
        raise TypeError(msg.format(str(data), FASTHASHER_DATA_ACCEPTED_FORMAT, str(type(data))))

    for i,item in enumerate(data):
        if isinstance(item, str):
            item = item.encode('UTF-8')
        elif isinstance(item, bytes):
            pass
        else:
            msg = 'data[{:d}]({:s}) must be {:s}, found {:s}'
            raise TypeError(msg.format(i, str(item), FASTHASHER_ITEM_ACCEPTED_FORMAT, str(type(item))))
        hasher.update(item)
    return hasher.hexdigest()
