import tkinter as tk
from tkinter import ttk, filedialog

def select_ssh_key_path(entry):
    """Allow the user to select the SSH key path using a file dialog."""
    filepath = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filepath)

def create_ssh_key_path_tab(notebook):
    """Create and return the SSH Key Path tab."""
    ssh_key_path_frame = ttk.Frame(notebook)

    ssh_key_path = tk.StringVar()
    ttk.Label(ssh_key_path_frame, text="SSH Key Path:").pack(padx=10, pady=5)
    ssh_key_entry = ttk.Entry(ssh_key_path_frame, textvariable=ssh_key_path)
    ssh_key_entry.pack(padx=10, pady=5, side=tk.LEFT)
    ttk.Button(ssh_key_path_frame, text="Browse", command=lambda: select_ssh_key_path(ssh_key_entry)).pack(padx=10, pady=5, side=tk.LEFT)

    return ssh_key_path_frame, ssh_key_entry  # Return the frame and the entry for use in other tabs
