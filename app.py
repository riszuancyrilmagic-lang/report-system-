import streamlit as st
import datetime
import os
from fpdf import FPDF
import folium
from streamlit_folium import folium_static
import urllib.parse

# ==========================================
# KONFIGURASI UI
# ==========================================
st.set_page_config(page_title="Sistem Siasatan Penipu", page_icon="🕵️‍♂️", layout="wide")

# --- KOD UNTUK SOROKKAN BUTANG STREAMLIT (UI BERSIH) ---
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
# -------------------------------------------------------

# --- MAKLUMAT SUSPEK ---
NAMA_SUSPEK = "ABDUL HADI BIN MOHD NOR"
NOMOR_SUSPEK = "+601128065526"
NOMOR_WA = "601128065526"
EMAIL_SUSPEK = "boyspark641@gmail.com"
USERNAME_TIKTOK = "hadimarkno"
LINK_FB = "https://www.facebook.com/adisprinter"
LINK_FB_PHOTOS = "https://www.facebook.com/adisprinter/photos"
PLAT_KERETA = "WHG 8164"
PLAT_MOTOR = "WGG 4317" # Dikemaskini!
CHECK_IN = "Ipoh, Perak"
CAPTION_FB = "Hati aku hanya pada Perak"

NAMA_MULE = "MOHAMMAD HILMI BIN MOHD HANIF"
BANK_MULE = "Bank Simpanan Nasional (BSN)"
AKAUN_MULE = "0820041100050836"

# ==========================================
# UI UTAMA (STREAMLIT)
# ==========================================
st.title("🕵️‍♂️ Sistem Siasatan Penipu")
st.markdown("---")

# ================= SIDEBAR =================
with st.sidebar:
    st.header("🎯 Profil Sasaran (Suspek)")
    
    st.error(f"**Nama:** {NAMA_SUSPEK}")
    st.warning(f"**Tel:** {NOMOR_SUSPEK}")
    st.markdown(f"💬 [Buka WhatsApp](https://wa.me/{NOMOR_WA})")
    st.info(f"**Email:** {EMAIL_SUSPEK}")
    
    st.success("**Media Sosial:**")
    st.markdown(f"📱 [TikTok (@{USERNAME_TIKTOK})](https://www.tiktok.com/@{USERNAME_TIKTOK})")
    st.markdown(f"📘 [Facebook (Adisprinter)]({LINK_FB})")
    st.markdown(f"📸 [Gambar Facebook]({LINK_FB_PHOTOS})")
    
    st.markdown("---")
    st.warning(f"🚗 **Plat Kereta:** {PLAT_KERETA}")
    st.warning(f"🏍️ **Plat Motor:** {PLAT_MOTOR}")
    st.info(f"📍 **Check-in FB:** {CHECK_IN}")
    st.success(f"💬 **Caption FB:** '{CAPTION_FB}'")
    
    st.markdown("---")
    st.error("🚨 **KELDAI AKAUN (MULE)**")
    st.code(f"Nama : {NAMA_MULE}\nBank : {BANK_MULE}\nAkaun: {AKAUN_MULE}")
# ==========================================

# Tab Navigation
tab1, tab2, tab3, tab4 = st.tabs(["📄 Laporan & Aduan", "🔍 Carian OSINT (Deep Web)", "🗺️ Peta Lokasi", "📧 Carian Email & Data"])

