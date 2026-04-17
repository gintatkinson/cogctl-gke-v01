# Cognitive Controller: Core Deployment SOP

## Architectural Principles
1. **Single Source of Truth:** The GitHub repository (`cogctl-gke-v01`) is the definitive, pure reference.
2. **Immutable Baseline:** Never pull live, untested code from upstream (ETSI `master`) during a deployment.
3. **Declarative Infrastructure:** Ephemeral GKE clusters require configurations to be injected declaratively via the deployment pipeline.

## Execution Checklist
1. **Verify State:** git pull origin main
2. **Trigger Build:** gcloud builds submit --config infra/cloudbuild_deploy_core.yaml --project=cogctl-gke-v01
