# Implementation Plan: Total Reclamation Protocol (v4.0)

This plan codifies the physical sanitization of the repository to eliminate all "Shadow Pipelines" and legacy artifacts that contradict the **Sovereign Resurrection v4.0** standard. Completion of this plan is a mandatory prerequisite for the **Phase 3: Declarative Ignition**.

## Phase 1: Archive & Purge (Infra)
- [ ] **Create Archive**: `mkdir -p infra/archive/legacy_pipelines`.
- [ ] **Archive Legacy Scripts**: Move the following to `infra/archive/legacy_pipelines/`:
    - `cloudbuild_deploy_core.yaml`
    - `cloudbuild_graduation_final.yaml`
    - `cloudbuild_foundations_fidelity.yaml`
    - `cloudbuild_patch_probes.yaml`
    - `cloudbuild_sync.yaml`
    - `cloudbuild_gold_master_sequential.yaml`
    - `cloudbuild_mirror_foundations.yaml`
    - `cloudbuild_foundations.yaml`
    - `genesis.sh`
    - `genesis.yaml`
    - `foundation_purge.sh`
    - `lifecycle.sh`
    - `vault_bootstrap.sh`
- [ ] **Nuclear Purge of Dirty Manifests**:
    - `rm -rf infra/manifests/` (These are un-normalized duplicates).
    - `rm infra/nginx_ingress_service.yaml`
    - `rm infra/nginx_ingress_rbac.yaml`

## Phase 2: Archive & Purge (Docs)
- [ ] **Create Archive**: `mkdir -p docs/archive/legacy_plans`.
- [ ] **Archive Legacy Plans**: Move all files in `docs/solutions/implementation_plans/` to `docs/archive/legacy_plans/`.
- [ ] **Archive Stale Resurrection Plans**: Move `docs/plans/2026-05-08-sovereign-resurrection-v3.3.md` and related files to `docs/archive/legacy_plans/`.

## Phase 3: Authority Re-Forge
- [ ] **README Update**: Rewrite `docs/README.md` to reflect v4.0 Resurrection context.
- [ ] **SOP-01 Resolution**: Manually resolve the merge conflict in `docs/solutions/SOP-01.md`.
- [ ] **Directives Update**: Update `docs/solutions/SOVEREIGN DIRECTIVES.MD` to v4.0.

## Phase 4: Verification
- [ ] **Grep Audit**: Confirm no `namespace: default` references remain in the documentation or active infrastructure scripts.
- [ ] **Final Checkpoint**: Present the sanitized state for final "Ignition" authorization.

---
**Status:** AWAITING APPROVAL
**Auditor:** Sovereign AI Agent (Disciplined Alignment)
