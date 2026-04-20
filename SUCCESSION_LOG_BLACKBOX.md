REC-005: Local Toolchain Isolation (Halt-on-Gap Adaptation). The local host lacks the 'docker' binary. Forensic audits of images must be delegated to Cloud Build verification workers using ad-hoc manifests (infra/cloudbuild_forensic_audit.yaml) to maintain Antigravity Purity.

REC-006: Sequential Memory Throttling (Cost Stewardship). Pivot to a single-threaded build loop (infra/cloudbuild_gold_master_sequential.yaml) to ensure image synthesis remains within the 4GB RAM threshold of standard workers, avoiding high-cost hardware tax.
