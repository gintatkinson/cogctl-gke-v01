# LOG_MISSION_LEARNINGS.md: Sovereign GKE Enclave

This ledger codifies the forensic architectural lessons learned during the v3.0 Enclave restoration.

## Lesson 1: The Parallel OOM Spiral
**Symptom**: Cloud Build failures during the 10-service synthesis phase.
**Physics**: Standard Cloud Build workers (4GB RAM) cannot sustain the parallel execution of multiple Docker builds inheriting from the same heavy Gold Master. 
**Resolution**: Parallel builds require the `E2_HIGHCPU_8` tier. Cost optimization requires **Sequential Throttling** on standard workers to maintain a low memory footprint.

## Lesson 2: The Module Isolation Gap
**Symptom**: `ModuleNotFoundError` during service ignition.
**Physics**: TFS microservices are not atomic binaries; they require the `common` shared logic AND the client libraries of peer services (`context`, `device`, `service`) to initialize internal collectors.
**Resolution**: Inter-service dependencies must be explicitly ingested during the "Gold Master" synthesis phase.

## Lesson 3: Foundation Purity (Gold Master)
**Symptom**: Inconsistent behavior and "Blind Births" across the enclave.
**Physics**: Shared logic drift occurs when services inherit from different foundation baselines.
**Resolution**: All core logic and client connectivity stubs must be anchored in the `Dockerfile.base` (The Gold Master) to ensure architectural parity across all 10 services.
