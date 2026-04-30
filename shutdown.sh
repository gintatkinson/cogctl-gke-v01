#!/bin/bash
CLUSTER_NAME="sovereign-genesis"
ZONE="us-central1-a"
echo "Initiating total infrastructure purge..."
gcloud container clusters delete $CLUSTER_NAME --zone $ZONE --quiet
