#!/bin/bash
CLUSTER_NAME="sovereign-genesis"
ZONE="us-central1-a"
echo "Igniting fresh Sovereign Enclave..."
gcloud container clusters create $CLUSTER_NAME --zone $ZONE --machine-type n1-standard-4 --num-nodes 3 --quiet
gcloud container clusters get-credentials $CLUSTER_NAME --zone $ZONE
gcloud builds submit --config infra/cloudbuild_graduation_final.yaml --substitutions=_TAG="rc13-verified" .
