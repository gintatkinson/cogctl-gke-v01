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
# 

reply_bid_txt = """
{
  "flow_id": 1,
  "src": "T1",
  "dst": "T2",
  "bitrate": 100,
  "bidir": 1,
  "flows": {
    "T1": {
      "f": {
        "in": "0",
        "out": "1"
      },
      "b": {
        "in": "1",
        "out": "0"
      }
    },
    "R1": {
      "f": {
        "in": "12",
        "out": "3"
      },
      "b": {
        "in": "13",
        "out": "2"
      }
    },
    "R2": {
      "f": {
        "in": "14",
        "out": "5"
      },
      "b": {
        "in": "15",
        "out": "4"
      }
    },
    "T2": {
      "f": {
        "in": "6",
        "out": "0"
      },
      "b": {
        "in": "0",
        "out": "6"
      }
    }
  },
  "band_type": "c_slots",
  "slots": [
    1,
    2,
    3,
    4
  ],
  "fiber_forward": {
    "T1-R1": "M1",
    "R2-T2": "S1"
  },
  "fiber_backward": {
    "R1-T1": "S1",
    "T2-R2": "M1"
  },
  "op-mode": 1,
  "n_slots": 4,
  "links": [
    "T1-R1",
    "R2-T2"
  ],
  "path": [
    "R1",
    "R2"
  ],
  "band": 50000,
  "freq": 192031250,
  "is_active": true,
  "parent_opt_band": 1,
  "new_optical_band": 1
}
  """
  
optical_band_bid_txt = """
{
  "optical_band_id": 1,
  "bidir": 1,
  "src": "R1",
  "dst": "R2",
  "flows": {
    "R1": {
      "f": {
        "in": "0", 
        "out": "3" 
      },
      "b": {
        "in": "13",
        "out": "0"
      }
    },
    "R2": {
      "f": {
        "in": "14",
        "out": "0"
      },
      "b": {
        "in": "0",
        "out": "4"
      }
    }
  },
  "band_type": "c_slots",
  "fiber_forward": {
    "R1-R2": "d1-1"
  },
  "fiber_backward": {
    "R2-R1": "d1-1"
  },
  "op-mode": 0,
  "n_slots": 16,
  "links": [
    "R1-R2"
  ],
  "path": [
    "R1",
    "R2"
  ],
  "band": 200000,
  "freq": 192106250,
  "is_active": true,
  "src_port": "101",
  "dst_port": "201",
  "rev_dst_port": "201",
  "rev_src_port": "101",
  "c_slots": [
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16
  ],
  "served_lightpaths": [
    1
  ]
}
  """

reply_uni_txt = """
{
  "flow_id": 2,
  "src": "T1",
  "dst": "T2",
  "bitrate": 100,
  "bidir": 0,
  "flows": {
    "T1": {
      "f": {
        "in": "0",
        "out": "1"
      },
      "b": {
        "in": "1",
        "out": "0"
      }
    },
    "R1": {
      "f": {
        "in": "12",
        "out": "3"
      },
      "b": {
        "in": "13",
        "out": "2"
      }
    },
    "R2": {
      "f": {
        "in": "14",
        "out": "5"
      },
      "b": {
        "in": "15",
        "out": "4"
      }
    },
    "T2": {
      "f": {
        "in": "6",
        "out": "0"
      },
      "b": {
        "in": "0",
        "out": "6"
      }
    }
  },
  "band_type": "c_slots",
  "slots": [
    1,
    2,
    3,
    4
  ],
  "fiber_forward": {
    "T1-R1": "M1",
    "R2-T2": "S1"
  },
  "fiber_backward": {
    "R1-T1": "S1",
    "T2-R2": "M1"
  },
  "op-mode": 1,
  "n_slots": 4,
  "links": [
    "T1-R1",
    "R2-T2"
  ],
  "path": [
    "R1",
    "R2"
  ],
  "band": 50000,
  "freq": 192031250,
  "is_active": true,
  "parent_opt_band": 2,
  "new_optical_band": 1
}
  """
  
optical_band_uni_txt = """
{
  "optical_band_id": 2,
  "bidir": 0,
  "src": "R1",
  "dst": "R2",
  "flows": {
    "R1": {
      "f": {
        "in": "0", 
        "out": "3" 
      },
      "b": {
        "in": "13",
        "out": "0"
      }
    },
    "R2": {
      "f": {
        "in": "14",
        "out": "0"
      },
      "b": {
        "in": "0",
        "out": "4"
      }
    }
  },
  "band_type": "c_slots",
  "fiber_forward": {
    "R1-R2": "d1-1"
  },
  "fiber_backward": {
    "R2-R1": "d1-1"
  },
  "op-mode": 0,
  "n_slots": 16,
  "links": [
    "R1-R2"
  ],
  "path": [
    "R1",
    "R2"
  ],
  "band": 200000,
  "freq": 192106250,
  "is_active": true,
  "src_port": "101",
  "dst_port": "201",
  "rev_dst_port": "201",
  "rev_src_port": "101",
  "c_slots": [
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16
  ],
  "served_lightpaths": [
    2
  ]
}
  """

