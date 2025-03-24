# Author: Syamraya
# educational purpose only
# Entry system DC MokletDev v1.0 (NOT LICENSED)



import datetime
import random
import time
import colorama
import os
import msvcrt
import itertools
import sys
from colorama import Fore, Style
from collections import Counter

colorama.init(autoreset=True)

LOG_FILE = "log_masuk.txt"
VIP_FILE = "vip_list.txt"
ADMIN_PASSWORD = "ibraganteng999369"
SECRET_CODE = "izinmasukmin"
MAX_GAGAL = 3
BLOCK_TIME = 30  # dalam detik (30s)

gagal_captcha = {}

def loading_spinner(duration=2):
    spinner = itertools.cycle(['◜', '◠', '◝', '◞', '◡', '◟'])  # Karakter animasi loading
    start_time = time.time()

    while time.time() - start_time < duration:
        sys.stdout.write(Fore.YELLOW + f"\rLogging in {next(spinner)} ")  
        sys.stdout.flush()  # Memaksa output langsung muncul di terminal
        time.sleep(0.1)

    sys.stdout.write("\r" + " " * 20 + "\r")  # Menghapus baris loading spinner
    
def generate_captcha():
    return str(random.randint(1000, 9999))

def simpan_log(nama):
    waktu_masuk = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as file:
        file.write(f"{nama},{waktu_masuk}\n")

def hitung_login(nama):
    if not os.path.exists(LOG_FILE):
        return 1
    with open(LOG_FILE, "r") as file:
        return sum(1 for line in file if line.startswith(nama)) + 1

