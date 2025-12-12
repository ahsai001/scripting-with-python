from tkinter import Tk
from tkinter import filedialog
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

# Fungsi untuk mendekripsi data dengan AES-256-CBC dan PKCS7 padding
def decrypt_aes256cbc_pkcs7(encrypted_data, key, iv):
    try:
        # Membuat objek cipher AES dengan mode CBC
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Mendekripsi data dan melakukan unpadding PKCS7
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        return decrypted_data.decode('utf-8')  # Decode hasil dekripsi dengan utf-8
    except (ValueError, KeyError) as e:
        print(f"Error dalam dekripsi: {e}")
        return None

# Fungsi untuk mendekripsi file yang dienkripsi per baris
def decrypt_file_with_aes256cbc(input_file, key, iv):
    # Menambahkan postfix pada nama file
    input_dir, input_filename = os.path.split(input_file)
    output_filename = os.path.splitext(input_filename)[0] + '_decrypted.txt'
    output_file = os.path.join(input_dir, output_filename)

    try:
        # Membuka file input dan output dengan encoding utf-8
        with open(input_file, 'r', encoding='utf-8') as enc_file, open(output_file, 'w', encoding='utf-8') as dec_file:
            for line in enc_file:
                # Mengonversi baris dari base64 (jika dienkripsi dalam base64)
                encrypted_data = base64.b64decode(line.strip())

                # Mendekripsi setiap baris dengan kunci dan iv yang diberikan
                decrypted_line = decrypt_aes256cbc_pkcs7(encrypted_data, key, iv)
                
                # Menulis hasil dekripsi ke file keluaran
                if decrypted_line:
                    dec_file.write(decrypted_line + '\n')

        print(f"File berhasil didekripsi dan disimpan sebagai {output_file}")
    except Exception as e:
        print(f"Kesalahan dalam memproses file: {e}")

# Fungsi untuk memilih file dengan file chooser tkinter
def choose_file():
    root = Tk()
    root.withdraw()  # Menyembunyikan jendela utama tkinter
    file_path = filedialog.askopenfilename()  # Menampilkan dialog file chooser
    return file_path


# Key harus 32 byte untuk AES-256
key = b''  # Sesuaikan key 32 byte

# IV harus 16 byte untuk AES-CBC
iv = b''                      # Sesuaikan iv 16 byte

# Memilih file input menggunakan file chooser
input_file = choose_file()

# Mengecek apakah file dipilih
if input_file:
    # Panggil fungsi untuk dekripsi file
    decrypt_file_with_aes256cbc(input_file, key, iv)
else:
    print("Tidak ada file yang dipilih.")
