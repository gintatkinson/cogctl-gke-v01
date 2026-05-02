# Sovereign "Wisdom Harvest" (Cognitive Controller)

**Mandate:** Zero-Local Contamination.
**Execution Engine:** GKE / Cloud Build.
**Source of Truth:** GitHub (gintatkinson/cogctl-gke-v01).

This repository is an **Induction Staging Area**. The local environment (Workstation) contains NO operational logic. All infrastructure lifecycle events are managed via Remote Induction.

---

## 🚀 Core Induction Gateways
These scripts are the ONLY authorized entry points for the system. They perform zero local execution and hand off all logic to stable, cloud-managed containers.

| Script | Purpose | Remote Manifest |
| :--- | :--- | :--- |
| `./awake.sh` | **Total Ignition**: Provisions GKE and deploys all services. | `infra/awake.yaml` |
| `./hibernate.sh`| **Total Purge**: Deletes cluster and disks (Zero-Debt). | `infra/hibernate.yaml` |
| `./lifecycle.sh`| **Orchestrator**: Unified Restart/Shutdown control. | (Delegates to above) |
| `./sovereign-control.sh`| **Control Plane**: Terraform-based state management. | `infra/terraform.yaml` |

---

## 🛡️ Sovereign Build Law
1.  **NO LOCAL TOOLS**: Never execute `gcloud container`, `kubectl`, or `terraform` directly from the workstation.
2.  **OS IMMUNITY**: The system must remain operational regardless of the workstation's OS version, CPU architecture, or local Python state.
3.  **HERMETIC BUILD**: All build steps must run in containerized environments (Cloud Build) using verified images (`cloud-sdk`, `terraform`).

---

## 📂 Documentation Structure
*   [`SOP_OPERATIONS.md`](SOP_OPERATIONS.md): The authoritative operational manual.
*   [`docs/solutions/`](docs/solutions/): Hardened architectural specifications.
*   [`infra/`](infra/): Remote Induction Manifests (The Reality).
*   [`baseline/`](baseline/): Project source code (TFS-Controller).

---
**Status:** All local logic has been EXCISED. The system is now IMMUNE to local environment drift.
