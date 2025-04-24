import os

def parse_advanced_mode(base_path, structure_text):
    lines = [line.rstrip() for line in structure_text.strip().splitlines() if line.strip()]
    stack = []  # Stack to keep track of parent folder path and indentation level
    created_folders = []

    for line in lines:
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        # Pop from stack until the correct level is found based on indentation
        while stack and stack[-1][0] >= indent:
            stack.pop()

        # Compute the full path for the current folder
        parent_path = stack[-1][1] if stack else base_path
        full_path = os.path.join(parent_path, stripped.rstrip('/'))

        # Skip files (we're only creating folders)
        if not stripped.endswith("/"):
            continue

        # Create the folder if it doesn't exist
        if not os.path.exists(full_path):
            os.makedirs(full_path, exist_ok=True)
            created_folders.append(full_path)

        # Push the created folder onto the stack
        stack.append((indent, full_path))

    return created_folders
