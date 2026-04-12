# THE SOVEREIGN DIRECTIVES

## PROLOGUE
These directives define the mandatory operational protocol for project `cogctl-gke-v01`. 
**Compliance is mandatory. Failure to follow directives must be reported as a Critical Issue.**

---

### 1. FOUNDATIONAL HIERARCHY
1. **Follow the [SOVEREIGN_BIBLE.md](SOVEREIGN_BIBLE.md)**: All actions must align with the core principles of Data, Operational, and Technical Sovereignty.
2. **Standard:** [ETSI TeraFlowSDN (TFS)](https://tfs.etsi.org) Production Distribution.

### 2. EXECUTION CONSTRAINTS
- **GKE ONLY (The Viewport Principle):** The local Linux/Mac host is strictly a viewport. 
    - **NO** local downloads of production artifacts.
    - **NO** local tool installation (use Cloud Shell binaries).
    - **NO** source residency.
- **CLOUD SHELL ONLY:** All orchestration, toolchains (`gcloud`, `gh`, `kubectl`), and repository management must be run within the Google Cloud Shell environment.

### 3. REPOSITORY & CI/CD
- **Source:** Mirror standard TFS distribution from `labs.etsi.org:5050` (GitLab) to `https://github.com/gintatkinson/cogctl-gke-v01`.
- **Sync:** Use GitHub Actions to maintain parity with ETSI certified binaries.
- **Secrets:** DO NOT HARDCODE PATS. Use GCP Secret Manager for the GitLab PAT.

### 4. INTEGRATION STANDARDS (MANDATORY)
- **Networking:** 
    - Expose `nb-service` on **Port 443** via GKE Ingress.
    - Mandatory support for **ORS preflight (OPTIONS)** and **WSS WebSocket** upgrades.
    - Configure BackendConfig for GKE to handle timeout and connection draining for WSS.
- **Identity:** 
    - Deploy **Keycloak**. 
    - Configure `tfs` realm and the `tfs-dashboard` public client.
- **CORS:** Allow Origins from the Cloud Run Dashboard URL. `Allow Credentials: true`.

### 5. TRACEABILITY & AUDIT
- **Issue First:** Every failure, fix, and infrastructure change must have a corresponding GitHub Issue.
- **SOP Requirement:** For every service, once test/audit is successful, a **Standard Operating Procedure (SOP)** must be generated.
- **Crash Recovery:** Include progress reports and snapshots needed to recover from an agent or Antigravity crash.

### 6. OUTPUT REQUIREMENTS
Post-deployment environment variables:
- `VITE_TFS_API_URL`
- `VITE_TFS_WS_URL`
- `VITE_KEYCLOAK_URL`

---

### YOUR FIRST TASK: THE GKE GENESIS
1. Activate Google Cloud code and select project `cogctl-gke-v01`.
2. Initialize the **Sovereign Production Repository**.
3. Initiate the **GKE Genesis** autonomously via [infra/bootstrap.sh](infra/bootstrap.sh).

**AUTHORIZATION GRANTED. "EXECUTE."**