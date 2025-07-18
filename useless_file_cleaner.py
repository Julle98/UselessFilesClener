import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, END

class UselessFileCleaner:
    def __init__(self, root):
        self.root = root
        self.languages = {
    "fi": {
        "app_name": "Useless File Cleaner",
        "select_folder": "Valitse kansio:",
        "browse": "Selaa",
        "list_files": "Listaa tiedostot",
        "delete_selected": "Poista valitut",
        "move_selected": "Siirrä valitut kansioon",
        "new_folder": "Luo uusi kansio",
        "error_select_folder": "Valitse kansio ensin.",
        "error": "Virhe",
        "error_delete": "Ei voitu poistaa:",
        "error_move": "Ei voitu siirtää:",
        "error_new_folder": "Ei voitu luoda kansiota:",
        "info_folder_created": "Kansio luotu",
        "info_folder_created_msg": "Kansio {target} luotu.",
        "error_no_target": "Anna kohdekansion nimi.",
        "error_no_new_folder": "Anna uuden kansion nimi."
    },
    "en": {
        "app_name": "Useless File Cleaner",
        "select_folder": "Select folder:",
        "browse": "Browse",
        "list_files": "List files",
        "delete_selected": "Delete selected",
        "move_selected": "Move selected to folder",
        "new_folder": "Create new folder",
        "error_select_folder": "Please select a folder first.",
        "error": "Error",
        "error_delete": "Could not delete:",
        "error_move": "Could not move:",
        "error_new_folder": "Could not create folder:",
        "info_folder_created": "Folder created",
        "info_folder_created_msg": "Folder {target} created.",
        "error_no_target": "Enter target folder name.",
        "error_no_new_folder": "Enter new folder name."
    }
}
        self.current_lang = "en"
        self.root.title("Useless File Cleaner")
        self.folder_path = tk.StringVar()
        self.setup_ui()

    def setup_ui(self):
        menubar = tk.Menu(self.root)
        lang_menu = tk.Menu(menubar, tearoff=0)
        lang_menu.add_command(label="Suomi", command=lambda: self.set_language("fi"))
        lang_menu.add_command(label="English", command=lambda: self.set_language("en"))
        menubar.add_cascade(label="Kieli / Language", menu=lang_menu)
        self.root.config(menu=menubar)
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(top_frame, text=self.languages[self.current_lang]["app_name"], font=("Arial", 16, "bold"), anchor="w").pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(top_frame, text="🧹", font=("Arial", 16)).pack(side=tk.LEFT, padx=5)
        author_frame = tk.Frame(self.root)
        author_frame.pack(side=tk.TOP, fill=tk.X)
        author_label = tk.Label(author_frame, text="Tehnyt Julle98 | Made by Julle98", fg="blue", cursor="hand2", font=("Arial", 10, "italic"))
        author_label.pack(side=tk.LEFT, padx=10)
        author_label.bind("<Button-1>", lambda e: self.open_github())
        instructions = {
            "fi": "Käyttöohje: Valitse kansio, listaa tiedostot, valitse tiedostot ja poista/siirrä. Voit luoda uuden kansion tärkeille tiedostoille.",
            "en": "Instructions: Select a folder, list files, select files and delete/move. You can create a new folder for important files."
        }
        tk.Label(self.root, text=instructions[self.current_lang], font=("Arial", 10)).pack(pady=(0,10))
        tk.Label(self.root, text=self.languages[self.current_lang]["select_folder"]).pack()
        tk.Entry(self.root, textvariable=self.folder_path, width=50).pack(side=tk.LEFT)
        tk.Button(self.root, text=self.languages[self.current_lang]["browse"], command=self.browse_folder).pack(side=tk.LEFT)
        tk.Button(self.root, text=self.languages[self.current_lang]["list_files"], command=self.list_files).pack(side=tk.LEFT)
        self.listbox = Listbox(self.root, selectmode=tk.MULTIPLE, width=80)
        self.listbox.pack()
        tk.Button(self.root, text=self.languages[self.current_lang]["delete_selected"], command=self.delete_selected).pack()
        tk.Button(self.root, text=self.languages[self.current_lang]["move_selected"], command=self.move_selected).pack()
        self.target_folder = tk.StringVar()
        tk.Entry(self.root, textvariable=self.target_folder, width=50).pack()
        tk.Button(self.root, text=self.languages[self.current_lang]["new_folder"], command=self.create_folder).pack()

    def set_language(self, lang):
        self.current_lang = lang
        self.refresh_ui()
    
    def open_github(self):
        import webbrowser
        webbrowser.open_new("https://github.com/Julle98")

    def refresh_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_ui()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def list_files(self):
        self.listbox.delete(0, END)
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror(self.languages[self.current_lang]["error"], self.languages[self.current_lang]["error_select_folder"])
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
                messagebox.showerror(self.languages[self.current_lang]["error"], self.languages[self.current_lang]["error_select_folder"])
        self.list_files()

    def move_selected(self):
        folder = self.folder_path.get()
        target = self.target_folder.get()
        if not target:
            messagebox.showerror(self.languages[self.current_lang]["error"], self.languages[self.current_lang]["error_select_folder"])
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
                messagebox.showerror(self.languages[self.current_lang]["error"], self.languages[self.current_lang]["error_select_folder"])
        self.list_files()

    def create_folder(self):
        folder = self.folder_path.get()
        target = self.target_folder.get()
        if not target:
            messagebox.showerror(self.languages[self.current_lang]["error"], self.languages[self.current_lang]["error_select_folder"])
            return
        target_path = os.path.join(folder, target)
        try:
            os.makedirs(target_path, exist_ok=True)
            messagebox.showerror(self.languages[self.current_lang]["error"], self.languages[self.current_lang]["error_select_folder"])
        except Exception as e:
            messagebox.showerror(self.languages[self.current_lang]["error"], self.languages[self.current_lang]["error_select_folder"])

if __name__ == "__main__":
    root = tk.Tk()
    app = UselessFileCleaner(root)
    root.mainloop()
