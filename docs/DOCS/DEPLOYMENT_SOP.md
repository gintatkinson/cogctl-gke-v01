# Cognitive Controller: Core Deployment SOP

## Architectural Principles
1. **Single Source of Truth:** The GitHub repository (`cogctl-gke-v01`) is the definitive, pure reference.
2. **Immutable Baseline:** Never pull live, untested code from upstream (ETSI `master`) during a deployment. Deployments strictly utilize the frozen snapshot committed to this repository.
3. **Declarative Infrastructure:** Ephemeral GKE clusters require configurations to be injected declaratively via the deployment pipeline, not manually patched in live pods.

## Deployment Pipeline: `infra/cloudbuild_deploy_core.yaml`
The core deployment utilizes Google Cloud Build to execute a declarative rollout.

### Key Operations:
* **Artifact Registry:** Images are pulled from the Sovereign registry (`us-central1-docker.pkg.dev/cogctl-gke-v01/sovereign-tfs`), bypassing public upstream registries.
* **CRDB Injection:** Database connection variables (`CRDB_NAMESPACE`, `CRDB_SQL_PORT`) are injected directly into targeted deployments (e.g., automation, analytics, telemetry) via `kubectl set env`.
* **Deadlock Relaxation:** Liveness and readiness probes are temporarily patched out of the `webuiservice` to prevent SOP readiness deadlocks during initial cluster spin-up.

## Execution Checklist
To execute a clean deployment from a fresh environment:

1. **Verify State:** Ensure the local environment matches the definitive repository:
   `git pull origin main`
2. **Trigger Build:** Submit the pipeline to Cloud Build:
   `gcloud builds submit --config infra/cloudbuild_deploy_core.yaml --project=cogctl-gke-v01`