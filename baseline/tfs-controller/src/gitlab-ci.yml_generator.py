#!/usr/bin/python
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

import argparse
import os.path

# Parse the arguments
parser = argparse.ArgumentParser(description='Generate .gitlab-cy.yml template for a TeraFlow microservice.')
parser.add_argument("microservice", help="name of your microservice", type=str)
parser.add_argument("-t", "--tag", help="tag of the microservice Docker container", type=str, default='latest', required=False)
args = parser.parse_args()

# Check if the file and the path already exists
path="./{microservice}".format(microservice = args.microservice)
file="{path}/.gitlab-ci.yml".format(path = path)
if(os.path.isfile(file)):
    if input("File already exists, do you want to overwrite? (y/n) ") != "y":
        exit()
if(os.path.lexists(path)!= True):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

# Create the gitlab-ci.yml template file
f=open(file,"w+")
yml_template = """
# build, tag and push the Docker image to the gitlab registry
build {microservice}:
  variables:
    IMAGE_NAME: '{microservice}' # name of the microservice
    IMAGE_TAG: '{tag}' # tag of the container image (production, development, etc)
  stage: build
  before_script:
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" $CI_REGISTRY
  script:
    - docker build -t "$IMAGE_NAME:$IMAGE_TAG" -f ./src/$IMAGE_NAME/Dockerfile ./src/
    - docker tag "$IMAGE_NAME:$IMAGE_TAG" "$CI_REGISTRY_IMAGE/$IMAGE_NAME:$IMAGE_TAG"
    - docker push "$CI_REGISTRY_IMAGE/$IMAGE_NAME:$IMAGE_TAG"
  after_script:
    - docker rmi $(docker images --quiet --filter=dangling=true)
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event" && ($CI_MERGE_REQUEST_TARGET_BRANCH_NAME == "develop" || $CI_MERGE_REQUEST_TARGET_BRANCH_NAME == $CI_DEFAULT_BRANCH)'
    - if: '$CI_PIPELINE_SOURCE == "push" && $CI_COMMIT_BRANCH == "develop"' 
    - changes:
      - src/$IMAGE_NAME/*.{{py,in,yml}}
      - src/$IMAGE_NAME/Dockerfile
      - src/$IMAGE_NAME/tests/*.py
      - src/$IMAGE_NAME/tests/Dockerfile
      - manifests/$IMAGE_NAME.yaml
      - .gitlab-ci.yml

# apply unit test to the {microservice} component
unit test {microservice}:
  variables:
    IMAGE_NAME: '{microservice}' # name of the microservice
    IMAGE_TAG: '{tag}' # tag of the container image (production, development, etc)
  stage: test
  needs:
    - build {microservice}
  before_script:
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" $CI_REGISTRY
    - if docker network list | grep teraflowbridge; then echo "teraflowbridge is already created"; else docker network create -d bridge teraflowbridge; fi
    - if docker container ls | grep influxdb; then docker rm -f influxdb; else echo "influxdb image is not in the system"; fi
    - if docker container ls | grep $IMAGE_NAME; then docker rm -f $IMAGE_NAME; else echo "$IMAGE_NAME image is not in the system"; fi
  script:
    - docker pull "$CI_REGISTRY_IMAGE/$IMAGE_NAME:$IMAGE_TAG"
    - docker run --name influxdb -d -p 8086:8086 -e INFLUXDB_DB=$INFLUXDB_DATABASE -e INFLUXDB_ADMIN_USER=$INFLUXDB_USER -e INFLUXDB_ADMIN_PASSWORD=$INFLUXDB_PASSWORD -e INXLUXDB_HTTP_AUTH_ENABLED=True --network=teraflowbridge --rm influxdb:1.8
    - docker run --name $IMAGE_NAME -d -p 7070:7070 --env INFLUXDB_USER=$INFLUXDB_USER --env INFLUXDB_PASSWORD=$INFLUXDB_PASSWORD --env INFLUXDB_DATABASE=$INFLUXDB_DATABASE --env INFLUXDB_HOSTNAME=influxdb -v "$PWD/src/$IMAGE_NAME/tests:/opt/results" --network=teraflowbridge  --rm $CI_REGISTRY_IMAGE/$IMAGE_NAME:$IMAGE_TAG
    - docker ps -a
    - docker exec -i $IMAGE_NAME bash -c "pytest --junitxml=/opt/results/report.xml"
  after_script:
    - docker rm -f $IMAGE_NAME
    - docker rm -f  influxdb
    - docker network rm teraflowbridge
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event" && ($CI_MERGE_REQUEST_TARGET_BRANCH_NAME == "develop" || $CI_MERGE_REQUEST_TARGET_BRANCH_NAME == $CI_DEFAULT_BRANCH)'
    - if: '$CI_PIPELINE_SOURCE == "push" && $CI_COMMIT_BRANCH == "develop"' 
      - src/$IMAGE_NAME/*.{{py,in,yml}}
      - src/$IMAGE_NAME/Dockerfile
      - src/$IMAGE_NAME/tests/*.py
      - src/$IMAGE_NAME/tests/Dockerfile
      - manifests/$IMAGE_NAME.yaml
      - .gitlab-ci.yml
  artifacts:
      when: always
      reports:
        junit: src/$IMAGE_NAME/tests/report.xml

# Deployment of the {microservice} service in Kubernetes Cluster
deploy {microservice}:
  variables:
    IMAGE_NAME: '{microservice}' # name of the microservice
    IMAGE_TAG: '{tag}' # tag of the container image (production, development, etc)
  stage: deploy
  needs:
    - unit test {microservice}
    # - dependencies all
    # - integ_test execute
  script:
    - 'sed -i "s/$IMAGE_NAME:.*/$IMAGE_NAME:$IMAGE_TAG/" manifests/$IMAGE_NAME.yaml'
    - kubectl version
    - kubectl get all
    - kubectl apply -f "manifests/$IMAGE_NAME.yaml"
    - kubectl get all
  # environment:
  #   name: test
  #   url: https://example.com
  #   kubernetes:
  #     namespace: test
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event" && $CI_MERGE_REQUEST_TARGET_BRANCH_NAME == "develop"'
    - if: '$CI_PIPELINE_SOURCE == "push" && $CI_COMMIT_BRANCH == "develop"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event" && $CI_MERGE_REQUEST_TARGET_BRANCH_NAME == $CI_DEFAULT_BRANCH'
      when: manual
"""
f.write(yml_template.format(microservice = args.microservice, tag=args.tag))
print("File created in the following path: {file}".format(file=file))
