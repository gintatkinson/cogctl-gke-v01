# SOP: GKE GENESIS BOOTSTRAP

## Purpose
This document provides the standard procedure for initiating the Sovereign Production environment and recovering from bootstrap failures.

## I. Pre-Flight Configuration
1. **Identify Target Project:** `cogctl-gke-v01`.
2. **Setup Secrets:**
   - Define `ETSI_GITLAB_PAT` in GCP Secret Manager.
   - Sync GitHub repository `gintatkinson/cogctl-gke-v01` context.
3. **Environment:** Execute solely within Google Cloud Shell.

## II. Bootstrap Sequence (Execution)
The `infra/bootstrap.sh` script automates the following steps:
1. **API Initiation:** Enable `container.googleapis.com`, `secretmanager.googleapis.com`, and `logging.googleapis.com`.
2. **VPC Construction:** Create the Sovereign-Strict VPC and restricted subnets.
3. **Cluster Creation:** Provision the `sovereign-genesis` cluster with:
   - Shielded Nodes enabled.
   - Workload Identity enabled.
   - Private nodes (no public IPs).
4. **Auth Hand-off:** Authenticate `kubectl` against the new cluster.

## III. Verification Points
- [ ] **Cluster State:** `gcloud container clusters list` shows cluster as `RUNNING`.
- [ ] **Secret Access:** `gcloud secrets versions access latest --secret="ETSI_GITLAB_PAT"` successful.
- [ ] **Internal Connectivity:** Deployment of a minimal 'Hello-Sovereign' test service to verify Ingress 443.

## IV. Recovery and Restore
In case of agent crash or Antigravity interruption:
1. **Retrieve Progress Report:** check the last GitHub Issue labeled `genesis-progress`.
2. **Re-activate Viewport:**
   - Execute `/home/parallels/google-cloud-sdk/bin/gcloud config set project cogctl-gke-v01`.
   - Re-run `infra/bootstrap.sh` (The script should be idempotent).
3. **Validation:** Check `logs/genesis.log` for the last successful phase.

## V. Incident Reporting
- Every failure **MUST** be logged as a GitHub Issue immediately.
- Use the prefix `[GENESIS-FAIL]` in the issue title.
