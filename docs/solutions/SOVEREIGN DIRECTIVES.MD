# PROJECT DIRECTIVES: cogctl-gke-v01 (Standard Edition)

## 0. THE PRIME DIRECTIVE: ZERO-LOCAL INDUCTION
- **RULE 0.1 (THE BIBLE)**: **There is no such thing as "local" for this project.** The workstation is strictly an "Induction Node."
- **RULE 0.2 (TOOL PROHIBITION)**: Execution of `kubectl`, `terraform`, `gcloud container`, or any infrastructure-mutating binary directly from the host OS is **STRICTLY PROHIBITED**.
- **RULE 0.3 (HERMETIC IMMUNITY)**: The system MUST be immune to local environment drift (OS upgrades, dependency failures, Python version changes). 
- **RULE 0.4 (INDUCTION ONLY)**: All operational logic must reside in containerized Remote Manifests (Cloud Build). The workstation's ONLY authorized action is the submission of these manifests via `gcloud builds submit`.

## 1. Environment Initialization
- **Rule 1.1**: The environment must be provisioned via standardized automation induction gateways (`./awake.sh`).
- **Rule 1.2**: All compute resources must be labeled with the project version `v3.0.0-stable`.

## 2. Infrastructure Isolation
- **Rule 2.1**: All cluster orchestration (kubectl, helm, etc.) must be executed within automated worker pipelines (GCP Cloud Build).
- **Rule 2.2**: Local viewport hosts are prohibited from maintaining long-lived cluster credentials.

## 3. Dependency Management
- **Rule 3.1**: Third-party services (CockroachDB, NATS, Kafka) must be mirrored into the local Artifact Registry before deployment.
- **Rule 3.2**: Direct pulls from uncertified external registries are prohibited in production-path deployments.

## 4. Immutable Configuration & The "Zero-Hack" Mandate
- **Rule 4.1 (Source of Truth)**: Service manifests in the `baseline/` directory are the absolute and sole Source of Truth.
- **Rule 4.2 (The Zero-Hack Mandate)**: Pipeline-injected code mutations (e.g., `sed` replacements), manual `kubectl edit` operations, and runtime overrides are strictly **PROHIBITED** by default. 
- **Rule 4.3 (The Executive Exception)**: Tactical overrides ("hacks") are only permitted in the rarest of critical emergencies to prevent total enclave failure. These maneuvers require documented **Executive Approval**.

## 5. Knowledge Anchoring (Succession)
- **Rule 5.1**: Every service crash or configuration gap must be documented in a Technical Solution Spec and a GitHub Issue.
- **Rule 5.2**: The `SUCCESSION_LOG_BLACKBOX.md` must be updated at the end of every operational session.

## 6. The Blueprint Law (Design Rigor)
- **Rule 6.1**: Every proposed design for infrastructure or automation MUST adhere to the **Sovereign Blueprint Law**.

---
**Status**: ACTIVE (Governance Structural Refactor v1.2 - ZERO-LOCAL ENFORCEMENT)
**Execution Standard**: Compliance with Rule 0 (The Prime Directive) is the baseline for all operations.
