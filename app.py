import streamlit as st
import datetime
from fpdf import FPDF
import folium
from streamlit_folium import folium_static
import urllib.parse
import json
import os
from PIL import Image
import io

# ==========================================
# KONFIGURASI UI
# ==========================================
st.set_page_config(page_title="Sistem Siasatan Penipu", page_icon="🕵️‍♂️", layout="wide")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            [data-testid="stStatusWidget"] {visibility: hidden;}
            [data-testid="stToolbar"] {visibility: hidden;}
            [data-testid="stDecoration"] {visibility: hidden;}
            .viewerBadge_container__1QSob {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- MAKLUMAT SUSPEK ---
NAMA_SUSPEK = "ABDUL HADI BIN MOHD NOR"
NOMOR_SUSPEK = "+601128065526"
NOMOR_WA = "601128065526"
EMAIL_SUSPEK = "boyspark641@gmail.com"
USERNAME_TIKTOK = "hadimarkno"
USERNAME_SMULE = "GSR_ADIJDT_RX15A"
LINK_FB = "https://www.facebook.com/adisprinter"
LINK_FB_PHOTOS = "https://www.facebook.com/adisprinter/photos"
PLAT_KERETA = "WHG 8164"
PLAT_MOTOR = "WGG 4317"
CHECK_IN = "Ipoh, Perak"
CAPTION_FB = "Hati aku hanya pada Perak"
KERJA_FB = "KDN, Putrajaya"

KAWAN_RAPAT = [
    "Faiz Badiozaman",
    "Fitri Azizi Ramli",
    "Muhd Syhmy"
]

NAMA_MULE = "MOHAMMAD HILMI BIN MOHD HANIF"
BANK_MULE = "Bank Simpanan Nasional (BSN)"
AKAUN_MULE = "0820041100050836"
BAKI_HUTANG = "RM 1,783.00"

KENDERAAN_1 = {
    "plat": "WHG 8164",
    "nama": "MOHAMAD SYAFIQ B BADRUL HISHAM",
    "ic": "020114081039",
    "alamat": "NO 14 RUMAH AWAM 5, JLN KENAS, 33000 PERAK",
    "model": "PROTON SATRIA 1.4 GLI M",
    "status": "1 Rekod Kemalangan"
}

KENDERAAN_2 = {
    "plat": "WGG 4317",
    "nama": "MOHD FAZLIN BIN LAH",
    "ic": "740728085339",
    "alamat": "NO 18 LALUAN CHEPOR DAMAIN 12, 31200 PERAK",
    "model": "YAMAHA TZM 150",
    "status": "1 Rekod Kemalangan"
}

# ==========================================
# SISTEM SIMPAN & LOAD DATA (JSON)
# ==========================================
DATA_FILE = "simpanan_laporan.json"

TEKS_DEFAULT = (
    "1. Saya mengenali suspek sebagai pelanggan perniagaan saya sejak awal tahun lepas. "
    "Beliau sering menawarkan projek serta urusan jual beli barang komputer (PC).\n\n"
    "2. KES PERTAMA (Barang PC - RAM 16GB x2): Suspek menawarkan barang tersebut dengan harga murah. "
    "Saya telah membuat pembayaran lebih RM500. Namun, sehingga ke hari ini, barang fizikal yang saya pesan "
    "(RAM 16GB x2) tidak diserahkan dan wang tidak dipulangkan.\n\n"
    "3. KES KEDUA (Modal Perniagaan): Ketika menunggu barang PC saya, suspek meminta saya menampung modal "
    "RM1,500 untuk pelanggannya, dengan janji akan memulangkan modal beserta keuntungan. Suspek hanya membayar "
    "RM800 (RM500 keuntungan + RM300 modal). Baki hutang yang belum dijelaskan ialah RM1,443 "
    "(termasuk RM160 hutang servis game).\n\n"
    "4. Suspek telah MENGIKTIRAF beliau berhutang melalui WhatsApp dan menulis: "
    "'Total baki aku hg belum settle RM1783'. Namun, beliau kini gagal membayar dan cuba mengelak.\n\n"
    "5. Saya juga mendapati suspek mempunyai pelbagai rekod digital yang mengaitkannya dengan kawasan Perak "
    "(Check-in Facebook di Ipoh, video TikTok di Sg Siput, tag 'Adi Ipoh' di GetContact, dan caption FB "
    "'Hati aku hanya pada Perak'). Nombor telefon suspek juga telah ditag sebagai penipu oleh 80 mangsa lain. "
    "Saya turut mempunyai bukti gambar kenderaan suspek (Kereta: WHG 8164, Motor: WGG 4317) yang saya peroleh "
    "daripada profil Facebook beliau.\n\n"
    "6. Suspek mendakwa beliau bekerja di KDN, Putrajaya dalam profil Facebooknya. Saya juga mempunyai bukti "
    "transaksi berjumlah RM2,083.00 yang dipindahkan ke akaun suspek dan akaun keldai (MOHAMMAD HILMI, BSN)."
)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "nama": "", "ic": "", "tel": "", "alamat": "", "kerugian": "", "kronologi": TEKS_DEFAULT
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if "data_tersimpan" not in st.session_state:
    st.session_state.data_tersimpan = load_data()

# ==========================================
# UI UTAMA
# ==========================================
st.title("🕵️‍♂️ Sistem Siasatan Penipu (Mega UI)")
st.markdown("---")

with st.sidebar:
    st.header("🎯 Profil Sasaran (Suspek)")
    st.error(f"**Nama:** {NAMA_SUSPEK}")
    st.warning(f"**Tel:** {NOMOR_SUSPEK}")
    st.markdown(f"💬 [Buka WhatsApp](https://wa.me/{NOMOR_WA})")
    st.info(f"**Email:** {EMAIL_SUSPEK}")
    st.success(f"**Baki Hutang:** {BAKI_HUTANG}")
    st.info(f"**Kerja (FB):** {KERJA_FB}")
    st.markdown("---")
    st.success("**Media Sosial:**")
    st.markdown(f"📱 [TikTok (@{USERNAME_TIKTOK})](https://www.tiktok.com/@{USERNAME_TIKTOK})")
    st.markdown(f"📘 [Facebook (Adisprinter)]({LINK_FB})")
    st.markdown(f"📸 [Gambar Facebook]({LINK_FB_PHOTOS})")
    st.markdown(f"🎤 [Smule (@{USERNAME_SMULE})](https://www.smule.com/{USERNAME_SMULE})")
    st.markdown("---")
    st.warning(f"🚗 **Plat Kereta:** {PLAT_KERETA}")
    st.warning(f"🏍️ **Plat Motor:** {PLAT_MOTOR}")
    st.info(f"📍 **Check-in FB:** {CHECK_IN}")
    st.info(f"📝 **Caption FB:** '{CAPTION_FB}'")
    st.markdown("---")
    st.error("👥 **KAWAN RAPAT / KONTAK**")
    for kawan in KAWAN_RAPAT:
        st.markdown(f"- {kawan}")
    st.markdown("---")
    st.error("🚨 **KELDAI AKAUN (MULE)**")
    st.code(f"Nama : {NAMA_MULE}\nBank : {BANK_MULE}\nAkaun: {AKAUN_MULE}")

# Tab Navigation
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📄 Laporan & Aduan", "🔍 Carian OSINT", "🗺️ Peta Lokasi", "📧 Carian Email & Data", "🚗 Kenderaan Suspek", "📁 Bukti & Gambar"
])

