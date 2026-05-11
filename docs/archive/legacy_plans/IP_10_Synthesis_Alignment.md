# Implementation Plan: Phase 7.45 (The Graduation Synthesis Alignment)

This plan resolves the **`Topographical Drift`** identified in the Build #61 audit. We discovered that several "Gold Master" Dockerfiles utilize repository-root relative paths (`COPY baseline/tfs-controller/...`), which collide with our new Controller-Root build context. By surgically removing these prefixes, we achieve 100% pathing alignment across the entire enclave.

## User Review Required

> [!IMPORTANT]
> **Global Prefix Removal**: I am surgically removing the **`baseline/tfs-controller/`** prefix from 18 lines across the `context`, `device`, `service`, `slice`, `pathcomp`, `nbi`, `webui`, `monitoring`, and `automation` Dockerfiles. This ensures they can correctly ingest their source code from the Controller-Root context.

> [!IMPORTANT]
> **Standardized Context**: All future builds will utilize the **`baseline/tfs-controller/`** directory as the absolute build context root.

> [!CAUTION]
> **Final Graduation Ignition (Build #62)**: This is the terminal sequence to bridge the topographical rift and achieve the 2/2 ready state.

## Proposed Changes

### [Component Name]
#### [MODIFY] [context/Dockerfile](file:///Users/perkunas/cogctl-gke-v01/baseline/tfs-controller/src/context/Dockerfile)
#### [MODIFY] [device/Dockerfile](file:///Users/perkunas/cogctl-gke-v01/baseline/tfs-controller/src/device/Dockerfile)
#### [MODIFY] [service/Dockerfile](file:///Users/perkunas/cogctl-gke-v01/baseline/tfs-controller/src/service/Dockerfile)
#### [MODIFY] [slice/Dockerfile](file:///Users/perkunas/cogctl-gke-v01/baseline/tfs-controller/src/slice/Dockerfile)
#### [MODIFY] [pathcomp/Dockerfile](file:///Users/perkunas/cogctl-gke-v01/baseline/tfs-controller/src/pathcomp/Dockerfile)
#### [MODIFY] [nbi/Dockerfile](file:///Users/perkunas/cogctl-gke-v01/baseline/tfs-controller/src/nbi/Dockerfile)
#### [MODIFY] [webui/Dockerfile](file:///Users/perkunas/cogctl-gke-v01/baseline/tfs-controller/src/webui/Dockerfile)
#### [MODIFY] [monitoring/Dockerfile](file:///Users/perkunas/cogctl-gke-v01/baseline/tfs-controller/src/monitoring/Dockerfile)
#### [MODIFY] [automation/Dockerfile](file:///Users/perkunas/cogctl-gke-v01/baseline/tfs-controller/src/automation/Dockerfile)

### Phase 2: Graduation Ignition (Build #62)
#### [EXECUTE] [Terminal Ignition]
- **Action**: Execute `Build #62`.

## Open Questions

- None. Forensic audit (Step 388) identified all toxic prefixes.

## Verification Plan

### Automated Verification
- **Readiness Audit**: Confirm all 11 services reach the **2/2 READY** state.
- **Audit**: Verify synthesis logs for "Step 3/5 : COPY src/context/ context/" (confirming prefix removal success).

### Manual Verification
- **SOP-06**: Perform the 13-Screen Audit.
