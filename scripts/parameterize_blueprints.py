import os
import yaml
import sys

# CONFIGURATION: Parameterization Tokens
REGISTRY_TARGET = "us-central1-docker.pkg.dev/cogctl-gke-v01/sovereign-tfs"
REGISTRY_REPLACEMENT = "${_CUSTOMER_REGISTRY}"
PROJECT_TARGET = "cogctl-gke-v01"
PROJECT_REPLACEMENT = "${_CUSTOMER_PROJECT_ID}"

def parameterize_object(obj):
    """Recursively search and replace target strings in a YAML object."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str):
                # Replace static registry paths
                if REGISTRY_TARGET in value:
                    obj[key] = value.replace(REGISTRY_TARGET, REGISTRY_REPLACEMENT)
                # Replace standalone project IDs
                elif PROJECT_TARGET in value:
                    obj[key] = value.replace(PROJECT_TARGET, PROJECT_REPLACEMENT)
                
                # Standardize legacy dev/local images
                if "localhost:32000" in obj[key]:
                    obj[key] = f"{REGISTRY_REPLACEMENT}/opticalcontroller:rc13-verified"
                if "busybox:" in obj[key] and "1.36" not in obj[key]:
                    obj[key] = "busybox:1.36"
                    
            else:
                parameterize_object(value)
    elif isinstance(obj, list):
        for item in obj:
            parameterize_object(item)

def process_directory(directory):
    print(f"[PROCESS] Auditing: {directory}")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        # Load all documents in the file
                        docs = list(yaml.load_all(f, Loader=yaml.SafeLoader))
                    
                    if not docs or all(d is None for d in docs):
                        continue

                    for doc in docs:
                        parameterize_object(doc)

                    with open(file_path, 'w') as f:
                        yaml.dump_all(docs, f, default_flow_style=False, sort_keys=False)
                    print(f"  [SUCCESS] Parameterized: {file}")
                except Exception as e:
                    print(f"  [ERROR] Failed to process {file}: {e}")

if __name__ == "__main__":
    target_dirs = ["infra", "baseline/tfs-controller/manifests"]
    for target in target_dirs:
        if os.path.exists(target):
            process_directory(target)
        else:
            print(f"[SKIP] Directory not found: {target}")
