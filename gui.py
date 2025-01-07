import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import sys

class ConsoleRedirect:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.config(state="normal")
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)
        self.text_widget.config(state="disabled")

    def flush(self):
        pass

def select_image(callback):
    file_path = filedialog.askopenfilename(
        title="Válassz egy képet",
        filetypes=[("Képfájlok", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("Minden fájl", "*.*")]
    )
    if file_path and os.path.splitext(file_path)[1].lower() in [".png", ".jpg", ".jpeg", ".bmp", ".gif"]:
        print(f"Kiválasztott fájl: {file_path}")
        callback(file_path)
    elif not file_path:
        messagebox.showinfo("Információ", "Nem választottál ki képet.")
    else:
        messagebox.showwarning("Figyelem", "Érvénytelen fájltípus! Válassz egy képfájlt.")

def create_gui(callback):
    def quit_app():
        root.destroy()

    def show_easter_egg():
        messagebox.showinfo("Easter Egg", "Vagyok végig!")

    root = tk.Tk()
    root.title("Sudoku kiválasztása és megoldása")
    root.geometry("600x400")
    root.resizable(False, False)
    root.configure(bg="#F0F0F0")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", font=("Arial", 14), background="#F0F0F0", foreground="black")
    style.configure("Custom.TButton", font=("Arial", 12), padding=10, foreground="black", background="#FDE100")
    style.map("Custom.TButton", background=[("active", "#FFD700")])

    label = ttk.Label(
        root,
        text="Válassz egy képet feldolgozáshoz!",
        anchor="center",
        style="TLabel"
    )
    label.pack(pady=10)

    select_button = ttk.Button(
        root,
        text="Kép kiválasztása",
        command=lambda: select_image(callback),
        style="Custom.TButton"
    )
    select_button.pack(pady=10)

    quit_button = tk.Button(
        root,
        text="Bezárás",
        command=quit_app,
        bg="red",
        activebackground="red",
        fg="white",
        font=("Arial", 12),
        pady=5
    )
    quit_button.pack(pady=10)

    console_output = tk.Text(root, height=10, width=70, state="disabled", bg="#EAEAEA", wrap="word")
    console_output.pack(pady=10)

    easter_egg_button = tk.Button(
        root,
        text="",
        command=show_easter_egg,
        bg="#F0F0F0",
        activebackground="#F0F0F0",
        bd=0
    )
    easter_egg_button.place(relx=0.95, rely=0.95, anchor="se")

    sys.stdout = ConsoleRedirect(console_output)

    root.mainloop()

    sys.stdout = sys.__stdout__
