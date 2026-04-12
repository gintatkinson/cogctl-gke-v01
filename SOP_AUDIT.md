# SOP: FINAL VERIFICATION & AUDIT

## STAGE 0: Recovery Checkpoint (Mandatory)
1. **Verify Ingress:** Ensure `SUCCESSION_LOG.md` confirms `SOP-INGRESS COMPLETE`.
2. **Verify URL:** Ensure the public GKE Ingress URL (443) is reachable.

## I. The 13-Screen UI Audit
Every deployment is verified ONLY when the following 13 primary WebUI modules load correctly:
1. Dashboard
2. Context Overview
3. Device Inventory
4. Service Topology
5. Slice Management
6. Monitoring/KPIs
7. Policy Inventory
8. Automation Status
9. Workflow History
10. Identity/Users
11. Audit Logs
12. System Health
13. API Explorer

## II. Performance Audit
1. **Load Time:** Every module MUST render within a **3-second** limit.
2. **Persistence:** Verify that a browser refresh does not clear active session states or WSS connections.

## III. Persistence Checkpoint (Sovereign Save)
1. **Commit:** `git commit -m "CHECKPOINT: SOVEREIGN PRODUCTION AUDIT COMPLETE"`.
2. **Push:** Push to GitHub.
