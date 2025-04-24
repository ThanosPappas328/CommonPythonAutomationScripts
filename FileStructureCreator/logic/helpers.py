import os
from datetime import datetime

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def ensure_export_folder(base_path):
    export_folder = os.path.join(base_path, "_folder_plans")
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    return export_folder
