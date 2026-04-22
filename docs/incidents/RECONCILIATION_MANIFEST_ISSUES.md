# RECONCILIATION MANIFEST: GITHUB ISSUE TRACKER

This document transforms the Technical Implementation Log (REC-001 to REC-048) into a formal GitHub Issue manifest for auditable graduation.

---

## ISSUE #001: Toolchain Path Hardening (REC-001)
### 1. Problem Statement
SDK binaries (`gcloud`, `gh`) failed to load in non-interactive shells and orchestration scripts due to legacy absolute paths (`/home/parallels/...`).

### 2. Forensic Audit
*   Environment: Parallels VM legacy artifacts detected.
*   Symptom: `command not found` in automation loops.

### 3. Authorized Solution
[SOP-01: Toolchain Alignment](../solutions/SOP-01.md)

---

## ISSUE #002: Service Endpoint & Sidecar Deadlocks (REC-002)
### 1. Problem Statement
GKE probes failed for 2nd-container sidecars (NGINX/Envoy), preventing pod readiness and stalling rollouts.

### 2. Forensic Audit
*   Resource: Sidecar containers in GKE Standard.
*   Root Cause: Readiness/Liveness probe timeout on constrained nodes.

### 3. Authorized Solution
[Solution Spec: Readiness Relaxation](../solutions/solution_spec_readiness_relaxation.md)

---

## ISSUE #003: Core Configuration Gap - CRDB_NAMESPACE (REC-003)
### 1. Problem Statement
`contextservice` crashed due to missing `CRDB_NAMESPACE` setting in the environment variables.

### 2. Forensic Audit
*   Symptom: `KeyError: 'CRDB_NAMESPACE'`.
*   Impact: Total database connection failure.

### 3. Authorized Solution
[Solution Spec: CRDB Resolution](../solutions/SPEC_CRDB_RESOLUTION.md)

---

## ISSUE #005: NBI Broker Synchronization OOM Deadlock (REC-005)
### 1. Problem Statement
`nbiservice` suffered OOM-kills during initial Kafka topic synchronization.

### 2. Forensic Audit
*   Symptom: `OOMKilled` (Exit Code 137).
*   Root Cause: Massive memory spike upon broker connection during hydration.

### 3. Authorized Solution
[Solution Spec: NBI OOM Relaxation](../solutions/solution_spec_nbi_oom_relaxation.md)

---

## ISSUE #012: Deterministic Path Resolution & Source-Floor Alignment (REC-012)
### 1. Problem Statement
Build #19 failed with persistent `ModuleNotFoundError` despite context expansion due to package nesting mismatches.

### 2. Forensic Audit
*   Symptom: `ModuleNotFoundError: No module named 'common'`.
*   Root Cause: Fractured directory structure in container root.

### 3. Authorized Solution
[SOP-02: Directory Anchoring](../solutions/SOP-02.md)

---

## ISSUE #040: Topographical Code Ingestion - Empty Shells (REC-040)
### 1. Problem Statement
Microservices reached `Running` but crashed immediately because Dockerfiles lacked code `COPY` commands.

### 2. Forensic Audit
*   Symptom: Container filesystem missing `/var/teraflow/common`.
*   Root Cause: Fractured blueprint inheritance.

### 3. Authorized Solution
[SOP-03: Blueprint Reconciliation](../solutions/SOP-03.md)

---

## ISSUE #041: Module Resolution - The Proto Rift (REC-041)
### 1. Problem Statement
Services failed with `ModuleNotFoundError: common.proto` due to missing generated gRPC stubs.

### 2. Forensic Audit
*   Symptom: `ImportError` on generated Python code.
*   Root Cause: Gencode was expected in `/var/teraflow/common/proto` but was missing.

### 3. Authorized Solution
[Spec: gRPC Python Deadlock](../solutions/SPEC_GRPC_PYTHON_DEADLOCK.md)

---

## ISSUE #043: Resource Throttling - The Cottage Squeeze (REC-043)
### 1. Problem Statement
GKE node reached 97% CPU reservation, triggering scheduling deadlocks for new graduation pods.

### 2. Forensic Audit
*   Metric: `kubectl top nodes` showed 4.1/4.0 vCPU reservation.
*   Root Cause: Over-provisioning on the restricted Standard floor.

### 3. Authorized Solution
[SOVEREIGN DIRECTIVES](../solutions/SOVEREIGN%20DIRECTIVES.MD)

---

## ISSUE #045: System Header Reconciliation - libyang Source Build (REC-045)
### 1. Problem Statement
Build #72 failed due to version mismatch between `libyang` Python wrapper and Debian C-headers.

### 2. Forensic Audit
*   Symptom: `cc1: all warnings being treated as errors`.
*   Root Cause: Debian Bookworm `libyang3` incompatibility with TFS `libyang` 2.8.4.

### 3. Authorized Solution
[SOP-04: Foundation Hardening](../solutions/SOP-04.md)

---

## ISSUE #047: Total Sterilization & Recovery (REC-047)
### 1. Problem Statement
System state became polluted with 300GB of corrupted storage and 1,000+ local workspace modifications.

### 2. Forensic Audit
*   State: Deadlocked GKE floor and drifted GitHub workspace.
*   Impact: Non-deterministic build environment.

### 3. Authorized Solution
[SOP-06: Clean Room Recovery](../solutions/SOP-06.md)

---

## ISSUE #048: Docker Build Context Realignment (REC-048)
### 1. Problem Statement
Build #74 failed after workspace reset because Dockerfiles could not resolve source code from sub-directory contexts.

### 2. Forensic Audit
*   Symptom: `COPY failed: file not found`.
*   Root Cause: Docker build context was misaligned with the Repository Root.

### 3. Authorized Solution
[SOP-02: Directory Anchoring](../solutions/SOP-02.md)
