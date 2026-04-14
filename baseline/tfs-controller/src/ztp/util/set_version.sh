#!/usr/bin/env bash
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

set -eu

if (( $# != 1 )); then
  echo "Usage: set_version.sh <version>" >&2
  exit 1
fi

version="$1"

if [ "$(git status --untracked-files=no --porcelain)" ]; then
    printf "Uncommitted changes in tracked files.\nPlease commit first and then run the script!\n"
    exit 0;
fi

./mvnw versions:set versions:commit -DnewVersion="${version}"
git commit -am "release(ztp): ${version}"
