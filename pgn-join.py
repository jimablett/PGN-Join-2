import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess

class PGNLoaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PGN-Join")
        self.root.geometry("300x250")
        self.root.configure(bg="#424242")
        
        self.keep_original_pgns = tk.BooleanVar()
        self.keep_original_checkbox = tk.Checkbutton(root, text="Keep original PGNs", variable=self.keep_original_pgns, bg="darkgrey", fg="white", selectcolor="darkgrey")
        self.keep_original_checkbox.pack(pady=5)

        self.cleanup_output_folder()

        self.load_button = tk.Button(root, text="Load PGNs", command=self.load_pgns, bg="#4CAF50", fg="white")
        self.load_button.pack(pady=10)

        self.join_button = tk.Button(root, text="Join PGNs", command=self.join_pgns, bg="#2196F3", fg="white")
        self.join_button.pack(pady=10)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=250, mode="determinate")
        self.progress.pack(pady=10)

        self.progress_label = tk.Label(root, text="", bg="#424242", fg="white")
        self.progress_label.pack(pady=5)

        self.percentage_loaded_label = tk.Label(root, text="Percentage Loaded: 0%", bg="#424242", fg="white")
        self.percentage_loaded_label.pack(pady=5)

        self.percentage_joined_label = tk.Label(root, text="Percentage Joined: 0%", bg="#424242", fg="white")
        self.percentage_joined_label.pack(pady=5)

    def cleanup_output_folder(self):
        output_folder = "OUTPUT"
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        os.makedirs(output_folder)

    def load_pgns(self):
        self.reset_progress_indicators()
        file_paths = filedialog.askopenfilenames(title="Select PGN files", filetypes=[("PGN files", "*.pgn"), ("PGN files", "*.PGN")])
        total_files = len(file_paths)
        for index, file_path in enumerate(file_paths):
            if os.path.isfile(file_path):
                shutil.copy(file_path, os.path.join(os.getcwd(), os.path.basename(file_path)))
            percentage_loaded = (index + 1) / total_files * 100
            self.percentage_loaded_label.config(text=f"Percentage Loaded: {int(percentage_loaded)}%")
            self.root.update_idletasks()
        messagebox.showinfo("Info", "PGNs loaded")
        self.convert_pgns_to_lowercase()

    def reset_progress_indicators(self):
        self.percentage_loaded_label.config(text="Percentage Loaded: 0%")
        self.percentage_joined_label.config(text="Percentage Joined: 0%")
        self.progress['value'] = 0
        self.progress_label.config(text="Merging... 0%")

    def convert_pgns_to_lowercase(self):
        pgn_files = [f for f in os.listdir() if f.lower().endswith('.pgn')]
        for pgn_file in pgn_files:
            new_name = pgn_file.lower()
            os.rename(pgn_file, new_name)

    def join_pgns(self):
        pgn_files = [f for f in os.listdir() if f.lower().endswith('.pgn')]
        output_file = os.path.join("OUTPUT", "output-merged.pgn")

        self.progress['maximum'] = len(pgn_files)
        self.progress['value'] = 0
        self.progress_label.config(text="Merging... 0%")
        self.percentage_joined_label.config(text="Percentage Joined: 0%")

        with open(output_file, 'w', encoding='utf-8') as outfile:
            for index, pgn_file in enumerate(pgn_files):
                with open(pgn_file, 'r', encoding='utf-8', errors='ignore') as infile:
                    # Add a newline before the content of each file
                    outfile.write('\n' + infile.read() + '\n')
                self.progress['value'] += 1
                percentage_joined = (index + 1) / len(pgn_files) * 100
                self.progress_label.config(text=f"Merging... {int(percentage_joined)}%")
                self.percentage_joined_label.config(text=f"Percentage Joined: {int(percentage_joined)}%")
                self.root.update_idletasks()

        messagebox.showinfo("Info", "PGNs joined successfully")
        subprocess.Popen(f'explorer "{os.path.abspath("OUTPUT")}"')

        if not self.keep_original_pgns.get():
            for pgn_file in pgn_files:
                os.remove(pgn_file)
        else:
            backup_folder = "BACKUPS"
            if not os.path.exists(backup_folder):
                os.makedirs(backup_folder)
            for pgn_file in pgn_files:
                shutil.move(pgn_file, os.path.join(backup_folder, pgn_file))

        self.rename_output_file()

        self.percentage_loaded_label.config(text="Percentage Loaded: 0%")
        self.percentage_joined_label.config(text="Done")

    def rename_output_file(self):
        output_folder = "OUTPUT"
        existing_files = os.listdir(output_folder)
        base_name = "output-merged.pgn"
        count = 1
        new_file_name = f"{count}-{base_name}"
        while new_file_name in existing_files:
            count += 1
            new_file_name = f"{count}-{base_name}"
        os.rename(os.path.join(output_folder, base_name), os.path.join(output_folder, new_file_name))

    def cleanup_files(self):
        for filename in os.listdir():
            if filename not in ['readme.rtf', 'OUTPUT'] and not (filename.endswith('.py') or filename.endswith('.exe')):
                os.remove(filename)

if __name__ == "__main__":
    root = tk.Tk()
    app = PGNLoaderApp(root)
    root.mainloop()
