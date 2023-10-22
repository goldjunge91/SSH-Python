import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def load_ssh_config(config_path, text_area):
    """Load and display the SSH config content."""
    try:
        with open(config_path, "r") as file:
            content = file.read()
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, content)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_show_config_tab(notebook):
    """Create and return the Show Config tab."""
    show_config_frame = ttk.Frame(notebook)

    # Config Path
    config_path = tk.StringVar()
    ttk.Label(show_config_frame, text="Config Path:").pack(padx=10, pady=5)
    config_path_entry = ttk.Entry(show_config_frame, textvariable=config_path)
    config_path_entry.pack(padx=10, pady=5, side=tk.LEFT)
    ttk.Button(show_config_frame, text="Browse", command=lambda: select_config_path(config_path_entry)).pack(padx=10, pady=5, side=tk.LEFT)

    # Text Area
    text_area = tk.Text(show_config_frame, height=10, width=50)
    text_area.pack(padx=10, pady=5)

    # Load Config Button
    ttk.Button(show_config_frame, text="Load Config", command=lambda: load_ssh_config(config_path.get(), text_area)).pack(padx=10, pady=5)

    return show_config_frame, config_path_entry  # Return both the frame and the entry

def select_config_path(entry):
    """Allow the user to select the SSH config path using a file dialog."""
    filepath = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filepath)
