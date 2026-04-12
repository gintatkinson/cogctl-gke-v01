# SOP: SOVEREIGN GKE GENESIS v5.0

## PURPOSE
To establish a "Certified Pure" GKE Sovereignty using an immutable, atomic bootstrap process.

## STAGE 0: WORKBENCH AUTHORIZATION
Before any infrastructure work begins, the agent MUST verify the persistent trust bond with the remote repository.

1. **Verify Handshake:** `ssh -T git@github.com`
2. **Identity Handshake:** Confirm authentication as `gintatkinson`.
3. **Restoration Rule:** If authentication fails, generate a new SSH key (`ssh-keygen`) and request authorization at [github.com/settings/keys](https://github.com/settings/keys).

## PREREQUISITES
1. **High-Entropy Identity:** Every ignition MUST generate a unique `$IDENTIFIER` (timestamp).
2. **Path Integrity:** Ensure `gcloud` is sourced from `/home/parallels/google-cloud-sdk/bin`.

---

## STEP I: IDENTITY INJECTION
Every deployment must generate a unique identifier to prevent metadata collision locks.
- **VPC Name:** `sovereign-vpc-$ID`
- **Subnet Name:** `sovereign-subnet-$ID`
- **Cluster Name:** `sovereign-genesis-$ID`

## STEP II: SOVEREIGN EGRESS (NAT)
A Cloud NAT gateway MUST be provisioned to allow private nodes to reach the Google Control Plane and Artifact Registry. Access without NAT is strictly prohibited for stability.

## STEP III: PRIVATE IGNITION
- **Rule 1:** Dedicated VPC per deployment.
- **Rule 2:** Mandate `--enable-private-nodes`.
- **Rule 3:** Mandate `--master-ipv4-cidr 172.16.0.0/28`.

---

## STAGE 0 RECOVERY: THE VACUUM SHIFT
If a deployment fails or stalls (e.g., Health-Checking 0/2 for >15 mins):
1. **LEAVE IT:** Do not attempt to patch or delete the stalled resources (which are likely metadata-locked).
2. **RE-START:** Execute the Genesis Engine with a NEW identifier.
3. **POST-PURGE:** Delete the old environment only after the new one is confirmed `RUNNING`.
