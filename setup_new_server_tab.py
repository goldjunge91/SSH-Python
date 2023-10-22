import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

def add_server_to_config(hostname, port, username, ssh_key_path, config_path):
    """Add a new server entry to the SSH config."""
    try:
        config_entry = f"""
Host {hostname}
    HostName {hostname}
    Port {port}
    User {username}
    IdentityFile {ssh_key_path}
"""
        with open(config_path, "a") as file:
            file.write(config_entry)

        messagebox.showinfo("Success", "Server added to SSH config successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_setup_new_server_tab(notebook, ssh_key_path_entry, config_path_entry):
    """Create and return the Setup New Server tab."""
    setup_server_frame = ttk.Frame(notebook)

    # Hostname
    ttk.Label(setup_server_frame, text="Hostname:").pack(padx=10, pady=5)
    hostname_entry = ttk.Entry(setup_server_frame)
    hostname_entry.pack(padx=10, pady=5)

    # Port
    ttk.Label(setup_server_frame, text="Port:").pack(padx=10, pady=5)
    port_entry = ttk.Entry(setup_server_frame)
    port_entry.pack(padx=10, pady=5)

    # Username
    ttk.Label(setup_server_frame, text="Username:").pack(padx=10, pady=5)
    username_entry = ttk.Entry(setup_server_frame)
    username_entry.pack(padx=10, pady=5)

    # Add Server Button
    add_server_btn = ttk.Button(setup_server_frame, text="Add Server", command=lambda: add_server_to_config(
        hostname_entry.get(),
        port_entry.get(),
        username_entry.get(),
        ssh_key_path_entry.get(),
        config_path_entry.get()
    ))
    add_server_btn.pack(padx=10, pady=20)

    return setup_server_frame