# --- TAB 1: BUAT LAPORAN PDF & ADUAN ---
with tab1:
    st.header("Jana Laporan Polis")
    st.write("Masukkan maklumat anda di bawah. Anda boleh edit teks kronologi mengikut kes anda sendiri sebelum jana PDF.")
    
    # BUTANG TELEGRAM
    st.info("💡 Anda boleh lihat semua bukti (gambar, resit, chat) di channel Telegram kami.")
    st.link_button("📢 Buka Channel Telegram Bukti", "https://t.me/+2M7Vwt8K3lQwYzE1", type="primary")
    st.markdown("---")
    
    if os.path.exists(DATA_FILE):
        st.success("✅ Data draf sebelum ini telah dimuatkan secara automatik dari fail simpanan.")

    data = st.session_state.data_tersimpan
    if "pengadu_nama" not in st.session_state: st.session_state.pengadu_nama = data["nama"]
    if "pengadu_ic" not in st.session_state: st.session_state.pengadu_ic = data["ic"]
    if "pengadu_tel" not in st.session_state: st.session_state.pengadu_tel = data["tel"]
    if "pengadu_alamat" not in st.session_state: st.session_state.pengadu_alamat = data["alamat"]
    if "pengadu_kerugian" not in st.session_state: st.session_state.pengadu_kerugian = data["kerugian"]
    if "kronologi_teks" not in st.session_state: st.session_state.kronologi_teks = data["kronologi"]

    nama_pengadu = st.text_input("Nama Penuh Anda (Pengadu)", key="pengadu_nama")
    ic_pengadu = st.text_input("No. IC Anda", key="pengadu_ic")
    tel_pengadu = st.text_input("No. Telefon Anda", key="pengadu_tel")
    alamat_pengadu = st.text_area("Alamat Penuh Anda", key="pengadu_alamat")
    jumlah_kerugian = st.text_input("Jumlah Kerugian (cth: RM 2,083.00)", key="pengadu_kerugian")
    
    st.markdown("### 📝 Teks Kronologi (Boleh Edit)")
    st.info("Sila edit atau tambah ayat di dalam kotak ini mengikut kes anda.")
    
    kronologi_edit = st.text_area("Kronologi Kejadian:", key="kronologi_teks", height=320)

    col_btn1, col_btn2, col_space = st.columns([1, 1, 2])
    with col_btn1:
        btn_save = st.button("💾 SAVE Draf", type="primary", use_container_width=True)
    with col_btn2:
        btn_reset = st.button("🔄 Reset ke Teks Asal", use_container_width=True)

    if btn_save:
        new_data = {
            "nama": st.session_state.pengadu_nama, "ic": st.session_state.pengadu_ic,
            "tel": st.session_state.pengadu_tel, "alamat": st.session_state.pengadu_alamat,
            "kerugian": st.session_state.pengadu_kerugian, "kronologi": st.session_state.kronologi_teks
        }
        save_data(new_data)
        st.session_state.data_tersimpan = new_data
        st.success("✅ Draf berjaya disimpan ke fail! Data ini akan kekal walaupun anda refresh page.")

    if btn_reset:
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        st.session_state.pengadu_nama = ""
        st.session_state.pengadu_ic = ""
        st.session_state.pengadu_tel = ""
        st.session_state.pengadu_alamat = ""
        st.session_state.pengadu_kerugian = ""
        st.session_state.kronologi_teks = TEKS_DEFAULT
        st.success("🔄 Draf telah di-reset ke teks asal.")

    st.markdown("---")
    if st.button("📥 Jana Laporan PDF Utama", type="secondary"):
        if not nama_pengadu or not ic_pengadu:
            st.error("Sila isi Nama dan No. IC anda dahulu!")
        else:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)

            pdf.set_font("Helvetica", "B", 16)
            pdf.cell(0, 10, "LAPORAN POLIS (DRAF PENGADU)", new_x="LMARGIN", new_y="NEXT", align="C")
            pdf.ln(8)

            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, "A. MAKLUMAT PENGADU", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 11)

            pdf.cell(35, 8, "Nama", new_x="RIGHT", new_y="TOP")
            pdf.cell(0, 8, f": {nama_pengadu}", new_x="LMARGIN", new_y="NEXT")
            pdf.cell(35, 8, "No. IC", new_x="RIGHT", new_y="TOP")
            pdf.cell(0, 8, f": {ic_pengadu}", new_x="LMARGIN", new_y="NEXT")
            pdf.cell(35, 8, "No. Telefon", new_x="RIGHT", new_y="TOP")
            pdf.cell(0, 8, f": {tel_pengadu}", new_x="LMARGIN", new_y="NEXT")
            pdf.cell(35, 8, "Alamat", new_x="RIGHT", new_y="TOP")
            pdf.multi_cell(0, 8, f": {alamat_pengadu}", new_x="LMARGIN", new_y="NEXT")
            pdf.cell(35, 8, "Jumlah Kerugian", new_x="RIGHT", new_y="TOP")
            pdf.cell(0, 8, f": {jumlah_kerugian}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(5)

            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, "B. MAKLUMAT SUSPEK & KELDAI AKAUN", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 11)

            suspek_data = [
                ("Suspek Utama", NAMA_SUSPEK), ("No. Telefon", NOMOR_SUSPEK), ("Email", EMAIL_SUSPEK),
                ("TikTok", f"@{USERNAME_TIKTOK}"), ("Facebook", LINK_FB), ("Smule", USERNAME_SMULE),
                ("Kerja (FB)", KERJA_FB), ("Plat Kereta", PLAT_KERETA), ("Plat Motor", PLAT_MOTOR),
                ("Check-in FB", CHECK_IN), ("Caption FB", f"'{CAPTION_FB}'"),
                ("Keldai Akaun", f"{NAMA_MULE} ({BANK_MULE})"), ("No. Akaun", AKAUN_MULE),
            ]
            for label, value in suspek_data:
                pdf.cell(40, 8, label, new_x="RIGHT", new_y="TOP")
                pdf.multi_cell(0, 8, f": {value}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(5)

            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, "C. RANGKAIAN SOSIAL (KAWAN RAPAT)", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 8, "Berdasarkan komen Facebook, suspek mempunyai hubungan rapat dengan individu berikut:", new_x="LMARGIN", new_y="NEXT")
            for kawan in KAWAN_RAPAT:
                pdf.cell(0, 8, f"   - {kawan}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(5)

            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, "D. KRONOLOGI KEJADIAN", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 8, kronologi_edit, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(5)

            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, "E. LAMPIRAN BUKTI", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 11)
            lampiran = [
                "1. [ ] Tangkapan skrin transaksi (Touch 'n Go / DuitNow).",
                "2. [ ] Tangkapan skrin perbualan WhatsApp (Pengakuan hutang).",
                "3. [ ] Tangkapan skrin profil TikTok, Facebook, Smule, gambar kereta & motor.",
                "4. [ ] Tangkapan skrin tag GetContact (80 tag aduan).",
                "5. [ ] Tangkapan skrin komen FB kawan rapat.",
                "6. [ ] Tangkapan skrin maklumat kenderaan & kerja (KDN).",
            ]
            for item in lampiran:
                pdf.multi_cell(0, 8, item, new_x="LMARGIN", new_y="NEXT")

            pdf.ln(10)
            pdf.set_font("Helvetica", "I", 10)
            pdf.multi_cell(0, 8, "Saya bersumpah bahawa maklumat yang diberikan adalah benar.", new_x="LMARGIN", new_y="NEXT")

            pdf.ln(15)
            pdf.set_font("Helvetica", "", 11)
            pdf.cell(0, 10, "Tandatangan Pengadu: _____________________", new_x="LMARGIN", new_y="NEXT")
            pdf.cell(0, 10, f"Nama: {nama_pengadu}", new_x="LMARGIN", new_y="NEXT")
            pdf.cell(0, 10, f"Tarikh: {datetime.datetime.now().strftime('%d/%m/%Y')}", new_x="LMARGIN", new_y="NEXT")

            pdf_bytes = pdf.output()

            st.download_button(
                label="📥 Klik Sini Untuk Download Laporan Utama",
                data=bytes(pdf_bytes),
                file_name=f"Laporan_Polis_{nama_pengadu.replace(' ', '_')}.pdf",
                mime="application/pdf",
            )
            st.success("✅ Laporan Utama berjaya dijana!")

