# SOP: BOOTSTRAP (The Pre-Flight Skill)

This is a mandatory operational guardrail for all mission participants (AI or Human).

## 1. Foundational Health Check (The Node Fabric)
- **Node Readiness**: BEFORE starting any Turn/SOP, you MUST verify the cluster fabric via `/home/parallels/google-cloud-sdk/bin/kubectl get nodes`. 
- **The Blind Birth Gate**: If nodes are not present or 'Ready,' you MUST halt. This prevents 'Phantom Deployments' onto a ghost foundation.

## 2. Environment Readiness (Zero Trust)
- **Identity Bond**: Verify access via `/home/parallels/google-cloud-sdk/bin/gh auth status`.
- **Absolute Pathing**: ALWAYS use absolute paths for system tools.

## 3. Purity & Pollution Control
- **Temporary Scripts**: Use the `scratch/` directory for all tactical logic.
