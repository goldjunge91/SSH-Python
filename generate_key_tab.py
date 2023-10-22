import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import csv
import platform
from datetime import datetime

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

##def log_key_details_to_csv(path):
##    """Log the generated key details to a CSV file."""
##    csv_filename = "ssh_keys_database.csv"
##    file_exists = os.path.exists(csv_filename)
##    
##    fields = ["Operating System", "File Name", "Creation Date", "Copied to Server"]
##    record = [platform.system(), os.path.basename(path), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "No"]
##    
##    with open(csv_filename, 'a', newline='') as csvfile:
##        writer = csv.writer(csvfile)
##        if not file_exists:
##            writer.writerow(fields)
##        writer.writerow(record)
def log_key_details_to_csv(path):
    print("Logging to CSV...")
    csv_filename = "ssh_keys_database.csv"
    file_exists = os.path.exists(csv_filename)
    
    fields = ["Operating System", "File Name", "Creation Date", "Copied to Server"]
    record = [platform.system(), os.path.basename(path), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "No"]
    
    print(f"Writing to {csv_filename}...")
    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(fields)
        writer.writerow(record)
    print("Logging done!")


def generate_ssh_key(options):
    print("Starting key generation...")

    directory = options["directory"].get()
    filename = options["-f"].get()
    if not directory or not filename:
        messagebox.showerror("Error", "Please specify both the directory and filename for the SSH key.")
        return

    path = os.path.join(directory, filename)
    counter = 1
    original_path = path
    while os.path.exists(path):
        path = f"{original_path}_{counter}"
        counter += 1
    options["-f"].set(path)

    command = ["ssh-keygen"]

#    for flag, value in options.items():
#        if flag != "directory" and value.get():
#            if flag == "-b" and options["-t"].get() not in ["rsa", "dsa"]:
#                continue
#            command.extend([flag, value.get()])
    for flag, value in options.items():
        if flag != "directory" and value.get():
            if flag == "-b" and options["-t"].get() not in ["rsa", "dsa"]:
                continue
            command.extend([flag, value.get()])
        elif flag == "-N":  # Explicitly set the passphrase as empty if not provided
            command.extend([flag, ""])
        
    print(f"Running command: {command}")
    try:
        subprocess.run(command, check=True)
        print("Key generated, logging details...")
        log_key_details_to_csv(path)
        messagebox.showinfo("Success", f"SSH key generated successfully at {path}!")
    except Exception as e:
        print(f"Error encountered: {e}")
        messagebox.showerror("Error", str(e))

def create_generate_key_tab(notebook):
    generate_key_frame = ttk.Frame(notebook)

    options = {
        "-t": tk.StringVar(value="rsa"),
        "-b": tk.StringVar(value="2048"),
        "directory": tk.StringVar(),
        "-f": tk.StringVar(),
        "-C": tk.StringVar(),
        "-N": tk.StringVar()
    }

    ttk.Label(generate_key_frame, text="Key Type:").pack(padx=10, pady=5)
    key_types = ["rsa", "dsa", "ecdsa", "ed25519"]
    key_type_dropdown = ttk.Combobox(generate_key_frame, textvariable=options["-t"], values=key_types, state="readonly")
    key_type_dropdown.pack(padx=10, pady=5)
    key_type_dropdown.bind("<<ComboboxSelected>>", lambda e: update_bit_lengths(key_type_dropdown.get(), bit_length_dropdown))

    ttk.Label(generate_key_frame, text="Bit Length:").pack(padx=10, pady=5)
    bit_length_dropdown = ttk.Combobox(generate_key_frame, textvariable=options["-b"], values=["1024", "2048", "3072", "4096"], state="readonly")
    bit_length_dropdown.pack(padx=10, pady=5)

    ttk.Label(generate_key_frame, text="Directory:").pack(padx=10, pady=5)
    directory_entry = ttk.Entry(generate_key_frame, textvariable=options["directory"])
    directory_entry.pack(padx=10, pady=5, side=tk.LEFT)
    ttk.Button(generate_key_frame, text="Browse", command=lambda: select_directory(options["directory"])).pack(padx=10, pady=5, side=tk.LEFT)

    ttk.Label(generate_key_frame, text="Filename:").pack(padx=10, pady=5)
    filename_entry = ttk.Entry(generate_key_frame, textvariable=options["-f"])
    filename_entry.pack(padx=10, pady=5)

    ttk.Label(generate_key_frame, text="Comment:").pack(padx=10, pady=5)
    comment_entry = ttk.Entry(generate_key_frame, textvariable=options["-C"])
    comment_entry.pack(padx=10, pady=5)

    ttk.Label(generate_key_frame, text="Passphrase:").pack(padx=10, pady=5)
    passphrase_entry = ttk.Entry(generate_key_frame, textvariable=options["-N"], show="*")
    passphrase_entry.pack(padx=10, pady=5)

    ttk.Button(generate_key_frame, text="Generate Key", command=lambda: generate_ssh_key(options)).pack(padx=10, pady=20)

    return generate_key_frame

def select_directory(var):
    directory = filedialog.askdirectory()
    if directory:
        var.set(directory)