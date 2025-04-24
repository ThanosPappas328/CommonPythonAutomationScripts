import os
import json
import yaml
from datetime import datetime

from logic.helpers import get_timestamp, ensure_export_folder

def export_all(base_path, structure_text):
    timestamp = get_timestamp()
    export_folder = ensure_export_folder(base_path)

    # Export TXT
    txt_file = os.path.join(export_folder, f"folder_structure_{timestamp}.txt")
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(structure_text.strip())

    # Export JSON
    json_file = os.path.join(export_folder, f"folder_structure_{timestamp}.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(structure_to_dict(structure_text), f, indent=2)

    # Export YAML
    yaml_file = os.path.join(export_folder, f"folder_structure_{timestamp}.yaml")
    with open(yaml_file, "w", encoding="utf-8") as f:
        yaml.dump(structure_to_dict(structure_text), f)

    return export_folder

def structure_to_dict(structure_text):
    lines = [line.rstrip() for line in structure_text.strip().splitlines() if line.strip()]
    result = {}
    stack = []

    for line in lines:
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        while stack and stack[-1][0] >= indent:
            stack.pop()

        parent = stack[-1][1] if stack else result
        parent[stripped.rstrip('/')] = {}

        stack.append((indent, parent[stripped.rstrip('/')]))  # Add the next folder to the stack

    return result
