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

import logging, pytest
from context.service.database.tools.FastHasher import (
    FASTHASHER_DATA_ACCEPTED_FORMAT, FASTHASHER_ITEM_ACCEPTED_FORMAT, fast_hasher)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


# ----- Test misc. Context internal tools ------------------------------------------------------------------------------

def test_tools_fast_string_hasher():
    with pytest.raises(TypeError) as e:
        fast_hasher(27)
    assert str(e.value) == "data(27) must be " + FASTHASHER_DATA_ACCEPTED_FORMAT + ", found <class 'int'>"

    with pytest.raises(TypeError) as e:
        fast_hasher({27})
    assert str(e.value) == "data({27}) must be " + FASTHASHER_DATA_ACCEPTED_FORMAT + ", found <class 'set'>"

    with pytest.raises(TypeError) as e:
        fast_hasher({'27'})
    assert str(e.value) == "data({'27'}) must be " + FASTHASHER_DATA_ACCEPTED_FORMAT + ", found <class 'set'>"

    with pytest.raises(TypeError) as e:
        fast_hasher([27])
    assert str(e.value) == "data[0](27) must be " + FASTHASHER_ITEM_ACCEPTED_FORMAT + ", found <class 'int'>"

    fast_hasher('hello-world')
    fast_hasher('hello-world'.encode('UTF-8'))
    fast_hasher(['hello', 'world'])
    fast_hasher(('hello', 'world'))
    fast_hasher(['hello'.encode('UTF-8'), 'world'.encode('UTF-8')])
    fast_hasher(('hello'.encode('UTF-8'), 'world'.encode('UTF-8')))
