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


ADDLIGHTPATH_REPLY = {
  "flow_id": 1,
  "src": "t1",
  "dst": "t2",
  "bitrate": 100,
  "bidir": 1,
  "flows": {
    "t1": [
      {
        "in": 0,
        "out": "1"
      },
      {
        "in": "1",
        "out": 0
      }
    ],
    "r1": [
      {
        "in": "101R",
        "out": "1T"
      },
      {
        "in": "1R",
        "out": "101T"
      }
    ],
    "r2": [
      {
        "in": "1R",
        "out": "101T"
      },
      {
        "in": "101R",
        "out": "1T"
      }
    ],
    "t2": [
      {
        "in": "1",
        "out": 0
      },
      {
        "in": 0,
        "out": "1"
      }
    ]
  },
  "band_type": "c_slots",
  "slots": [
    1,
    2,
    3,
    4
  ],
  "fiber_forward": {
    "t1-r1": "M1",
    "r1-r2": "d1-1",
    "r2-t2": "S1"
  },
  "fiber_backward": {
    "r1-t1": "S1",
    "r2-r1": "d1-1",
    "t2-r2": "M1"
  },
  "op-mode": 1,
  "n_slots": 4,
  "links": [
    "t1-r1",
    "r1-r2",
    "r2-t2"
  ],
  "path": [
    "t1",
    "r1",
    "r2",
    "t2"
  ],
  "band": 50,
  "freq": 192031.25,
  "is_active": True
}

