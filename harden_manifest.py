import sys, yaml

def repair_and_harden():
    """Formally repairs the manifest patching agent."""
    if len(sys.argv) < 5: sys.exit(1)
    file_path, service_name, tag, registry = sys.argv[1:]
    try:
        with open(file_path, 'r') as f:
            data = list(yaml.load_all(f, Loader=yaml.FullLoader))
        for doc in data:
            if not doc or 'kind' not in doc: continue
            if doc['kind'] in ['Deployment', 'StatefulSet']:
                for container in doc['spec']['template']['spec']['containers']:
                    container['image'] = f"{registry}/{service_name}:{tag}"
                    container['imagePullPolicy'] = 'Always'
        with open(file_path, 'w') as f:
            yaml.dump_all(data, f)
    except Exception as e:
        print(f"FATAL: Agent failed to patch {file_path}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    repair_and_harden()
