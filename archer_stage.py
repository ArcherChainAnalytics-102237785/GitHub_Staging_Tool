import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import tempfile
import shutil

class ArcherStagingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Archer Chain Analytics - GitHub Staging Tool")
        self.root.geometry("700x750")
        
        self.items = []  # Stores dicts of {'name': str, 'content': str}
        self.idx = 0
        self.temp_dir = None

        # --- UI LAYOUT ---
        tk.Label(root, text="1. SELECT PROJECT", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Button(root, text="Open Folder or ZIP", command=self.load_project, bg="#2ea44f", fg="white", height=2).pack()
        
        self.status = tk.Label(root, text="Waiting for input...", fg="gray")
        self.status.pack(pady=5)

        tk.Frame(root, height=2, bd=1, relief="sunken").pack(fill="x", padx=20, pady=10)

        # Navigation
        self.nav_frame = tk.Frame(root)
        self.nav_frame.pack()
        self.prev_btn = tk.Button(self.nav_frame, text="<< Back", command=self.prev, state="disabled")
        self.prev_btn.grid(row=0, column=0, padx=10)
        self.counter = tk.Label(self.nav_frame, text="Step 0 of 0", font=("Arial", 10))
        self.counter.grid(row=0, column=1)
        self.next_btn = tk.Button(self.nav_frame, text="Next >>", command=self.next, state="disabled")
        self.next_btn.grid(row=0, column=2, padx=10)

        # Data Display
        tk.Label(root, text="TARGET FIELD / FILENAME:", font=("Arial", 9, "bold")).pack(pady=(20, 0))
        self.name_box = tk.Entry(root, width=60, font=("Courier", 10))
        self.name_box.pack()
        tk.Button(root, text="COPY FIELD NAME", command=lambda: self.copy(self.name_box.get())).pack(pady=5)

        tk.Label(root, text="CONTENT TO PASTE:", font=("Arial", 9, "bold")).pack(pady=(15, 0))
        self.content_box = scrolledtext.ScrolledText(root, width=75, height=18, font=("Courier", 9))
        self.content_box.pack()
        tk.Button(root, text="COPY CONTENT", command=lambda: self.copy(self.content_box.get("1.0", tk.END).strip()), bg="#0366d6", fg="white").pack(pady=5)

        tk.Label(root, text="❗ WARNING: ENSURE GITHUB REPO IS SET TO 'PRIVATE'", fg="red", font=("Arial", 9, "bold")).pack(side="bottom", pady=10)

    def copy(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update() # Keeps clipboard alive after app close

    def load_project(self):
        path = filedialog.askdirectory(title="Select Project Folder") or filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
        if not path: return

        self.items = []
        name = os.path.basename(path).replace(".zip", "").lower().replace(" ", "-")

        # --- GENERATE STAGING SEQUENCE ---
        # 1. Metadata
        self.items.append({'name': 'Repository Name', 'content': name})
        self.items.append({'name': 'Description Box', 'content': "⚠️ PRIVATE AND PROPRIETARY. Copyright © 2026 Archer Chain Analytics. All rights reserved."})
        
        # 2. Mandatory Legal Files
        self.items.append({'name': 'LICENSE', 'content': "PROPRIETARY AND CONFIDENTIAL\n\nCopyright (c) 2026 Archer Chain Analytics. All rights reserved.\nUnauthorized use is strictly forbidden."})
        self.items.append({'name': 'README.md', 'content': f"# {name.upper()}\n\n> **NOTICE: PRIVATE PROPERTY OF ARCHER CHAIN ANALYTICS**"})

        # 3. Project Content Analysis
        if path.endswith(".zip"):
            self.temp_dir = tempfile.mkdtemp()
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
            self.walk_dir(self.temp_dir)
        else:
            self.walk_dir(path)

        self.idx = 0
        self.status.config(text=f"Project: {name}", fg="black")
        self.next_btn.config(state="normal")
        self.prev_btn.config(state="normal")
        self.refresh()

    def walk_dir(self, directory):
        for root_dir, _, files in os.walk(directory):
            for file in files:
                if any(x in file.lower() for x in ['.ds_store', '.git', '.pyc']): continue
                full_path = os.path.join(root_dir, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        self.items.append({'name': file, 'content': f.read()})
                except:
                    self.items.append({'name': file, 'content': '[BINARY FILE - MANUALLY UPLOAD]'})

    def refresh(self):
        item = self.items[self.idx]
        self.counter.config(text=f"Step {self.idx + 1} of {len(self.items)}")
        self.name_box.delete(0, tk.END)
        self.name_box.insert(0, item['name'])
        self.content_box.delete("1.0", tk.END)
        self.content_box.insert("1.0", item['content'])

    def next(self):
        if self.idx < len(self.items) - 1:
            self.idx += 1
            self.refresh()

    def prev(self):
        if self.idx > 0:
            self.idx -= 1
            self.refresh()

if __name__ == "__main__":
    root = tk.Tk()
    app = ArcherStagingApp(root)
    root.mainloop()
