import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, END

class UselessFileCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("Useless File Cleaner")
        self.folder_path = tk.StringVar()
        self.setup_ui()

    def setup_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(top_frame, text="Useless File Cleaner", font=("Arial", 16, "bold"), anchor="w").pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(top_frame, text="🧹", font=("Arial", 16)).pack(side=tk.LEFT, padx=5)
        tk.Label(self.root, text="Valitse kansio:").pack()
        tk.Entry(self.root, textvariable=self.folder_path, width=50).pack(side=tk.LEFT)
        tk.Button(self.root, text="Selaa", command=self.browse_folder).pack(side=tk.LEFT)
        tk.Button(self.root, text="Listaa tiedostot", command=self.list_files).pack(side=tk.LEFT)
        self.listbox = Listbox(self.root, selectmode=tk.MULTIPLE, width=80)
        self.listbox.pack()
        tk.Button(self.root, text="Poista valitut", command=self.delete_selected).pack()
        tk.Button(self.root, text="Siirrä valitut kansioon", command=self.move_selected).pack()
        self.target_folder = tk.StringVar()
        tk.Entry(self.root, textvariable=self.target_folder, width=50).pack()
        tk.Button(self.root, text="Luo uusi kansio", command=self.create_folder).pack()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def list_files(self):
        self.listbox.delete(0, END)
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror("Virhe", "Valitse kansio ensin.")
            return
        for f in os.listdir(folder):
            self.listbox.insert(END, f)

    def delete_selected(self):
        folder = self.folder_path.get()
        selected = [self.listbox.get(i) for i in self.listbox.curselection()]
        for f in selected:
            path = os.path.join(folder, f)
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
            except Exception as e:
                messagebox.showerror("Virhe", f"Ei voitu poistaa: {f}\n{e}")
        self.list_files()

    def move_selected(self):
        folder = self.folder_path.get()
        target = self.target_folder.get()
        if not target:
            messagebox.showerror("Virhe", "Anna kohdekansion nimi.")
            return
        target_path = os.path.join(folder, target)
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        selected = [self.listbox.get(i) for i in self.listbox.curselection()]
        for f in selected:
            src = os.path.join(folder, f)
            dst = os.path.join(target_path, f)
            try:
                shutil.move(src, dst)
            except Exception as e:
                messagebox.showerror("Virhe", f"Ei voitu siirtää: {f}\n{e}")
        self.list_files()

    def create_folder(self):
        folder = self.folder_path.get()
        target = self.target_folder.get()
        if not target:
            messagebox.showerror("Virhe", "Anna uuden kansion nimi.")
            return
        target_path = os.path.join(folder, target)
        try:
            os.makedirs(target_path, exist_ok=True)
            messagebox.showinfo("Kansio luotu", f"Kansio {target} luotu.")
        except Exception as e:
            messagebox.showerror("Virhe", f"Ei voitu luoda kansiota: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = UselessFileCleaner(root)
    root.mainloop()
