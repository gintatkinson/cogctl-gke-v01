import os
import re

def extract_imports(file_path):
    with open(file_path, 'r', errors='ignore') as f:
        content = f.read()
    
    # Match 'import module' and 'from module import ...'
    imports = re.findall(r'^\s*import\s+([\w\.]+)', content, re.MULTILINE)
    from_imports = re.findall(r'^\s*from\s+([\w\.]+)', content, re.MULTILINE)
    
    return [i.split('.')[0] for i in (imports + from_imports)]

def main():
    src_dir = 'baseline/tfs-controller/src'
    all_deps = set()
    
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                all_deps.update(extract_imports(os.path.join(root, file)))
    
    # Filter out local modules and standard library (coarse filter)
    # We'll just print them all and pick the obvious ones
    print('\n'.join(sorted(list(all_deps))))

if __name__ == '__main__':
    main()
