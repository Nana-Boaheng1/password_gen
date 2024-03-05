import tkinter as tk
from tkinter import messagebox, colorchooser
import random
import string
import pyperclip
from password_strength import PasswordPolicy
import re

COMMON_PASSWORDS = ["password", "123456", "qwerty", "abc123", "admin", "letmein", "welcome"]

def is_common_password(password):
    return password.lower() in COMMON_PASSWORDS

def has_repeated_patterns(password):
    pattern = re.compile(r"(.)\1{2,}")  # Detects repeated characters (3 or more times)
    return bool(pattern.search(password))

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.configure(bg='#F0F0F0')
        self.root.option_add('*TButton*background', '#F0F0F0')
        self.root.option_add('*TButton*foreground', 'black')

        self.password_var = tk.StringVar()
        self.length_var = tk.IntVar(value=12)
        self.include_letters_var = tk.BooleanVar(value=True)
        self.include_numbers_var = tk.BooleanVar(value=True)
        self.include_symbols_var = tk.BooleanVar(value=True)

        self.current_theme = "Light"
        self.animation_speed = 100

        self.create_widgets()

    def create_widgets(self):
        length_label = tk.Label(self.root, text="Password Length:")
        length_entry = tk.Entry(self.root, textvariable=self.length_var, width=5)

        letters_cb = tk.Checkbutton(self.root, text="Letters", variable=self.include_letters_var)
        numbers_cb = tk.Checkbutton(self.root, text="Numbers", variable=self.include_numbers_var)
        symbols_cb = tk.Checkbutton(self.root, text="Symbols", variable=self.include_symbols_var)

        generate_button = tk.Button(self.root, text="Generate Password", command=lambda: [self.generate_password(), self.animate_button(generate_button)])

        password_label = tk.Label(self.root, text="Generated Password:")
        password_entry = tk.Entry(self.root, textvariable=self.password_var, state='readonly', width=30)

        copy_button = tk.Button(self.root, text="Copy to Clipboard", command=self.copy_to_clipboard)

        self.strength_label = tk.Label(self.root, text="Password Strength:")
        self.strength_indicator = tk.Label(self.root, text="", fg="red")

        self.preview_label = tk.Label(self.root, text="Password Preview:")
        self.preview_entry = tk.Entry(self.root, textvariable=self.password_var, state='readonly', width=30)

        theme_button = tk.Button(self.root, text="Toggle Theme", command=self.toggle_theme)
        theme_button.grid(row=5, column=2, pady=10)

        length_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
        length_entry.grid(row=0, column=1, padx=10, pady=10)
        letters_cb.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        numbers_cb.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        symbols_cb.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)
        generate_button.grid(row=2, column=0, columnspan=3, pady=10)
        password_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        password_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=10)
        copy_button.grid(row=4, column=0, pady=10)
        self.strength_label.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)
        self.strength_indicator.grid(row=4, column=2, padx=10, pady=10)
        self.preview_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        self.preview_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

    def generate_password(self):
        letters = string.ascii_letters if self.include_letters_var.get() else ""
        numbers = string.digits if self.include_numbers_var.get() else ""
        symbols = string.punctuation if self.include_symbols_var.get() else ""
        all_chars = letters + numbers + symbols

        if not all_chars:
            messagebox.showwarning("Warning", "Please select at least one character type.")
            return

        password = ''.join(random.choice(all_chars) for _ in range(self.length_var.get()))

        self.password_var.set(password)

        strength = self.calculate_strength(password)
        self.strength_indicator.config(text=strength, fg=self.get_strength_color(strength))

    def copy_to_clipboard(self):
        password = self.password_var.get()
        pyperclip.copy(password)
        messagebox.showinfo("Success", "Password copied to clipboard!")

    def animate_button(self, button):
        button.config(relief=tk.SUNKEN)
        self.root.after(self.animation_speed, lambda: button.config(relief=tk.RAISED))

    def calculate_strength(self, password):
        policy = PasswordPolicy.from_names(
            length=8,
            uppercase=1,
            numbers=1,
            special=1,
            nonletters=1,
        )

        if is_common_password(password):
            return "Weak"

        if has_repeated_patterns(password):
            return "Weak"

        feedback = policy.test(password)

        if "length" in feedback:
            return "Weak"
        elif "entropy" in feedback:
            return "Strong"
        else:
            return "Medium"

    def get_strength_color(self, strength):
        if strength == "Weak":
            return "red"
        elif strength == "Medium":
            return "orange"
        elif strength == "Strong":
            return "green"
        else:
            return "black"

    def toggle_theme(self):
        if self.current_theme == "Light":
            self.root.configure(bg='#121212')
            self.root.option_add('*TButton*background', '#121212')
            self.root.option_add('*TButton*foreground', 'white')
            self.current_theme = "Dark"
        else:
            self.root.configure(bg='#F0F0F0')
            self.root.option_add('*TButton*background', '#F0F0F0')
            self.root.option_add('*TButton*foreground', 'black')
            self.current_theme = "Light"

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
