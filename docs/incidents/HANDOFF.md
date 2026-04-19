# Gint's Project Handoff

## Current Status
- Repository: Sync confirmed.
- Structure: Cognitive Controller core is in this repo.
- Task: Deployment.

## Deployment Command
Run this exact command:
gcloud builds submit --config infra/cloudbuild_deploy_core.yaml --project=cogctl-gke-v01 .
