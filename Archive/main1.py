import tkinter as tk
from tkinter import ttk, filedialog

def create_gui():
    root = tk.Tk()
    root.title("SSH Tool")

    # Create a notebook (for tabs)
    notebook = ttk.Notebook(root)
    notebook.pack(padx=10, pady=10, expand=True, fill="both")

    # SSH Key Path Tab
    ssh_key_path_frame = ttk.Frame(notebook)
    notebook.add(ssh_key_path_frame, text="SSH Key Path")

    ssh_key_path = tk.StringVar()
    ttk.Label(ssh_key_path_frame, text="SSH Key Path:").pack(padx=10, pady=5)
    ttk.Entry(ssh_key_path_frame, textvariable=ssh_key_path).pack(padx=10, pady=5)

    # Generate Key Tab
    generate_key_frame = ttk.Frame(notebook)
    notebook.add(generate_key_frame, text="Generate Key")

    ttk.Button(generate_key_frame, text="Generate Key").pack(padx=10, pady=20)

    # Copy to Server Tab
    copy_key_frame = ttk.Frame(notebook)
    notebook.add(copy_key_frame, text="Copy to Server")

    ttk.Label(copy_key_frame, text="Hostname:").pack(padx=10, pady=5)
    ttk.Entry(copy_key_frame).pack(padx=10, pady=5)
    ttk.Label(copy_key_frame, text="Port:").pack(padx=10, pady=5)
    ttk.Entry(copy_key_frame).pack(padx=10, pady=5)
    ttk.Label(copy_key_frame, text="Username:").pack(padx=10, pady=5)
    ttk.Entry(copy_key_frame).pack(padx=10, pady=5)
    ttk.Button(copy_key_frame, text="Copy Key").pack(padx=10, pady=20)

    # Show Config Tab
    show_config_frame = ttk.Frame(notebook)
    notebook.add(show_config_frame, text="Show Config")

    config_path = tk.StringVar()
    ttk.Label(show_config_frame, text="Config Path:").pack(padx=10, pady=5)
    ttk.Entry(show_config_frame, textvariable=config_path).pack(padx=10, pady=5)
    ttk.Button(show_config_frame, text="Load Config").pack(padx=10, pady=5)
    text_area = tk.Text(show_config_frame, height=10, width=50)
    text_area.pack(padx=10, pady=5)

    # Setup New Server Tab
    setup_server_frame = ttk.Frame(notebook)
    notebook.add(setup_server_frame, text="Setup New Server")

    ttk.Label(setup_server_frame, text="Hostname:").pack(padx=10, pady=5)
    ttk.Entry(setup_server_frame).pack(padx=10, pady=5)
    ttk.Label(setup_server_frame, text="Port:").pack(padx=10, pady=5)
    ttk.Entry(setup_server_frame).pack(padx=10, pady=5)
    ttk.Label(setup_server_frame, text="Username:").pack(padx=10, pady=5)
    ttk.Entry(setup_server_frame).pack(padx=10, pady=5)
    ttk.Button(setup_server_frame, text="Choose SSH Key").pack(padx=10, pady=5)
    ttk.Button(setup_server_frame, text="Add Server").pack(padx=10, pady=20)

    root.mainloop()

create_gui()
