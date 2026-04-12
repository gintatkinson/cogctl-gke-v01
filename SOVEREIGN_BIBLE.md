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
