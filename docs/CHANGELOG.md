# Changelog

All notable changes to this project will be documented in this file.

## [v3.1-graduation-fixes] - 2026-04-29
### Fixed
- **telemetryservice**: Resolved a `CrashLoopBackOff` state in the `frontend` container by reapplying the baseline manifest. The active cluster configuration had drifted and was missing the `CRDB_SSLMODE=disable` environment variable. 
