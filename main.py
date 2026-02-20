#!/usr/bin/env python3

import sys
import os
import importlib.util

def load_package(pkg_name, pkg_path):
    init_path = os.path.join(pkg_path, "__init__.py")
    spec = importlib.util.spec_from_file_location(pkg_name, init_path)
    pkg_module = importlib.util.module_from_spec(spec)
    sys.modules[pkg_name] = pkg_module
    spec.loader.exec_module(pkg_module)
    pkg_module.__path__ = [pkg_path]
    return pkg_module

def load_module(pkg_name, module_name, pkg_path):
    module_path = os.path.join(pkg_path, f"{module_name}.py")
    full_module_name = f"{pkg_name}.{module_name}"
    spec = importlib.util.spec_from_file_location(full_module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    module.__package__ = pkg_name
    sys.modules[full_module_name] = module
    spec.loader.exec_module(module)
    return module

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pkg_dir = os.path.join(base_dir, ".omni-autonomous-agent")
    pkg_name = "omni_agent_internal"
    
    try:
        load_package(pkg_name, pkg_dir)
        load_module(pkg_name, "constants", pkg_dir)
        load_module(pkg_name, "installer", pkg_dir)
        load_module(pkg_name, "session_manager", pkg_dir)
        cli = load_module(pkg_name, "cli", pkg_dir)
        cli.main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()