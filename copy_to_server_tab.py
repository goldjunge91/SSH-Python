import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess

def copy_key_to_server(hostname, port, username, ssh_key_path):
    """Copy the SSH key to the server using ssh-copy-id."""
    # ... [rest of the function remains unchanged]

def create_copy_to_server_tab(notebook, ssh_key_entry):
    """Create and return the modified Copy to Server tab."""
    copy_key_frame = ttk.Frame(notebook)

    # Server Name
    ttk.Label(copy_key_frame, text="Server Name:").pack(padx=10, pady=5)
    server_name_entry = ttk.Entry(copy_key_frame)
    server_name_entry.pack(padx=10, pady=5)

    # Hostname
    ttk.Label(copy_key_frame, text="Hostname:").pack(padx=10, pady=5)
    hostname_entry = ttk.Entry(copy_key_frame)
    hostname_entry.pack(padx=10, pady=5)

    # Port
    ttk.Label(copy_key_frame, text="Port:").pack(padx=10, pady=5)
    port_entry = ttk.Entry(copy_key_frame)
    port_entry.pack(padx=10, pady=5)

    # Username
    ttk.Label(copy_key_frame, text="Username:").pack(padx=10, pady=5)
    username_entry = ttk.Entry(copy_key_frame)
    username_entry.pack(padx=10, pady=5)

    # SSH Key Path with Browse Button
    ttk.Label(copy_key_frame, text="SSH Key Path:").pack(padx=10, pady=5)
    ssh_key_path_entry = ttk.Entry(copy_key_frame)
    ssh_key_path_entry.pack(padx=10, pady=5, fill=tk.X, expand=True)

    def browse_file():
        """Open file dialog to select the SSH key."""
        file_path = filedialog.askopenfilename()
        if file_path:
            ssh_key_path_entry.delete(0, tk.END)
            ssh_key_path_entry.insert(0, file_path)

    browse_btn = ttk.Button(copy_key_frame, text="Browse File", command=browse_file)
    browse_btn.pack(padx=10, pady=5)

    # Button to copy key
    copy_btn = ttk.Button(copy_key_frame, text="Copy Key", command=lambda: copy_key_to_server(
        hostname_entry.get(),
        port_entry.get(),
        username_entry.get(),
        ssh_key_path_entry.get()
    ))
    copy_btn.pack(padx=10, pady=20)

    return copy_key_frame