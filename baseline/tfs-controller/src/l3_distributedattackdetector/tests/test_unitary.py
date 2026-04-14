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

import logging
import os
from subprocess import Popen, DEVNULL
from time import sleep

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

def test_demo():
    print('Demo Test')
    pass

def test_tstat():
    here = os.path.dirname(os.path.abspath(__file__))
    generator_filename = os.path.join(here, 'data_generator.py')
    p2 = Popen(["python3",generator_filename], stdout=DEVNULL)
    print('Started')
    sleep(15)
    #p1.terminate()
    os.system("kill %s" % (p2.pid, ))
    print('Ended Successfully')
