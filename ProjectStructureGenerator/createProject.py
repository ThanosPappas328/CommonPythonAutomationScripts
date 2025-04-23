import os
import tkinter as tk
from tkinter import messagebox, ttk

PROJECT_TEMPLATES = {
    "React": ["src", "public", "components", "README.md", ".gitignore"],
    "Next.js": ["pages", "public", "components", "README.md", ".gitignore"],
    "Express": ["routes", "controllers", "models", "README.md", ".gitignore", "index.js"],
    "Flutter": ["lib", "assets", "README.md", ".gitignore"],
}

def create_boilerplate(project_name, project_type):
    if not project_name or not project_type:
        messagebox.showerror("Error", "Please enter a project name and type.")
        return

    base_path = os.path.join(os.getcwd(), project_name)
    try:
        os.makedirs(base_path, exist_ok=True)
        for item in PROJECT_TEMPLATES[project_type]:
            path = os.path.join(base_path, item)
            if '.' in item:
                with open(path, 'w') as f:
                    f.write(f"# {project_type} Boilerplate\n") if item == "README.md" else None
            else:
                os.makedirs(path, exist_ok=True)
        messagebox.showinfo("Success", f"{project_type} project '{project_name}' created!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not create project: {e}")

# GUI Setup
root = tk.Tk()
root.title("Boilerplate Generator")

tk.Label(root, text="Project Name:").pack(pady=5)
project_name_entry = tk.Entry(root, width=40)
project_name_entry.pack()

tk.Label(root, text="Select Project Type:").pack(pady=5)
project_type_var = tk.StringVar()
project_type_menu = ttk.Combobox(root, textvariable=project_type_var, values=list(PROJECT_TEMPLATES.keys()), state="readonly")
project_type_menu.pack()

tk.Button(root, text="Generate Project", command=lambda: create_boilerplate(project_name_entry.get(), project_type_var.get())).pack(pady=15)

root.geometry("350x200")
root.mainloop()
