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

import os
from time import sleep

line = '221.181.185.159 26406 11 0 10 4 1111 6 1111 0 0 0 1 0 10.25.0.6 22 10 0 10 5 1497 4 1497 0 0 0 1 0 1631699183883.141113 1631699185936.677002 2053.536000 327.059000 334.471000 2053.536000 1726.893000 326.976000 327.081000 1 1 0 0 0 0 0 13.977100 0.022000 42.534000 21.563233 6 40 40 334.779504 326.582000 367.107000 18.068151 5 64 64 0 0 0 0 0 0 1 1 7 1 0 1460 856 15 33536 29200 0 856 15 15 0 0 0 0 0 0 0 0 0 1 1 7 1 0 1410 1080 41 64384 64128 0 1080 41 41 0 0 0 0 0 0 0 0 0 0 0 --- 6 4 - - 0 0 0 0.000000 0.000000 0.000000 0.000000 0 0 - - 0.0 0.0 -\n'

here = os.path.dirname(os.path.abspath(__file__))
tstat_piped = os.path.join(here, '../service/piped/')
tstat_dirs = os.listdir(tstat_piped)
if len(tstat_dirs) > 0:
    tstat_dirs.sort()
    new_dir = tstat_dirs[-1]
    tstat_file = tstat_piped + new_dir + "/log_tcp_temp_complete"

print('Loaded',tstat_file)
with open(tstat_file, 'a') as f:
    for i in range(100):
        f.write(line)
        sleep(0.5)
