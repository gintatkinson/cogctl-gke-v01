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

# configure the correct folder on the .coveragerc file
cat $PROJECTDIR/coverage/.coveragerc.template | sed s+~/teraflow/controller+$PROJECTDIR+g > $RCFILE

# Run unitary tests and analyze coverage of code at same time

# Set the name of the Kubernetes namespace and hostname to use.
K8S_NAMESPACE="tf-dev"
K8S_HOSTNAME="kubernetes-master"
# Populate environment variables for context to use Redis in a development machine running Kubernetes
# Uncomment below lines to create a Redis instance within Context for testing purposes.
#kubectl delete namespace $K8S_NAMESPACE
#kubectl create namespace $K8S_NAMESPACE
#kubectl --namespace $K8S_NAMESPACE apply -f ../manifests/contextservice.yaml
#kubectl --namespace $K8S_NAMESPACE apply -f ../manifests/monitoringservice.yaml
#kubectl create secret generic influxdb-secrets --namespace=$K8S_NAMESPACE --from-literal=INFLUXDB_DB="monitoring" --from-literal=INFLUXDB_ADMIN_USER="teraflow" --from-literal=INFLUXDB_ADMIN_PASSWORD="teraflow" --from-literal=INFLUXDB_HTTP_AUTH_ENABLED="True"
#kubectl create secret generic monitoring-secrets --namespace=$K8S_NAMESPACE --from-literal=INFLUXDB_DATABASE="monitoring" --from-literal=INFLUXDB_USER="teraflow" --from-literal=INFLUXDB_PASSWORD="teraflow" --from-literal=INFLUXDB_HOSTNAME="localhost"
#kubectl --namespace $K8S_NAMESPACE expose deployment contextservice --port=6379 --type=NodePort --name=redis-tests
#kubectl --namespace $K8S_NAMESPACE expose deployment monitoringservice --port=8086 --type=NodePort --name=influx-tests
#echo "Waiting 10 seconds for Redis/Influx to start..."
#sleep 10
export REDIS_SERVICE_HOST=$(kubectl get node $K8S_HOSTNAME -o 'jsonpath={.status.addresses[?(@.type=="InternalIP")].address}')
export REDIS_SERVICE_PORT=$(kubectl get service redis-tests --namespace $K8S_NAMESPACE -o 'jsonpath={.spec.ports[?(@.port==6379)].nodePort}')
export INFLUXDB_HOSTNAME=$(kubectl get node $K8S_HOSTNAME -o 'jsonpath={.status.addresses[?(@.type=="InternalIP")].address}')
export INFLUXDB_PORT=$(kubectl get service influx-tests --namespace $K8S_NAMESPACE -o 'jsonpath={.spec.ports[?(@.port==8086)].nodePort}')
export INFLUXDB_USER=$(kubectl --namespace $K8S_NAMESPACE get secrets influxdb-secrets -o jsonpath='{.data.INFLUXDB_ADMIN_USER}' | base64 --decode)
export INFLUXDB_PASSWORD=$(kubectl --namespace $K8S_NAMESPACE get secrets influxdb-secrets -o jsonpath='{.data.INFLUXDB_ADMIN_PASSWORD}' | base64 --decode)
export INFLUXDB_DATABASE=$(kubectl --namespace $K8S_NAMESPACE get secrets influxdb-secrets -o jsonpath='{.data.INFLUXDB_DB}' | base64 --decode)

# First destroy old coverage file
rm -f $COVERAGEFILE

coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose \
    common/orm/tests/test_unitary.py \
    common/message_broker/tests/test_unitary.py \
    common/method_wrappers/tests/test_unitary.py

coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose \
    context/tests/test_unitary.py

coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose \
    device/tests/test_unitary_emulated.py

coverage run --rcfile=$RCFILE --append -m pytest -s --log-level=INFO --verbose \
    l3_centralizedattackdetector/tests/test_unitary.py

coverage run --rcfile=$RCFILE --append -m pytest -s --log-level=INFO --verbose \
    l3_distributedattackdetector/tests/test_unitary.py

coverage run --rcfile=$RCFILE --append -m pytest -s --log-level=INFO --verbose \
    l3_attackmitigator/tests/test_unitary.py

coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose \
    opticalcentralizedattackdetector/tests/test_unitary.py

coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose \
    dbscanserving/tests/test_unitary.py

coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose \
    opticalattackmitigator/tests/test_unitary.py

coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose \
    service/tests/test_unitary.py

coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose \
    nbi/tests/test_unitary.py

coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose \
    webui/tests/test_unitary.py

coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose \
    monitoring/tests/test_unitary.py

coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose \
    slice/tests/test_unitary.py

coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose \
    pathcomp/tests/test_unitary.py
