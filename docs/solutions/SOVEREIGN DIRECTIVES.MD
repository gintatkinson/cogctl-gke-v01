# PROJECT DIRECTIVES: Sovereign GKE Genesis (v4.0)

## 1. Environment Initialization
- **Rule 1.1**: The environment must be provisioned via standardized Cloud Build automation. The ONLY authorized ignition engines are:
  - `infra/awake.yaml` (Remote Ignition)
  - `infra/hibernate.yaml` (Zero Consumption Suspension)
  - `infra/resurrect.yaml` (Total Tabula Rasa Rebuild)
- **Rule 1.2**: All compute resources must be labeled with the project version `v4.0-resurrection`.
- **Rule 1.3**: The "Zero State" must be verified via `SOP-07` (State Audit) BEFORE any ignition sequence is triggered.

## 2. Infrastructure Isolation
- **Rule 2.1**: All cluster orchestration (kubectl, terraform, etc.) must be executed within automated Cloud Build pipelines. "Shadow Pipelines" (unauthorized or ad-hoc scripts) are strictly prohibited.
- **Rule 2.2**: Manual `kubectl` execution from local viewports is permitted ONLY for informational audits (`get`, `describe`, `logs`). Local mutation commands (`apply`, `delete`, `patch`) are ABSOLUTELY PROHIBITED.

## 3. Dependency Management
- **Rule 3.1**: Third-party services must be mirrored into the local Artifact Registry.
- **Rule 3.2**: Image tags must be pinned to verified release versions (e.g., `rc13-verified`).

## 4. Immutable Configuration (The Purity Law)
- **Rule 4.1**: Service manifests in the `baseline/` directory are the sole Source of Truth.
- **Rule 4.2**: **NO `sed` hacks** are permitted in the CI/CD pipeline to mutate manifests at runtime. If a manifest requires a change, the architecture must be updated declaratively.
- **Rule 4.3**: All deployments must target the `sovereign-genesis` namespace. Use of the `default` namespace for Sovereign services is a **Critical Governance Breach**.

## 5. Knowledge Anchoring (Succession)
- **Rule 5.1**: Every service crash or configuration gap must be documented in a Technical Solution Spec and the `SUCCESSION_LOG_BLACKBOX.md`.
- **Rule 5.2**: The `DURABILITY_CHECKLIST.md` must be updated if a new failure mode is identified.

---
**Status**: ACTIVE (Sovereign Resurrection v4.0)
**Execution Standard**: Compliance with the Durability Checklist and SOPs 01-07 is mandatory.
