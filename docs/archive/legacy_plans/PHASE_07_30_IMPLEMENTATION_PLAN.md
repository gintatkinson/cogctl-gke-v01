# PHASE 7.30: Enclave Resuscitation & RC4 Synthesis

## 1. Architectural Context
The deployment of `rc3` resulted in an enclave-wide `CrashLoopBackOff` cascade due to two distinct packaging failures:
1.  **Baseline Regression:** The `nats-py` broker dependency was lost during the Phase 7.18 cryptographic revert, leaving the foundational layer unable to boot.
2.  **Namespace Drift:** Phase 7.25 successfully isolated gRPC synthesis to the `proto/` directory, but failed to map the resulting stubs to the `/var/teraflow/common/proto/` namespace expected by the Werkzeug/Flask workers.

## 2. Execution Parameters
The Antigravity Agent is authorized to lift the Dead Man's Switch to execute the following structural anchors:

### Step 1: Dependency Anchoring
* **Target:** `baseline/tfs-controller/src/common/requirements_unified.in`
* **Action:** Append `nats-py` to permanently cure the foundational DNA.

### Step 2: Namespace Routing
* **Target:** `baseline/tfs-controller/src/webui/Dockerfile` (and related build files)
* **Action:** Inject the following routing command post-synthesis:
    `RUN mkdir -p /var/teraflow/common/proto && cp -r /var/teraflow/proto/* /var/teraflow/common/proto/ && touch /var/teraflow/common/proto/__init__.py`

### Step 3: Global Synthesis (RC4)
* **Target:** `infra/cloudbuild_gold_master_sequential.yaml`
* **Action:** Expand `_SERVICES` to include all 10 microservices, bump `_TAG` to `2026-04-21-rc4`, and trigger the global build factory. Commit all changes to `main` prior to execution.
