# SPEC_CONNECTIVE_TISSUE_GAP.md: Universal Foundation Integrity

## 1. Incident Overview
**IncidentID**: IG-055 (Connective Tissue Failure)
**Status**: REMEDIATED
**Symptom**: `ModuleNotFoundError: No module named 'common.Constants'` and `ModuleNotFoundError: No module named 'context'` during service ignition.

## 2. Forensic Analysis
TeraFlowSDN (TFS) microservices are not standalone binaries. They rely on:
1. **Shared Logic**: The `common/` package (Constants, Config, Logging).
2. **Peer Clients**: Client-side stubs for inter-service communication (e.g., `context.client`, `device.client`).

The initial "Gold Master" synthesis omitted these modules, resulting in "Module Isolation" where even peer services could not see the vital connective tissue of the enclave.

## 3. Resolution Logic
The Gold Master Foundation (`Dockerfile.base`) has been refactored to ingest all core connective tissue:
- **Common Module**: Full source tree ingestion.
- **Service Clients**: Explicit `COPY` of `context/client`, `device/client`, and `service/client`.

## 4. Lesson 4: The Packaging Gap
**IncidentID**: IG-056 (Packaging Gap)
**Symptom**: `ModuleNotFoundError` despite file presence.
**Physics**: Python requires the parent directory of a package to contain an `__init__.py` for the loader to recognize the sub-namespace. Additionally, `PYTHONPATH` must explicitly anchor the enclave root.
**Resolution**: 
1. Ingest mandatory `__init__.py` files into core service roots.
2. Hard-lock `ENV PYTHONPATH="/var/teraflow"` in the Gold Master foundation.

## 5. Verification
Confirmed via Cloud-Native Audit (Build #f1df3ad3):
`-rw-r--r-- 1 root root 6016 Apr 19 15:34 /var/teraflow/common/Constants.py`

## 5. Cost Stewardship (REC-006)
To avoid the "High-CPU Tax" during synthesis, all future builds of the Connective Tissue Foundation must utilize the **Sequential Throttling** pattern (infra/cloudbuild_gold_master_sequential.yaml).
