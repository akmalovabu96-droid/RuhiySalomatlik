import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

# --- DATABASE MECHANICS ---
DB_FILE = "effort_log.json"


def load_data():
    if not os.path.exists(DB_FILE):
        return {"total_points": 0, "history": []}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return {"total_points": 0, "history": []}


def save_data(data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Database write error: {e}")


# --- INTERFACE COMMAND LOGIC ---

def submit_effort():
    text_input = input_box.get("1.0", "end-1c").strip()

    if not text_input or text_input == "Describe your quiet grit here...":
        messagebox.showwarning("Effort Tracker", "Please write down an effort before logging.")
        return

    points_awarded = 10
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    user_data["total_points"] += points_awarded
    new_entry = {
        "date": current_time,
        "description": text_input,
        "points": points_awarded
    }
    user_data["history"].insert(0, new_entry)

    save_data(user_data)

    points_display.config(text=f"{user_data['total_points']}")
    refresh_history_box()

    input_box.delete("1.0", tk.END)
    messagebox.showinfo("Effort Tracker", f"Grit Recorded! +{points_awarded} Points logged.")


def refresh_history_box():
    history_display.config(state="normal")
    history_display.delete("1.0", tk.END)

    if not user_data["history"]:
        history_display.insert(tk.END, "Your dashboard timeline is clear. Start tracking your victories below.")
        history_display.config(state="disabled")
        return

    for entry in user_data["history"]:
        log_line = f"🗓️  [{entry['date']}]  ✨ +{entry['points']} Pts\n"
        desc_line = f"   ↳ \"{entry['description']}\"\n"
        divider = "   " + "—" * 45 + "\n\n"

        history_display.insert(tk.END, log_line, "meta_tag")
        history_display.insert(tk.END, desc_line, "desc_tag")
        history_display.insert(tk.END, divider, "div_tag")

    history_display.config(state="disabled")


def clear_placeholder(_event):
    if input_box.get("1.0", "end-1c").strip() == "Describe your quiet grit here...":
        input_box.delete("1.0", tk.END)
        input_box.config(fg=COLOR_DARK)


# --- GRAPHICAL INTERFACE SETUP ---
user_data = load_data()

root = tk.Tk()
root.title("The Effort Tracker")
root.geometry("600x550")  # Compact baseline size

BG_MAIN = "#F1F5F9"
CARD_BG = "#FFFFFF"
COLOR_DARK = "#0F172A"
COLOR_MUTED = "#64748B"
ACCENT_GREEN = "#10B981"

root.configure(bg=BG_MAIN)

# Configure rows to stretch dynamically. Row 3 (Timeline) will absorb the scaling changes.
root.rowconfigure(3, weight=1)
root.columnconfigure(0, weight=1)

# 1. Total Points Dashboard Hero Frame
score_card = tk.Frame(root, bg=CARD_BG, bd=0, highlightthickness=1, highlightbackground="#E2E8F0")
score_card.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="ew")

points_title = tk.Label(score_card, text="TOTAL EFFORT POINTS", font=("Segoe UI", 9, "bold"), fg=COLOR_MUTED,
                        bg=CARD_BG)
points_title.pack(pady=(10, 2))

points_display = tk.Label(score_card, text=f"{user_data['total_points']}", font=("Segoe UI", 24, "bold"),
                          fg=ACCENT_GREEN, bg=CARD_BG)
points_display.pack(pady=(0, 10))

# 2. Historical Timeline Tracker Header
history_title = tk.Label(root, text="YOUR INVISIBLE VICTORIES TIMELINE", font=("Segoe UI", 9, "bold"), fg=COLOR_MUTED,
                         bg=BG_MAIN)
history_title.grid(row=2, column=0, padx=22, pady=(10, 2), sticky="w")

# 3. The Scrollable Timeline Container (This expands and shrinks automatically based on window size!)
history_frame = tk.Frame(root, bg=CARD_BG, bd=0, highlightthickness=1, highlightbackground="#E2E8F0")
history_frame.grid(row=3, column=0, padx=20, pady=5, sticky="nsew")

history_display = tk.Text(history_frame, bg=CARD_BG, font=("Segoe UI", 10), bd=0, wrap="word", padx=10, pady=10)
history_display.pack(fill="both", expand=True)

history_display.tag_configure("meta_tag", font=("Segoe UI", 10, "bold"), foreground=COLOR_DARK)
history_display.tag_configure("desc_tag", font=("Georgia", 10, "italic"), foreground=COLOR_MUTED)
history_display.tag_configure("div_tag", foreground="#E2E8F0")

# 4. Effort Entry Workspace Box
input_title = tk.Label(root, text="RECORD NEW GLIMMER OF GRIT", font=("Segoe UI", 9, "bold"), fg=COLOR_MUTED,
                       bg=BG_MAIN)
input_title.grid(row=4, column=0, padx=22, pady=(10, 2), sticky="w")

input_frame = tk.Frame(root, bg=CARD_BG, bd=0, highlightthickness=1, highlightbackground="#E2E8F0")
input_frame.grid(row=5, column=0, padx=20, pady=0, sticky="ew")

input_box = tk.Text(input_frame, height=2, font=("Segoe UI", 10), bg=CARD_BG, bd=0, wrap="word", padx=10, pady=5,
                    fg=COLOR_MUTED)
input_box.insert("1.0", "Describe your quiet grit here...")
input_box.bind("<FocusIn>", clear_placeholder)
input_box.pack(fill="x")

# 5. Action Push Control Button (Guaranteed to show at the bottom)
log_button = tk.Button(
    root, text="LOG EFFORT TO TIMELINE", font=("Segoe UI", 10, "bold"), fg=CARD_BG, bg=COLOR_DARK,
    activebackground=COLOR_MUTED, activeforeground=CARD_BG, bd=0, pady=10, cursor="hand2", command=submit_effort
)
log_button.grid(row=6, column=0, padx=20, pady=(10, 15), sticky="ew")

refresh_history_box()

root.mainloop()