def tampilkan_log():
    if not os.path.exists(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
        print(Fore.RED + "\nBelum ada yang masuk DC MokletDev 😔\n")
        time.sleep(1)
        return

    print(Fore.CYAN + "\n=== Daftar User yang Masuk DC MokletDev ===")
    time.sleep(1)
    
    with open(LOG_FILE, "r") as file:
        for line in file:
            nama, waktu = line.strip().split(",")
            print(Fore.YELLOW + f"{nama} masuk pada {waktu}")
    print("")

def reset_log():
    countdown = 30  # Waktu hitung mundur dalam detik

    print(Fore.RED + "\n⚠️  Log masuk dan daftar VIP/VVIP akan dihapus!")
    print("Tekan 1 untuk melanjutkan, 2 untuk membatalkan.")

    start_time = time.time()  # Catat waktu mulai
    while True:
        elapsed_time = int(time.time() - start_time)
        remaining_time = countdown - elapsed_time

        if remaining_time <= 0:
            print(Fore.RED + "\n⏳ Waktu habis! Menghapus data...\n")
            break
            
        print(Fore.YELLOW + f"\r⏳ Waktu tersisa: {remaining_time} detik ", end="")
        if msvcrt.kbhit():  # Mengecek jika ada input dari keyboard (hanya untuk Windows)
            pilihan = msvcrt.getch().decode("utf-8")
            if pilihan == "1":
                print(Fore.GREEN + "\n✅ Penghapusan dilanjutkan!\n")
                time.sleep(1)
                break
                
            elif pilihan == "2":
                print(Fore.CYAN + "\n❌ Penghapusan dibatalkan!\n")
                time.sleep(1)
                return

        time.sleep(1)

    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        print(Fore.RED + "Log masuk telah dihapus!\n")
        time.sleep(1)
    else:
        print(Fore.RED + "Tidak ada log yang bisa dihapus.\n")

    if os.path.exists(VIP_FILE):
        os.remove(VIP_FILE)
        print(Fore.RED + "Daftar VIP/VVIP juga telah dihapus!\n")
        time.sleep(1)
    else:
        print(Fore.RED + "Tidak ada daftar VIP/VVIP yang bisa dihapus.\n")


def leaderboard():
    if not os.path.exists(LOG_FILE):
        print(Fore.RED + "\nBelum ada yang masuk DC MokletDev 😔\n")
        time.sleep(1)
        return
    
    with open(LOG_FILE, "r") as file:
        users = [line.strip().split(",")[0] for line in file]

    ranking = Counter(users).most_common()
    
    print(Fore.CYAN + "\n=== Leaderboard MokletDev ===")
    time.sleep(1)
    for i, (user, count) in enumerate(ranking, 1):
        role = cek_vip(user)  # Mengecek apakah user VIP/VVIP atau biasa
        role_text = Fore.YELLOW + "(User Common)"
        if role == "VIP":
            role_text = Fore.GREEN + "(VIP) 🌟"
        elif role == "VVIP":
            role_text = Fore.RED + "(VVIP) 👑"

        print(Fore.YELLOW + f"{i}. {user} - {count} kali masuk {role_text}")
        
    print("")

def tambah_vip():
    if not os.path.exists(LOG_FILE):
        print(Fore.RED + "\nBelum ada user yang bisa dijadikan VIP/VVIP!\n")
        return

    with open(LOG_FILE, "r") as file:
        users = list(set(line.strip().split(",")[0] for line in file))  # Menghapus duplikat jika ada 2 nama yang sama
    
    users.sort()  # Mengurutkan nama secara alfabetis a-z
    
    print(Fore.CYAN + "\n=== Pilih User untuk Dijadikan VIP/VVIP ===")
    for i, user in enumerate(users, 1):
        print(Fore.YELLOW + f"{i}. {user}")

    try:
        pilihan = int(input(Fore.YELLOW + "\nPilih nomor user: ").strip())
        if 1 <= pilihan <= len(users):
            nama = users[pilihan - 1]

            # Pilihan Role
            print(Fore.YELLOW + "\nPilih Role:")
            print("1. VIP")
            print("2. VVIP")

            role_pilihan = input(Fore.YELLOW + "Masukkan nomor role: ").strip()

            if role_pilihan == "1":
                role = "VIP"
            elif role_pilihan == "2":
                role = "VVIP"
            else:
                print(Fore.RED + "Role tidak valid!\n")
                return

            with open(VIP_FILE, "a") as file:
                file.write(f"{nama},{role}\n")
            print(Fore.GREEN + f"\n{nama} sekarang adalah {role} MokletDev! 🎉")
        else:
            print(Fore.RED + "Nomor tidak valid!\n")
    except ValueError:
        print(Fore.RED + "Masukkan angka yang valid!\n")

def cek_vip(nama):
    if not os.path.exists(VIP_FILE):
        return "User"
    with open(VIP_FILE, "r") as file:
        for line in file:
            user, role = line.strip().split(",")
            if user == nama:
                return role
    return "User"

def history_user():
    if not os.path.exists(LOG_FILE):
        print(Fore.RED + "\nBelum ada riwayat masuk.\n")
        return

    with open(LOG_FILE, "r") as file:
        users = list(set(line.strip().split(",")[0] for line in file))  # Menghapus duplikat

    users.sort()  # Mengurutkan nama secara alfabetis a-z

    print(Fore.CYAN + "\n=== Pilih User untuk Melihat Riwayat ===")
    for i, user in enumerate(users, 1):
        print(Fore.YELLOW + f"{i}. {user}")

    try:
        pilihan = int(input(Fore.YELLOW + "\nPilih nomor user: ").strip())
        if 1 <= pilihan <= len(users):
            nama = users[pilihan - 1]
            print(Fore.CYAN + f"\n=== Riwayat Masuk {nama} ===")
            
            with open(LOG_FILE, "r") as file:
                history = [line.strip().split(",")[1] for line in file if line.startswith(nama)]
            
            if history:
                for time in history:
                    print(Fore.YELLOW + f"{nama} masuk pada {time}")
            else:
                print(Fore.RED + f"{nama} belum pernah masuk.")
            print("")
        else:
            print(Fore.RED + "Nomor tidak valid!\n")
    except ValueError:
        print(Fore.RED + "Masukkan angka yang valid!\n")


def masuk_dc():
    print(Fore.CYAN + "\n=== Selamat datang di MokletDev! ===\n")
    time.sleep(1)
    
    nama = input(Fore.CYAN + "Masukkan nama Anda: ").strip()
    time.sleep(1)
    
    if not nama:
        print(Fore.RED + "Nama tidak boleh kosong!\n")
        time.sleep(1)
        return
    
    if nama in gagal_captcha and gagal_captcha[nama]["blokir"]:
        sisa_waktu = int(BLOCK_TIME - (time.time() - gagal_captcha[nama]["waktu"]))
        if sisa_waktu > 0:
            print(Fore.RED + f"Anda telah diblokir! Coba lagi dalam {sisa_waktu} detik.\n")
            return
        else:
            gagal_captcha[nama] = {"gagal": 0, "blokir": False}

    captcha = generate_captcha()
    print(Fore.MAGENTA + f"\nVerifikasi Captcha: {captcha}")
    user_captcha = input(Fore.YELLOW + "Masukkan kode verifikasi: ").strip()
    
    if user_captcha != captcha:
        gagal_captcha.setdefault(nama, {"gagal": 0, "blokir": False})
        gagal_captcha[nama]["gagal"] += 1
        
        if gagal_captcha[nama]["gagal"] >= MAX_GAGAL:
            gagal_captcha[nama]["blokir"] = True
            gagal_captcha[nama]["waktu"] = time.time()
            print(Fore.RED + f"Anda telah gagal {MAX_GAGAL} kali! Coba lagi dalam {BLOCK_TIME} detik.\n")
            return
        
        print(Fore.RED + f"Kode verifikasi salah! ({gagal_captcha[nama]['gagal']}x gagal)\n")
        return

    gagal_captcha[nama] = {"gagal": 0, "blokir": False}
    
    role = cek_vip(nama)
    jumlah_login = hitung_login(nama)
    
    simpan_log(nama)
    
    if jumlah_login == 1:
        print(Fore.BLUE + f"\nHi {nama}, ini pertama kalinya masuk! 🎉")
    else:
        if role == "VVIP":
            print(Fore.YELLOW + f"\n👑 Selamat datang VVIP {nama}! Ini masuk ke-{jumlah_login} kalinya! 🎉")
        elif role == "VIP":
            print(Fore.GREEN + f"\n🌟 Selamat datang VIP {nama}! Ini masuk ke-{jumlah_login} kalinya! 🎉")
        else:
            print(Fore.BLUE + f"\nHi {nama}, ini masuk ke-{jumlah_login} kalinya!")

def login_admin():
    password = input(Fore.YELLOW + "Masukkan password admin: ").strip()
    if password == ADMIN_PASSWORD:
        loading_spinner(2)  # Memunculkan animasi selama 2 detik
        print(Fore.GREEN + "Login berhasil ✅\n")  # Muncul setelah animasi selesai
        time.sleep(1)
        while True:
            
            print(Fore.CYAN + "\n=== Admin Panel MokletDev ===")
            print("1. Tampilkan Daftar User")
            print("2. Reset Log")
            print("3. Leaderboard")
            print("4. Tambah VIP/VVIP")
            print("5. Cek Riwayat User")
            print("6. Keluar")

            pilihan = input(Fore.YELLOW + "Pilih opsi: ").strip()

            if pilihan == "1":
                tampilkan_log()
            elif pilihan == "2":
                reset_log()
            elif pilihan == "3":
                leaderboard()
            elif pilihan == "4":
                tambah_vip()
            elif pilihan == "5":
                history_user()
            elif pilihan == "6":
                break
            else:
                print(Fore.RED + "Pilihan tidak valid!\n")
    else:
        print(Fore.RED + "Password salah!\n")

def main():
    while True:
        print(Fore.CYAN + "\n=== Sistem Masuk DC MokletDev ===")
        print("1. Masuk DC")
        print("2. Leaderboard")
        print("3. Keluar")
        print("4. Info Program")

        pilihan = input(Fore.YELLOW + "Pilih opsi (1/2/3/4): ").strip()

        if pilihan.lower() == SECRET_CODE:
            login_admin()
        elif pilihan == "1":
            masuk_dc()
        elif pilihan == "2":
            leaderboard()
        elif pilihan == "3":
            print(Fore.CYAN + "Keluar dari program...")
            time.sleep(2)
            print(Fore.GREEN + "Terima kasih telah menggunakan program ini! 😊")
            break
        elif pilihan == "4":
            print(Fore.CYAN + "\n=== Info Program ===")
            print("Sistem Masuk DC MokletDev " + Fore.YELLOW + "v1.0")
            print("Dibuat oleh: Syamraya Slebeww")
            print("GitHub: https://github.com/syamraya\n")
        else:
            print(Fore.RED + "Pilihan tidak valid!\n")

if __name__ == "__main__":
    main()

