#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import os

# === Konfigurasi Subdomain Dinamis ===
# Key = label subdomain
# Value = suffix unik untuk nama file
DOMAINS = {
    "api.syshab.com": "",
    "api2.syshab.com": "2",
    "s.syshab.com": "_s",
    # tambahkan subdomain baru di sini 👇
    # "xyz.syshab.com": "_xyz",
}

def save_to_files():
    a_text = text_a.get("1.0", tk.END).strip()
    b_text = text_b.get("1.0", tk.END).strip()
    c_text = text_c.get("1.0", tk.END).strip()

    selected_api = api_choice.get()

    if selected_api not in DOMAINS:
        messagebox.showerror("Error", "Subdomain tidak valid!")
        return

    suffix = DOMAINS[selected_api]

    try:
        base_path = r"C:/xampp7433/apache/conf"

        file_x = os.path.join(base_path, f"ssl.crt/server{suffix}.crt")
        file_y = os.path.join(base_path, f"ssl.key/server{suffix}.key")
        file_z = os.path.join(base_path, f"ssl.chain/server{suffix}.chain")
        file_p = os.path.join(base_path, f"ssl.crt/fullchain{suffix}.pem")

        with open(file_x, "w", encoding="utf-8") as fx:
            fx.write(a_text)

        with open(file_y, "w", encoding="utf-8") as fy:
            fy.write(b_text)

        with open(file_z, "w", encoding="utf-8") as fz:
            fz.write(c_text)

        with open(file_p, "w", encoding="utf-8") as fp:
            fp.write(f"{a_text}\n{c_text}")

        messagebox.showinfo("Success", f"✅ Files saved for domain: {selected_api}")

    except Exception as e:
        messagebox.showerror("Error", f"❌ Failed to save files:\n{e}")

# === GUI ===
root = tk.Tk()
root.title("SSL File Writer")
root.geometry("500x700")

api_choice = tk.StringVar(value=list(DOMAINS.keys())[0])

tk.Label(root, text="Pilih Subdomain:").pack(pady=5)
for domain in DOMAINS.keys():
    tk.Radiobutton(root, text=domain, variable=api_choice, value=domain).pack(anchor="w", padx=40)

tk.Label(root, text="Input (CRT)").pack()
text_a = tk.Text(root, height=5)
text_a.pack(pady=5)

tk.Label(root, text="Input (KEY)").pack()
text_b = tk.Text(root, height=5)
text_b.pack(pady=5)

tk.Label(root, text="Input (CABUNDLE)").pack()
text_c = tk.Text(root, height=5)
text_c.pack(pady=5)

tk.Button(root, text="Save to SSL Files", command=save_to_files).pack(pady=20)

if __name__ == "__main__":
    root.mainloop()