# --- TAB 6: BUKTI & GAMBAR (UPLOAD & JANA PDF) ---
with tab6:
    st.header("Muat Naik Bukti & Jana PDF")
    st.write("Anda boleh upload gambar (resit, chat, atau bukti lain) dan jadikannya satu fail PDF untuk diserahkan kepada polis.")
    
    uploaded_files = st.file_uploader(
        "Pilih gambar bukti (Boleh pilih lebih dari satu)", 
        type=["jpg", "jpeg", "png"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} gambar telah berjaya dimuat naik.")
        
        # Preview gambar
        cols = st.columns(3)
        for idx, file in enumerate(uploaded_files):
            img = Image.open(file)
            with cols[idx % 3]:
                st.image(img, caption=f"Gambar {idx+1}", use_container_width=True)

        # Butang untuk jana PDF bukti
        if st.button("📄 Jana PDF Bukti", type="primary"):
            pdf = FPDF()
            
            for idx, file in enumerate(uploaded_files):
                # Buat page baru untuk setiap gambar
                pdf.add_page()
                
                # Simpan gambar sementara
                img = Image.open(file)
                img_path = f"temp_img_{idx}.jpg"
                img = img.convert("RGB") # Pastikan format RGB
                img.save(img_path, "JPEG")

                # Dapatkan saiz gambar dan page A4
                img_w, img_h = img.size
                page_w, page_h = 210, 297 # Saiz A4 (mm)
                
                # Kira nisbah untuk fit gambar dalam page
                ratio = min((page_w - 20) / img_w, (page_h - 20) / img_h)
                new_w = img_w * ratio
                new_h = img_h * ratio
                
                # Letak gambar di tengah
                x = (page_w - new_w) / 2
                y = (page_h - new_h) / 2
                
                pdf.image(img_path, x=x, y=y, w=new_w, h=new_h)
                
                # Padam fail sementara
                os.remove(img_path)

            pdf_bytes = pdf.output()
            
            st.download_button(
                label="📥 Klik Sini Untuk Download Bukti (PDF)",
                data=bytes(pdf_bytes),
                file_name="Bukti_Kes_Penipu.pdf",
                mime="application/pdf",
            )
            st.success("✅ PDF Bukti berjaya dijana! Sila muat turun.")
