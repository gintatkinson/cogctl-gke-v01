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
from sys import stdout
import sys
from l3_distributedattackdetector import l3_distributedattackdetector

#  Setup LOGGER
LOGGER = logging.getLogger("main_dad_LOGGER")
LOGGER.setLevel(logging.INFO)
logFormatter = logging.Formatter(fmt="%(levelname)-8s %(message)s")
consoleHandler = logging.StreamHandler(stdout)
consoleHandler.setFormatter(logFormatter)
LOGGER.addHandler(consoleHandler)

PROFILING = False

def main():
    l3_distributedattackdetector()


if __name__ == "__main__":
    if PROFILING:
        import cProfile, pstats, io

        pr = cProfile.Profile()
        pr.enable()

    main()

    if PROFILING:
        pr.disable()
        s = io.StringIO()
        sortby = "cumulative"
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        LOGGER.info(s.getvalue())

    sys.exit(0)