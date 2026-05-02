#!/bin/bash
# SOVEREIGN GENESIS INDUCTION (v3.0)
# This script is a Remote Induction Portal.
# It contains NO local tools. It triggers the Sovereign Clean Room.

ID=$(date +%s)
REGION="us-central1"

echo "--- INDUCTING REMOTE GENESIS IGNITION (ID: $ID) ---"

gcloud builds submit --config infra/genesis.yaml \
    --substitutions=_ID="$ID",_REGION="$REGION" .

echo "--- IGNITION INDUCTED. MONITOR CLOUD CONSOLE ---"
