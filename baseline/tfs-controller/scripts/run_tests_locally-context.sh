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

PROJECTDIR=`pwd`

cd $PROJECTDIR/src
RCFILE=$PROJECTDIR/coverage/.coveragerc
COVERAGEFILE=$PROJECTDIR/coverage/.coverage

# Destroy old coverage file and configure the correct folder on the .coveragerc file
rm -f $COVERAGEFILE
cat $PROJECTDIR/coverage/.coveragerc.template | sed s+~/tfs-ctrl+$PROJECTDIR+g > $RCFILE

echo
echo "Pre-test clean-up:"
echo "------------------"
docker rm -f crdb nats
docker volume rm -f crdb
docker network rm tfs-br

echo
echo "Pull Docker images:"
echo "-------------------"
docker pull cockroachdb/cockroach:latest-v22.2
docker pull nats:2.9

echo
echo "Create test environment:"
echo "------------------------"
docker network create -d bridge --subnet=172.254.254.0/24 --gateway=172.254.254.1 --ip-range=172.254.254.0/24 tfs-br
docker volume create crdb
docker run --name crdb -d --network=tfs-br --ip 172.254.254.10 -p 26257:26257 -p 8080:8080 \
    --env COCKROACH_DATABASE=tfs_test --env COCKROACH_USER=tfs --env COCKROACH_PASSWORD=tfs123\
    --volume "crdb:/cockroach/cockroach-data" \
    cockroachdb/cockroach:latest-v22.2 start-single-node
docker run --name nats -d --network=tfs-br --ip 172.254.254.11 -p 4222:4222 -p 8222:8222 \
    nats:2.9 --http_port 8222 --user tfs --pass tfs123

echo
echo "Waiting for initialization..."
echo "-----------------------------"
#docker logs -f crdb 2>&1 | grep --max-count=1 'finished creating default user "tfs"'
while ! docker logs crdb 2>&1 | grep -q 'finished creating default user \"tfs\"'; do sleep 1; done
docker logs crdb
#docker logs -f nats 2>&1 | grep --max-count=1 'Server is ready'
while ! docker logs nats 2>&1 | grep -q 'Server is ready'; do sleep 1; done
docker logs nats
#sleep 10
docker ps -a

echo
echo "Run unitary tests and analyze code coverage:"
echo "--------------------------------------------"
export CRDB_URI="cockroachdb://tfs:tfs123@172.254.254.10:26257/tfs_test?sslmode=require"
export MB_BACKEND="nats"
export NATS_URI="nats://tfs:tfs123@172.254.254.11:4222"
export PYTHONPATH=/home/tfs/tfs-ctrl/src
# helpful pytest flags: --log-level=INFO -o log_cli=true --verbose --maxfail=1 --durations=0
coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose --maxfail=1 \
    context/tests/test_*.py

echo
echo "Coverage report:"
echo "----------------"
#coverage report --rcfile=$RCFILE --sort cover --show-missing --skip-covered | grep --color -E -i "^context/.*$|$"
coverage report --rcfile=$RCFILE --sort cover --show-missing --skip-covered --include="context/*"

echo
echo "Post-test clean-up:"
echo "-------------------"
docker rm -f crdb nats
docker volume rm -f crdb
docker network rm tfs-br
