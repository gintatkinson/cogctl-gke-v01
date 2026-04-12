# SUCCESSION LOG: THE BLACK BOX (FLIGHT RECORDER)

## Purpose
Knowledge acquired during failure is the most critical asset for recovery. This high-frequency log records tactical discoveries, dependency conflicts, and failed attempts *immediately* during SOP execution to survive system crashes.

---

## I. Genesis Recovery Stream

### BB-001: Antigravity Context Persistence
- **Discovery:** In the event of a hard crash, the agent's internal thought history is lost.
- **Lock:** The **Succession Log** (GitHub) and this **Black Box** (Local/Sync) are the only survival mechanisms.
- **Protocol:** Manual sync/push is required regularly even mid-SOP until agent authentication is established.

### BB-002: Service Timeout (Handshake Storms)
- **Discovery:** Rapid-fire deployment of microservices causes GRP-web timeouts.
- **Lock:** Implemented **The Backoff Law** (mandatory sleep) in `infra/bootstrap.sh`.

### BB-003: Viewport Violation (RECOVERY)
- **Discovery:** Attempting to use local Docker for Artifact Sync violated the **Viewport Principle** (Rule 2) and failed due to missing toolchains on the host.
- **Lock:** All binary movements MUST occur within the GCP Data Plane (Cloud Build).
- **Protocol:** Use `gcloud builds submit` with `infra/cloudbuild_sync.yaml`.

### BB-004: GitHub Auth Blocker
- **Discovery:** git push failed due to missing auth. gh status is unauthenticated.
- **Action:** Awaiting user to populate GITHUB_SOVEREIGN_PAT in Secret Manager.


### BB-005: Identity Secured
- **Discovery:** Received GitHub PAT. Stored securely in Secret Manager (v1).
- **Action:** Proceeding to Sovereign Save (Push).


### BB-009: Git Ref Mismatch Recovery
- **Discovery:** fatal: cannot lock ref 'HEAD'. Caused by IDE watcher vs. Agent URL-reset conflict.
- **Status:** origin/main is confirmed at 1fb6774. Sync is successful.
- **Action:** Executing git reset to satisfy IDE state.

