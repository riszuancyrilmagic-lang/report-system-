import webbrowser
import urllib.parse
import time

def cari_jejak():
    print("="*50)
    print("   CARIAN OSINT: EMAIL & NAMA SUSPEK   ")
    print("="*50)
    
    # Data sasaran
    email = "boyspark641@gmail.com"
    nama = "ABDUL HADI BIN MOHD NOR"
    
    # Encode untuk URL carian
    email_encoded = urllib.parse.quote(email)
    nama_encoded = urllib.parse.quote(nama)
    
    print(f"[*] Mencari jejak untuk: {email} & {nama}\n")
    
    # Senarai carian
    carian_list = [
        (f"Google: {email}", f"https://www.google.com/search?q=%22{email_encoded}%22"),
        (f"Google: Nama + Black Cafe", f"https://www.google.com/search?q=%22{nama_encoded}%22+%22Black+Cafe%22"),
        (f"Google: Nama + TikTok", f"https://www.google.com/search?q=%22{nama_encoded}%22+TikTok+OR+hadimarkno"),
        (f"Semak Data Bocor (HIBP)", f"https://haveibeenpwned.com/account/{email_encoded}"),
        (f"Facebook: Cari Emel", f"https://www.facebook.com/search/top?q={email_encoded}"),
        (f"Semak SSM (Pendaftaran Bisnes)", "https://www.ssm-einfo.my/")
    ]
    
    for tajuk, url in carian_list:
        print(f"➡️ Membuka: {tajuk}...")
        webbrowser.open_new_tab(url)
        time.sleep(1.5) 
        
    print("\n✅ Selesai! Sila semak tab browser yang terbuka.")

if __name__ == "__main__":
    cari_jejak()