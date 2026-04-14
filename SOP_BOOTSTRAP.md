# SOP: BOOTSTRAP (The Pre-Flight Skill)

This is a mandatory operational guardrail for all mission participants (AI or Human).

## 1. Foundational Health Check (The Node Fabric)
- **Node Readiness**: BEFORE starting any Turn/SOP, you MUST verify the cluster fabric via the **Google Cloud Console** (Kubernetes Engine -> Clusters) or by submitting a **Cloud Build Audit Job**. 
- **The Blind Birth Gate**: If nodes are not present or 'Ready,' you MUST halt. This prevents 'Phantom Deployments' onto a ghost foundation.

## 2. Environment Readiness (Zero Trust)
- **Identity Bond**: Verify access via `/home/parallels/google-cloud-sdk/bin/gh auth status`.
- **Absolute Pathing**: ALWAYS use absolute paths for system tools (`gh`, `gcloud`).
- **Forbidden Tools**: `kubectl` and `gke-gcloud-auth-plugin` are strictly forbidden on the viewport host. 

## 3. Purity & Pollution Control
- **Temporary Scripts**: Use the `scratch/` directory for all tactical logic.
- **Experience Harvest**: BEFORE executing any `git clean` or infrastructure deletion, you MUST distilling raw logs into the `SUCCESSION_LOG.md`.

## 4. Knowledge Anchoring (Fidelity Gate)
- **Problem/Solution Mapping**: Before executing any major architectural fix, follow [SOP_KNOWLEDGE_ANCHORING.md](SOP_KNOWLEDGE_ANCHORING.md). 
- **Requirement**: Create a high-fidelity GitHub Issue and link it to a standalone Solution Specification.
