import os
import ast
import pkg_resources

# Set path to your project folder
project_dir = "."

all_imports = set()

for root, _, files in os.walk(project_dir):
    for file in files:
        if file.endswith(".py"):
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                try:
                    tree = ast.parse(f.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for n in node.names:
                                all_imports.add(n.name.split('.')[0])
                        elif isinstance(node, ast.ImportFrom):
                            all_imports.add(node.module.split('.')[0])
                except Exception:
                    continue

# Get installed packages
installed = {pkg.key: pkg.version for pkg in pkg_resources.working_set}

print("✅ Packages used by your app:")
for name in sorted(all_imports):
    pkg_name = name.lower()
    if pkg_name in installed:
        print(f"{pkg_name}=={installed[pkg_name]}")
    else:
        print(f"# {name} not found in installed packages")
