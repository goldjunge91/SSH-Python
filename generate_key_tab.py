import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os

def generate_ssh_key(options):
    """Generate a new SSH key using ssh-keygen."""
    path = options["-f"].get()
    if not path:
        messagebox.showerror("Error", "Please specify a path for the SSH key.")
        return

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
        if value.get():
            if flag == "-b" and options["-t"].get() not in ["rsa", "dsa", "ecdsa"]:
                continue
            command.extend([flag, value.get()])

    try:
        subprocess.run(command, check=True)
        messagebox.showinfo("Success", f"SSH key generated successfully at {path}!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Rest of the code remains the same...

def create_generate_key_tab(notebook):
    """Create and return the Generate Key tab."""
    generate_key_frame = ttk.Frame(notebook)

    options = {
        "-t": tk.StringVar(value="rsa"),  # Key type
        "-b": tk.StringVar(value="2048"),  # Bit length
        "-f": tk.StringVar(),  # File path
        "-C": tk.StringVar(),  # Comment
        "-N": tk.StringVar()   # Passphrase
    }

    # Key Type Dropdown
    ttk.Label(generate_key_frame, text="Key Type:").pack(padx=10, pady=5)
    key_types = ["rsa", "dsa", "ecdsa", "ed25519"]
    key_type_dropdown = ttk.Combobox(generate_key_frame, textvariable=options["-t"], values=key_types, state="readonly")
    key_type_dropdown.pack(padx=10, pady=5)

    # Bit Length Dropdown
    ttk.Label(generate_key_frame, text="Bit Length:").pack(padx=10, pady=5)
    bit_lengths = ["1024", "2048", "3072", "4096"]
    bit_length_dropdown = ttk.Combobox(generate_key_frame, textvariable=options["-b"], values=bit_lengths, state="readonly")
    bit_length_dropdown.pack(padx=10, pady=5)

    # File Path Entry with Browse button
    ttk.Label(generate_key_frame, text="File Path:").pack(padx=10, pady=5)
    file_path_entry = ttk.Entry(generate_key_frame, textvariable=options["-f"])
    file_path_entry.pack(padx=10, pady=5, side=tk.LEFT)
    ttk.Button(generate_key_frame, text="Browse", command=lambda: select_save_path(options["-f"])).pack(padx=10, pady=5, side=tk.LEFT)

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

def select_save_path(var):
    """Open a file dialog to select the save path and update the given variable."""
    filepath = filedialog.asksaveasfilename(defaultextension=".key", filetypes=[("Key Files", "*.key"), ("All Files", "*.*")])
    if filepath:
        var.set(filepath)
