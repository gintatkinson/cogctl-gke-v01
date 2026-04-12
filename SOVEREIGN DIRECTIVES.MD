# THE SOVEREIGN DIRECTIVES

## PROLOGUE
These directives define the mandatory operational protocol for project `cogctl-gke-v01`. 
**Compliance is mandatory. Failure to follow directives must be reported as a Critical Issue.**

### THE EXECUTION GUARD
I (the AI Agent) will never initiate modifications based on ambiguous intent. I will HALT and request clarification unless I receive a direct command such as "GO", "EXECUTE", or "COMMENCE".

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
- **Baseline Fidelity:** I (the agent) MUST NOT deviate from official ETSI TFS deployment scripts (e.g., `tfs.sh`). "Hacking" YAMLs or manual `kubectl` overrides is strictly prohibited unless the official script fails and a project issue is approved.

### 3. REPOSITORY & CI/CD
- **Source:** Mirror standard TFS distribution from `labs.etsi.org:5050` (GitLab) to `https://github.com/gintatkinson/cogctl-gke-v01`.
- **Immutable Snapshot:** Once the ETSI baseline is cloned, it must be treated as an immutable snapshot. Do not pull upstream changes automatically; all updates must be manually archived and cross-referenced.
- **Artifact Sync (Binary Locking):** Mirroring the repository is insufficient. All mandated container binaries MUST be pulled from the ETSI registry, re-tagged, and pushed to the local **GCP Artifact Registry** to ensure total independence from external flux.
- **Sync:** Use GitHub Actions to manage the local mirror and archive local modifications.
- **Secrets:** DO NOT HARDCODE PATS. Use GCP Secret Manager for the GitLab PAT.

### 4. INTEGRATION STANDARDS (MANDATORY)
- **Networking:** 
    - Expose `nb-service` on **Port 443** via GKE Ingress.
    - Mandatory support for **OPTIONS** requests (CORS preflight) and **WSS WebSocket** upgrades.
    - Configure BackendConfig for GKE to handle timeout and connection draining for WSS.
- **Identity & Access (Keycloak):** 
    - Realm: `tfs`
    - Client ID: `tfs-dashboard`
    - Access Type: `public` (for PKCE flow).
- **CORS Configuration:** 
    - Allowed Origins: `https://<DASHBOARD_URL>`
    - Allowed Methods: `GET, POST, PUT, DELETE, OPTIONS`
    - Allowed Headers: `Content-Type, Authorization, X-Requested-With`
    - Allow Credentials: `true`.
- **Audit-First Verification (UI Success):** System health is defined by the WebUI. A deployment is successful ONLY when all 13 primary WebUI modules load correctly within a 3-second limit.
- **Architectural Whitelist:** Reconcile active services ONLY against the mandated architectural whitelist (to be defined).
- **Deployment Throttle:** Every service deployment MUST have a mandatory cooldown (sleep) before the next activation to prevent handshake storms.

### 5. TRACEABILITY & AUDIT
- **The Black Box Protocol (High-Frequency Logging):** To survive Antigravity or OS crashes, every tactical discovery, dependency conflict, or failed attempt MUST be recorded in **SUCCESSION_LOG_BLACKBOX.md** *immediately* upon detection.
- **Persistence Checkpoint (Sovereign Save):** After the successful completion of each SOP transition (e.g., SOP-01 finish), a "Checkpoint Commit" MUST be pushed to GitHub.
- **Commit Format:** Use `git commit -m "CHECKPOINT: SOP-XX COMPLETE"` followed by a push to ensure the mission remains recoverable mid-restoration.
- **Issue First:** Every failure, fix, and infrastructure change must have a corresponding GitHub Issue.
- **SOP Requirement:** For every service, once test/audit is successful, a **Standard Operating Procedure (SOP)** must be generated.
- **Crash Recovery:** Include progress reports and snapshots needed to recover from an agent or Antigravity crash.

