# SOVEREIGN GKE GENESIS: DURABILITY CHECKLIST (GOLDEN RULES)

Before initiating ANY infrastructure deployment or "resurrection," the agent MUST verify that these proven fixes are declaratively anchored in the repository.

## 1. STORAGE (SOP-01)
- [ ] `infra/storage-class-hardened.yaml` exists and is the FIRST induction step.
- [ ] Baseline manifests (CockroachDB, Kafka, QuestDB) use `storageClassName: hardened-storage`.

## 2. PERSISTENCE PERMISSIONS (SOP-02)
- [ ] `baseline/tfs-controller/manifests/kafka/single-node.yaml` includes:
  ```yaml
  securityContext:
    fsGroup: 1001
  ```
- [ ] Volume mounts are correctly configured for non-root user access.

## 3. OPERATOR VISIBILITY (SOP-03)
- [ ] `baseline/tfs-controller/manifests/cockroachdb/operator.yaml` is set to global watch:
  ```yaml
  - name: WATCH_NAMESPACE
    value: ""
  ```

## 4. DECLARATIVE PURITY (SOP-04)
- [ ] NO `sed` commands in `infra/awake.yaml` or `infra/resurrect.yaml`.
- [ ] Baseline manifests are permanently corrected for the target namespace (`sovereign-genesis`).
- [ ] Image tags are pinned to the verified graduation release (`rc13-verified`).

## 5. SECRET INDUCTION (SOP-05)
- [ ] `baseline/tfs-controller/manifests/graduation_secrets.yaml` exists.
- [ ] Pipeline inducts secrets BEFORE inducting backbone or application services.

## 6. NAMESPACE GOVERNANCE (SOP-06)
- [ ] All deployments are targeted at `sovereign-genesis`.
- [ ] NEVER deploy to `default`.

## 7. STATE AUDIT (SOP-07)
- [ ] Verify `gs://cogctl-gke-v01-tfstate/` is free of orphaned `.tflock` files.
- [ ] Confirm no concurrent Terraform processes are active.
