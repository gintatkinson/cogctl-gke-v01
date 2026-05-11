#!/bin/bash
# SOVEREIGN CONTROL INDUCTION
# Replaces local Terraform logic with Remote Orchestration.

ACTION=$1

if [ "$ACTION" == "start" ]; then
    echo "[CONTROL] Inducting REMOTE INFRASTRUCTURE BIRTH..."
    gcloud builds submit --config infra/terraform.yaml --substitutions=_TF_ACTION="apply" .
    echo "[CONTROL] Inducting REMOTE SERVICE GRADUATION..."
    gcloud builds submit --config infra/cloudbuild_graduation_final.yaml .
elif [ "$ACTION" == "stop" ]; then
    echo "[CONTROL] Inducting REMOTE INFRASTRUCTURE DEATH..."
    gcloud builds submit --config infra/terraform.yaml --substitutions=_TF_ACTION="destroy" .
else
    echo "Usage: ./sovereign-control.sh [start|stop]"
    exit 1
fi
