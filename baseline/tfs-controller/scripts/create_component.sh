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

COMPONENT_NAME=$1
PROJECTDIR=`pwd`

mkdir -p ${PROJECTDIR}/src/${COMPONENT_NAME}
mkdir -p ${PROJECTDIR}/src/${COMPONENT_NAME}/client
mkdir -p ${PROJECTDIR}/src/${COMPONENT_NAME}/service
mkdir -p ${PROJECTDIR}/src/${COMPONENT_NAME}/tests

touch ${PROJECTDIR}/src/${COMPONENT_NAME}/client/__init__.py
touch ${PROJECTDIR}/src/${COMPONENT_NAME}/service/__init__.py
touch ${PROJECTDIR}/src/${COMPONENT_NAME}/tests/__init__.py
touch ${PROJECTDIR}/src/${COMPONENT_NAME}/.gitlab-ci.yml
touch ${PROJECTDIR}/src/${COMPONENT_NAME}/__init__.py
touch ${PROJECTDIR}/src/${COMPONENT_NAME}/Config.py
touch ${PROJECTDIR}/src/${COMPONENT_NAME}/Dockerfile
touch ${PROJECTDIR}/src/${COMPONENT_NAME}/requirements.in

cd ${PROJECTDIR}/src
python gitlab-ci.yml_generator.py -t latest forecaster

cd ${PROJECTDIR}/src/${COMPONENT_NAME}
mv .gitlab-ci.yml gitlab-ci.yaml
${PROJECTDIR}/scripts/add_license_header_to_files.sh
mv gitlab-ci.yaml .gitlab-ci.yml
