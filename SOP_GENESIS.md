# SOP: GKE GENESIS BOOTSTRAP

## STAGE 0: Recovery Checkpoint (Mandatory)
Every new session or restart MUST begin here:
1. **Verify Black Box:** Read `SUCCESSION_LOG_BLACKBOX.md` for any mid-SOP tactical discoveries or recent failures.
2. **Verify Network Purity:** Audit `gcloud compute networks subnets list`. Any existing `sovereign-genesis` secondary ranges on the target network MUST be purged or the network abandoned before ignition.
3. **Verify State:** If any verification fails, mark state as **"Dirty"** and perform a **Ground Zero Reset.**

## I. Pre-Flight Configuration
1. **Identify Target Project:** `cogctl-gke-v01`.
2. **Setup Secrets:**
   - Define `ETSI_GITLAB_PAT` (Personal Access Token) OR:
   - Define `ETSI_GITLAB_USERNAME` and `ETSI_GITLAB_PASSWORD` in GCP Secret Manager.
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

4. **Validation:** Check `logs/genesis.log` for the last successful phase.

## IV. Repository Mirroring
1. **Clone Baseline:** Mirror `labs.etsi.org:5050/tfs/controller` to the Sovereign GitHub repo.
2. **Snapshot Archive:** Tag the baseline as `etsi-certified-baseline-v01`.

## V. Artifact Sync (Binary Locking)
1. **Identify Registry:** Select `us-central1-docker.pkg.dev/cogctl-gke-v01/sovereign-tfs`.
2. **Execute Mirror Job:** Run `gcloud builds submit --config infra/cloudbuild_sync.yaml .`.
3. **Validation:** Ensure `docker images` list matches the ETSI baseline manifests exactly.

> [!IMPORTANT]
> **Prerequisites & Gotchas:**
> - **IAM:** The default Compute Engine Service Account (`[PROJECT_NUMBER]-compute@developer.gserviceaccount.com`) MUST have the **Secret Manager Secret Accessor** role for the `ETSI_GITLAB_PAT`.
> - **Syntax:** Cloud Build YAML reserves `${VAR}` for its own substitutions. Bash variables in scripts MUST use the double-dollar `$$IMAGE` syntax.

## VI. Persistence Checkpoint (Sovereign Save)
1. **Commit:** `git commit -m "CHECKPOINT: SOP-GENESIS COMPLETE"`.
2. **Push:** Push to GitHub to ensure state persistence.

## VII. Lifecycle Management (Sleep/Wake)
To comply with the **Resource Conservation** directive:
1. **Summon (Wake):** Run `./infra/lifecycle.sh up`. This initiates the Genesis and prepares the cluster.
2. **Dismiss (Sleep):** Run `./infra/lifecycle.sh down`. This deletes the cluster to ensure zero management fee during idle time.
3. **Automated Vigilance:** The `infra/watcher.yml` (template) defines a CronJob that triggers `lifecycle.sh down` if no activity is detected for 120 minutes.

## VI. Incident Reporting
- Every failure **MUST** be logged as a GitHub Issue immediately.
- Use the prefix `[GENESIS-FAIL]` in the issue title.
