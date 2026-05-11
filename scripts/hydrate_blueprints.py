import os
import sys

# Hydration Map
REGISTRY = sys.argv[1]
PROJECT_ID = sys.argv[2]

REPLACEMENTS = {
    "${_CUSTOMER_REGISTRY}": REGISTRY,
    "${_CUSTOMER_PROJECT_ID}": PROJECT_ID
}

def hydrate_file(file_path):
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
    target_dirs = ["baseline/tfs-controller/manifests"]
    count = 0
    for target in target_dirs:
        for root, dirs, files in os.walk(target):
            for file in files:
                if hydrate_file(os.path.join(root, file)):
                    count += 1
    print(f"[SUCCESS] Total files hydrated: {count}")

if __name__ == "__main__":
    main()
