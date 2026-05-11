import os
import sys

# CONFIGURATION: Prohibited Legacy Strings
PROHIBITED_STRINGS = [
    "cogctl-gke-v01",
    "us-central1-docker.pkg.dev",
    "localhost:32000"
]

# TARGET DIRECTORIES
TARGET_DIRS = ["infra", "baseline"]

def verify_file(file_path):
    violations = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                for prohibited in PROHIBITED_STRINGS:
                    if prohibited in line:
                        violations.append((i + 1, prohibited, line.strip()))
    except Exception as e:
        print(f"[ERROR] Could not read {file_path}: {e}")
    return violations

def main():
    print("--- [SOP-07] MANIFEST PURITY AUDIT v4.0 ---")
    total_violations = 0
    for target in TARGET_DIRS:
        if not os.path.exists(target):
            continue
        print(f"[AUDIT] Scanning: {target}")
        for root, dirs, files in os.walk(target):
            for file in files:
                file_path = os.path.join(root, file)
                # Skip known binary or non-relevant files if necessary
                if file.endswith((".png", ".jpg", ".pyc", ".git")):
                    continue
                
                violations = verify_file(file_path)
                if violations:
                    print(f"  [VIOLATION] {file_path}:")
                    for line_num, string, content in violations:
                        print(f"    L{line_num}: Found '{string}' -> {content}")
                        total_violations += 1
    
    print("\n--- AUDIT SUMMARY ---")
    if total_violations == 0:
        print("[SUCCESS] Repository is PURIFIED. No legacy strings found in baseline/ or infra/.")
        sys.exit(0)
    else:
        print(f"[FAILURE] Found {total_violations} legacy string instances.")
        sys.exit(1)

if __name__ == "__main__":
    main()
