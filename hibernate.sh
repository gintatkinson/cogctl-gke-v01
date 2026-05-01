#!/usr/bin/env bash
set -euo pipefail
mkdir -p "$(pwd)/logs"
LOG_FILE="$(pwd)/logs/hibernate_$(date +%Y%m%d_%H%M%S).log"
export CLOUDSDK_CORE_DISABLE_PROMPTS=1
echo "--- INITIATING TOTAL PURGE ---"
nohup bash infra/foundation_purge.sh > "$LOG_FILE" 2>&1 < /dev/null &
disown
echo "[SUCCESS] Master Hibernation engine successfully detached."
echo "[INFO] Tracking execution at: $LOG_FILE"
echo "The background process is running safely. You have your prompt back."
