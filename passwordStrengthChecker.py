import customtkinter as ctk
from tkinter import messagebox
import re
import hashlib
import random
import string

# ---------- GLOBAL STYLE ----------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")   # we override most colors manually

APP_BG = "#050816"        # dark background (AI SaaS vibe)
CARD_BG = "#020617"       # slightly lighter for card
ACCENT_PURPLE = "#7c3aed"
ACCENT_PINK = "#ec4899"
TEXT_MAIN = "#e5e7eb"
TEXT_MUTED = "#9ca3af"

# ---------- ROOT WINDOW ----------
app = ctk.CTk()
app.title("Password Strength Lab")
app.geometry("720x480")
app.configure(fg_color=APP_BG)


# ---------- LOGIC ----------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def suggest_password(password: str) -> str:
    suggestions = []
    if not re.search(r"[A-Z]", password):
        suggestions.append(random.choice(string.ascii_uppercase))
    if not re.search(r"[a-z]", password):
        suggestions.append(random.choice(string.ascii_lowercase))
    if not re.search(r"[0-9]", password):
        suggestions.append(random.choice(string.digits))
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        suggestions.append(random.choice("!@#$%^&*()"))
    while len(password) + len(suggestions) < 8:
        suggestions.append(random.choice(string.ascii_letters + string.digits + "!@#$%^&*()"))
    return password + ''.join(suggestions)

def get_strength_color(strength: int) -> str:
    # strength is from 0–6
    if strength <= 2:
        return "#f97373"   # red-ish
    elif strength <= 4:
        return "#fbbf24"   # amber
    elif strength <= 5:
        return "#22c55e"   # green
    else:
        return ACCENT_PURPLE  # purple for maxed out

def check_password():
    password = password_entry.get()
    strength = 0

    # length
    if len(password) >= 12:
        strength += 2
    elif len(password) >= 8:
        strength += 1
    
    # character types
    if re.search(r"[A-Z]", password):
        strength += 1
    if re.search(r"[a-z]", password):
        strength += 1
    if re.search(r"[0-9]", password):
        strength += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        strength += 1

    ratio = strength / 6
    strength_color = get_strength_color(strength)

    # update progress bar
    progress_bar.set(ratio)
    progress_bar.configure(progress_color=strength_color)

    # update headline strength label
    if strength <= 2:
        result_label.configure(text="WEAK", text_color=strength_color)
        suggestion = suggest_password(password) if password else ""
        suggestion_label.configure(
            text=f"Try this:  {suggestion}" if password else "Use at least 8+ characters with symbols and numbers.",
            text_color=ACCENT_PINK
        )
    elif strength <= 4:
        result_label.configure(text="MODERATE", text_color=strength_color)
        suggestion_label.configure(
            text="Tip: Add more length, symbols, and numbers to harden it.",
            text_color=TEXT_MUTED
        )
    elif strength <= 5:
        result_label.configure(text="STRONG", text_color=strength_color)
        suggestion_label.configure(
            text="Nice. A bit more randomness and length would make it elite.",
            text_color=TEXT_MUTED
        )
    else:
        result_label.configure(text="EXCELLENT", text_color=strength_color)
        suggestion_label.configure(
            text="Maxed out. This is what security engineers like to see.",
            text_color=TEXT_MUTED
        )

    # save hash if checked
    if save_var.get():
        hashed = hash_password(password)
        with open("passwords.txt", "a") as file:
            file.write(hashed + "\n")
        messagebox.showinfo("Saved", "Password hash saved securely!")

def toggle_password():
    if password_entry.cget('show') == "*":
        password_entry.configure(show="")
        toggle_button.configure(text="Hide")
    else:
        password_entry.configure(show="*")
        toggle_button.configure(text="Show")


# ---------- HEADER (hero-style) ----------
header_frame = ctk.CTkFrame(master=app, fg_color="transparent")
header_frame.pack(pady=(30, 10))

title_label = ctk.CTkLabel(
    master=header_frame,
    text="Password Strength Lab",
    font=("Segoe UI Semibold", 30),
    text_color=TEXT_MAIN
)
title_label.pack()

subtitle_label = ctk.CTkLabel(
    master=header_frame,
    text="Are your passwords REALLY secure? Test them out!",
    font=("Segoe UI", 14),
    text_color=TEXT_MUTED
)
subtitle_label.pack(pady=(5, 0))


# ---------- MAIN CARD ----------
card = ctk.CTkFrame(
    master=app,
    fg_color=CARD_BG,
    corner_radius=26
)
card.pack(padx=40, pady=10, fill="both", expand=False)

# label for input
password_label = ctk.CTkLabel(
    master=card,
    text="Enter your password",
    font=("Segoe UI", 14),
    text_color=TEXT_MAIN
)
password_label.pack(anchor="w", padx=24, pady=(22, 4))

# password entry
password_entry = ctk.CTkEntry(
    master=card,
    placeholder_text="Use a mix of letters, numbers, and symbols",
    show="*",
    height=40,
    corner_radius=12,
    fg_color="#020617",
    border_width=1,
    border_color="#1f2937",
    text_color=TEXT_MAIN
)
password_entry.pack(padx=24, fill="x", pady=(0, 10))

# row: show/hide + check button
row = ctk.CTkFrame(master=card, fg_color="transparent")
row.pack(padx=24, fill="x", pady=(0, 10))

toggle_button = ctk.CTkButton(
    master=row,
    text="Show",
    width=80,
    command=toggle_password,
    fg_color="#111827",
    hover_color="#1f2937",
    corner_radius=10
)
toggle_button.pack(side="left")

check_button = ctk.CTkButton(
    master=row,
    text="Check Strength",
    command=check_password,
    fg_color=ACCENT_PURPLE,
    hover_color="#6d28d9",
    corner_radius=10
)
check_button.pack(side="right")

# save checkbox
save_var = ctk.BooleanVar()
save_checkbox = ctk.CTkCheckBox(
    master=card,
    text="Save a hashed version of this password",
    variable=save_var,
    text_color=TEXT_MUTED,
    fg_color=ACCENT_PURPLE,
    hover_color="#4c1d95",
    border_color="#4c1d95"
)
save_checkbox.pack(anchor="w", padx=24, pady=(0, 16))

# strength meter label
meter_label = ctk.CTkLabel(
    master=card,
    text="Strength meter",
    font=("Segoe UI", 13),
    text_color=TEXT_MUTED
)
meter_label.pack(anchor="w", padx=24, pady=(0, 4))

# progress bar
progress_bar = ctk.CTkProgressBar(
    master=card,
    width=420,
    height=12,
    corner_radius=999,
    fg_color="#020617",
    progress_color=ACCENT_PURPLE
)
progress_bar.set(0)
progress_bar.pack(padx=24, pady=(0, 16))

# BIG strength text
result_label = ctk.CTkLabel(
    master=card,
    text="",
    font=("Segoe UI Black", 28),
    text_color=ACCENT_PURPLE
)
result_label.pack(pady=(0, 4))

# suggestion / tips
suggestion_label = ctk.CTkLabel(
    master=card,
    text="",
    font=("Segoe UI", 13),
    text_color=TEXT_MUTED,
    wraplength=440,
    justify="center"
)
suggestion_label.pack(pady=(0, 22))

# ---------- MAINLOOP ----------
app.mainloop()
