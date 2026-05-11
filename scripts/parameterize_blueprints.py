import os

# CONFIGURATION: Parameterization Map
REPLACEMENTS = {
    "us-central1-docker.pkg.dev/cogctl-gke-v01/sovereign-tfs": "${_CUSTOMER_REGISTRY}",
    "us-central1-docker.pkg.dev": "${_TARGET_REGION}-docker.pkg.dev",
    "cogctl-gke-v01": "${_CUSTOMER_PROJECT_ID}",
    "localhost:32000": "${_CUSTOMER_REGISTRY}"
}

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        new_content = content
        for target, replacement in REPLACEMENTS.items():
            new_content = new_content.replace(target, replacement)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
    except Exception as e:
        print(f"[ERROR] Failed {file_path}: {e}")
    return False

def main():
    target_dirs = ["infra", "baseline"]
    count = 0
    for target in target_dirs:
        for root, dirs, files in os.walk(target):
            for file in files:
                if process_file(os.path.join(root, file)):
                    count += 1
    print(f"[SUCCESS] Total files purified: {count}")

if __name__ == "__main__":
    main()
