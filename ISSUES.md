# MISSION ISSUES LEDGER

## ISSUE-001: Missing Keycloak Manifests
- **Raised:** 2026-04-13
- **Severity:** CRITICAL (Blocker for SOP-VAULT Stage II)
- **Description:** The SOP_VAULT document mandates deployment of Keycloak via the "official TFS installation path," yet these manifests are absent from the `tfs/controller` distribution. 
- **Impact:** Cannot move to Identity Bootstrap or WebUI Audit without the OIDC provider.
- **Action Plan:**
    1. Auditing ETSI GitLab group `tfs` for a `deployment` project.
    2. Checking `tfs/controller` sub-directories for hidden Helm charts.
    3. Reporting to User if no CLI-native source is found.
- **Status:** OPEN (Auditing)
