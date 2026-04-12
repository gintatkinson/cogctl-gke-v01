# SOVEREIGN SYSTEM DESIGN SPECIFICATION (v2.0)

## 1. Architectural Mandates (Directive 12)
The Sovereign Domain requires absolute topological isolation and **Infrastructure Immutability**.

## 2. Infrastructure Standards

### **2.1 Immutable Identity (High-Entropy Naming)**
- **Requirement:** Every infrastructure resource (VPC, Subnet, Cluster) MUST possess a unique high-entropy suffix (e.g., `$(date +%s)`).
- **Purpose:** To eliminate project-level metadata locks (BB-015) and ensure that restoration/recovery is never blocked by a failed previous state.
- **Constraint:** Static naming for VPCs is strictly prohibited in Production.

### **2.2 Sovereign Egress (Cloud NAT)**
- **Requirement:** Every Sovereign VPC must possess a Cloud NAT gateway.
- **Purpose:** To allow private GKE nodes to securely reach Google Control Plane public endpoints and fetch container images/metadata.

### **2.3 Private Ignition (GKE Nodes)**
- **Isolation Level:** `--enable-private-nodes`.
- **Visibility:** Master API endpoint is accessible via the Service Bridge (VPC Peering).
- **Security:** Public node IPs are strictly prohibited.

## 3. Deployment Logic (The Vacuum Shift)
- **Model:** Deployment follows an "Immutable Birth" pattern. A new environment is birthed on a fresh identifier while old environments are background-decommissioned.

## 4. Operational Requirements

### 4.1: Workbench Authorization (The Succession Gate)
To maintain the **Succession Log** and achieve **Persistence Checkpoints**, the workbench MUST be authenticated with GitHub via a verified SSH key. 
- **Requirement:** Active SSH handshake (`ssh -T git@github.com`).
- **Dependency:** Valid Ed25519 key registered in GitHub account settings.
- **Fail-Safe:** No infrastructure modifications are permitted unless this trust bond is confirmed.
- **Persistence:** Mandatory commit of architecture state (VPC IDs) to the Succession Log.

---
**Standard Reference:** SUCCESSION_LOG_BLACKBOX.md -> BB-011, BB-012, BB-013, BB-014, BB-015.
