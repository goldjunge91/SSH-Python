import csv
import platform
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os

def log_key_details_to_csv(path):
    """Log the generated key details to a CSV file."""
    # Define the CSV filename
    csv_filename = "ssh_keys_database.csv"
    # Check if the CSV file exists to decide on the write mode and header
    file_exists = os.path.exists(csv_filename)
    
    # Fields for the CSV
    fields = ["Operating System", "File Name", "Creation Date", "Copied to Server"]
    record = [platform.system(), os.path.basename(path), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "No"]
    
    # Write to the CSV
    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(fields)
        writer.writerow(record)

def update_bit_lengths(key_type, bit_length_dropdown):
    """Update the available bit lengths based on the selected key type."""
    bit_lengths = {
        "rsa": ["1024", "2048", "3072", "4096"],
        "dsa": ["1024"],
        "ecdsa": [],  # ECDSA doesn't use the -b option
        "ed25519": []  # ED25519 doesn't use the -b option
    }
    bit_length_dropdown["values"] = bit_lengths[key_type]
    if key_type in ["ecdsa", "ed25519"]:
        bit_length_dropdown.set("")
    else:
        bit_length_dropdown.set(bit_lengths[key_type][0])

def generate_ssh_key(options):
    """Generate a new SSH key using ssh-keygen."""
    directory = options["directory"].get()
    filename = options["-f"].get()
    if not directory or not filename:
        messagebox.showerror("Error", "Please specify both the directory and filename for the SSH key.")
        return

    path = os.path.join(directory, filename)

    # Ensure we don't overwrite an existing key
    counter = 1
    original_path = path
    while os.path.exists(path):
        path = f"{original_path}_{counter}"
        counter += 1
    options["-f"].set(path)

    command = ["ssh-keygen"]

    # Add options to the command
    for flag, value in options.items():
        if flag != "directory" and value.get():
            if flag == "-b" and options["-t"].get() not in ["rsa", "dsa"]:
                continue
            command.extend([flag, value.get()])

    try:
        subprocess.run(command, check=True)
        # Log to the CSV
        log_key_details_to_csv(path)
        messagebox.showinfo("Success", f"SSH key generated successfully at {path}!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_generate_key_tab(notebook):
    """Create and return the Generate Key tab."""
    generate_key_frame = ttk.Frame(notebook)

    options = {
        "-t": tk.StringVar(value="rsa"),  # Key type
        "-b": tk.StringVar(value="2048"),  # Bit length
        "directory": tk.StringVar(),  # Directory
        "-f": tk.StringVar(),  # Filename
        "-C": tk.StringVar(),  # Comment
        "-N": tk.StringVar()   # Passphrase
    }

    # Key Type Dropdown
    ttk.Label(generate_key_frame, text="Key Type:").pack(padx=10, pady=5)
    key_types = ["rsa", "dsa", "ecdsa", "ed25519"]
    key_type_dropdown = ttk.Combobox(generate_key_frame, textvariable=options["-t"], values=key_types, state="readonly")
    key_type_dropdown.pack(padx=10, pady=5)
    key_type_dropdown.bind("<<ComboboxSelected>>", lambda e: update_bit_lengths(key_type_dropdown.get(), bit_length_dropdown))

    # Bit Length Dropdown
    ttk.Label(generate_key_frame, text="Bit Length:").pack(padx=10, pady=5)
    bit_length_dropdown = ttk.Combobox(generate_key_frame, textvariable=options["-b"], values=["1024", "2048", "3072", "4096"], state="readonly")
    bit_length_dropdown.pack(padx=10, pady=5)

    # Directory Entry with Browse button
    ttk.Label(generate_key_frame, text="Directory:").pack(padx=10, pady=5)
    directory_entry = ttk.Entry(generate_key_frame, textvariable=options["directory"])
    directory_entry.pack(padx=10, pady=5, side=tk.LEFT)
    ttk.Button(generate_key_frame, text="Browse", command=lambda: select_directory(options["directory"])).pack(padx=10, pady=5, side=tk.LEFT)

    # Filename Entry
    ttk.Label(generate_key_frame, text="Filename:").pack(padx=10, pady=5)
    filename_entry = ttk.Entry(generate_key_frame, textvariable=options["-f"])
    filename_entry.pack(padx=10, pady=5)

    # Comment Entry
    ttk.Label(generate_key_frame, text="Comment:").pack(padx=10, pady=5)
    comment_entry = ttk.Entry(generate_key_frame, textvariable=options["-C"])
    comment_entry.pack(padx=10, pady=5)

    # Passphrase Entry
    ttk.Label(generate_key_frame, text="Passphrase:").pack(padx=10, pady=5)
    passphrase_entry = ttk.Entry(generate_key_frame, textvariable=options["-N"], show="*")
    passphrase_entry.pack(padx=10, pady=5)

    # Generate Key Button
    ttk.Button(generate_key_frame, text="Generate Key", command=lambda: generate_ssh_key(options)).pack(padx=10, pady=20)

    return generate_key_frame

def select_directory(var):
    """Open a directory dialog to select the save directory and update the given variable."""
    directory = filedialog.askdirectory()
    if directory:
        var.set(directory)
