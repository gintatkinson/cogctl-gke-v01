# INCIDENT: WebUI Orchestrator Deadlock - Dangling Proto Symlink (v3.0)

## 1. Problem Statement
The Sovereign TeraFlowSDN WebUI (v3.0) is currently failing its readiness probes, trapped in a continuous CrashLoopBackOff. The container logs report a fatal `ModuleNotFoundError: No module named 'vnt_manager'`, despite the `src/` logic floor being successfully birthed in Build #20.

## 2. Forensic Audit Results
- **The Dangling Bridge**: The `common/proto` directory—the architectural bridge to the enclave's gRPC vocabulary—is a dangling symlink inside the isolated container context.
- **Context Omission**: While the previous build expanded the Docker context to include the entire `src/` tree, it omitted the sibling `proto/` tree.
- **Host-Centric Bias Failure**: On developer workstations, the host OS seamlessly follows the relative symlink (`../../proto/src/python`). Inside the Docker container, because the target was outside the build boundary, the link was dead on arrival, snapping the Python import chain during `DescriptorLoader` initialization.

## 3. Sovereign Directive Alignment
- **Rule 3.1 (Dependency Management)**: Failing to provide the master orchestrator with its required gRPC vocabulary is a breach of dependency sovereignty.
- **Rule 5.1 (Succession)**: This failure and its resolution are formally anchored as **REC-013** in the technical implementation log.

## 4. Authorized Solution Document
The Antigravity Agent is directed to execute the following Master Execution Plan to harden the context:
👉 **PHASE 7.10: UNIFIED CONTEXT HARDENING**

## 5. Technical Execution Path
1. **Unified Context**: Modify `webui/Dockerfile` to ingest BOTH `baseline/tfs-controller/src/` and `baseline/tfs-controller/proto/`.
2. **Symlink Reconciliation**: Inject a `RUN` command to surgically replace the dangling `common/proto` link with a direct pointer to the new container floor: `/var/teraflow/proto/src/python`.
3. **Atomic Sync**: Execute `infra/cloudbuild_final.yaml` (Build #21) to complete the final restoration.
