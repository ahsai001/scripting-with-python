import tkinter as tk
from tkinter import messagebox
import os

def save_to_files():
    a_text = text_a.get("1.0", tk.END).strip()
    b_text = text_b.get("1.0", tk.END).strip()
    c_text = text_c.get("1.0", tk.END).strip()

    # Ambil pilihan API
    selected_api = api_choice.get()

    # Tentukan file names berdasarkan pilihan
    suffix = "" if selected_api == "api" else "2"
    try:
        # Path dasar
        base_path = r"C:/xampp7433/apache/conf"

        file_x = os.path.join(base_path, f"ssl.crt/server{suffix}.crt")
        file_y = os.path.join(base_path, f"ssl.key/server{suffix}.key")
        file_z = os.path.join(base_path, f"ssl.chain/server{suffix}.chain")
        file_p = os.path.join(base_path, f"ssl.crt/fullchain{suffix}.pem")

        # Simpan ke file
        with open(file_x, "w", encoding="utf-8") as fx:
            fx.write(a_text)

        with open(file_y, "w", encoding="utf-8") as fy:
            fy.write(b_text)

        with open(file_z, "w", encoding="utf-8") as fz:
            fz.write(c_text)

        with open(file_p, "w", encoding="utf-8") as fp:
            fp.write(f"{a_text}\n{c_text}")

        messagebox.showinfo("Success", f"Files saved as API version: {selected_api}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save files:\n{e}")

# GUI setup
root = tk.Tk()
root.title("SSL File Writer")
root.geometry("500x650")

# Pilihan API
api_choice = tk.StringVar(value="api")
tk.Label(root, text="Pilih API:").pack()
tk.Radiobutton(root, text="api.domain.com", variable=api_choice, value="api").pack()
tk.Radiobutton(root, text="api2.domain.com", variable=api_choice, value="api2").pack()

# Input A
tk.Label(root, text="Input(CRT)").pack()
text_a = tk.Text(root, height=5)
text_a.pack(pady=5)

# Input B
tk.Label(root, text="Input (KEY)").pack()
text_b = tk.Text(root, height=5)
text_b.pack(pady=5)

# Input C
tk.Label(root, text="Input (CABUNDLE)").pack()
text_c = tk.Text(root, height=5)
text_c.pack(pady=5)

# Tombol Simpan
tk.Button(root, text="Save to SSL Files", command=save_to_files).pack(pady=20)

# Launch GUI
if __name__ == "__main__":
    root.mainloop()
