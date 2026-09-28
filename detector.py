import cv2
import numpy as np
import pickle
import os

# ============================================================
# HAAR CASCADE — Detektor Wajah
# ============================================================
# Menggunakan os.path agar fleksibel di server manapun
BASE_DIR = os.path.dirname(__file__)
XML_PATH = os.path.join(BASE_DIR, 'haarcascade_frontalface_default.xml')
FACE_CASCADE = cv2.CascadeClassifier(XML_PATH)

# ============================================================
# LOAD MODEL K-MEANS (REAL MACHINE LEARNING INFERENCE)
# ============================================================
# Memuat "Otak" AI (.pkl) ke dalam memori aplikasi
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model_kmeans.pkl")
MAPPING_PATH = os.path.join(BASE_DIR, "label_mapping.pkl")

if os.path.exists(MODEL_PATH) and os.path.exists(MAPPING_PATH):
    with open(MODEL_PATH, "rb") as f:
        KMEANS_MODEL = pickle.load(f)
    with open(MAPPING_PATH, "rb") as f:
        LABEL_MAPPING = pickle.load(f)
    print("✅ Model K-Means berhasil dimuat!")
else:
    print("⚠️ WARNING: File model_kmeans.pkl atau label_mapping.pkl tidak ditemukan!")


def detect_face_and_extract_color(image):
    result = {
        "face_detected": False,
        "skin_tone"    : None,
        "undertone"    : None,
        "lab_values"   : None,
        "roi_image"    : None
    }

    # ── Deteksi wajah ──────────────────────────────────────
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = FACE_CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    if len(faces) == 0:
        return result

    x, y, fw, fh = faces[0]
    face_region  = image[y:y+fh, x:x+fw]

    if face_region.size == 0:
        return result

    fh_r, fw_r = face_region.shape[:2]

    # ── Ambil 3 Area ROI (Dahi, Pipi Kiri, Pipi Kanan) ──────
    forehead = face_region[
        int(fh_r * 0.08):int(fh_r * 0.22),
        int(fw_r * 0.35):int(fw_r * 0.65)
    ]
    cheek_left = face_region[
        int(fh_r * 0.45):int(fh_r * 0.62),
        int(fw_r * 0.10):int(fw_r * 0.30)
    ]
    cheek_right = face_region[
        int(fh_r * 0.45):int(fh_r * 0.62),
        int(fw_r * 0.70):int(fw_r * 0.90)
    ]

    roi_combined = []
    for roi in [forehead, cheek_left, cheek_right]:
        if roi.size > 0:
            roi_combined.append(roi.reshape(-1, 3))

    if not roi_combined:
        return result

    all_pixels = np.vstack(roi_combined)

    # ── Filter Pixel Kecerahan (Buang bayangan & pantulan) ──
    brightness = all_pixels.mean(axis=1)
    filtered   = all_pixels[(brightness >= 45) & (brightness <= 215)]

    if len(filtered) < 10:
        filtered = all_pixels

    # ── Konversi ke CIELAB ─────────────────────────────────
    roi_img    = np.uint8(filtered.reshape(-1, 1, 3))
    lab_pixels = cv2.cvtColor(roi_img, cv2.COLOR_BGR2LAB)
    lab_mean   = np.mean(lab_pixels.reshape(-1, 3), axis=0)

    L, A, B = lab_mean

   # ============================================================
   # KLASIFIKASI SKIN TONE MENGGUNAKAN PREDIKSI K-MEANS ASLI
   # ============================================================
    if KMEANS_MODEL is not None:
        titik_wajah = np.array([[L, A, B]])
        cluster_id = KMEANS_MODEL.predict(titik_wajah)[0]
        
        # KITA OVERRIDE (PAKSA) PENAMAANNYA DI SINI SESUAI HASIL TERMINAL
        # Cluster 0: Centroid L=176 (Putih)
        # Cluster 1: Centroid L=103 (Coklat Gelap)
        # Cluster 2: Centroid L=140 (Sawo Matang)
        if cluster_id == 0:
            skin_tone = "Putih"
        elif cluster_id == 2:
            skin_tone = "Sawo Matang"
        elif cluster_id == 1:
            skin_tone = "Coklat Gelap"
    else:
        # Cadangan kalau file .pkl terhapus (tetap pakai If-Else threshold)
        if L > 158:
            skin_tone = "Putih"
        elif L > 122:
            skin_tone = "Sawo Matang"
        else:
            skin_tone = "Coklat Gelap"

    # ============================================================
    # KLASIFIKASI UNDERTONE (Tetap Rule-Based)
    # ============================================================
    a_shifted = A - 128
    b_shifted = B - 128
    diff      = b_shifted - a_shifted

    if diff > 8 and b_shifted > 4:
        undertone = "Hangat / Warm"
    elif a_shifted > 4 and diff < -2:
        undertone = "Sejuk / Cool"
    elif b_shifted < -3:
        undertone = "Sejuk / Cool"
    else:
        undertone = "Netral / Neutral"

    # ── Simpan hasil ────────────────────────────────
    result["face_detected"] = True
    result["skin_tone"]     = skin_tone
    result["undertone"]     = undertone
    result["lab_values"]    = {
        "L": round(L, 2),
        "A": round(A, 2),
        "B": round(B, 2)
    }
    result["roi_image"] = face_region

    return result

def detect_from_image_path(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return {"face_detected": False, "error": "Gambar tidak bisa dibaca"}
    return detect_face_and_extract_color(image)

def detect_from_frame(frame):
    return detect_face_and_extract_color(frame)