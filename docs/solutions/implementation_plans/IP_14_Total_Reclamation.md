# Implementation Plan: IP_14 (Total Reclamation & Blueprint Sterilization)

**Status**: DRAFT (Awaiting Approval)
**Author**: Sovereign AI (Karpathy Skill Active)
**Directives**: RE-ALIGNMENT v4.0

## Phase 1: Issue Tracking & Governance (Mandatory)
The following GitHub Issues must be created and linked to ensure auditability of the sterilization process:

- **ISSUE: Repository Pollution (Shadow Pipelines)**: Tracking the required purge of `infra/cloudbuild_deploy_core.yaml`, `infra/cloudbuild_graduation_final.yaml`, and legacy bash scripts.
- **ISSUE: SOP Corruption**: Tracking the mandatory resolution of the merge conflict in `docs/solutions/SOP-01.md` and the misalignment of `SOP-03.md`.
- **ISSUE: Manifest Governance Breach**: Tracking the unauthorized agent mutations applied to `baseline/tfs-controller/manifests/` and the unauthorized creation of `graduation_secrets.yaml`.

## Phase 2: Repository Sterilization (The Purge)
Explicit operations to achieve 100% compliance with the `DURABILITY_CHECKLIST.md`:

- **Archive Obsolete Plans**: `mkdir -p docs/archive/legacy_plans/` and `mv docs/plans/*.md docs/solutions/implementation_plans/*.md docs/archive/legacy_plans/`.
- **Annihilate Redundancy**: `git rm -r infra/manifests/` (Eliminating secondary sources of drift).
- **Isolate Defective Pipelines**: `mkdir -p infra/archive/legacy_pipelines/` and `mv infra/cloudbuild_deploy_core.yaml infra/cloudbuild_graduation_final.yaml infra/archive/legacy_pipelines/`.

## Phase 3: Blueprint Reconciliation
Finalizing the Sovereign Genesis v4.0 Ground Truth:

- **SOP-01 Resolution**: Manually resolve the textual merge conflict in `docs/solutions/SOP-01.md` and anchor the provision step to `infra/terraform/main.tf`.
- **Directives Anchor**: Update `docs/solutions/SOVEREIGN DIRECTIVES.MD` to establish `infra/awake.yaml` as the sole authorized ignition engine, prohibiting local `kubectl` mutations.

---
**Verification Gate**: 100% compliance with `DURABILITY_CHECKLIST.md`. Zero shadow pipelines remaining in active paths.
