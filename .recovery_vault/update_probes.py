import os
import glob
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True

manifests_dir = "baseline/tfs-controller/manifests"
for filename in glob.glob(os.path.join(manifests_dir, "*.yaml")):
    with open(filename, 'r') as f:
        try:
            docs = list(yaml.load_all(f))
        except Exception as e:
            continue
            
    changed = False
    for doc in docs:
        if not doc: continue
        if doc.get('kind') == 'Deployment':
            spec = doc.get('spec', {})
            template = spec.get('template', {})
            tspec = template.get('spec', {})
            
            containers = tspec.get('containers', [])
            for c in containers:
                for probe_type in ['livenessProbe', 'readinessProbe', 'startupProbe']:
                    if probe_type in c:
                        probe = c[probe_type]
                        if 'initialDelaySeconds' not in probe or probe['initialDelaySeconds'] < 10:
                            probe['initialDelaySeconds'] = 10
                            changed = True
                        if probe.get('failureThreshold') != 5:
                            probe['failureThreshold'] = 5
                            changed = True
                            
    if changed:
        with open(filename, 'w') as f:
            yaml.dump_all(docs, f)
        print(f"Updated {filename}")
