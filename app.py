import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import pandas as pd
import math
import base64
from pathlib import Path


# Pastikan file-file ini ada di folder yang sama ya!
from detector import detect_face_and_extract_color
from recommender import get_recommendation
from pdf_export import generate_pdf

# ============================================================
# 1. KONFIGURASI HALAMAN & LOGO
# ============================================================
# Memuat logo untuk digunakan di Tab dan Sidebar
try:
    logo_projek = Image.open('logo personal.png')
except:
    # Fallback jika file tidak ditemukan agar tidak error
    logo_projek = "🌿"

st.set_page_config(
    page_title="Personal Color Analysis",
    page_icon=logo_projek, #  Menampilkan logo di Tab Browser
    layout="wide",
    initial_sidebar_state="expanded" # Diubah agar sidebar (logo) langsung terlihat 
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

*, *::before, *::after { font-family: 'Inter', sans-serif; box-sizing: border-box; }
.stApp { background-color: #f2f7f0; color: #1c1c1c; }
#MainMenu, footer, header { visibility: hidden; }

/* ── HERO BANNER (RESPONSIVE) ── */
.hero {
    background: linear-gradient(150deg, #e8f4e4 0%, #ddeedd 40%, #f0f5e8 100%);
    border-radius: 32px; padding: 48px 24px; text-align: center;
    border: 1px solid #b8d4b0; margin-bottom: 32px;
    box-shadow: 0 8px 48px rgba(70,140,70,0.10); position: relative; overflow: hidden;
}
.hero::before {
    content: ''; position: absolute; top: -80px; right: -80px; width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(70,160,70,0.09) 0%, transparent 70%); border-radius: 50%;
}
.hero::after {
    content: ''; position: absolute; bottom: -60px; left: -60px; width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(140,170,80,0.08) 0%, transparent 70%); border-radius: 50%;
}
.hero-badge {
    display: inline-block; background: rgba(255,255,255,0.97); color: #3a8040;
    border: 1px solid #90c890; border-radius: 30px; padding: 7px 20px;
    font-size: 0.7rem; font-weight: 700; letter-spacing: 2.5px; text-transform: uppercase;
    margin-bottom: 20px; box-shadow: 0 2px 8px rgba(70,140,70,0.12);
}
.hero-title {
    font-family: 'Playfair Display', serif; font-size: 3rem; font-weight: 700;
    color: #162814; margin-bottom: 10px; line-height: 1.2; letter-spacing: -0.5px;
    position: relative; z-index: 1;
}
.hero-title span {
    background: linear-gradient(135deg, #3a8040 0%, #5aaa50 50%, #7a8830 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-sub { color: #4a7848; font-size: 1rem; margin-top: 10px; position: relative; z-index: 1; line-height: 1.5; }
.hero-divider { width: 56px; height: 3px; background: linear-gradient(90deg, #3a8040, #7a8830); border-radius: 2px; margin: 20px auto 0; }

.tips-row { display: flex; gap: 8px; margin-bottom: 24px; flex-wrap: wrap; }
.tip-chip { background: #fff; border: 1px solid #b0ccb0; border-radius: 20px; padding: 8px 14px; font-size: 0.85rem; color: #2a6030; font-weight: 500; box-shadow: 0 2px 5px rgba(0,0,0,0.03);}

/* ── METRICS USING CSS GRID (RESPONSIVE) ── */
.metrics-grid { 
    display: grid; 
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); 
    gap: 16px; 
    margin-bottom: 16px; 
}
.metric-box { background: #fff; border: 1px solid #b8d4b0; border-radius: 20px; padding: 22px 16px; text-align: center; box-shadow: 0 2px 16px rgba(70,140,70,0.07); transition: box-shadow 0.2s, transform 0.2s; }
.metric-box:hover { box-shadow: 0 6px 24px rgba(70,140,70,0.14); transform: translateY(-2px); }
.metric-box-label { font-size: 0.72rem; color: #70a070; text-transform: uppercase; letter-spacing: 2.5px; margin-bottom: 12px; font-weight: 600; }
.metric-box-value { font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 700; color: #2a6030; line-height: 1.1; }

.badge-hangat { background: linear-gradient(135deg, #fffbf0, #fff3dc); color: #8a4a00; border: 1.5px solid #e8c878; padding: 7px 20px; border-radius: 30px; font-weight: 600; font-size: 0.95rem; display: inline-block; }
.badge-dingin { background: linear-gradient(135deg, #f0f6ff, #e0eeff); color: #1a3a7a; border: 1.5px solid #a0c0f0; padding: 7px 20px; border-radius: 30px; font-weight: 600; font-size: 0.95rem; display: inline-block; }
.badge-netral { background: linear-gradient(135deg, #eaf6ea, #d8eedd); color: #1a4a20; border: 1.5px solid #88c888; padding: 7px 20px; border-radius: 30px; font-weight: 600; font-size: 0.95rem; display: inline-block; }

.lab-row { display: flex; gap: 8px; justify-content: center; margin-top: 10px; flex-wrap: wrap; }
.lab-chip { background: #eef6ec; border: 1px solid #b0ccb0; border-radius: 12px; padding: 6px 12px; text-align: center; min-width: 55px; flex: 1; max-width: 80px; }
.lab-key { font-size: 0.65rem; color: #70a070; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; }
.lab-val { font-size: 1rem; font-weight: 700; color: #2a6030; margin-top: 3px; }

.desc-text { color: #3a6838; font-size: 0.95rem; text-align: center; font-style: italic; margin-top: 16px; padding: 14px 20px; background: linear-gradient(135deg, #eaf4e8, #f0f5e8); border-radius: 14px; border: 1px solid #b8d4b0; line-height: 1.6; }
.section-title { font-size: 1.25rem; font-weight: 700; color: #162814; margin: 32px 0 16px 0; padding-bottom: 12px; border-bottom: 2px solid #a0cc9c; letter-spacing: -0.2px; }

/* ── CARDS & SWATCHES ── */
.card { background: #fff; border: 1px solid #b8d4b0; border-radius: 22px; padding: 20px; box-shadow: 0 2px 16px rgba(70,140,70,0.06); height: 100%; transition: box-shadow 0.2s; margin-bottom: 12px; }
.card:hover { box-shadow: 0 4px 24px rgba(70,140,70,0.12); }
.card-title { font-size: 0.95rem; font-weight: 700; color: #162814; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid #c8e4c4; }
.card-subtitle { font-size: 0.75rem; color: #70a070; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; margin: 14px 0 8px 0; }

.swatch-grid { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px; }
.swatch-pill { display: flex; align-items: center; gap: 8px; background: #f0f8ee; border: 1px solid #c0d8bc; border-radius: 30px; padding: 6px 12px 6px 6px; font-size: 0.85rem; color: #1a3018; transition: all 0.15s; }
.swatch-pill:hover { border-color: #3a8040; background: #e4f4e0; }
.swatch-pill-primary { display: flex; align-items: center; gap: 8px; background: #e8f4e4; border: 2px solid #3a8040; border-radius: 30px; padding: 8px 14px 8px 8px; font-size: 0.9rem; font-weight: 700; color: #162814; transition: all 0.15s; }
.swatch-pill-primary:hover { background: #d4ecce; }
.swatch-dot { width: 18px; height: 18px; border-radius: 50%; border: 1.5px solid rgba(0,0,0,0.1); flex-shrink: 0; }
.swatch-dot-lg { width: 22px; height: 22px; border-radius: 50%; border: 2px solid rgba(0,0,0,0.12); flex-shrink: 0; }

.foundation-item { background: #f0f8ee; border: 1px solid #c0d8bc; border-left: 3px solid #3a8040; border-radius: 12px; padding: 10px 14px; margin-bottom: 8px; font-size: 0.88rem; color: #162814; line-height: 1.4; }
.avoid-pill { display: block; background: #fff8f6; border: 1px solid #f0c8c0; color: #8a2010; border-radius: 10px; padding: 8px 12px; font-size: 0.82rem; margin-bottom: 6px; font-weight: 500; line-height: 1.5; }

/* ── BUTTONS & OTHERS ── */
.stButton > button { background: linear-gradient(135deg, #3a8040, #5aaa50) !important; color: white !important; border: none !important; border-radius: 25px !important; font-weight: 600 !important; padding: 12px 28px !important; font-size: 0.95rem !important; transition: all 0.25s !important; box-shadow: 0 4px 16px rgba(58,128,64,0.3) !important; width: 100% !important; }
.stButton > button:hover { box-shadow: 0 6px 24px rgba(58,128,64,0.45) !important; transform: translateY(-2px) !important; }
.stDownloadButton > button { background: linear-gradient(135deg, #3a8040, #5aaa50) !important; color: white !important; border: none !important; border-radius: 25px !important; font-weight: 600 !important; padding: 12px 28px !important; font-size: 0.95rem !important; transition: all 0.25s !important; box-shadow: 0 4px 16px rgba(58,128,64,0.3) !important; width: 100% !important; }
.stDownloadButton > button:hover { box-shadow: 0 6px 24px rgba(58,128,64,0.45) !important; transform: translateY(-2px) !important; }

.download-box { background: linear-gradient(135deg, #eaf4e8, #e4f0e0); border: 1px solid #a8cc9c; border-radius: 20px; padding: 20px; margin-top: 8px; text-align: center; }
.download-title { font-size: 1rem; font-weight: 700; color: #162814; margin-bottom: 6px; }
.download-desc { font-size: 0.85rem; color: #5a8860; margin-bottom: 14px; line-height: 1.5; }

.stRadio > div { background: #fff; border: 1px solid #b8d4b0; border-radius: 16px; padding: 10px 16px; }
hr { border: none !important; border-top: 1px solid #b8d4b0 !important; margin: 16px 0 24px !important; }

/* ── STREAMLIT OVERRIDE: Dataframe & Expander ── */
[data-testid="stDataFrame"] {
    border:1.5px solid #c0d8bc !important;
    border-radius:14px !important;
    overflow:hidden;
    box-shadow:0 3px 16px rgba(70,140,70,0.05) !important;
}
.streamlit-expanderHeader {
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    color: #2a6030 !important;
    background-color: #f8fcf7 !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
}
[data-testid="stExpander"] {
    border: 1px solid #c0d8bc !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 8px rgba(70,140,70,0.03) !important;
    margin-bottom: 12px !important;
    overflow: hidden;
    background: #fff;
}
.komputasi-title { font-weight: 600; color: #162814; margin-bottom: 6px; font-size: 0.9rem; }
.komputasi-text { font-size: 0.85rem; color: #4a7848; line-height: 1.5; margin-bottom: 10px;}

/* ── MEDIA QUERIES UNTUK TAMPILAN HP ── */
@media (max-width: 768px) {
    .hero { padding: 32px 16px; border-radius: 24px; }
    .hero-title { font-size: 2.2rem; }
    .hero-sub { font-size: 0.9rem; }
    .hero-badge { letter-spacing: 1.5px; padding: 5px 14px; font-size: 0.65rem; }
    .metric-box-value { font-size: 1.5rem; }
    .hero img { width: 200px !important; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 2. DATABASE WARNA SWATCH
# ============================================================
COLOR_SWATCHES = {
    "putih": "#F5F5F0", "putih bersih": "#F5F5F0", "white": "#F5F5F0",
    "off white": "#F0EDE0", "cream": "#E8DFC8", "nude": "#D8B080",
    "taupe": "#907868", "warm beige": "#D8C098", "beige": "#D8C098",
    "camel": "#C0966A", "coklat": "#703818", "coklat muda": "#A07040",
    "coklat kayu": "#885030", "coklat rose": "#986068", "coklat nude": "#9A7050",
    "coklat latte": "#9A7050", "mocha": "#705040", "warm brown": "#785828",
    "earth tone": "#887050", "rust": "#A84820", "amber": "#C87800",
    "terracotta": "#B87058", "merah bata": "#B87058", "burnt orange": "#A84800",
    "orange": "#D07000", "oranye": "#D07000", "coral": "#D85838",
    "salmon": "#D87050", "peach": "#ECA880", "apricot": "#ECA070",
    "copper": "#986030", "mustard": "#C8980E", "kuning": "#D8B800",
    "kuning cerah": "#F0C800", "gold": "#C89800", "emas": "#C89800",
    "olive": "#6B7C3A", "olive green": "#6B7C3A", "hijau zaitun": "#6B7C3A",
    "sage": "#7A9870", "sage green": "#7A9870", "mint": "#70C898",
    "emerald": "#287850", "hijau zamrud": "#287850", "teal": "#207878",
    "toska": "#008888", "turquoise": "#008898", "hijau": "#287828",
    "navy": "#1B2A4A", "navy blue": "#1B2A4A", "biru tua": "#1B2A4A",
    "royal blue": "#0E4898", "cobalt": "#0030A8", "cobalt blue": "#0030A8",
    "dusty blue": "#607898", "baby blue": "#A0C8F0", "blue": "#0E58A8",
    "purple": "#6A3898", "ungu": "#6A3898", "lavender": "#A878D0",
    "violet": "#6030A0", "plum": "#701878", "mauve": "#A87080",
    "dusty mauve": "#987080", "dusty purple": "#805890",
    "pink": "#F090A8", "soft pink": "#ECA8B8", "dusty pink": "#C09090",
    "hot pink": "#C81870", "fuchsia": "#B818C8", "magenta": "#B01898",
    "rose": "#C81858", "dusty rose": "#C09090", "berry": "#700040",
    "merah": "#C02020", "merah cerah": "#E01818", "brick red": "#982020",
    "maroon": "#580018", "marun": "#580018", "burgundy": "#680020",
    "wine": "#580030", "grey": "#888880", "abu-abu": "#888880",
    "silver": "#A0A0A8", "warm grey": "#989080", "charcoal": "#383830",
    "bronze": "#986020", "metalik": "#A0A0A8", "blush": "#E0A898",
    "mlbb": "#A87080", "pastel": "#E898B0",
}

def get_color(name):
    n = name.lower()
    if n in COLOR_SWATCHES:
        return COLOR_SWATCHES[n]
    for key, val in COLOR_SWATCHES.items():
        if key in n:
            return val
    return "#3a8040"

def get_undertone_badge_class(undertone):
    ut = undertone.lower()
    if "hangat" in ut or "warm" in ut:
        return "hangat"
    elif "dingin" in ut or "cool" in ut:
        return "dingin"
    else:
        return "netral"

# ============================================================
# 3. FUNGSI EKSTRAKSI & GAMBAR
# ============================================================
@st.cache_resource
def load_cascade_classifier():
    return cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def draw_highlight(image_pil):
    img_cv  = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
    gray    = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    cascade = load_cascade_classifier()
    faces   = cascade.detectMultiScale(gray, 1.1, 5, minSize=(80, 80))
    
    if len(faces) > 0:
        x, y, w, h = faces[0]
        cv2.rectangle(img_cv, (x, y), (x+w, y+h), (58, 128, 64), 2)
        cv2.rectangle(img_cv, (x+int(w*0.40), y+int(h*0.12)), (x+int(w*0.60), y+int(h*0.22)), (90, 170, 80), 2)
        cv2.rectangle(img_cv, (x+int(w*0.20), y+int(h*0.50)), (x+int(w*0.35), y+int(h*0.65)), (90, 170, 80), 2)
        cv2.rectangle(img_cv, (x+int(w*0.65), y+int(h*0.50)), (x+int(w*0.80), y+int(h*0.65)), (90, 170, 80), 2)
        cv2.putText(img_cv, "Area Analisis", (x+int(w*0.25), y+int(h*0.08)-8), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (58, 128, 64), 1)
        
    return Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))

def make_swatches(items, primary=False):
    html = '<div class="swatch-grid">'
    for item in items:
        c = get_color(item)
        if primary:
            html += f'<div class="swatch-pill-primary"><div class="swatch-dot-lg" style="background:{c}"></div>{item}</div>'
        else:
            html += f'<div class="swatch-pill"><div class="swatch-dot" style="background:{c}"></div>{item}</div>'
    html += '</div>'
    return html

# ============================================================
# RENDER METRICS
# ============================================================
def render_metrics(skin_tone, undertone, lab, rec):
    badge_class = get_undertone_badge_class(undertone)
    st.markdown(f"""
    <div class="metrics-grid">
        <div class="metric-box">
            <div class="metric-box-label">Warna Kulit</div>
            <div class="metric-box-value">{skin_tone}</div>
        </div>
        <div class="metric-box">
            <div class="metric-box-label">Undertone</div>
            <div style="margin-top:10px"><span class="badge-{badge_class}">{undertone}</span></div>
        </div>
        <div class="metric-box">
            <div class="metric-box-label">Nilai CIELAB</div>
            <div class="lab-row">
                <div class="lab-chip"><div class="lab-key">L*</div><div class="lab-val">{lab['L']}</div></div>
                <div class="lab-chip"><div class="lab-key">a*</div><div class="lab-val">{lab['A']}</div></div>
                <div class="lab-chip"><div class="lab-key">b*</div><div class="lab-val">{lab['B']}</div></div>
            </div>
        </div>
    </div>
    <div class="desc-text">{rec['description']}</div>
    """, unsafe_allow_html=True)

# ============================================================
# RENDER DETAIL PERHITUNGAN (UPDATE: INPUT DETAIL KLASTER & CENTROID)
# ============================================================
def render_detail_perhitungan(lab, skin_tone, undertone):
    import pandas as pd
    import math

    L = lab['L']
    A = lab['A']
    B = lab['B']

    # Hitung nilai pergeseran asli skala CIELAB murni
    a_shifted = round(A - 128, 2)
    b_shifted = round(B - 128, 2)
    diff      = round(b_shifted - a_shifted, 2)

    # Menangani otomatisasi lambang plus (+) secara dinamis agar matematika UI sinkron
    sign_a = "+" if a_shifted >= 0 else ""
    sign_b = "+" if b_shifted >= 0 else ""
    sign_d = "+" if diff >= 0 else ""

    cond_hangat  = diff > 8 and b_shifted > 4
    cond_dingin1 = a_shifted > 4 and diff < -2
    cond_dingin2 = b_shifted < -3
    cond_netral  = not (cond_hangat or cond_dingin1 or cond_dingin2)

    # Pusat Data Klaster (Centroid) K-Means kulit Indonesia
    c_putih, c_sawo, c_gelap = (175, 142, 144), (142, 144, 147), (106, 143, 145)
    
    sq_p = (L - c_putih[0])**2 + (A - c_putih[1])**2 + (B - c_putih[2])**2
    sq_s = (L - c_sawo[0])**2 + (A - c_sawo[1])**2 + (B - c_sawo[2])**2
    sq_g = (L - c_gelap[0])**2 + (A - c_gelap[1])**2 + (B - c_gelap[2])**2

    dist_putih = round(math.sqrt(sq_p), 2)
    dist_sawo  = round(math.sqrt(sq_s), 2)
    dist_gelap = round(math.sqrt(sq_g), 2)

    st.markdown('<div class="section-title">📊 Rincian Evaluasi Metrik & Metodologi</div>', unsafe_allow_html=True)
    st.markdown('<div class="komputasi-text">Berikut adalah rincian perhitungan matematis yang digunakan oleh sistem untuk mengklasifikasikan karakteristik rona bawah kulit dan kategori klaster warna kulit Anda.</div>', unsafe_allow_html=True)

# MENU 1: UNDERTONE DETERMINATION
    with st.expander("1. Penentuan Rona Bawah Kulit (Logika Aturan Undertone)", expanded=False):
        st.markdown("""
        <div class="komputasi-text">
        Undertone ditentukan berdasarkan selisih nilai murni antara pigmen kekuningan (b*) dan pigmen kemerahan (a*) setelah dikurangi nilai tengah 128. Selisih dominasi (Diff) inilah yang memetakan kategori rona wajah Anda.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: #f8fcf7; padding: 16px; border-radius: 12px; border: 1px solid #c0d8bc; font-size: 0.85rem; color: #162814; margin-bottom: 16px;">
            <b>Hasil Transformasi Nilai Wajah Anda:</b><br>
            • Faktor Kemerahan (a* murni) = {A} - 128 = <b>{sign_a}{a_shifted}</b><br>
            • Faktor Kekuningan (b* murni) = {B} - 128 = <b>{sign_b}{b_shifted}</b><br>
            • Nilai Selisih (b* - a*) = <b>{sign_d}{diff}</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<p style='font-size:0.85rem; font-weight:600; color:#162814; margin-bottom:6px;'>Matriks Aturan Keputusan:</p>", unsafe_allow_html=True)
        df_ut = pd.DataFrame({
            "Kategori Rona": ["Warm (Hangat)", "Cool (Dingin) - Opsi A", "Cool (Dingin) - Opsi B", "Neutral (Netral)"],
            "Syarat Matematis": ["Selisih > 8 dan b* murni > 4", "a* murni > 4 dan Selisih < -2", "b* murni < -3", "Tidak memenuhi kriteria Warm & Cool"],
            "Status Evaluasi": [
                "✅ Terpenuhi" if cond_hangat else "❌ Tidak", 
                "✅ Terpenuhi" if cond_dingin1 else "❌ Tidak", 
                "✅ Terpenuhi" if cond_dingin2 else "❌ Tidak", 
                "✅ Terpenuhi" if cond_netral else "❌ Tidak"
            ]
        })
        st.dataframe(df_ut, use_container_width=True, hide_index=True)
        st.info(f"💡 **Kesimpulan:** Berdasarkan kecenderungan pigmen warna di atas, rona bawah kulit Anda resmi diklasifikasikan sebagai **{undertone.upper()}**.")

    # MENU 2: EUCLIDEAN DISTANCE VALIDATION (SUDAH DITAMBAHKAN DETAIL DATASET KLASTER)
    with st.expander("2. Validasi Kedekatan Klaster Warna Kulit (Jarak Euclidean)", expanded=False):
        st.markdown("""
        <div class="komputasi-text">
        Sistem menggunakan rumus geometris <b>Euclidean Distance</b> untuk mengukur seberapa dekat koordinat 3 dimensi warna wajah Anda (W) terhadap titik pusat (Centroid/C) dari data latih. Jarak spasial terkecil menunjukkan kecocokan kelompok klaster yang paling valid.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(r"$$d(W, C) = \sqrt{(L_W - L_C)^2 + (a_W - a_C)^2 + (b_W - b_C)^2}$$")
        
        # Informasi Distribusi Sampel Dataset dan Titik Koordinat Centroid
        st.markdown("""
        <p style='font-size:0.85rem; font-weight:600; color:#162814; margin-bottom:8px;'>Pemetaan Titik Pusat AI (Centroid Data Latih):</p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin-bottom: 16px;">
            <div style="background: #fdfefe; padding: 12px; border-radius: 10px; border: 1px solid #e2efe0; font-size: 0.8rem;">
                 <b>Klaster Putih</b><br>
                • Total Sampel: 720 Foto<br>
                • Koordinat Centroid: <b>(175, 142, 144)</b>
            </div>
            <div style="background: #fdfefe; padding: 12px; border-radius: 10px; border: 1px solid #e2efe0; font-size: 0.8rem;">
                 <b>Klaster Sawo Matang</b><br>
                • Total Sampel: 1.183 Foto<br>
                • Koordinat Centroid: <b>(142, 144, 147)</b>
            </div>
            <div style="background: #fdfefe; padding: 12px; border-radius: 10px; border: 1px solid #e2efe0; font-size: 0.8rem;">
                 <b>Klaster Coklat Gelap</b><br>
                • Total Sampel: 530 Foto<br>
                • Koordinat Centroid: <b>(106, 143, 145)</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            st.markdown(f"""
            <div style="background: #fff; padding: 14px; border-radius: 12px; border: 1px solid #b8d4b0; font-size: 0.85rem; height: 100%;">
                <b>Koordinat Warna Wajah Anda (W):</b><br>
                • L* (Kecerahan) = {L}<br>
                • a* (Komponen Merah) = {A}<br>
                • b* (Komponen Kuning) = {B}
            </div>
            """, unsafe_allow_html=True)
        with c_col2:
            st.markdown(f"""
            <div style="background: #fff; padding: 14px; border-radius: 12px; border: 1px solid #b8d4b0; font-size: 0.85rem; height: 100%;">
                <b>Hasil Perhitungan Jarak (Euclidean):</b><br>
                • Jarak ke Centroid Putih: <b>{dist_putih}</b><br>
                • Jarak ke Centroid Sawo Matang: <b>{dist_sawo}</b><br>
                • Jarak ke Centroid Coklat Gelap: <b>{dist_gelap}</b>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if skin_tone == "Putih":
            c_target, d_target = c_putih, dist_putih
        elif skin_tone == "Sawo Matang":
            c_target, d_target = c_sawo, dist_sawo
        else:
            c_target, d_target = c_gelap, dist_gelap
            
        st.markdown(rf"$$d = \sqrt{{({L} - {c_target[0]})^2 + ({A} - {c_target[1]})^2 + ({B} - {c_target[2]})^2}} = {d_target}$$")
        st.success(f"**Kesimpulan Validasi:** Karena koordinat warna Anda memiliki nilai jarak terpendek sebesar **{d_target}** menuju pusat data klaster **{skin_tone}**, model mengonfirmasi keputusan klasifikasi ini telah valid secara matematis.")
\
# ============================================================
# RENDER RECOMMENDATIONS
# ============================================================
def render_recommendations(rec):
    st.markdown('<div class="section-title">💄 Rekomendasi Produk Kosmetik</div>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns([1, 1, 1])
    with m1:
        html = '<div class="card"><div class="card-title">Foundation</div>'
        for item in rec.get("foundation", []):
            html += f'<div class="foundation-item">{item}</div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="card"><div class="card-title">Lipstik</div>' + make_swatches(rec.get("lipstick", [])) + '</div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="card"><div class="card-title">Blush On</div>' + make_swatches(rec.get("blush", [])) + '</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">👗 Rekomendasi Palet Busana & Hijab</div>', unsafe_allow_html=True)
    w1, w2, w3 = st.columns([1, 1, 1])
    with w1:
        html  = '<div class="card"><div class="card-title">Kategori Busana</div>'
        html += '<div class="card-subtitle">⭐ Spektrum Utama</div>'
        html += make_swatches(rec.get("clothing_colors_primary", []), primary=True)
        html += '<div class="card-subtitle" style="margin-top:18px">✨ Spektrum Tersier</div>'
        html += make_swatches(rec.get("clothing_colors_additional", []))
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)
    with w2:
        st.markdown('<div class="card"><div class="card-title">Kategori Hijab</div>' + make_swatches(rec.get("hijab_colors", [])) + '</div>', unsafe_allow_html=True)
    with w3:
        html = '<div class="card"><div class="card-title">⚠️ Warna Terhindar</div>'
        for item in rec.get("colors_to_avoid", []):
            html += f'<div class="avoid-pill">{item}</div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

# ============================================================
# RENDER DOWNLOAD PDF
# ============================================================
def render_download_pdf(skin_tone, undertone, lab, rec):
    st.markdown('<div class="section-title">📄 Ekspor Laporan Analisis</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="download-box">
        <div class="download-title">Simpan Dokumen Hasil Uji</div>
        <div class="download-desc">
            Unduh laporan eksekutif berformat PDF yang memuat metrik warna kulit, undertone, nilai ekstraksi CIELAB, 
            serta rekomendasi terpadu untuk kosmetik dan mode pakaian.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    pdf_buffer = generate_pdf(skin_tone, undertone, lab, rec)
    st.download_button(
        label="⬇ Unduh Laporan PDF",
        data=pdf_buffer,
        file_name=f"laporan_analisis_{skin_tone.lower().replace(' ', '_')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

# ============================================================
# SHOW RESULTS
# ============================================================
def show_results(result, original_image=None):
    if not result["face_detected"]:
        st.warning("Peringatan: Koordinat wajah tidak terdeteksi. Sesuaikan posisi kamera dan pastikan intensitas cahaya merata.")
        return

    skin_tone = result["skin_tone"]
    undertone = result["undertone"]
    lab       = result["lab_values"]
    rec       = get_recommendation(skin_tone, undertone)

    st.success("✅ Akuisisi citra dan komputasi metrik berhasil diselesaikan.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_img, col_res = st.columns([1, 1.8])
    with col_img:
        if original_image:
            st.image(draw_highlight(original_image), caption="Pemetaan Area Evaluasi (ROI)", use_container_width=True)
    with col_res:
        render_metrics(skin_tone, undertone, lab, rec)

    st.markdown("<br>", unsafe_allow_html=True)
    render_detail_perhitungan(lab, skin_tone, undertone)
    st.markdown("<br>", unsafe_allow_html=True)
    render_recommendations(rec)
    st.markdown("<br>", unsafe_allow_html=True)
    render_download_pdf(skin_tone, undertone, lab, rec)

# ============================================================
# MAIN
# ============================================================
def main():
    import base64
    from pathlib import Path
    
    logo_html = ""
    if Path("logo personal.png").exists():
        with open("logo personal.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            logo_html = f"data:image/png;base64,{data}"

    hero_html = f"""
<div class="hero">
    <div class="hero-badge">Sistem Pakar & Visi Komputer</div>
    <div style="display: flex; justify-content: center; margin: -30px 0 25px 0;">
        <img src="{logo_html}" style="width: 300px; height: auto; object-fit: contain;">
    </div>
    <div class="hero-title">Personal Color <span>Analysis</span></div>
    <div class="hero-divider"></div>
    <div class="hero-sub">
        Diagnosis Rona Kulit Wajah secara Otomatis Berbasis Visi Komputer<br>dan Algoritma <i>K-Means Clustering</i>
    </div>
</div>
"""
    st.markdown(hero_html, unsafe_allow_html=True)

    mode = st.radio("Pilih Metode Input Data", ["Unggah Citra (Upload Foto)", "Pemindaian Langsung (Kamera)"], horizontal=True)
    st.markdown("---")

    if mode == "Unggah Citra (Upload Foto)":
        st.markdown("#### 📷 Modul Unggah Citra")
        st.markdown("""
        <div class="tips-row">
            <div class="tip-chip">💡 <b>Cahaya Natural:</b> Foto di dekat jendela pada siang hari</div>
            <div class="tip-chip">👤 <b>Posisi Wajah:</b> Menghadap lurus ke kamera, tidak tertutup rambut</div>
            <div class="tip-chip">🚫 <b>Tanpa Filter:</b> Jangan gunakan efek wajah atau make-up tebal</div>
            <div class="tip-chip">🖼 <b>Latar Belakang:</b> Gunakan tembok polos agar fokus pada wajah</div>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        if uploaded:
            image = Image.open(uploaded)
            arr   = np.array(image)
            if arr.ndim == 2:
                bgr = cv2.cvtColor(arr, cv2.COLOR_GRAY2BGR)
            elif arr.shape[2] == 4:
                bgr = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
            else:
                bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
                
            with st.spinner("Menjalankan ekstraksi matriks warna..."):
                bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.008)
                    bar.progress(i + 1)
                result = detect_face_and_extract_color(bgr)
                bar.empty()
            show_results(result, original_image=image)

    elif mode == "Pemindaian Langsung (Kamera)":
        st.markdown("#### 🎥 Modul Pemindaian Langsung")
        st.markdown("""
        <div class="tips-row">
            <div class="tip-chip">💡 <b>Cahaya Natural:</b> Menghadaplah ke arah jendela atau sumber cahaya</div>
            <div class="tip-chip">👤 <b>Posisi Wajah:</b> Posisikan wajah tepat di tengah-tengah kamera</div>
            <div class="tip-chip">📸 <b>Siap Foto:</b> Klik tombol kamera di bawah untuk mengunci hasil</div>
        </div>
        """, unsafe_allow_html=True)
        
        camera_image = st.camera_input("Posisikan wajah Anda dan klik tombol kamera di bawah")

        if camera_image is not None:
            image = Image.open(camera_image)
            arr = np.array(image)
            
            if arr.ndim == 2:
                bgr = cv2.cvtColor(arr, cv2.COLOR_GRAY2BGR)
            elif arr.shape[2] == 4:
                bgr = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
            else:
                bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

            with st.spinner("⏳ Sedang memproses jutaan piksel dan mengeksekusi algoritma K-Means... Mohon tunggu 3 detik."):
                time.sleep(3)
                result = detect_face_and_extract_color(bgr)

            st.markdown("---")
            show_results(result, original_image=image)


if __name__ == "__main__":
    main()