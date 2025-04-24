import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES

def show_help():
    help_text = """
📁 Folder Structure Format Help

- Use indentation (spaces) to define hierarchy.
- End folder names with '/'.
- File names should not end with '/'. 

Example:
project/
    backend/
        src/
        tests/
    frontend/
        public/
        src/
            components/
            App.js
    README.md
"""
    messagebox.showinfo("📘 Help - Folder Structure Format", help_text)

def enable_drag_and_drop(text_widget):
    def on_drop(event):
        file_path = event.data
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                text_widget.delete(1.0, tk.END)
                text_widget.insert(tk.END, file.read())

    text_widget.drop_target_register(DND_FILES)
    text_widget.dnd_bind('<<Drop>>', on_drop)
