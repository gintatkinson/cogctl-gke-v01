# SOP: BOOTSTRAP (The Pre-Flight Skill)

This is a mandatory operational guardrail for all mission participants (AI or Human).

## 1. Environment Readiness (Zero Trust)
- **Identity Bond**: Verify access via `/home/parallels/google-cloud-sdk/bin/gh auth status`.
- **Absolute Pathing**: ALWAYS use absolute paths for system tools:
  - `/home/parallels/google-cloud-sdk/bin/gcloud`
  - `/home/parallels/google-cloud-sdk/bin/kubectl`
  - `/home/parallels/google-cloud-sdk/bin/gh`

## 2. Purity & Pollution Control
- **Temporary Scripts**: All tactical/debug scripts MUST be created in the `scratch/` directory.
- **Log Hygiene**: Standalone `.log` files are prohibited in the repository root. Log directly to the **Succession Log**.
- **Issue Tracking**: Use native GitHub Issues. Local `ISSUES.md` files are forbidden.

## 3. The "Absolute Beginning" Disposal
In the event of a "Genesis Reset," this SOP must be archived in `.sovereign_archive/` to restore the repository to a state of absolute purity.
