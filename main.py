import tkinter as tk
from tkinter import ttk
from ssh_key_path_tab import create_ssh_key_path_tab
from generate_key_tab import create_generate_key_tab
from copy_to_server_tab import create_copy_to_server_tab
from show_config_tab import create_show_config_tab, select_config_path
from setup_new_server_tab import create_setup_new_server_tab


def create_gui():
    root = tk.Tk()
    root.title("SSH Tool")

    # Create a notebook (for tabs)
    notebook = ttk.Notebook(root)
    notebook.pack(padx=10, pady=10, expand=True, fill="both")

    # SSH Key Path Tab
    ssh_key_path_frame, ssh_key_entry = create_ssh_key_path_tab(notebook)
    notebook.add(ssh_key_path_frame, text="SSH Key Path")

    # Generate Key Tab
    generate_key_frame = create_generate_key_tab(notebook)
    notebook.add(generate_key_frame, text="Generate Key")

    # ... [Add other tabs here using a similar pattern]
    
    # Copy to Server Tab
    copy_key_frame = create_copy_to_server_tab(notebook, ssh_key_entry)
    notebook.add(copy_key_frame, text="Copy to Server")
    
    # Show Config Tab
    show_config_frame, config_path_entry = create_show_config_tab(notebook)
    notebook.add(show_config_frame, text="Show Config")
    
    # Setup New Server Tab
    setup_server_frame = create_setup_new_server_tab(notebook, ssh_key_entry, config_path_entry)
    notebook.add(setup_server_frame, text="Setup New Server")
    
    

    root.mainloop()

if __name__ == "__main__":
    create_gui()
