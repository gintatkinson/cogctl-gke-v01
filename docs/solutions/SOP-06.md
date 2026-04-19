# SOP-06: Operational Validation & Handover

## 1. Subprocess: 13-Screen UI Audit
- **Action**: Manually verify all 13 modules (Context, Device, Service, etc.) load correctly.
- **Checklist**: `13_SCREEN_AUDIT.md`.

## 2. Subprocess: KPI Trace Verification
- **Action**: Confirm telemetry flow through Kafka and KPI Manager pods.

## 3. Subprocess: Log Aggregation Review
- **Action**: Check `webuiservice` and `nbiservice` logs for 404 or 502 errors during the audit.

## 4. Subprocess: Knowledge Anchoring
- **Action**: Ensure all technical resolutions (e.g., `CRDB_NAMESPACE`) are logged in the project's permanent record.
- **Reference**: `SUCCESSION_LOG_BLACKBOX.md`, GitHub Issues.

## 5. Subprocess: Mission Graduation
- **Action**: Perform final clean-up and update the `walkthrough.md`.

---
**Status**: ACTIVE
**Source Files**: Refactored from `SOP_AUDIT.md`, `SOP_KNOWLEDGE_ANCHORING.md`.
