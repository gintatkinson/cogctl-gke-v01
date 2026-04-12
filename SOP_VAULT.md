# SOP: VAULT & IDENTITY

## STAGE 0: Recovery Checkpoint (Mandatory)
1. **Verify Genesis:** Ensure `SUCCESSION_LOG.md` confirms `SOP-GENESIS COMPLETE`.
2. **Verify Registry:** Confirm Artifact Registry contains the "Locked" ETSI binaries.
3. **Verify Auth:** Ensure `gcloud` is authenticated for project `cogctl-gke-v01`.

## I. Secret Management
1. **Sync GitLab PAT:** Retrieve from GCP Secret Manager.
2. **Infrastructure Secrets:** Create K8s secrets for GKE:
   - `tfs-gitlab-auth` (Docker login for Artifact Registry/GitLab).
   - `tfs-database-creds` (For CockroachDB/PostgreSQL).
   - `tfs-keycloak-creds` (For Identity).

## II. Keycloak Deployment
1. **Bootstrap:** Deploy Keycloak following the official TFS installation path.
2. **Realm Configuration:**
   - Create `tfs` realm.
   - Configure `tfs-dashboard` public client.
3. **Validation:** Verify Keycloak Login UI is reachable on internal pod IP.

## III. Persistence Checkpoint (Sovereign Save)
1. **Commit:** `git commit -m "CHECKPOINT: SOP-VAULT COMPLETE"`.
2. **Push:** Push to GitHub.
