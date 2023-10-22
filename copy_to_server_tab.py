import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import platform

def check_host_connectivity(hostname):
    """Check if the host is reachable using ping."""
    command = f'ping -n 1 {hostname}'
    try:
        subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def copy_key_to_server(hostname, port, username, ssh_key_path, output_label, method="ssh-copy-id"):
    """Copy the SSH key to the server."""
    # Check connectivity first
    if not check_host_connectivity(hostname):
        output_label.config(text=f"Error: Unable to connect to {hostname}.", foreground="red")
        return

    # Determine the command based on the selected method
    if method == "ssh-copy-id":
        command = f'ssh-copy-id -i {ssh_key_path} {username}@{hostname} -p {port}'
    else:
        command = f'cat {ssh_key_path}.pub | ssh {username}@{hostname} -p {port} "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"'

    # Determine the platform and run the command in a new terminal window
    os_type = platform.system()
    if os_type == "Windows":
        subprocess.Popen(['cmd.exe', '/k', command])
    elif os_type == "Linux":
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command])
    elif os_type == "Darwin":  # macOS
        subprocess.Popen(['osascript', '-e', f'tell app "Terminal" to do script "{command}"'])

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

    # Output Line
    output_label = ttk.Label(copy_key_frame, text="")
    output_label.pack(padx=10, pady=10, fill=tk.X)

    # Button to copy key
    copy_btn = ttk.Button(copy_key_frame, text="Copy Key", command=lambda: copy_key_to_server(
        hostname_entry.get(),
        port_entry.get(),
        username_entry.get(),
        ssh_key_path_entry.get(),
        output_label
    ))
    copy_btn.pack(padx=10, pady=20)

    return copy_key_frame
