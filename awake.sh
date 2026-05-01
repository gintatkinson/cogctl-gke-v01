#!/usr/bin/env bash
set -euo pipefail
mkdir -p "$(pwd)/logs"
LOG_FILE="$(pwd)/logs/awake_$(date +%Y%m%d_%H%M%S).log"
export CLOUDSDK_CORE_DISABLE_PROMPTS=1
# Force the zone to us-central1-a
export CLOUDSDK_COMPUTE_ZONE=us-central1-a
echo "--- INITIATING MASTER IGNITION (ZONE: us-central1-a) ---"
nohup bash infra/master_ignition.sh > "$LOG_FILE" 2>&1 < /dev/null &
disown
echo "[SUCCESS] Master Ignition engine successfully detached."
echo "[INFO] Tracking execution at: $LOG_FILE"
echo "[INFO] The enclave will rebuild in the background (~12 minutes)."
echo "The background process is running safely. You have your prompt back."
