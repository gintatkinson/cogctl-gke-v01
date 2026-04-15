# PROJECT DIRECTIVES: cogctl-gke-v01 (Standard Edition)

## 1. Environment Initialization
- **Rule 1.1**: The environment must be provisioned via standardized automation (`infra/master_ignition.sh`).
- **Rule 1.2**: All compute resources must be labeled with the project version `v3.0.0-stable`.

## 2. Infrastructure Isolation
- **Rule 2.1**: All cluster orchestration (kubectl, helm, etc.) must be executed within automated worker pipelines (GCP Cloud Build).
- **Rule 2.2**: Local viewport hosts are prohibited from maintaining long-lived cluster credentials.

## 3. Dependency Management
- **Rule 3.1**: Third-party services (CockroachDB, NATS, Kafka) must be mirrored into the local Artifact Registry before deployment.
- **Rule 3.2**: Direct pulls from uncertified external registries are prohibited in production-path deployments.

## 4. Immutable Configuration
- **Rule 4.1**: Service manifests in the `baseline/` directory are the sole Source of Truth.
- **Rule 4.2**: Manual `kubectl edit` or `kubectl patch` operations must be ported into the baseline manifests within 24 hours of execution.

## 5. Knowledge Anchoring (Succession)
- **Rule 5.1**: Every service crash or configuration gap (e.g., `CRDB_NAMESPACE`) must be documented in a Technical Solution Spec and a GitHub Issue.
- **Rule 5.2**: The `SUCCESSION_LOG_BLACKBOX.md` must be updated at the end of every operational session.

---
**Status**: ACTIVE (Governance Structural Refactor v1.0)
**Execution Standard**: Compliance with SOP-01 through SOP-06 is mandatory.
