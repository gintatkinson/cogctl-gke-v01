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

# Create a set of tests enabling to run tests as follows ...
#   from common.tests.PytestGenerateTests import pytest_generate_tests # pylint: disable=unused-import
#
#   scenario1 = ('basic', {'attribute': 'value'})
#   scenario2 = ('advanced', {'attribute': 'value2'})
#
#   class TestSampleWithScenarios:
#       scenarios = [scenario1, scenario2]
#
#       def test_demo1(self, attribute):
#           assert isinstance(attribute, str)
#
#       def test_demo2(self, attribute):
#           assert isinstance(attribute, str)
#
# ... and run them as:
#   $ pytest --log-level=INFO --verbose my_test.py
#   =================== test session starts ===================
#   platform linux -- Python 3.9.6, pytest-6.2.4, py-1.10.0, pluggy-0.13.1 -- /home/.../.pyenv/.../bin/python3.9
#   cachedir: .pytest_cache
#   benchmark: 3.4.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0
#                               calibration_precision=10 warmup=False warmup_iterations=100000)
#   rootdir: /home/.../tests
#   plugins: benchmark-3.4.1
#   collected 4 items
#
#   my_test.py::TestSampleWithScenarios::test_demo1[basic] PASSED          [ 25%]
#   my_test.py::TestSampleWithScenarios::test_demo2[basic] PASSED          [ 50%]
#   my_test.py::TestSampleWithScenarios::test_demo1[advanced] PASSED       [ 75%]
#   my_test.py::TestSampleWithScenarios::test_demo2[advanced] PASSED       [100%]
#
#   ==================== 4 passed in 0.02s ====================

def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for scenario in metafunc.cls.scenarios:
        idlist.append(scenario[0])
        items = scenario[1].items()
        argnames = [x[0] for x in items]
        argvalues.append([x[1] for x in items])
    metafunc.parametrize(argnames, argvalues, ids=idlist, scope='class')
