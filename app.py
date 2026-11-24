import streamlit as st
import datetime
from fpdf import FPDF
import folium
from streamlit_folium import folium_static
import urllib.parse
import json
import os

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

# Fungsi load data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "nama": "", "ic": "", "tel": "", "alamat": "", "kerugian": "", "kronologi": TEKS_DEFAULT
    }

# Fungsi save data
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Load data ke dalam session_state masa mula-mula buka
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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 Laporan & Aduan", "🔍 Carian OSINT", "🗺️ Peta Lokasi", "📧 Carian Email & Data", "🚗 Kenderaan Suspek"
])

# --- TAB 1: BUAT LAPORAN PDF & ADUAN ---
with tab1:
    st.header("Jana Laporan Polis")
    st.write("Masukkan maklumat anda di bawah. Anda boleh edit teks kronologi mengikut kes anda sendiri sebelum jana PDF.")
    
    # Papar notifikasi jika ada data yang di-load dari fail
    if os.path.exists(DATA_FILE):
        st.success("✅ Data draf sebelum ini telah dimuatkan secara automatik dari fail simpanan.")
    
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        btn_save = st.button("💾 SAVE Draf (Kekal Walaupun Refresh)", type="primary", use_container_width=True)
    with col_btn2:
        btn_reset = st.button("🔄 Reset ke Teks Asal", use_container_width=True)

    # Logik untuk butang Save & Reset
    if btn_save:
        new_data = {
            "nama": st.session_state.get("pengadu_nama", ""),
            "ic": st.session_state.get("pengadu_ic", ""),
            "tel": st.session_state.get("pengadu_tel", ""),
            "alamat": st.session_state.get("pengadu_alamat", ""),
            "kerugian": st.session_state.get("pengadu_kerugian", ""),
            "kronologi": st.session_state.get("kronologi_teks", TEKS_DEFAULT)
        }
        save_data(new_data)
        st.session_state.data_tersimpan = new_data
        st.success("✅ Draf berjaya disimpan ke fail! Data ini akan kekal walaupun anda refresh page.")

    if btn_reset:
        # Padam fail simpanan dan reset input
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        st.session_state.pengadu_nama = ""
        st.session_state.pengadu_ic = ""
        st.session_state.pengadu_tel = ""
        st.session_state.pengadu_alamat = ""
        st.session_state.pengadu_kerugian = ""
        st.session_state.kronologi_teks = TEKS_DEFAULT
        st.success("🔄 Draf telah di-reset ke teks asal.")

    # Set default value untuk text input berdasarkan data_tersimpan (jika belum ada dalam session_state)
    data = st.session_state.data_tersimpan
    if "pengadu_nama" not in st.session_state: st.session_state.pengadu_nama = data["nama"]
    if "pengadu_ic" not in st.session_state: st.session_state.pengadu_ic = data["ic"]
    if "pengadu_tel" not in st.session_state: st.session_state.pengadu_tel = data["tel"]
    if "pengadu_alamat" not in st.session_state: st.session_state.pengadu_alamat = data["alamat"]
    if "pengadu_kerugian" not in st.session_state: st.session_state.pengadu_kerugian = data["kerugian"]
    if "kronologi_teks" not in st.session_state: st.session_state.kronologi_teks = data["kronologi"]

    st.markdown("---")
    nama_pengadu = st.text_input("Nama Penuh Anda (Pengadu)", key="pengadu_nama")
    ic_pengadu = st.text_input("No. IC Anda", key="pengadu_ic")
    tel_pengadu = st.text_input("No. Telefon Anda", key="pengadu_tel")
    alamat_pengadu = st.text_area("Alamat Penuh Anda", key="pengadu_alamat")
    jumlah_kerugian = st.text_input("Jumlah Kerugian (cth: RM 2,083.00)", key="pengadu_kerugian")
    
    st.markdown("### 📝 Teks Kronologi (Boleh Edit)")
    st.info("Sila edit atau tambah ayat di dalam kotak ini mengikut kes anda.")
    
    kronologi_edit = st.text_area("Kronologi Kejadian:", key="kronologi_teks", height=320)
    
    st.markdown("---")
    if st.button("📥 Jana Laporan PDF", type="secondary"):
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
                label="📥 Klik Sini Untuk Download PDF",
                data=bytes(pdf_bytes),
                file_name=f"Laporan_Polis_{nama_pengadu.replace(' ', '_')}.pdf",
                mime="application/pdf",
            )
            st.success("✅ Laporan berjaya dijana! Sila semak PDF anda.")

    st.markdown("---")
    st.subheader("Pautan Aduan Segera & Pangkalan Data")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.link_button("🚨 NSRC 997 (Sekat Bank)", "https://nfcc.jpm.gov.my/")
    with col2: st.link_button("📞 Semak Mule PDRM", "https://semakmule.rmp.gov.my/")
    with col3: st.link_button("📧 Aduan MCMC", "https://aduan.mcmc.gov.my/")
    with col4: st.link_button("🔎 Truecaller (80 Tags)", f"https://www.truecaller.com/search/my/{NOMOR_SUSPEK.replace('+', '')}")

