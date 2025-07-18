import os
import pygame
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, END

class UselessFileCleaner:
    def __init__(self, root):
        self.root = root
        self.root.bind("<Configure>", self.on_resize)
        self.resize_after_id = None
        self.last_width = self.root.winfo_width() if hasattr(self.root, 'winfo_width') else 800
        self.theme = "light"  
        self.default_theme = "light"
        self.default_lang = "en"
        self.sound_effects = True
        self.music_enabled = False
        self.volume = 0.5
        pygame.mixer.init()
        self.sound_file = os.path.join(os.path.dirname(__file__), "click.wav")
        self.music_file = os.path.join(os.path.dirname(__file__), "background.mp3")
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

    def set_language(self, lang):
        self.current_lang = lang
        self.refresh_ui()    

    def setup_ui(self):
        self.widgets = []  
        menubar = tk.Menu(self.root)
        lang_menu = tk.Menu(menubar, tearoff=0)
        lang_menu.add_command(label="Suomi", command=lambda: self.set_language("fi"))
        lang_menu.add_command(label="English", command=lambda: self.set_language("en"))
        menubar.add_cascade(label="Kieli / Language", menu=lang_menu)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Tumma teema", command=lambda: self.set_theme("dark"))
        settings_menu.add_command(label="Vaalea teema", command=lambda: self.set_theme("light"))
        settings_menu.add_separator()
        settings_menu.add_command(label=f"Ääniefektit {'Päällä' if self.sound_effects else 'Pois'}", command=self.toggle_sound_effects)
        settings_menu.add_command(label=f"Taustamusiikki {'Päällä' if self.music_enabled else 'Pois'}", command=self.toggle_music)
        volume_menu = tk.Menu(settings_menu, tearoff=0)
        for v in [0, 20, 40, 60, 80, 100]:
            volume_menu.add_command(label=f"{v}", command=lambda val=v: self.set_volume_menu(val))
        settings_menu.add_cascade(label=f"Äänenvoimakkuus: {int(self.volume*100)}", menu=volume_menu)
        settings_menu.add_separator()
        settings_menu.add_command(label="Palauta oletusasetukset", command=self.reset_defaults)
        menubar.add_cascade(label="Asetukset / Settings", menu=settings_menu)

        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        self.label_appname = tk.Label(top_frame, text=self.languages[self.current_lang]["app_name"], anchor="w")
        self.label_appname.pack(side=tk.LEFT, padx=10, pady=5)
        self.label_icon = tk.Label(top_frame, text="🧹")
        self.label_icon.pack(side=tk.LEFT, padx=5)

        author_text = {
            "fi": "Tehnyt Julle98",
            "en": "Made by Julle98"
        }
        self.author_label = tk.Label(top_frame, text=author_text[self.current_lang], fg="blue", cursor="hand2")
        self.author_label.pack(side=tk.LEFT, padx=10)
        self.author_label.bind("<Button-1>", lambda e: self.open_github())

        instructions = {
            "fi": "Käyttöohje: Valitse kansio, listaa tiedostot, valitse tiedostot ja poista/siirrä. Voit luoda uuden kansion tärkeille tiedostoille.",
            "en": "Instructions: Select a folder, list files, select files and delete/move. You can create a new folder for important files."
        }
        self.label_instructions = tk.Label(top_frame, text=instructions[self.current_lang], anchor="w", fg="gray")
        self.label_instructions.pack(side=tk.TOP, anchor="w", fill=tk.X, padx=10, pady=(0,5))

        folder_frame = tk.Frame(self.root)
        folder_frame.pack(fill=tk.X, padx=10, pady=5)
        self.label_select_folder = tk.Label(folder_frame, text=self.languages[self.current_lang]["select_folder"])
        self.label_select_folder.pack(side=tk.LEFT)
        self.entry_folder = tk.Entry(folder_frame, textvariable=self.folder_path)
        self.entry_folder.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.button_browse = tk.Button(folder_frame, text=self.languages[self.current_lang]["browse"], command=self.browse_folder)
        self.button_browse.pack(side=tk.LEFT, padx=5)
        self.button_list_files = tk.Button(folder_frame, text=self.languages[self.current_lang]["list_files"], command=self.list_files)
        self.button_list_files.pack(side=tk.LEFT, padx=5)

        listbox_frame = tk.Frame(self.root)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.listbox = Listbox(listbox_frame, selectmode=tk.MULTIPLE)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        action_frame = tk.Frame(self.root)
        action_frame.pack(fill=tk.X, padx=10, pady=5)
        self.button_delete = tk.Button(action_frame, text=self.languages[self.current_lang]["delete_selected"], command=self.delete_selected)
        self.button_delete.pack(side=tk.LEFT, padx=5)
        self.button_move = tk.Button(action_frame, text=self.languages[self.current_lang]["move_selected"], command=self.move_selected)
        self.button_move.pack(side=tk.LEFT, padx=5)

        target_frame = tk.Frame(self.root)
        target_frame.pack(fill=tk.X, padx=10, pady=5)
        self.target_folder = tk.StringVar()
        self.entry_target_folder = tk.Entry(target_frame, textvariable=self.target_folder)
        self.entry_target_folder.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.button_new_folder = tk.Button(target_frame, text=self.languages[self.current_lang]["new_folder"], command=self.create_folder)
        self.button_new_folder.pack(side=tk.LEFT, padx=5)

        self.widgets = [
            self.label_appname, self.label_icon, self.author_label, self.label_instructions,
            self.label_select_folder, self.entry_folder, self.button_browse, self.button_list_files,
            self.listbox, self.button_delete, self.button_move, self.entry_target_folder, self.button_new_folder
        ]

        self.root.config(menu=menubar)
    def set_volume_menu(self, value):
        self.volume = float(value) / 100.0
        pygame.mixer.music.set_volume(self.volume)
        self.refresh_ui()
        
    def toggle_sound_effects(self):
        self.sound_effects = not self.sound_effects
        self.refresh_ui()

    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            try:
                pygame.mixer.music.load(self.music_file)
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play(-1)
            except Exception:
                pass
        else:
            pygame.mixer.music.stop()
        self.refresh_ui()

    def set_volume(self, value):
        self.volume = float(value) / 100.0
        pygame.mixer.music.set_volume(self.volume)
    def set_theme(self, theme):
        self.theme = theme
        self.apply_theme()

    def apply_theme(self):
        if not hasattr(self, "widgets") or not self.widgets:
            return
        bg = "#222" if self.theme == "dark" else "#f0f0f0"
        fg = "#fff" if self.theme == "dark" else "#000"
        self.root.configure(bg=bg)
        for widget in self.widgets:
            try:
                widget.configure(bg=bg, fg=fg)
            except Exception:
                pass
        if hasattr(self, "listbox"):
            self.listbox.configure(bg=bg, fg=fg, selectbackground="#444" if self.theme=="dark" else "#cce", selectforeground=fg)
        for frame in self.root.winfo_children():
            if isinstance(frame, tk.Frame):
                try:
                    frame.configure(bg=bg)
                except Exception:
                    pass

    def reset_defaults(self):
        self.theme = self.default_theme
        self.current_lang = self.default_lang
        self.sound_effects = True
        self.music_enabled = False
        self.volume = 0.5
        pygame.mixer.music.set_volume(self.volume)
        self.refresh_ui()

        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        self.label_appname = tk.Label(top_frame, text=self.languages[self.current_lang]["app_name"], anchor="w")
        self.label_appname.pack(side=tk.LEFT, padx=10, pady=5)
        self.label_icon = tk.Label(top_frame, text="🧹")
        self.label_icon.pack(side=tk.LEFT, padx=5)

        author_text = {
            "fi": "Tehnyt Julle98",
            "en": "Made by Julle98"
        }
        self.author_label = tk.Label(top_frame, text=author_text[self.current_lang], fg="blue", cursor="hand2")
        self.author_label.pack(side=tk.LEFT, padx=10)
        self.author_label.bind("<Button-1>", lambda e: self.open_github())

        instructions = {
            "fi": "Käyttöohje: Valitse kansio, listaa tiedostot, valitse tiedostot ja poista/siirrä. Voit luoda uuden kansion tärkeille tiedostoille.",
            "en": "Instructions: Select a folder, list files, select files and delete/move. You can create a new folder for important files."
        }
        self.label_instructions = tk.Label(top_frame, text=instructions[self.current_lang], anchor="w", fg="gray")
        self.label_instructions.pack(side=tk.TOP, anchor="w", fill=tk.X, padx=10, pady=(0,5))

        folder_frame = tk.Frame(self.root)
        folder_frame.pack(fill=tk.X, padx=10, pady=5)
        self.label_select_folder = tk.Label(folder_frame, text=self.languages[self.current_lang]["select_folder"])
        self.label_select_folder.pack(side=tk.LEFT)
        self.entry_folder = tk.Entry(folder_frame, textvariable=self.folder_path)
        self.entry_folder.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.button_browse = tk.Button(folder_frame, text=self.languages[self.current_lang]["browse"], command=self.browse_folder)
        self.button_browse.pack(side=tk.LEFT, padx=5)
        self.button_list_files = tk.Button(folder_frame, text=self.languages[self.current_lang]["list_files"], command=self.list_files)
        self.button_list_files.pack(side=tk.LEFT, padx=5)

        listbox_frame = tk.Frame(self.root)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.listbox = Listbox(listbox_frame, selectmode=tk.MULTIPLE)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        action_frame = tk.Frame(self.root)
        action_frame.pack(fill=tk.X, padx=10, pady=5)
        self.button_delete = tk.Button(action_frame, text=self.languages[self.current_lang]["delete_selected"], command=self.delete_selected)
        self.button_delete.pack(side=tk.LEFT, padx=5)
        self.button_move = tk.Button(action_frame, text=self.languages[self.current_lang]["move_selected"], command=self.move_selected)
        self.button_move.pack(side=tk.LEFT, padx=5)

        target_frame = tk.Frame(self.root)
        target_frame.pack(fill=tk.X, padx=10, pady=5)
        self.target_folder = tk.StringVar()
        self.entry_target_folder = tk.Entry(target_frame, textvariable=self.target_folder)
        self.entry_target_folder.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.button_new_folder = tk.Button(target_frame, text=self.languages[self.current_lang]["new_folder"], command=self.create_folder)
        self.button_new_folder.pack(side=tk.LEFT, padx=5)

        self.widgets = [
            self.label_appname, self.label_icon, self.author_label, self.label_instructions,
            self.label_select_folder, self.entry_folder, self.button_browse, self.button_list_files,
            self.listbox, self.button_delete, self.button_move, self.entry_target_folder, self.button_new_folder
        ]
    
    def open_github(self):
        import webbrowser
        webbrowser.open_new("https://github.com/Julle98")

    def on_resize(self, event):
        new_width = event.width
        if abs(new_width - getattr(self, 'last_width', 0)) < 50:
            return
        self.last_width = new_width
        if self.resize_after_id:
            self.root.after_cancel(self.resize_after_id)
        self.resize_after_id = self.root.after(150, lambda: self.update_fonts(max(10, min(20, int(new_width / 50)))))

    def update_fonts(self, size):
        if not hasattr(self, "widgets") or not self.widgets:
            return
        font_main = ("Arial", size, "bold")
        font_normal = ("Arial", size)
        for widget in self.widgets:
            if isinstance(widget, tk.Label):
                widget.config(font=font_main)
            else:
                widget.config(font=font_normal)

    def refresh_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_ui()
        self.apply_theme()

    def play_click(self):
        if self.sound_effects:
            try:
                sound = pygame.mixer.Sound(self.sound_file)
                sound.set_volume(self.volume)
                sound.play()
            except Exception:
                pass

    def browse_folder(self):
        self.play_click()
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def list_files(self):
        self.play_click()
        self.listbox.delete(0, END)
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror(self.languages[self.current_lang]["error"], self.languages[self.current_lang]["error_select_folder"])
            return
        for f in os.listdir(folder):
            self.listbox.insert(END, f)

    def delete_selected(self):
        self.play_click()
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
        self.play_click()
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
        self.play_click()
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
