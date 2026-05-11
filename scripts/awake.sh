#!/bin/bash
# SOVEREIGN IGNITION INDUCTION
# This script is a wrapper for Remote Execution.
# It contains NO local logic to avoid environment contamination.

echo "--- INDUCTING REMOTE IGNITION (CLOUD BUILD) ---"

# Trigger the remote manifest which uses containerized tools in GKE/GCP.
gcloud builds submit --config infra/awake.yaml .

echo "--- INDUCTION COMPLETE. MONITOR CLOUD CONSOLE FOR DEPLOYMENT STATUS ---"
