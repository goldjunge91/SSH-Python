import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

def copy_key_to_server(hostname, port, username, ssh_key_path):
    """Copy the SSH key to the server using ssh-copy-id."""
    try:
        command = ["ssh-copy-id", f"{username}@{hostname}"]
        if port:
            command.extend(["-p", port])
        if ssh_key_path:
            command.append(f"-i {ssh_key_path}")
        
        subprocess.run(command, check=True)
        messagebox.showinfo("Success", "SSH key copied successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_copy_to_server_tab(notebook, ssh_key_path_entry):
    """Create and return the Copy to Server tab."""
    copy_key_frame = ttk.Frame(notebook)

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

    # Button to copy key
    copy_btn = ttk.Button(copy_key_frame, text="Copy Key", command=lambda: copy_key_to_server(
        hostname_entry.get(),
        port_entry.get(),
        username_entry.get(),
        ssh_key_path_entry.get()
    ))
    copy_btn.pack(padx=10, pady=20)

    return copy_key_frame
