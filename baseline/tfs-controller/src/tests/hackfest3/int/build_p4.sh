#!/bin/bash
# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

get_next_backup_dir() {
  local prefix="/home/teraflow/controller/src/tests/hackfest3/p4/backup"
  local num=1

  while [[ -d "$prefix$num" ]]; do
    ((num++))
  done

  echo "$prefix$num"
}

backup_dir=$(get_next_backup_dir)
mkdir "$backup_dir"

if [[ -d "$backup_dir" ]]; then
  mv ~/controller/src/tests/hackfest3/p4/*json "$backup_dir"
  mv ~/controller/src/tests/hackfest3/p4/*p4 "$backup_dir"
  mv ~/controller/src/tests/hackfest3/p4/*txt "$backup_dir"
else
  echo "Backup directory not created. Files were not moved."
fi

cp $1 ~/controller/src/tests/hackfest3/p4/

rm -rf ~/ngsdn-tutorial/p4src/*
cp $1 ~/ngsdn-tutorial/p4src/main.p4
cd ~/ngsdn-tutorial
make p4-build

cp ~/ngsdn-tutorial/p4src/build/* ~/controller/src/tests/hackfest3/p4/
