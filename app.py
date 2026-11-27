import streamlit as st
import streamlit.components.v1 as components
import datetime
from fpdf import FPDF
import folium
from streamlit_folium import st_folium
import urllib.parse
import json
import os
from PIL import Image

# ==========================================
# KONFIGURASI UI
# ==========================================
st.set_page_config(page_title="Sistem Siasatan Penipu", page_icon="🕵️‍♂️", layout="wide")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton {display:none;}
            [data-testid="stStatusWidget"] {visibility: hidden;}
            [data-testid="stToolbar"] {visibility: hidden;}
            [data-testid="stDecoration"] {visibility: hidden;}
            .viewerBadge_container__1QSob {visibility: hidden !important;}
            
            @media (max-width: 768px) {
                .block-container {padding-left: 0.5rem !important; padding-right: 0.5rem !important;}
                [data-testid="stSidebar"] {min-width: 85vw !important; max-width: 85vw !important;}
                .stButton > button {width: 100% !important; font-size: 0.85rem !important;}
                .stTabs [data-baseweb="tab"] {font-size: 0.75rem !important; padding: 0.5rem 0.3rem !important;}
                h1 {font-size: 1.5rem !important;}
                h2 {font-size: 1.2rem !important;}
                h3 {font-size: 1.0rem !important;}
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ==========================================
# FONT UNICODE
# ==========================================
FONT_DIRS = ["fonts", "/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/dejavu", "/Library/Fonts", "C:\\Windows\\Fonts"]

def _find_font(*filenames):
    for d in FONT_DIRS:
        for fn in filenames:
            p = os.path.join(d, fn)
            if os.path.exists(p):
                return p
    return None

def add_unicode_font(pdf):
    regular = _find_font("DejaVuSans.ttf", "arial.ttf", "Arial.ttf", "calibri.ttf")
    bold    = _find_font("DejaVuSans-Bold.ttf", "arialbd.ttf", "Arial Bold.ttf", "calibrib.ttf")
    italic  = _find_font("DejaVuSans-Oblique.ttf", "ariali.ttf", "Arial Italic.ttf", "calibrii.ttf")

    if not regular:
        raise FileNotFoundError("Font Unicode tidak dijumpai. Sila letak 'DejaVuSans.ttf' dalam folder 'fonts/'.")

    pdf.add_font("DejaVu", "", regular)
    pdf.add_font("DejaVu", "B", bold if bold else regular)
    pdf.add_font("DejaVu", "I", italic if italic else regular)

def set_font(pdf, style="", size=10):
    pdf.set_font("DejaVu", style, size)

# ==========================================
# BACAAN SUARA (Teks-ke-Suara pelayar)
# Percuma, tiada had aksara, tiada API/duit.
# ==========================================
def baca_suara_ui(nama, ic, tel, alamat, kerugian, kron_polis, kron_mahkamah):
    data = {
        "nama": nama or "",
        "ic": ic or "",
        "tel": tel or "",
        "alamat": alamat or "",
        "kerugian": kerugian or "",
        "polis": kron_polis or "",
        "mahkamah": kron_mahkamah or "",
    }
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

    html_code = r"""
    <style>
      .tts{font-family:system-ui,-apple-system,'Segoe UI',sans-serif;color:#0f172a}
      .tts .row{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}
      .tts button{cursor:pointer;border:0;border-radius:10px;padding:10px 14px;font-size:14px;font-weight:600}
      .tts .play{background:#1d4ed8;color:#fff}
      .tts .stop{background:#b91c1c;color:#fff}
      .tts .ghost{background:#e2e8f0;color:#0f172a}
      .tts textarea{width:100%;min-height:90px;border-radius:10px;border:1px solid #cbd5e1;padding:10px;font:inherit}
      .tts .note{font-size:12px;color:#475569;margin-top:8px}
      .tts .status{font-size:13px;font-weight:600;color:#1d4ed8;margin-top:8px;min-height:18px}
    </style>
    <div class="tts">
      <div class="row">
        <button class="play" id="b-polis">🔊 Baca Kronologi Polis</button>
        <button class="play" id="b-mahkamah">🔊 Baca Kronologi Mahkamah</button>
        <button class="stop" id="b-henti">⏹ Henti</button>
      </div>
      <div class="row">
        <textarea id="teks-bebas" placeholder="Tampal apa-apa teks di sini (chat WhatsApp, mesej suspek, nota) untuk dibaca…"></textarea>
      </div>
      <div class="row">
        <button class="ghost" id="b-teks">🔊 Baca teks ini</button>
      </div>
      <div class="status" id="tts-status"></div>
      <div class="note">Percuma dan tiada had aksara. Suara dibaca oleh enjin Teks-ke-Suara dalam pelayar/peranti anda. Bacaan berhenti sendiri bila teks habis.</div>
    </div>
    <script>
    var DATA = __DATA__;
    var synth = window.speechSynthesis;
    var statusEl = document.getElementById('tts-status');
    var queue = [];
    var idx = 0;

    function speakable(t){
      return String(t || '')
        .replace(/(\d),(?=\d{3})/g, '$1')
        .replace(/\bRM\s*/gi, 'Ringgit ')
        .replace(/\bNo\.\s*/gi, 'Nombor ')
        .replace(/&/g, ' dan ')
        .replace(/[•·►▶]/g, ', ')
        .replace(/[ \t]+/g, ' ')
        .trim();
    }

    function laporan(kind){
      var isPolis = (kind === 'polis');
      var kron = isPolis ? DATA.polis : DATA.mahkamah;
      if(!kron || !kron.trim()){
        statusEl.textContent = isPolis ? 'Isi Kronologi Polis dahulu.' : 'Isi Kronologi Mahkamah dahulu.';
        return '';
      }
      var rows = [isPolis ? 'Laporan Polis berkenaan kes penipuan.' : 'Laporan Mahkamah berkenaan tuntutan balik wang.'];
      if(DATA.nama) rows.push('Nama pengadu: ' + DATA.nama + '.');
      if(DATA.ic) rows.push('Nombor kad pengenalan: ' + DATA.ic + '.');
      if(DATA.tel) rows.push('Nombor telefon: ' + DATA.tel + '.');
      if(DATA.alamat) rows.push('Alamat: ' + DATA.alamat + '.');
      if(DATA.kerugian) rows.push('Jumlah kerugian: ' + DATA.kerugian + '.');
      rows.push(kron);
      return rows.join('. ');
    }

    function pecah(text, max){
      var bersih = String(text).replace(/\s+/g, ' ').trim();
      var out = [];
      var rest = bersih;
      while(rest.length > max){
        var cut = Math.max(rest.lastIndexOf('. ', max), rest.lastIndexOf('? ', max), rest.lastIndexOf('! ', max));
        if(cut < max * 0.4) cut = rest.lastIndexOf(' ', max);
        if(cut <= 0) cut = max;
        out.push(rest.slice(0, cut + 1).trim());
        rest = rest.slice(cut + 1).trim();
      }
      if(rest) out.push(rest);
      return out;
    }

    function suaraMelayu(){
      var senarai = synth.getVoices() || [];
      for(var i = 0; i < senarai.length; i++){
        if(/^ms/i.test(senarai[i].lang)) return senarai[i];
      }
      return null;
    }

    function berhenti(){
      queue = [];
      idx = 0;
      try { synth.cancel(); } catch (e) {}
      statusEl.textContent = '';
    }

    function seterusnya(){
      if(idx >= queue.length){
        statusEl.textContent = '✅ Selesai.';
        return;
      }
      var u = new SpeechSynthesisUtterance(queue[idx]);
      var v = suaraMelayu();
      if(v){ u.voice = v; u.lang = v.lang; } else { u.lang = 'ms-MY'; }
      u.rate = 1.0;
      u.pitch = 1.0;
      u.onend = function(){ idx++; seterusnya(); };
      u.onerror = function(){ statusEl.textContent = 'Suara tidak tersedia pada peranti ini. Pasang suara Bahasa Melayu di tetapan sistem.'; };
      synth.speak(u);
    }

    function main(teks){
      var t = speakable(teks);
      if(!t) return;
      berhenti();
      queue = pecah(t, 180);
      idx = 0;
      statusEl.textContent = '🔊 Membaca…';
      seterusnya();
    }

    document.getElementById('b-polis').addEventListener('click', function(){ main(laporan('polis')); });
    document.getElementById('b-mahkamah').addEventListener('click', function(){ main(laporan('mahkamah')); });
    document.getElementById('b-teks').addEventListener('click', function(){
      var box = document.getElementById('teks-bebas');
      if(!box.value.trim()){ statusEl.textContent = 'Tampal atau taip teks dahulu.'; return; }
      main(box.value);
    });
    document.getElementById('b-henti').addEventListener('click', berhenti);
    if(synth && typeof synth.getVoices === 'function'){ synth.getVoices(); }
    </script>
    """
    html_code = html_code.replace("__DATA__", payload)
    components.html(html_code, height=330, scrolling=False)


# ==========================================
# SISTEM LOG MASUK
# ==========================================
def check_password():
    def password_entered():
        correct_password = "Along123"
        if st.session_state["password"] == correct_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔒 Sistem Siasatan Penipu")
        st.info("Sila masukkan kata laluan untuk mengakses sistem ini.")
        st.text_input("Kata Laluan", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.title("🔒 Sistem Siasatan Penipu")
        st.text_input("Kata Laluan", type="password", on_change=password_entered, key="password")
        st.error("😕 Kata laluan salah. Sila cuba lagi.")
        return False
    else:
        return True

if check_password():
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

    NAMA_MULE = "MOHAMMAD HILMI BIN MOHD HANIF"
    BANK_MULE = "Bank Simpanan Nasional (BSN)"
    AKAUN_MULE = "0820041100050836"
    BAKI_HUTANG = "RM 1,783.00"

    KENDERAAN_1 = {
        "plat": "WHG 8164", "nama": "MOHAMAD SYAFIQ B BADRUL HISHAM",
        "ic": "020114081039", "alamat": "NO 14 RUMAH AWAM 5, JLN KENAS, 33000 PERAK",
        "model": "PROTON SATRIA 1.4 GLI M", "status": "1 Rekod Kemalangan"
    }
    KENDERAAN_2 = {
        "plat": "WGG 4317", "nama": "MOHD FAZLIN BIN LAH",
        "ic": "740728085339", "alamat": "NO 18 LALUAN CHEPOR DAMAIN 12, 31200 PERAK",
        "model": "YAMAHA TZM 150", "status": "1 Rekod Kemalangan"
    }

    # ==========================================
    # SISTEM SIMPAN & LOAD DATA (JSON)
    # ==========================================
    DATA_FILE = "simpanan_laporan.json"

    def load_data():
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "nama": "", "ic": "", "tel": "", "alamat": "", "kerugian": "", 
            "kronologi_polis": "", "kronologi_mahkamah": ""
        }

    def save_data(data):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    if "data_tersimpan" not in st.session_state:
        st.session_state.data_tersimpan = load_data()

    # ==========================================
    # UI UTAMA
    # ==========================================
    st.title("🕵️‍♂️ Sistem Siasatan Penipu")
    st.markdown("---")

    # ==========================================
    # SIDEBAR
    # ==========================================
    with st.sidebar:
        if st.button("🚪 Log Keluar", type="primary", use_container_width=True):
            st.session_state["password_correct"] = False
            st.rerun()

        st.markdown("---")
        st.header("🎯 Profil Sasaran (Suspek)")

        with st.container(border=True):
            st.error(f"**Nama:** {NAMA_SUSPEK}")
            st.warning(f"**Tel:** {NOMOR_SUSPEK}")
            st.markdown(f"💬 [Buka WhatsApp](https://wa.me/{NOMOR_WA})")
            st.info(f"**Email:** {EMAIL_SUSPEK}")
            st.success(f"**Baki Hutang:** {BAKI_HUTANG}")

        with st.expander("📱 Media Sosial & Pekerjaan", expanded=False):
            st.info(f"**Kerja (FB):** {KERJA_FB}")
            st.markdown(f"📱 [TikTok (@{USERNAME_TIKTOK})](https://www.tiktok.com/@{USERNAME_TIKTOK})")
            st.markdown(f"📘 [Facebook (Adisprinter)]({LINK_FB})")
            st.markdown(f"📸 [Gambar Facebook]({LINK_FB_PHOTOS})")
            st.markdown(f"🎤 [Smule (@{USERNAME_SMULE})](https://www.smule.com/{USERNAME_SMULE})")

        with st.expander("🚗 Maklumat Kenderaan", expanded=False):
            st.warning(f"🚗 **Plat Kereta:** {PLAT_KERETA}")
            st.markdown(f"**Pemilik:** {KENDERAAN_1['nama']}")
            st.markdown(f"**IC:** {KENDERAAN_1['ic']}")
            st.markdown(f"**Alamat:** {KENDERAAN_1['alamat']}")
            st.markdown(f"**Model:** {KENDERAAN_1['model']}")
            st.markdown(f"**Status:** {KENDERAAN_1['status']}")

            st.markdown("---")

            st.warning(f"🏍️ **Plat Motor:** {PLAT_MOTOR}")
            st.markdown(f"**Pemilik:** {KENDERAAN_2['nama']}")
            st.markdown(f"**IC:** {KENDERAAN_2['ic']}")
            st.markdown(f"**Alamat:** {KENDERAAN_2['alamat']}")
            st.markdown(f"**Model:** {KENDERAAN_2['model']}")
            st.markdown(f"**Status:** {KENDERAAN_2['status']}")

        with st.expander("📍 Check-in & Caption FB", expanded=False):
            st.info(f"📍 **Check-in FB:** {CHECK_IN}")
            st.info(f"📝 **Caption FB:** '{CAPTION_FB}'")

        with st.expander("🚨 Keldai Akaun (Mule)", expanded=False):
            st.code(f"Nama : {NAMA_MULE}\nBank : {BANK_MULE}\nAkaun: {AKAUN_MULE}")

        with st.expander("🎵 Kaitan MVM Music", expanded=False):
            st.info("Individu 'Hadi' (Booking Artis)")
            st.write("Suspek mendakwa mempunyai kaitan dengan MVM Music. Saya mendapati dalam promosi rasmi MVM Music terdapat nama Hadi dengan nombor 016 217 3665 dan email mvm.hadi@gmail.com untuk urusan booking artis. Saya memohon pihak polis menyemak sama ada suspek mempunyai kaitan dengan individu ini atau sama ada suspek menyamar menggunakan identiti tersebut.")
            st.code("No. Tel: 016-217 3665\nEmail: mvm.hadi@gmail.com")

    # ==========================================
    # TABS
    # ==========================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📄 Laporan", "🔍 OSINT", "🗺️ Peta", "📧 Email", "📁 Bukti"])

    # --- TAB 1: BUAT LAPORAN PDF & ADUAN ---
    with tab1:
        st.header("Jana Laporan (Polis & Mahkamah)")
        st.write("Masukkan maklumat anda di bawah. Sila isi teks kronologi yang berasingan untuk Laporan Polis dan Laporan Mahkamah.")

        if os.path.exists(DATA_FILE):
            st.success("✅ Data draf sebelum ini telah dimuatkan secara automatik dari fail simpanan.")

        data = st.session_state.data_tersimpan
        if "pengadu_nama" not in st.session_state: st.session_state.pengadu_nama = data["nama"]
        if "pengadu_ic" not in st.session_state: st.session_state.pengadu_ic = data["ic"]
        if "pengadu_tel" not in st.session_state: st.session_state.pengadu_tel = data["tel"]
        if "pengadu_alamat" not in st.session_state: st.session_state.pengadu_alamat = data["alamat"]
        if "pengadu_kerugian" not in st.session_state: st.session_state.pengadu_kerugian = data["kerugian"]
        
        # Tambah state untuk dua kronologi berasingan
        if "kronologi_polis" not in st.session_state: st.session_state.kronologi_polis = data.get("kronologi_polis", "")
        if "kronologi_mahkamah" not in st.session_state: st.session_state.kronologi_mahkamah = data.get("kronologi_mahkamah", "")

        nama_pengadu = st.text_input("Nama Penuh Anda (Pengadu)", key="pengadu_nama")
        ic_pengadu = st.text_input("No. IC Anda", key="pengadu_ic")
        tel_pengadu = st.text_input("No. Telefon Anda", key="pengadu_tel")
        alamat_pengadu = st.text_area("Alamat Penuh Anda", key="pengadu_alamat")
        jumlah_kerugian = st.text_input("Jumlah Kerugian (cth: RM 2,083.00)", key="pengadu_kerugian")

        st.markdown("### 📝 Teks Kronologi (Boleh Edit)")
        
        # Dua kotak teks berasingan
        col_kron1, col_kron2 = st.columns(2)
        with col_kron1:
            st.warning("🚨 **Kronologi untuk Laporan Polis** (Fokus pada ugutan/gangguan/penipuan)")
            kronologi_polis = st.text_area("Kronologi Polis:", key="kronologi_polis", height=350)
        with col_kron2:
            st.info("⚖️ **Kronologi untuk Mahkamah** (Fokus pada aliran wang & hutang)")
            kronologi_mahkamah = st.text_area("Kronologi Mahkamah:", key="kronologi_mahkamah", height=350)

        # ==========================================
        # BACAAN SUARA (PERCUMA, TIADA HAD)
        # ==========================================
        st.markdown("### 🔊 Baca dengan Suara")
        st.caption("Tekan butang di bawah untuk mendengar kronologi anda. Percuma, tiada had aksara, dan tiada akaun diperlukan.")
        baca_suara_ui(nama_pengadu, ic_pengadu, tel_pengadu, alamat_pengadu, jumlah_kerugian, kronologi_polis, kronologi_mahkamah)

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            btn_save = st.button("💾 SAVE Draf", type="primary", use_container_width=True)
        with col_btn2:
            btn_reset = st.button("🔄 Reset", use_container_width=True)

        if btn_save:
            new_data = {
                "nama": st.session_state.pengadu_nama, "ic": st.session_state.pengadu_ic,
                "tel": st.session_state.pengadu_tel, "alamat": st.session_state.pengadu_alamat,
                "kerugian": st.session_state.pengadu_kerugian, 
                "kronologi_polis": st.session_state.kronologi_polis,
                "kronologi_mahkamah": st.session_state.kronologi_mahkamah
            }
            save_data(new_data)
            st.session_state.data_tersimpan = new_data
            st.success("✅ Draf berjaya disimpan ke fail!")

        if btn_reset:
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            for key in ["pengadu_nama", "pengadu_ic", "pengadu_tel", "pengadu_alamat", "pengadu_kerugian", "kronologi_polis", "kronologi_mahkamah"]:
                st.session_state[key] = ""
            st.success("🔄 Draf telah di-reset.")

        st.markdown("---")
        
        # Butang Jana PDF (Dua pilihan)
        col_pdf_polis, col_pdf_mahkamah = st.columns(2)

        with col_pdf_polis:
            if st.button("📥 Jana Laporan POLIS (PDF)", type="secondary", use_container_width=True):
                if not nama_pengadu or not ic_pengadu:
                    st.error("Sila isi Nama dan No. IC anda dahulu!")
                else:
                    try:
                        pdf = FPDF()
                        add_unicode_font(pdf)
                        pdf.add_page()
                        pdf.set_auto_page_break(auto=True, margin=15)
                        line_h = 6

                        set_font(pdf, "B", 14)
                        pdf.cell(0, 10, "LAPORAN POLIS (DRAF PENGADU)", align="C")
                        pdf.ln(8)

                        # Bahagian A
                        set_font(pdf, "B", 11)
                        pdf.cell(0, 8, "A. MAKLUMAT PENGADU")
                        pdf.ln(6)
                        set_font(pdf, "", 10)
                        pengadu_data = [("Nama", nama_pengadu), ("No. IC", ic_pengadu), ("No. Telefon", tel_pengadu), ("Alamat", alamat_pengadu)]
                        for label, value in pengadu_data:
                            pdf.cell(35, line_h, label); pdf.cell(4, line_h, ":"); pdf.multi_cell(0, line_h, str(value)); pdf.ln(2)
                        
                        pdf.ln(3)
                        # Bahagian B (Suspek)
                        set_font(pdf, "B", 11)
                        pdf.cell(0, 8, "B. MAKLUMAT SUSPEK")
                        pdf.ln(6)
                        set_font(pdf, "", 10)
                        suspek_data = [("Nama", NAMA_SUSPEK), ("No. Tel", NOMOR_SUSPEK), ("Email", EMAIL_SUSPEK)]
                        for label, value in suspek_data:
                            pdf.cell(35, line_h, label); pdf.cell(4, line_h, ":"); pdf.multi_cell(0, line_h, str(value)); pdf.ln(2)

                        pdf.ln(3)
                        # Bahagian C (Kronologi POLIS)
                        set_font(pdf, "B", 11)
                        pdf.cell(0, 8, "C. KRONOLOGI KEJADIAN (JENAYAH)")
                        pdf.ln(6)
                        set_font(pdf, "", 10)
                        pdf.multi_cell(0, line_h, kronologi_polis)
                        pdf.ln(4)

                        set_font(pdf, "I", 9)
                        pdf.multi_cell(0, line_h, "Saya bersumpah bahawa maklumat yang diberikan adalah benar.")
                        pdf.ln(10)
                        set_font(pdf, "", 10)
                        pdf.cell(0, line_h, "Tandatangan: _____________________")
                        pdf.ln(6)
                        pdf.cell(0, line_h, f"Tarikh: {datetime.datetime.now().strftime('%d/%m/%Y')}")

                        pdf_bytes = bytes(pdf.output())
                        st.download_button(label="📥 Download Laporan Polis", data=pdf_bytes, file_name=f"Laporan_Polis_{nama_pengadu.replace(' ', '_')}.pdf", mime="application/pdf", use_container_width=True)
                    except Exception as e:
                        st.error(f"❌ Ralat: {e}")

        with col_pdf_mahkamah:
            if st.button("⚖️ Jana Laporan MAHKAMAH (PDF)", type="secondary", use_container_width=True):
                if not nama_pengadu or not ic_pengadu:
                    st.error("Sila isi Nama dan No. IC anda dahulu!")
                else:
                    try:
                        pdf = FPDF()
                        add_unicode_font(pdf)
                        pdf.add_page()
                        pdf.set_auto_page_break(auto=True, margin=15)
                        line_h = 6

                        set_font(pdf, "B", 14)
                        pdf.cell(0, 10, "TUNTUTAN SIVIL (MAHKAMAH)", align="C")
                        pdf.ln(8)

                        # Bahagian A
                        set_font(pdf, "B", 11)
                        pdf.cell(0, 8, "A. MAKLUMAT PENGADU (PLAINTIFF)")
                        pdf.ln(6)
                        set_font(pdf, "", 10)
                        pengadu_data = [("Nama", nama_pengadu), ("No. IC", ic_pengadu), ("No. Telefon", tel_pengadu), ("Alamat", alamat_pengadu)]
                        for label, value in pengadu_data:
                            pdf.cell(35, line_h, label); pdf.cell(4, line_h, ":"); pdf.multi_cell(0, line_h, str(value)); pdf.ln(2)

                        pdf.ln(3)
                        # Bahagian B (Defendan)
                        set_font(pdf, "B", 11)
                        pdf.cell(0, 8, "B. MAKLUMAT DEFENDAN & KELDAI AKAUN")
                        pdf.ln(6)
                        set_font(pdf, "", 10)
                        suspek_data = [("Defendan", NAMA_SUSPEK), ("Keldai Akaun", f"{NAMA_MULE} ({BANK_MULE})"), ("No. Akaun", AKAUN_MULE)]
                        for label, value in suspek_data:
                            pdf.cell(35, line_h, label); pdf.cell(4, line_h, ":"); pdf.multi_cell(0, line_h, str(value)); pdf.ln(2)

                        pdf.ln(3)
                        # Bahagian C (Kronologi MAHKAMAH)
                        set_font(pdf, "B", 11)
                        pdf.cell(0, 8, "C. KRONOLOGI TRANSAKSI & HUTANG")
                        pdf.ln(6)
                        set_font(pdf, "", 10)
                        pdf.multi_cell(0, line_h, kronologi_mahkamah)
                        pdf.ln(4)

                        # Bahagian D (Tuntutan)
                        set_font(pdf, "B", 11)
                        pdf.cell(0, 8, "D. TUNTUTAN")
                        pdf.ln(6)
                        set_font(pdf, "", 10)
                        pdf.multi_cell(0, line_h, f"Saya menuntut bayaran balik sejumlah {jumlah_kerugian} daripada Defendan berserta kos guaman.")
                        
                        pdf.ln(10)
                        set_font(pdf, "", 10)
                        pdf.cell(0, line_h, "Tandatangan Plaintif: _____________________")
                        pdf.ln(6)
                        pdf.cell(0, line_h, f"Tarikh: {datetime.datetime.now().strftime('%d/%m/%Y')}")

                        pdf_bytes = bytes(pdf.output())
                        st.download_button(label="📥 Download Laporan Mahkamah", data=pdf_bytes, file_name=f"Tuntutan_Mahkamah_{nama_pengadu.replace(' ', '_')}.pdf", mime="application/pdf", use_container_width=True)
                    except Exception as e:
                        st.error(f"❌ Ralat: {e}")

        st.markdown("---")
        st.subheader("Pautan Aduan Segera & Pangkalan Data")
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("🚨 NSRC 997", "https://nfcc.jpm.gov.my/", use_container_width=True)
            st.link_button("📧 Aduan MCMC", "https://aduan.mcmc.gov.my/", use_container_width=True)
        with col2:
            st.link_button("📞 Semak Mule PDRM", "https://semakmule.rmp.gov.my/", use_container_width=True)
            st.link_button("🔎 Truecaller", f"https://www.truecaller.com/search/my/{NOMOR_SUSPEK.replace('+', '')}", use_container_width=True)

    # --- TAB 2: CARIAN OSINT ---
    with tab2:
        st.header("Carian OSINT (Open Source Intelligence)")
        st.write("Klik butang di bawah untuk membuka carian di tab baru.")

        st.subheader("Jejak Suspek (Hadi)")
        st.link_button("💬 Buka WhatsApp Suspek", f"https://wa.me/{NOMOR_WA}", use_container_width=True)
        st.link_button("🔎 Cari Email di Google", f"https://www.google.com/search?q=%22{urllib.parse.quote(EMAIL_SUSPEK)}%22", use_container_width=True)
        st.link_button("📱 Buka TikTok Suspek", f"https://www.tiktok.com/@{USERNAME_TIKTOK}", use_container_width=True)
        st.link_button("📘 Buka Profil Facebook (Adisprinter)", LINK_FB, use_container_width=True)
        st.link_button("📸 Buka Gambar Facebook (Photos)", LINK_FB_PHOTOS, use_container_width=True)
        st.link_button("🎤 Buka Akaun Smule", f"https://www.smule.com/{USERNAME_SMULE}", use_container_width=True)
        st.link_button("🎵 Cari 'Boyspark Band' di FB", "https://www.facebook.com/search/top?q=Boyspark+Band", use_container_width=True)
        st.link_button("🚗 Semak Plat Kereta (WHG 8164)", "https://www.google.com/search?q=%22WHG+8164%22", use_container_width=True)
        st.link_button("🏍️ Semak Plat Motor (WGG 4317)", "https://www.google.com/search?q=%22WGG+4317%22", use_container_width=True)
        st.link_button("📍 Cari 'Ipoh, Perak' di Maps", "https://www.google.com/maps/search/Ipoh,+Perak", use_container_width=True)

        st.markdown("---")
        st.subheader("Kaitan MVM Music")
        st.link_button("🎵 Cari MVM Music di Google", "https://www.google.com/search?q=MVM+Music+Puchong", use_container_width=True)
        st.link_button("🎤 Cari 'Hadi MVM Music'", "https://www.google.com/search?q=%22Hadi%22+%22MVM+Music%22", use_container_width=True)
        st.link_button("📞 Cari No. Tel MVM (016-217 3665)", "https://www.google.com/search?q=%22016-217+3665%22", use_container_width=True)

        st.markdown("---")
        st.subheader("Jejak Keldai Akaun")
        st.link_button("🏦 Cari Nama Hilmi di FB", f"https://www.facebook.com/search/top?q={urllib.parse.quote(NAMA_MULE)}", use_container_width=True)
        st.link_button("🔍 Cari Hilmi di Google", f"https://www.google.com/search?q=%22{urllib.parse.quote(NAMA_MULE)}%22", use_container_width=True)

    # --- TAB 3: PETA LOKASI ---
    with tab3:
        st.header("Peta Anggaran Lokasi")
        st.write("Peta ini menunjukkan kawasan tumpuan suspek berdasarkan siasatan (Sungai Siput / Kuala Kangsar).")
        m = folium.Map(location=[4.7735, 101.1000], zoom_start=11)
        folium.Marker(
            [4.7735, 101.1000], popup="Kawasan Sasaran: Kuala Kangsar / Sg Siput", tooltip="Klik untuk info", icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
        st_folium(m, use_container_width=True, height=400)

    # --- TAB 4: CARIAN EMAIL & DATA ---
    with tab4:
        st.header("Carian Email & Data Bocor")
        st.write("Klik butang di bawah untuk semak jejak email suspek.")
        email_encoded = urllib.parse.quote(EMAIL_SUSPEK)
        nama_encoded = urllib.parse.quote(NAMA_SUSPEK)

        st.subheader("Carian Emel")
        st.link_button("🔎 Cari Email di Google", f"https://www.google.com/search?q=%22{email_encoded}%22", use_container_width=True)
        st.link_button("📧 Semak Data Bocor (HIBP)", f"https://haveibeenpwned.com/account/{email_encoded}", use_container_width=True)
        st.link_button("📘 Cari Emel di Facebook", f"https://www.facebook.com/search/top?q={email_encoded}", use_container_width=True)

        st.markdown("---")
        st.subheader("Carian Nama & Bisnes")
        st.link_button("🔍 Cari Nama + Black Cafe", f"https://www.google.com/search?q=%22{nama_encoded}%22+%22Black+Cafe%22", use_container_width=True)
        st.link_button("🎵 Cari Nama + TikTok", f"https://www.google.com/search?q=%22{nama_encoded}%22+TikTok+OR+hadimarkno", use_container_width=True)
        st.link_button("🏢 Semak Pendaftaran SSM", "https://www.ssm-einfo.my/", use_container_width=True)

    # --- TAB 5: BUKTI & GAMBAR (UPLOAD & JANA PDF) ---
    with tab5:
        st.header("Muat Naik Bukti & Jana PDF")
        st.write("Anda boleh upload gambar (resit, chat, atau bukti lain) dan jadikannya satu fail PDF untuk diserahkan kepada polis.")

        uploaded_files = st.file_uploader("Pilih gambar bukti (Boleh pilih lebih dari satu)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} gambar telah berjaya dimuat naik.")

            cols = st.columns(2)
            for idx, file in enumerate(uploaded_files):
                img = Image.open(file)
                with cols[idx % 2]:
                    st.image(img, caption=f"Gambar {idx+1}", use_container_width=True)

            if st.button("📄 Jana PDF Bukti", type="primary", use_container_width=True):
                try:
                    pdf = FPDF()
                    add_unicode_font(pdf)

                    for idx, file in enumerate(uploaded_files):
                        pdf.add_page()

                        img = Image.open(file)
                        img_path = f"temp_img_{idx}.jpg"
                        img = img.convert("RGB")
                        img.save(img_path, "JPEG")

                        img_w, img_h = img.size
                        page_w, page_h = 210, 297

                        ratio = min((page_w - 20) / img_w, (page_h - 20) / img_h)
                        new_w = img_w * ratio
                        new_h = img_h * ratio

                        x = (page_w - new_w) / 2
                        y = (page_h - new_h) / 2

                        pdf.image(img_path, x=x, y=y, w=new_w, h=new_h)

                        os.remove(img_path)

                    pdf_bytes = bytes(pdf.output())

                    st.download_button(
                        label="📥 Download Bukti (PDF)",
                        data=pdf_bytes,
                        file_name="Bukti_Kes_Penipu.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    st.success("✅ PDF Bukti berjaya dijana! Sila muat turun.")
                except FileNotFoundError as e:
                    st.error(f"❌ {e}")
                except Exception as e:
                    st.error(f"❌ Ralat jana PDF Bukti: {e}")

    st.markdown("---")
    st.caption("Sistem dibangunkan untuk tujuan siasatan sah. Sila bawa laporan ke balai polis untuk tindakan lanjut.")
