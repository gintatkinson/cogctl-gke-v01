#!/bin/bash
# SOVEREIGN FOUNDATION PURGE INDUCTION
# This script is a wrapper for Remote Execution.
# It contains NO local logic to avoid environment contamination.

echo "--- INDUCTING REMOTE FOUNDATION PURGE (CLOUD BUILD) ---"

# Trigger the remote manifest which uses containerized tools in GKE/GCP.
gcloud builds submit --config infra/foundation_purge.yaml .

echo "--- INDUCTION COMPLETE. MONITOR CLOUD CONSOLE FOR PURGE STATUS ---"
