#!/usr/bin/env python3

import re
import json
import mysql.connector
import tkinter as tk
from tkinter import filedialog

# Fungsi untuk mengekstrak nama kelas dari file PHP
def extract_class_name(contents):
    class_pattern = r'class\s+(\w+)\s+extends\s+REST_Controller'
    match = re.search(class_pattern, contents)
    if match:
        return match.group(1)
    return None

# Fungsi untuk mengekstrak data fungsi dan metodenya dari file PHP
def extract_functions(file_path):
    with open(file_path, 'r') as file:
        contents = file.read()

    # Ekstrak nama kelas
    class_name = extract_class_name(contents)
    if not class_name:
        print("Nama kelas tidak ditemukan.")
        return []

    # Regex untuk mencari semua public functions dan metode HTTP
    pattern = r'public\s+function\s+(\w+)_([a-z]+)\(\)'
    matches = re.findall(pattern, contents)

    # Membuat list dengan format yang diinginkan (menggabungkan nama kelas dan nama fungsi)
    result = []
    for match in matches:
        function_name, method = match
        result.append({
            "function": f"{class_name}/{function_name}",  # Menggabungkan nama kelas dan fungsi
            "method": method
        })

    return result

# Fungsi untuk memasukkan data ke database
def insert_into_db(functions_list):
    try:
        # Menghubungkan ke database MySQL
        connection = mysql.connector.connect(
            host="<ip>",    # Sesuaikan dengan host MySQL Anda
            port=30600,           # Sesuaikan dengan port MySQL Anda    
            user="<user>",         # Sesuaikan dengan username MySQL Anda
            password="<password>",         # Sesuaikan dengan password MySQL Anda
            database="<database>"  # Sesuaikan dengan nama database Anda
        )

        cursor = connection.cursor()

        sql_check_duplicate = "SELECT COUNT(*) FROM api WHERE api_path = %s AND api_method = %s"
        sql_insert = "INSERT INTO api (api_path, api_method) VALUES (%s, %s)"

        for item in functions_list:
            cursor.execute(sql_check_duplicate, (item['function'], item['method']))
            result = cursor.fetchone()
            if result[0] == 0:  # No duplicate found
                cursor.execute(sql_insert, (item['function'], item['method']))
                print(f"Inserted: {item['function']} - {item['method']}")
            else:
                print(f"Duplicate found: {item['function']} - {item['method']}")

        # Commit transaksi
        connection.commit()

        print(f"{cursor.rowcount} record(s) inserted successfully.")

    except mysql.connector.Error as error:
        print(f"Failed to insert record into MySQL table: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Fungsi untuk membuka dialog file chooser
def choose_file():
    root = tk.Tk()
    root.withdraw()  # Menyembunyikan jendela utama Tkinter
    file_path = filedialog.askopenfilename(
        title="Pilih File PHP",
        filetypes=[("PHP Files", "*.php"), ("All Files", "*.*")]
    )
    
    if file_path:
        functions_list = extract_functions(file_path)
        print(json.dumps(functions_list, indent=4))
        # Masukkan data ke database
        insert_into_db(functions_list)
    else:
        print("Tidak ada file yang dipilih.")

if __name__ == "__main__":
    choose_file()
