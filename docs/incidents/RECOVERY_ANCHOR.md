# RECOVERY ANCHOR: SOVEREIGN REBIRTH v3.5

**Current State**: TABULA RASA (Account Sterilization in Progress)
**Mandated Priority**: 100% Replication of Core 11 Graduation.

## I. THE CORE 11 WHITELIST
Only these 11 services are permitted for induction:
1. `contextservice` | 2. `deviceservice` | 3. `serviceservice`
4. `pathcompservice` | 5. `sliceservice` | 6. `interdomainservice`
7. `monitoringservice` | 8. `automationservice` | 9. `policyservice`
10. `teservice` | 11. `webuiservice`

## II. INFRASTRUCTURE BASELINE
*   **Hardware**: 3 Nodes (e2-standard-4)
*   **Networking**: Global Static IP `tfs-static-ip`
*   **Storage**: StorageClass `hardened-storage` (Immediate Binding)

## III. PERSISTENCE BACKBONE (EXTERNAL SOURCE)
*   **Operator**: `cockroachdb/cockroach-operator:v2.10.0`
*   **Cluster**: `cockroachdb/cockroach:v22.2.8`
*   **Message Broker**: NATS / Kafka (Single Node)

## IV. SUCCESS CRITERIA
1.  All 11 Core pods in `Running` state.
2.  GCE Ingress mapped to `/webui/`.
3.  Accessible WebUI at `http://34.49.238.225/webui/`.

---
**STATUS**: Awaiting GKE Deletion Confirmation...
