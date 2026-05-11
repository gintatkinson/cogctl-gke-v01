# Sovereign Graduation v3.2 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Deterministic graduation of the 48-service Sovereign stack with a parallelized forge and validated chaos survivability.

**Architecture:** Parallelized Cloud Build for component forging, structural YAML mutation via PyYAML for induction, and automated CSP-01 execution with T-Delta telemetry.

**Tech Stack:** GKE, Google Cloud Build, Terraform, PyYAML.

---

### Task 1: Parallelize The Forge
**Goal:** Accelerate image building by running 13 service builds concurrently.

**Files:**
- Modify: `infra/cloudbuild_graduation_final.yaml`

**Step 1: Define concurrent steps**
Split the sequential loop in `infra/cloudbuild_graduation_final.yaml` into 13 separate `waitFor: ['foundation']` steps.

**Step 2: Commit**
```bash
git add infra/cloudbuild_graduation_final.yaml
git commit -m "feat: parallelize component forge"
```

### Task 2: Implement Structural Truth Engine
**Goal:** Replace regex-based manifest patching with PyYAML to ensure schema integrity.

**Files:**
- Modify: `infra/cloudbuild_graduation_final.yaml`

**Step 1: Inject PyYAML induction logic**
Add `pip3 install --user PyYAML --break-system-packages` to the induction step.

**Step 2: Rewrite harden_manifest.py**
Implement `yaml.safe_load_all()` and structural mutation for `env`, `resources`, and `strategy`.

**Step 3: Commit**
```bash
git add infra/cloudbuild_graduation_final.yaml
git commit -m "feat: implement structural YAML orchestrator"
```

### Task 3: Execute Green Sweep & CSP-01
**Goal:** Hydrate the cluster and trigger the node amputation protocol.

**Step 1: Trigger Graduation**
Run: `gcloud builds submit --config infra/cloudbuild_graduation_final.yaml ...`

**Step 2: Monitor Context-Gate**
Run: `kubectl get pods -w`
Expected: `contextservice` 1/1 Running.

**Step 3: Execute Amputation**
Run: `gcloud compute instances delete [NODE_NAME] --zone us-central1-a --quiet`

**Step 4: Audit T-Delta**
Measure recovery time. Update GitHub Issue #87.
