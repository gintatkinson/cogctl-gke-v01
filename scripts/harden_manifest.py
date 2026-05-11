import sys, yaml

def harden():
    if len(sys.argv) < 5:
        sys.exit(1)
    file_path, service_name, tag, registry = sys.argv[1:]
    try:
        with open(file_path, 'r') as f:
            data = list(yaml.load_all(f, Loader=yaml.FullLoader))
        for doc in data:
            if not doc or 'kind' not in doc:
                continue
            if doc['kind'] in ['Deployment', 'StatefulSet']:
                for container in doc['spec']['template']['spec']['containers']:
                    if 'v3.1-graduation' in container.get('image', ''):
                        # Heuristic: if container name is 'backend' and service is pathcomp, use pathcomp-backend
                        if container['name'] == 'backend' and service_name == 'pathcompservice':
                            container['image'] = f"{registry}/pathcomp-backend:{tag}"
                        else:
                            container['image'] = f"{registry}/{service_name}:{tag}"
                        container['imagePullPolicy'] = 'Always'
        with open(file_path, 'w') as f:
            yaml.dump_all(data, f)
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    harden()
