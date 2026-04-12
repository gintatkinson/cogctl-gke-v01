# THE SOVEREIGN BIBLE

## I. Foundational Principles

### 1. Data Sovereignty
All data including primary application data, metadata, backups, and logs must reside entirely within the authorized jurisdiction. Cross-border data flows are prohibited unless expressly permitted.
- **Jurisdiction:** Google Cloud Platform (GCP) project `cogctl-gke-v01`.
- **Encryption:** All data at rest must be encrypted with Customer-Managed Encryption Keys (CMEK).

### 2. Operational Sovereignty
The operation and maintenance of the Sovereign environment must be independent, transparent, and auditable.
- **Access Control:** No foreign entity or cloud provider personnel shall have unauthorized access to the execution environment.
- **Non-Residency:** Production source code and sensitive toolchains must NEVER reside on local viewports (the "Mac").
- **Orchestration:** All deployments must be initiated from secure, ephemeral cloud-side environments (Google Cloud Shell).

### 3. Technical (Digital) Sovereignty
The environment shall be built on open standards and certified binaries to avoid vendor lock-in and ensure supply-chain transparency.
- **Standard:** ETSI TeraFlowSDN (TFS) Distribution.
- **Source:** Production-certified binaries from `labs.etsi.org`.

## II. The Sovereign Covenant

### "The Viewport"
The local machine is a viewport, not a vault. It is a portal to the Sovereign Cloud.
- **Do not download** sensitive artifacts.
- **Do not install** local toolchains for production.
- **Do not persist** source code outside the authorized repository.

### "The Genesis"
Infrastructure creation is a sacred and reproducible act.
- Every resource must be defined by code or script.
- Every failure must be recorded as an audit trail (Issue).
- Every success must be documented as an SOP.

### "The Audit"
Silence is the enemy of safety.
- Every change requires a traceable cause and a documented effect.
- Failure to document is a violation of the Sovereign Directives.

## III. The Meta-Cognitive Locks

### 1. The Succession Law (Documentation-First)
Every bug encountered, architectural decision made, or dependency added MUST first be documented in the **SUCCESSION_LOG.md** BEFORE applying the fix. We prevent "Wisdom Loss" by maintaining a persistent ledger of all corrections.

### 2. The Ground Truth Lock
Never trust the runtime state (e.g., `kubectl get pods`) as the benchmark for architectural correctness. Runtime is transient; the **Bible** and **Directives** are absolute. Reconcile active services only against the mandated architectural whitelist.

### 3. The Backoff Law (Deployment Throttle)
Speed is the enemy of stability in a safety-critical system. To prevent "Handshake Storms" and gRPC timeouts, services must be deployed with an appropriate mandatory cooldown. We formalize "patience" as a core operational standard.

### 4. The Minimalism Lock (Configuration Over Modification)
No code or manifest modifications are permitted if a configuration variable, environment variable, or official script can achieve the same result. We prioritize standard configuration patterns (e.g., `TFS_COMPONENTS` in tfs.sh) over manual "hacking" of YAMLs or source code. Any non-trivial modification must be cross-referenced against the original ETSI baseline and explicitly approved.

### 5. The Recovery Law (Context Persistence)
Every new session, context reset, or Antigravity restart MUST begin by executing a Recovery Checkpoint. We verify the "Ground Truth" of the last completed SOP. If verification fails, the system is considered "Dirty" and must be forensicly audited or reset to Ground Zero.

### 6. Explicit Authorization Lock (The Execution Guard)
The AI Agent MUST NEVER initiate system-modifying operations (builds, deployments, or resets) based on informational queries or ambiguous responses. Proceed ONLY upon receiving a clear, total approval or a direct order (e.g., "GO", "COMMENCE", "EXECUTE"). Any ambiguity MUST result in a halt and a request for confirmation.

### 7. The SBOM Integrity Law (No External Garbage)
The AI Agent MUST NOT introduce any standalone software packages, binary wrappers, or external snaps that are not part of the official TFS distribution or its mandated addons. The Software Bill of Materials (SBOM) must remain pure and identical to the TFS baseline. We use only native snap aliases and official TFS binaries. Any unauthorized "garbage" is an architectural breach and MUST be purged immediately.

### 8. The Baseline Fidelity Lock (No Unauthorized Deviation)
The AI Agent MUST NOT deviate from the official TFS installation scripts or certified baseline procedures. "Clever" automated fixes or manual rewrites of official scripts are strictly forbidden. If an official script fails, the agent must HALT, report the failure as a project issue, and await explicit approval for any deviation. We trust the Baseline; we do not "hack" it.

### 9. The Wisdom Locking Law (The Black Box Rule)
Knowledge acquired during failure is more valuable than knowledge acquired during success. To survive Antigravity or OS crashes, every tactical discovery, dependency conflict, or failed attempt MUST be recorded in the **Succession Log** (Black Box) *immediately* upon detection. We do not wait for SOP completion to lock in "Wisdom."

### 10. The Data Plane Isolation Lock (Viewport Purity)
The AI Agent MUST NOT execute any command that causes production binaries, container images, or sensitive data packets to transit through or reside on the local viewport host. The Viewport is strictly for Control logic (Metadata). The Data Plane (Binaries) must remain isolated within the cloud security perimeter. All binary orchestration MUST be performed by Cloud-Native or in-cluster tools.
