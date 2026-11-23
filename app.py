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

# --- MAKLUMAT SUSPEK (Maklumat Awam untuk diburu) ---
NAMA_SUSPEK = "ABDUL HADI BIN MOHD NOR"
NOMOR_SUSPEK = "+601128065526"
EMAIL_SUSPEK = "boyspark641@gmail.com"
USERNAME_TIKTOK = "hadimarkno"

NAMA_MULE = "MOHAMMAD HILMI BIN MOHD HANIF"
BANK_MULE = "Bank Simpanan Nasional (BSN)"
AKAUN_MULE = "0820041100050836"
BAKI_HUTANG = "RM 1,783.00"

# ==========================================
# UI UTAMA (STREAMLIT)
# ==========================================
st.title("🕵️‍♂️ Sistem Siasatan Penipu (Mega UI Final)")
st.markdown("---")

# Sidebar (Maklumat Suspek)
with st.sidebar:
    st.header("Profil Sasaran (Suspek)")
    st.error(f"**Nama:** {NAMA_SUSPEK}")
    st.warning(f"**Tel:** {NOMOR_SUSPEK}")
    st.info(f"**Email:** {EMAIL_SUSPEK}")
    st.success(f"**Baki Hutang:** {BAKI_HUTANG}")
    st.markdown("---")
    st.write("**Keldai Akaun (Mule):**")
    st.code(f"{NAMA_MULE}\n{BANK_MULE}\n{AKAUN_MULE}")

# Tab Navigation
tab1, tab2, tab3 = st.tabs(["📄 Jana Laporan & Aduan", "🔍 Carian OSINT (Deep Web)", "🗺️ Peta Lokasi"])

# --- TAB 1: JANA LAPORAN PDF & ADUAN ---
with tab1:
    st.header("Jana Laporan Polis")
    st.write("Masukkan maklumat anda di bawah untuk menjana draf laporan polis dalam format PDF.")
    
    # KOTAK INPUT MANUAL (Selamat, tiada data disimpan di web)
    nama_pengadu = st.text_input("Nama Penuh Anda (Pengadu)")
    ic_pengadu = st.text_input("No. IC Anda")
    tel_pengadu = st.text_input("No. Telefon Anda")
    alamat_pengadu = st.text_area("Alamat Penuh Anda")
    jumlah_kerugian = st.text_input("Jumlah Kerugian (cth: RM 2,083.00)")
    
    if st.button("📥 Jana Laporan PDF", type="primary"):
        if not nama_pengadu or not ic_pengadu:
            st.error("Sila isi Nama dan No. IC anda dahulu!")
        else:
            # Proses jana PDF
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
            pdf.cell(200, 8, txt=f"   Keldai Akaun : {NAMA_MULE} ({BANK_MULE})", ln=True)
            pdf.cell(200, 8, txt=f"   No. Akaun    : {AKAUN_MULE}", ln=True)
            pdf.ln(5)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt="C. KRONOLOGI & PENGAKUAN SUSPEK", ln=True)
            pdf.set_font("Arial", size=11)
            kronologi = (
                f"1. Saya telah membuat transaksi pindahan wang kepada suspek dan keldai akaunnya berjumlah {jumlah_kerugian}.\n"
                f"2. Suspek mengiktiraf berhutang baki {BAKI_HUTANG} melalui WhatsApp.\n"
                f"3. Suspek gagal membayar dan menyekat panggilan.\n"
                f"4. Nombor suspek ditag 'Penipu' oleh 80 mangsa lain."
            )
            pdf.multi_cell(0, 8, txt=kronologi)
            
            pdf.output("Laporan_Polis_UI.pdf")
            
            with open("Laporan_Polis_UI.pdf", "rb") as f:
                st.download_button(
                    label="Klik Sini Untuk Download PDF",
                    data=f,
                    file_name=f"Laporan_Polis_{nama_pengadu}.pdf",
                    mime="application/pdf"
                )
            st.success("Laporan berjaya dijana!")

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
        # Guna st.link_button supaya boleh dibuka di telefon
        st.link_button("🔎 Cari Email di Google", f"https://www.google.com/search?q=%22{urllib.parse.quote(EMAIL_SUSPEK)}%22")
        st.link_button("📱 Buka TikTok Suspek", f"https://www.tiktok.com/@{USERNAME_TIKTOK}")
        st.link_button("🎵 Cari 'Boyspark Band' di FB", "https://www.facebook.com/search/top?q=Boyspark+Band")
        st.link_button("☕ Cari 'Black Cafe Sg Siput' di Maps", "https://www.google.com/maps/search/Black+Cafe+Sungai+Siput")
            
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

st.markdown("---")
st.caption("Sistem dibangunkan untuk tujuan siasatan sah. Sila bawa laporan ke balai polis untuk tindakan lanjut.")
