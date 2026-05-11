#!/bin/bash
# SOVEREIGN LIFECYCLE INDUCTION
# This script is a wrapper for Remote Execution.
# It contains NO local logic to avoid environment contamination.

COMMAND=$1

case $COMMAND in
  shutdown)
    echo "[LIFECYCLE] Inducting REMOTE SHUTDOWN..."
    ./hibernate.sh
    ;;
  
  restart)
    echo "[LIFECYCLE] Inducting REMOTE RESTART..."
    # 1. First trigger the remote ignition (which handles cluster creation)
    ./awake.sh
    # 2. The remote ignition manifest should ideally trigger the build, 
    # but we will follow the SOP and trigger the graduation build here as a second remote step.
    echo "[LIFECYCLE] Inducting GRADUATION INDUCTION..."
    gcloud builds submit --config infra/cloudbuild_graduation_final.yaml --substitutions=_TAG="rc13-verified" .
    ;;

  *)
    echo "Usage: ./lifecycle.sh {shutdown|restart}"
    exit 1
    ;;
esac
