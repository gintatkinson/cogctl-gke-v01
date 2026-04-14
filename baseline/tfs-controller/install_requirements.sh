#!/bin/bash
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

# If not already set, set the list of components you want to install dependencies for.
# By default, dependencies for all components are installed.
# Components still not supported by this script:
#   ztp & policy : implemented in Java
#   dlt                 : under design
#   pathcomp            : under design
ALL_COMPONENTS="context device service nbi monitoring webui interdomain slice"
ALL_COMPONENTS="${ALL_COMPONENTS} dbscanserving opticalattackmitigator opticalattackdetector"
ALL_COMPONENTS="${ALL_COMPONENTS} l3_attackmitigator l3_centralizedattackdetector l3_distributedattackdetector"
ALL_COMPONENTS="${ALL_COMPONENTS} kpi_manager kpi_value_writer kpi_value_api"
TFS_COMPONENTS=${TFS_COMPONENTS:-$ALL_COMPONENTS}

# Some components require libyang built from source code
# - Ref: https://github.com/CESNET/libyang
# - Ref: https://github.com/CESNET/libyang-python/
echo "Installing libyang..."
sudo apt-get --yes --quiet --quiet update
sudo apt-get --yes --quiet --quiet install build-essential cmake libpcre2-dev python3-dev python3-cffi
mkdir libyang
git clone https://github.com/CESNET/libyang.git libyang
cd libyang
git fetch
git checkout v2.1.148
cd ..
mkdir libyang/build
cd libyang/build
echo "*" > .gitignore
cmake -D CMAKE_BUILD_TYPE:String="Release" ..
make
sudo make install
sudo ldconfig
cd ../..

echo "Updating PIP, SetupTools and Wheel..."
# Bring basic tooling for other requirements, package compilation, and code linting.
# Ensure next packages get the fixed versions to prevent:
#   "'InstallRequirement' object has no attribute 'use_pep517'"
pip install --upgrade 'pip==25.2'
pip install --upgrade 'setuptools==79.0.0' 'wheel==0.45.1'
pip install --upgrade 'pip-tools==7.3.0'
printf "\n"

echo "Creating integrated requirements file..."
touch requirements.in
diff requirements.in common_requirements.in | grep '^>' | sed 's/^>\ //' >> requirements.in
printf "\n"

echo "Collecting requirements from components..."
for COMPONENT in $TFS_COMPONENTS
do
    if [ "$COMPONENT" == "ztp" ] || [ "$COMPONENT" == "policy" ]; then continue; fi
    diff requirements.in src/$COMPONENT/requirements.in | grep '^>' | sed 's/^>\ //' >> requirements.in
done
printf "\n"

echo "Compiling requirements..."
# Done in a single step to prevent breaking dependencies between components
pip-compile --quiet --output-file=requirements.txt requirements.in
printf "\n"

echo "Installing requirements..."
python -m pip install -r requirements.txt
printf "\n"

#echo "Removing the temporary files..."
rm requirements.in
rm requirements.txt
printf "\n"