### 6. OUTPUT REQUIREMENTS (INTEGRATION)
The following endpoints must be provided:
- `VITE_TFS_API_URL`: Public HTTPS URL of nb-service.
- `VITE_TFS_WS_URL`: Public WSS URL for WebSocket stream.
- `VITE_KEYCLOAK_URL`: Public HTTPS URL of Keycloak.
- `VITE_KEYCLOAK_REALM`: `tfs`
- `VITE_KEYCLOAK_CLIENT_ID`: `tfs-dashboard`

### 7. RESOURCE CONSERVATION & COST STEWARDSHIP
- **Ephemeral Infrastructure:** Non-production environments MUST follow an "Ephemeral-by-Default" policy. They should be summoned for active work and dismissed immediately upon completion.
- **Pay-per-Pod Billing:** GKE Autopilot must be the primary choice for dev/test to ensure zero cost when pods are scaled to 0.
- **Spot Provisioning:** All non-critical workloads (everything except Keycloak and basic API connectivity) MUST utilize Spot Pods.
- **Idle Shutdown:** Infrastructure must be configured to ramp down or hibernate after a maximum of 120 minutes of inactivity.

### 8. RECOVERY & INTEGRITY (GROUND ZERO)
- **Recovery Checkpoint:** Every new session focus MUST begin with a "Ground Truth" verification of the last successful SOP. 
- **Dirty State:** If verification fails, the environment is considered "Dirty." Do not proceed. Perform a Forensic Audit (check logs/issues) or execute a **Zero-Anchor Reset**.
- **The Guard:** Never initiate a **Zero-Anchor Reset** or any system modification without receiving an explicit, unambiguous "EXECUTE" or "COMMENCE" command.
- **Zero-Anchor Reset:** If the system's Source of Truth is compromised or significantly deviates from the Bible/Directives, do not attempt to "patch" the failure.
- **The Action:** Execute a total "Ground Zero" purge (delete cluster and reset workspace) and rebuild from the official ETSI Master.

### 9. ARTIFACT CONTROL & SBOM INTEGRITY
- **Software Purity:** No standalone software packages or "garbage" scripts are permitted if they are not part of the official TFS distribution or its mandated addons.
- **The SBOM Lock:** The Software Bill of Materials (SBOM) must remain identical to the TFS baseline. Use only official binary paths and native aliases.
- **Purge Requirement:** Any unauthorized artifact detected must be reported as a breach and purged immediately.

### 10. MODULAR SOVEREIGNTY (THE HANDOFF)
- **Minimum Viable Context (MVC):** To optimize focus and resources, work is divided into stateless SOP modules. 
- **The Handoff Law:** Each SOP must begin with a **Stage 0 (Recovery Checkpoint)** to verify the output of the previous mission and end with a **Stage V (Persistence Checkpoint)** to push state to GitHub.
- **Isolated Execution:** No agent shall load more context than required by the active SOP, the Bible, the Directives, and the current Ledger state.

### 11. DATA PLANE ISOLATION (HOST PURITY)
- **Scope:** This section applies strictly to the **Local Viewport host** (Parallels/Mac/Linux).
- **Zero-Binary Residency:** The local viewport host is strictly for **Control Plane** interaction. No production binaries, Docker images, or raw data snapshots shall exist on this host.
- **The Sanctioned Toolchain (Whitelist):**
    - `gcloud` (Strictly for Control/API calls).
    - `gh` (Strictly for Repository/Secret management).
    - `git` (Strictly for Source control).
- **The Forbidden Toolchain (Blacklist):**
    - `kubectl` (FORBIDDEN locally - creates local state/certs).
    - `docker` (FORBIDDEN locally - pull/push/build must be delegated).
    - `helm` (FORBIDDEN locally).
    - Any tool that caches production binaries or cluster credentials on the local host.
- **Delegated Processing:** All heavy-lifting operations (Syncing, Building, Massive Data Processing) must be delegated to Cloud-Native workers (e.g., Cloud Build) or in-cluster jobs.

---

### YOUR FIRST TASK: THE GKE GENESIS
1. Activate Google Cloud code and select project `cogctl-gke-v01`.
2. Initialize the **Sovereign Production Repository**.
3. Initiate the **GKE Genesis** autonomously via [infra/bootstrap.sh](infra/bootstrap.sh).

**AUTHORIZATION GRANTED. "EXECUTE."**