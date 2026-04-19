# SOP-03: Foundation Layer Deployment

## 1. Subprocess: Database Layer Provisioning
- **Action**: Deploy the CockroachDB (CRDB) stateful set.
- **Verification**: Pods `-0`, `-1`, `-2` must be `Running`.
- **Constraint**: `CRDB_NAMESPACE` must be set to `default`.

## 2. Subprocess: Messaging Middleware Recovery
- **Action**: Deploy NATS (JetStream) for internal service communication.
- **Reference**: `baseline/tfs-controller/manifests/nats.yaml`.

## 3. Subprocess: Streaming Configuration
- **Action**: Deploy Kafka for KPI management and telemetry.

## 4. Subprocess: Database Schema Initialization
- **Action**: Run SQL/Init scripts to create the `tfs_context` and `tfs_device` databases.

## 5. Subprocess: Foundation Health Probing
- **Action**: Verify that the NATS and Kafka external services are reachable within the VPC.

---
**Status**: ACTIVE
**Source Files**: Refactored from `SOP_GENESIS.md`, `SUCCESSION_LOG_BLACKBOX.md`.