# --- TAB 1: BUAT LAPORAN PDF & ADUAN ---
with tab1:
    st.header("Laporan Polis")
    st.write("Masukkan maklumat anda di bawah. Anda boleh edit teks kronologi mengikut kes anda sendiri sebelum jana PDF.")
    
    nama_pengadu = st.text_input("Nama Penuh Anda (Pengadu)")
    ic_pengadu = st.text_input("No. IC Anda")
    tel_pengadu = st.text_input("No. Telefon Anda")
    alamat_pengadu = st.text_area("Alamat Penuh Anda")
    
    st.markdown("### 📝 Teks Kronologi (Boleh Edit)")
    st.info("Sila edit atau tambah ayat di dalam kotak ini mengikut kes anda.")
    
    teks_default = (
        "1. Saya mengenali suspek sebagai pelanggan perniagaan saya sejak awal tahun lepas. Beliau sering menawarkan projek dan perkhidmatan.\n\n"
        "2. KES PERTAMA (Pembuatan PC): Suspek menawarkan untuk membina PC dengan harga murah. Saya telah membuat pembayaran lebih RM500. Namun, sehingga kini PC tidak disiapkan, barang tidak diserahkan, dan wang tidak dipulangkan.\n\n"
        "3. KES KEDUA (Modal Perniagaan): Ketika menunggu PC, suspek meminta saya menampung modal RM1,500 untuk pelanggannya, dengan janji akan memulangkan modal beserta keuntungan. Suspek hanya membayar RM800 (RM500 keuntungan + RM300 modal). Baki hutang yang belum dijelaskan ialah RM1,443 (termasuk RM160 hutang servis game).\n\n"
        "4. Suspek telah MENGIKTIRAF beliau berhutang melalui aplikasi WhatsApp. Beliau menulis: 'Total baki aku hg belum settle RM1783'. Namun, beliau kini gagal membayar dan cuba mengelak.\n\n"
        "5. Saya juga mendapati suspek mempunyai pelbagai rekod digital yang mengaitkannya dengan kawasan Perak (Check-in Facebook di Ipoh, video TikTok di Sg Siput, tag 'Adi Ipoh' di GetContact, dan caption FB 'Hati aku hanya pada Perak'). Nombor telefon suspek juga telah ditag sebagai 'Penipu' oleh 80 mangsa lain. Saya juga mempunyai bukti gambar kenderaan suspek (Kereta: WHG 8164, Motor: WGG 4317)."
    )
    
    kronologi_edit = st.text_area("Kronologi Kejadian:", value=teks_default, height=300)
    
    if st.button("📥 Buat Laporan PDF", type="primary"):
        if not nama_pengadu or not ic_pengadu:
            st.error("Sila isi Nama dan No. IC anda dahulu!")
        else:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="LAPORAN POLIS (DRAF PENGADU)", ln=True, align='C')
            pdf.ln(10)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt="A. MAKLUMAT PENGADU", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.cell(200, 8, txt=f"   Nama        : {nama_pengadu}", ln=True)
            pdf.cell(200, 8, txt=f"   No. IC      : {ic_pengadu}", ln=True)
            pdf.cell(200, 8, txt=f"   No. Telefon : {tel_pengadu}", ln=True)
            pdf.multi_cell(0, 8, txt=f"   Alamat      : {alamat_pengadu}")
            pdf.ln(5)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt="B. MAKLUMAT SUSPEK & KELDAI AKAUN", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.cell(200, 8, txt=f"   Suspek Utama : {NAMA_SUSPEK}", ln=True)
            pdf.cell(200, 8, txt=f"   No. Telefon  : {NOMOR_SUSPEK}", ln=True)
            pdf.cell(200, 8, txt=f"   Email        : {EMAIL_SUSPEK}", ln=True)
            pdf.cell(200, 8, txt=f"   TikTok       : @{USERNAME_TIKTOK}", ln=True)
            pdf.cell(200, 8, txt=f"   Facebook     : {LINK_FB}", ln=True)
            pdf.cell(200, 8, txt=f"   Plat Kereta  : {PLAT_KERETA}", ln=True)
            pdf.cell(200, 8, txt=f"   Plat Motor   : {PLAT_MOTOR}", ln=True) 
            pdf.cell(200, 8, txt=f"   Check-in FB  : {CHECK_IN}", ln=True)
            pdf.cell(200, 8, txt=f"   Caption FB   : '{CAPTION_FB}'", ln=True)
            pdf.cell(200, 8, txt=f"   Keldai Akaun : {NAMA_MULE} ({BANK_MULE})", ln=True)
            pdf.cell(200, 8, txt=f"   No. Akaun    : {AKAUN_MULE}", ln=True)
            pdf.ln(5)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt="C. KRONOLOGI KEJADIAN", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 8, txt=kronologi_edit)
            pdf.ln(5)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt="D. LAMPIRAN BUKTI", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.cell(200, 8, txt="1. [ ] Tangkapan skrin transaksi (Touch 'n Go / DuitNow).", ln=True)
            pdf.cell(200, 8, txt="2. [ ] Tangkapan skrin perbualan WhatsApp (Pengakuan hutang).", ln=True)
            pdf.cell(200, 8, txt="3. [ ] Tangkapan skrin Profil TikTok, Facebook, Gambar Kereta & Motor.", ln=True)
            pdf.cell(200, 8, txt="4. [ ] Tangkapan skrin Tag/GetContact (80 tag aduan).", ln=True)
            
            pdf.ln(10)
            pdf.set_font("Arial", 'I', 10)
            pdf.multi_cell(0, 8, txt="Saya bersumpah bahawa maklumat yang diberikan adalah benar.")
            
            pdf.ln(15)
            pdf.cell(200, 10, txt="Tandatangan Pengadu: _____________________", ln=True)
            pdf.cell(200, 10, txt=f"Nama: {nama_pengadu}", ln=True)
            pdf.cell(200, 10, txt=f"Tarikh: {datetime.datetime.now().strftime('%d/%m/%Y')}", ln=True)
            
            pdf.output("Laporan_Polis_UI.pdf")
            
            with open("Laporan_Polis_UI.pdf", "rb") as f:
                st.download_button(
                    label="Klik Sini Untuk Download PDF",
                    data=f,
                    file_name=f"Laporan_Polis_{nama_pengadu}.pdf",
                    mime="application/pdf"
                )
            st.success("Laporan berjaya dijana! Sila semak PDF anda.")

    st.markdown("---")
    st.subheader("Pautan Aduan Segera & Pangkalan Data")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.link_button("🚨 NSRC 997 (Sekat Bank)", "https://nfcc.jpm.gov.my/")
    with col2:
        st.link_button("📞 Semak Mule PDRM", "https://semakmule.rmp.gov.my/")
    with col3:
        st.link_button("📧 Aduan MCMC", "https://aduan.mcmc.gov.my/")
    with col4:
        st.link_button("🔎 Truecaller (80 Tags)", f"https://www.truecaller.com/search/my/{NOMOR_SUSPEK.replace('+', '')}")

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
        st.link_button("🎵 Cari 'Boyspark Band' di FB", "https://www.facebook.com/search/top?q=Boyspark+Band")
        st.link_button("🚗 Semak Plat Kereta (WHG 8164)", "https://www.google.com/search?q=%22WHG+8164%22")
        st.link_button("🏍️ Semak Plat Motor (WGG 4317)", "https://www.google.com/search?q=%22WGG+4317%22")
        st.link_button("📍 Cari 'Ipoh, Perak' di Maps", "https://www.google.com/maps/search/Ipoh,+Perak")
            
    with col2:
        st.subheader("Jejak Keldai Akaun (Hilmi)")
        st.link_button("🏦 Cari Nama Hilmi di FB", f"https://www.facebook.com/search/top?q={urllib.parse.quote(NAMA_MULE)}")
        st.link_button("🔍 Cari Hilmi di Google", f"https://www.google.com/search?q=%22{urllib.parse.quote(NAMA_MULE)}%22")
        st.link_button("📞 Cari Info Nombor Suspek", f"https://www.truecaller.com/search/my/{NOMOR_SUSPEK.replace('+', '')}")
        st.link_button("🕵️‍♂️ Semak GetContact", f"https://getcontact.com/en/search?q={NOMOR_SUSPEK.replace('+', '')}")

# --- TAB 3: PETA LOKASI ---
with tab3:
    st.header("Peta Anggaran Lokasi")
    st.write("Peta ini menunjukkan kawasan tumpuan suspek berdasarkan siasatan (Sungai Siput / Kuala Kangsar).")
    
    m = folium.Map(location=[4.7735, 101.1000], zoom_start=11)
    folium.Marker(
        [4.7735, 101.1000], 
        popup="Kawasan Sasaran: Kuala Kangsar / Sg Siput",
        tooltip="Klik untuk info",
        icon=folium.Icon(color='red', icon='info-sign')
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

st.markdown("---")
st.caption("Sistem dibangunkan untuk tujuan siasatan sah. Sila bawa laporan ke balai polis untuk tindakan lanjut.")