# --- TAB 2: CARIAN OSINT ---
with tab2:
    st.header("Carian OSINT (Open Source Intelligence)")
    st.write("Klik butang di bawah untuk membuka carian di tab baru.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Jejak Suspek (Hadi)")
        st.link_button("💬 Buka WhatsApp Suspek", f"https://wa.me/{NOMOR_WA}")
        st.link_button("🔎 Cari Email di Google", f"https://www.google.com/search?q=%22{urllib.parse.quote(EMAIL_SUSPEK)}%22")
        st.link_button("📱 Buka TikTok Suspek", f"https://www.tiktok.com/@{USERNAME_TIKTOK}")
        st.link_button("📘 Buka Profil Facebook (Adisprinter)", LINK_FB)
        st.link_button("📸 Buka Gambar Facebook (Photos)", LINK_FB_PHOTOS)
        st.link_button("🎤 Buka Akaun Smule", f"https://www.smule.com/{USERNAME_SMULE}")
        st.link_button("🎵 Cari 'Boyspark Band' di FB", "https://www.facebook.com/search/top?q=Boyspark+Band")
        st.link_button("🚗 Semak Plat Kereta (WHG 8164)", "https://www.google.com/search?q=%22WHG+8164%22")
        st.link_button("🏍️ Semak Plat Motor (WGG 4317)", "https://www.google.com/search?q=%22WGG+4317%22")
        st.link_button("📍 Cari 'Ipoh, Perak' di Maps", "https://www.google.com/maps/search/Ipoh,+Perak")
    with col2:
        st.subheader("Jejak Keldai Akaun & Kawan")
        st.link_button("🏦 Cari Nama Hilmi di FB", f"https://www.facebook.com/search/top?q={urllib.parse.quote(NAMA_MULE)}")
        st.link_button("🔍 Cari Hilmi di Google", f"https://www.google.com/search?q=%22{urllib.parse.quote(NAMA_MULE)}%22")
        st.markdown("**Cari Kawan Rapat:**")
        for kawan in KAWAN_RAPAT:
            kawan_encoded = urllib.parse.quote(kawan)
            st.link_button(f"🔍 Cari {kawan} di FB", f"https://www.facebook.com/search/top?q={kawan_encoded}")

# --- TAB 3: PETA LOKASI ---
with tab3:
    st.header("Peta Anggaran Lokasi")
    st.write("Peta ini menunjukkan kawasan tumpuan suspek berdasarkan siasatan (Sungai Siput / Kuala Kangsar).")
    m = folium.Map(location=[4.7735, 101.1000], zoom_start=11)
    folium.Marker(
        [4.7735, 101.1000], popup="Kawasan Sasaran: Kuala Kangsar / Sg Siput", tooltip="Klik untuk info", icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    folium_static(m)

# --- TAB 4: CARIAN EMAIL & DATA ---
with tab4:
    st.header("Carian Email & Data Bocor")
    st.write("Klik butang di bawah untuk semak jejak email suspek.")
    email_encoded = urllib.parse.quote(EMAIL_SUSPEK)
    nama_encoded = urllib.parse.quote(NAMA_SUSPEK)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Carian Emel")
        st.link_button("🔎 Cari Email di Google", f"https://www.google.com/search?q=%22{email_encoded}%22")
        st.link_button("📧 Semak Data Bocor (HIBP)", f"https://haveibeenpwned.com/account/{email_encoded}")
        st.link_button("📘 Cari Emel di Facebook", f"https://www.facebook.com/search/top?q={email_encoded}")
    with col2:
        st.subheader("Carian Nama & Bisnes")
        st.link_button("🔍 Cari Nama + Black Cafe", f"https://www.google.com/search?q=%22{nama_encoded}%22+%22Black+Cafe%22")
        st.link_button("🎵 Cari Nama + TikTok", f"https://www.google.com/search?q=%22{nama_encoded}%22+TikTok+OR+hadimarkno")
        st.link_button("🏢 Semak Pendaftaran SSM", "https://www.ssm-einfo.my/")

# --- TAB 5: MAKLUMAT KENDERAAN ---
with tab5:
    st.header("Maklumat Kenderaan Disyaki")
    st.write("Maklumat ini diperoleh daripada semakan rekod pendaftaran kenderaan. Berguna untuk siasatan lanjut pihak polis.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"🚗 Kereta: {KENDERAAN_1['plat']}")
        st.info(f"**Pemilik Berdaftar:** {KENDERAAN_1['nama']}")
        st.warning(f"**No. IC:** {KENDERAAN_1['ic']}")
        st.write(f"**Alamat:** {KENDERAAN_1['alamat']}")
        st.write(f"**Model:** {KENDERAAN_1['model']}")
        st.error(f"**Status:** {KENDERAAN_1['status']}")
    with col2:
        st.subheader(f"🏍️ Motor: {KENDERAAN_2['plat']}")
        st.info(f"**Pemilik Berdaftar:** {KENDERAAN_2['nama']}")
        st.warning(f"**No. IC:** {KENDERAAN_2['ic']}")
        st.write(f"**Alamat:** {KENDERAAN_2['alamat']}")
        st.write(f"**Model:** {KENDERAAN_2['model']}")
        st.error(f"**Status:** {KENDERAAN_2['status']}")
    st.markdown("---")
    st.warning("**Nota Siasatan:** Pemilik kenderaan mungkin bukan suspek utama. Pihak polis perlu menyiasat sama ada kenderaan ini dijual, disewa, atau digunakan oleh suspek (ABDUL HADI).")

st.markdown("---")
st.caption("Sistem dibangunkan untuk tujuan siasatan sah. Sila bawa laporan ke balai polis untuk tindakan lanjut.")
