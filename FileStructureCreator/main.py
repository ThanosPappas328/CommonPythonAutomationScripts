import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES

from logic.parser import parse_advanced_mode
from logic.exporter import export_all
from ui.components import show_help, enable_drag_and_drop

# --- GUI SETUP ---
root = TkinterDnD.Tk()  # Use this to initialize the Tkinter window
root.title("📁 Folder Structure Generator")

# Window size and center
w, h = 600, 550
x = (root.winfo_screenwidth() - w) // 2
y = (root.winfo_screenheight() - h) // 2
root.geometry(f"{w}x{h}+{x}+{y}")
root.resizable(False, False)

base_path_var = tk.StringVar()

# --- UI Elements ---
tk.Label(root, text="Select Base Folder:").pack(pady=(10, 0))
frame = tk.Frame(root)
frame.pack(padx=10, pady=5, fill="x")

entry = tk.Entry(frame, textvariable=base_path_var, width=50)
entry.pack(side="left", padx=(0, 5), fill="x", expand=True)
tk.Button(frame, text="Browse", command=lambda: base_path_var.set(filedialog.askdirectory())).pack(side="right")

# Folder structure input
tk.Label(root, text="Enter folder structure:").pack(pady=(5, 0))
folder_structure_text = tk.Text(root, height=18, wrap="word")
folder_structure_text.insert("1.0", "project/\n    src/\n    tests/\nREADME.md")
folder_structure_text.pack(padx=10, pady=5, fill="both", expand=True)

# Drag-and-drop support
enable_drag_and_drop(folder_structure_text)

# Action buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Create Folders", command=lambda: generate_folders(), bg="#4CAF50", fg="white", padx=10, pady=5).pack(side="left", padx=5)
tk.Button(btn_frame, text="Help", command=show_help, padx=10, pady=5).pack(side="right", padx=5)


# --- Folder Creation Handler ---
def generate_folders():
    base_path = base_path_var.get()
    structure_text = folder_structure_text.get("1.0", tk.END)

    if not base_path or not os.path.isdir(base_path):
        messagebox.showerror("Error", "Please select a valid base folder.")
        return

    if not structure_text.strip():
        messagebox.showerror("Error", "Please enter folder structure.")
        return

    try:
        # Use the advanced mode for folder creation
        created = parse_advanced_mode(base_path, structure_text)

        # Export the folder structure
        export_path = export_all(base_path, structure_text)
        messagebox.showinfo("Success", f"✅ Created {len(created)} folders.\n📁 Plan saved in: {export_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

root.mainloop()
