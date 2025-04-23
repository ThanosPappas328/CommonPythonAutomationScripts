import os
import tkinter as tk
from tkinter import filedialog, messagebox


def create_structure(base_path, structure_text):
    folders = [line.strip() for line in structure_text.strip().splitlines() if line.strip()]
    created_folders = []

    for folder in folders:
        full_path = os.path.join(base_path, folder)
        os.makedirs(full_path, exist_ok=True)
        created_folders.append(full_path)

    return created_folders


def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        base_path_var.set(folder)


def generate_folders():
    base_path = base_path_var.get()
    structure_text = folder_structure_text.get("1.0", tk.END)

    if not base_path or not os.path.isdir(base_path):
        messagebox.showerror("Error", "Please select a valid base folder.")
        return

    if not structure_text.strip():
        messagebox.showerror("Error", "Please enter folder structure.")
        return

    created = create_structure(base_path, structure_text)
    messagebox.showinfo("Success", f"✅ Created {len(created)} folders successfully.")


# --- GUI SETUP ---
root = tk.Tk()
root.title("📁 Folder Structure Generator")

# Set window size and center
w, h = 500, 400
x = (root.winfo_screenwidth() - w) // 2
y = (root.winfo_screenheight() - h) // 2
root.geometry(f"{w}x{h}+{x}+{y}")
root.resizable(False, False)

# Base folder selection
base_path_var = tk.StringVar()

tk.Label(root, text="Select Base Folder:").pack(pady=(10, 0))
frame = tk.Frame(root)
frame.pack(padx=10, pady=5, fill="x")

entry = tk.Entry(frame, textvariable=base_path_var, width=50)
entry.pack(side="left", padx=(0, 5), fill="x", expand=True)

tk.Button(frame, text="Browse", command=browse_folder).pack(side="right")

# Folder structure input
tk.Label(root, text="Enter folder structure (one per line):").pack(pady=(10, 0))
folder_structure_text = tk.Text(root, height=10, wrap="word")
folder_structure_text.pack(padx=10, pady=5, fill="both", expand=True)

# Create button
tk.Button(root, text="Create Folders", command=generate_folders, bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=10)

root.mainloop()
