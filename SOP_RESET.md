# SOP: Total Ground-Zero Reset (Nuclear Mode)

## Purpose
This protocol defines the mandatory sequence for destroying and re-igniting the Sovereign foundation. It ensures that no "Ghost State" persists and that all historical wisdom is anchored before destruction.

## Stage 0: The Wisdom Harvest (MANDATORY)
1. **Raw Log Review**: Review all `.log` files and tactical archives in `scratch/` and `.sovereign_archive/`.
2. **Succession Anchoring**: Distill every failure, bug, and tactical recovery into `SUCCESSION_LOG.md`.
3. **Fidelity Check**: Ensure all critical fixes are `git add`ed and `git commit`ed to the `main` branch.
4. **ISSUE Linkage**: Document the current system symptoms in a formal GitHub Issue.

## Stage 1: Workspace Purification
1. **Clean Debris**: Execute `git clean -fd` (WARNING: DO NOT use `-x` unless you have explicitly confirmed the Harvest is complete).
2. **Path Verification**: Ensure the viewport toolchain (`gh`, `gcloud`) is functional and authenticated.

## Stage 2: Foundation Demolition
1. **Resource Purge**: Execute `infra/foundation_purge.sh --project <PROJECT_ID> --quiet`.
2. **Zero-State Audit**: Confirm via `gcloud` that all Sovereign-labeled Clusters, VPCs, and Firewalls are GONE.

## Stage 3: Total Ignition (Genesis vX.Y)
1. **Network Birth**: Execute `infra/master_ignition.sh` to provision the hardened VPC/NAT fabric.
2. **Remote-Native Deployment**: Delegate all `kubectl` and secret orchestration to **Cloud Build** workers via `infra/cloudbuild_final.yaml` and `infra/cloudbuild_vault.yaml`.

## Protocol Guardrails
- **Implicit Consent**: NEVER imply consent from ambiguous inputs like "Continue".
- **Authorization**: Proceed ONLY upon receiving an explicit "GO", "EXECUTE", or "PROCEED" command.
