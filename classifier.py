import numpy as np
import cv2
import os
from sklearn.cluster import KMeans
import pickle

# ============================================================
# PENJELASAN CIELAB COLOR SPACE
# ============================================================
# CIE L*a*b* (CIELAB) adalah model warna yang dikembangkan oleh
# Commission Internationale de l'Éclairage (CIE) pada tahun 1976.
#
# Keunggulan CIELAB dibanding RGB untuk analisis warna kulit:
#   1. Perceptually uniform: jarak antar nilai LAB mencerminkan
#      perbedaan warna yang benar-benar dirasakan oleh mata manusia.
#   2. Memisahkan kecerahan (L*) dari informasi warna (a*, b*),
#      sehingga lebih robust terhadap perubahan pencahayaan.
#   3. Lebih akurat untuk membedakan warna kulit dibanding RGB
#      karena RGB tidak memisahkan kecerahan dan kromatisitas.
#
# Referensi jurnal:
#   - Ly, B.C.K., et al. (2020). "Research Techniques Made Simple:
#     Cutaneous Colorimetry: A Reliable Technique for Objective Skin
#     Color Measurement." Journal of Investigative Dermatology.
#   - Del Bino, S., et al. (2006). "Quantitative Comparison of Skin
#     Colour in Populations of Different Origins." Photochemistry
#     and Photobiology.
#
# Komponen LAB (skala OpenCV 0–255):
#
#   L* = Lightness (Kecerahan kulit)
#        0   → hitam pekat
#        128 → abu-abu sedang
#        255 → putih sempurna
#        Contoh: L*=146 artinya kecerahan menengah ke terang
#        → Digunakan untuk menentukan SKIN TONE (Putih/Sawo Matang/Coklat Gelap)
#
#   a* = Sumbu Merah–Hijau
#        < 128 → condong kehijauan
#          128 → netral
#        > 128 → condong kemerahan (pink/kemerahan pada kulit)
#        Contoh: a*=142 artinya sedikit kemerahan (142-128 = +14)
#        → Digunakan untuk mendeteksi undertone Dingin / Cool
#
#   b* = Sumbu Kuning–Biru
#        < 128 → condong kebiruan
#          128 → netral
#        > 128 → condong kekuningan (golden/warm pada kulit)
#        Contoh: b*=143 artinya sedikit kekuningan (143-128 = +15)
#        → Digunakan untuk mendeteksi undertone Hangat / Warm
#
# Konversi BGR → LAB dilakukan OpenCV secara otomatis:
#   cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
# ============================================================


# ============================================================
# KATEGORI WARNA KULIT — KONTEKS INDONESIA
# ============================================================
# Klasifikasi 3 kategori ini digunakan berdasarkan:
#   - Konteks dermatologi lokal Indonesia
#   - Fitzpatrick Scale yang diadaptasi untuk Asia Tenggara
#   - Hasil cluster K-Means dari dataset wajah Indonesia
#
#   "Putih"        → Kulit terang/cerah (Fitzpatrick Type I–II)
#                    L* > 158 (skala OpenCV)
#
#   "Sawo Matang"  → Kulit kuning langsat hingga kecoklatan sedang
#                    (Fitzpatrick Type III–IV)
#                    Tipe warna kulit paling umum di Indonesia
#                    124 < L* ≤ 158
#
#   "Coklat Gelap" → Kulit coklat tua hingga gelap
#                    (Fitzpatrick Type V–VI)
#                    L* ≤ 124
#
# Threshold L* dihitung dari midpoint antar centroid K-Means (2.433 foto):
#   Centroid Putih        ≈ L* 175
#   Centroid Sawo Matang  ≈ L* 141
#   Centroid Coklat Gelap ≈ L* 106
#   Batas Putih / Sawo Matang  = (175 + 141) / 2 = 158
#   Batas Sawo Matang / Coklat = (141 + 106) / 2 = 124
#
# Referensi:
#   Syarif, I., et al. (2019). "Klasifikasi Warna Kulit Wajah
#   Menggunakan Metode K-Means dan CIE L*a*b*."
#   Jurnal Teknik Informatika.
# ============================================================

CATEGORIES = ["putih", "sawo_matang", "coklat_gelap"]

# Mapping nama folder → label tampil ke user
FOLDER_TO_LABEL = {
    "putih":        "Putih",
    "sawo_matang":  "Sawo Matang",
    "coklat_gelap": "Coklat Gelap"
}

# ============================================================
# EKSTRAK FITUR WARNA DARI GAMBAR
# ============================================================

def extract_color_features(image_path):
    """
    Membaca gambar dan mengekstrak rata-rata nilai L*, a*, b* (CIELAB).

    Proses:
    1. Baca gambar → resize ke 200x200
    2. Ambil area tengah (ROI 60%x60%) simulasi area wajah
    3. Filter pixel terlalu gelap (bayangan/rambut) atau terang (sorotan cahaya)
    4. Konversi BGR → LAB → ambil rata-rata L*, a*, b*

    Return:
        np.array([L, a, b]) atau None jika gagal
    """
    image = cv2.imread(image_path)
    if image is None:
        return None

    image = cv2.resize(image, (200, 200))
    h, w  = image.shape[:2]

    # Ambil area tengah sebagai ROI (simulasi area wajah)
    roi = image[int(h*0.2):int(h*0.8), int(w*0.2):int(w*0.8)]

    if roi.size == 0:
        return None

    pixels     = roi.reshape(-1, 3).astype(np.float32)
    brightness = pixels.mean(axis=1)

    # Filter pixel terlalu gelap (< 45: bayangan, rambut, alis)
    # dan terlalu terang (> 220: sorotan cahaya, background putih)
    filtered = pixels[(brightness > 45) & (brightness < 220)]

    if len(filtered) < 10:
        filtered = pixels  # fallback jika terlalu banyak yang difilter

    roi_filtered = np.uint8(filtered.reshape(-1, 1, 3))
    lab          = cv2.cvtColor(roi_filtered, cv2.COLOR_BGR2LAB)
    mean_lab     = np.mean(lab.reshape(-1, 3), axis=0)

    return mean_lab  # [L*, a*, b*]

# ============================================================
# LOAD DATASET (Hanya Kaggle)
# ============================================================

def load_dataset():
    """
    Memuat dataset gambar wajah dari folder terstruktur tunggal:
        dataset/kaggle/
            putih/
            sawo_matang/
            coklat_gelap/

    Setiap gambar diekstrak fitur LAB-nya.
    Label yang disimpan adalah label tampil (bukan nama folder).

    Return:
        features (np.array), labels (np.array)
    """
    # Menemukan lokasi folder dataset secara otomatis
    base_dir = os.path.dirname(__file__)
    dataset_path = os.path.join(base_dir, "dataset", "kaggle")
    features = []
    labels   = []

    print("=" * 52)
    print(f"Memuat dataset tunggal dari: {dataset_path}")

    for folder_name in CATEGORIES:
        folder = os.path.join(dataset_path, folder_name)
        label  = FOLDER_TO_LABEL[folder_name]

        if not os.path.exists(folder):
            print(f"  [!] Folder tidak ditemukan: {folder}")
            continue

        count = 0
        for filename in os.listdir(folder):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(folder, filename)
                feature  = extract_color_features(img_path)

                if feature is not None:
                    features.append(feature)
                    labels.append(label)
                    count += 1

        print(f"  [{label}]: {count} foto berhasil dimuat")

    print(f"\nTotal seluruh dataset: {len(features)} foto")
    print("=" * 52)

    return np.array(features), np.array(labels)

# ============================================================
# TRAINING K-MEANS CLUSTERING
# ============================================================

def train_model():
    """
    Melatih model K-Means (K=3) menggunakan fitur LAB dari dataset tunggal.
    Menyimpan model (model_kmeans.pkl) dan label mapping (label_mapping.pkl).
    """
    features, labels = load_dataset()

    if len(features) == 0:
        print("Dataset kosong! Pastikan folder dataset/kaggle sudah benar.")
        return None, None

    print(f"\nMelatih K-Means dengan {len(features)} foto, K=3...")

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans.fit(features)

    print("\nTraining selesai!")
    print("\nCluster Centers (nilai L*, a*, b* skala OpenCV 0–255):")
    
    # -------------------------------------------------------------
    # PENGURUTAN CENTROID (URUTAN WAJIB: GELAP -> SAWO -> PUTIH)
    # -------------------------------------------------------------
    # Mengurutkan centroid berdasarkan nilai L* (Kecerahan) dari yang tergelap
    centroids = kmeans.cluster_centers_
    sorted_indices = np.argsort(centroids[:, 0]) 
    
    cluster_gelap = sorted_indices[0] # L* terkecil
    cluster_sawo = sorted_indices[1]  # L* di tengah
    cluster_putih = sorted_indices[2] # L* terbesar

    print(f"  Cluster {cluster_putih}: L*={centroids[cluster_putih][0]:.1f} | a*={centroids[cluster_putih][1]:.1f} | b*={centroids[cluster_putih][2]:.1f}  → Putih")
    print(f"  Cluster {cluster_sawo}: L*={centroids[cluster_sawo][0]:.1f} | a*={centroids[cluster_sawo][1]:.1f} | b*={centroids[cluster_sawo][2]:.1f}  → Sawo Matang")
    print(f"  Cluster {cluster_gelap}: L*={centroids[cluster_gelap][0]:.1f} | a*={centroids[cluster_gelap][1]:.1f} | b*={centroids[cluster_gelap][2]:.1f}  → Coklat Gelap")

    # MAPPING OTOMATIS BERDASARKAN URUTAN L* (Bukan Majority Vote yang bisa salah)
    label_mapping = {
        cluster_putih: "Putih",
        cluster_sawo: "Sawo Matang",
        cluster_gelap: "Coklat Gelap"
    }

    print("\nCluster → Label Mapping (Fixed berdasarkan kecerahan L*):")
    for cid, lbl in label_mapping.items():
        print(f"  Cluster {cid} → {lbl}")

    # Menyimpan file .pkl di folder yang sama dengan script ini
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, "model_kmeans.pkl")
    mapping_path = os.path.join(base_dir, "label_mapping.pkl")

    with open(model_path, "wb") as f:
        pickle.dump(kmeans, f)

    with open(mapping_path, "wb") as f:
        pickle.dump(label_mapping, f)

    print("\nModel tersimpan  : model_kmeans.pkl")
    print("Mapping tersimpan: label_mapping.pkl")

    return kmeans, label_mapping

# ============================================================
# PREDIKSI SKIN TONE BERDASARKAN NILAI L* (CADANGAN)
# ============================================================

def predict_skin_tone(lab_values):
    """
    Mengklasifikasikan warna kulit berdasarkan nilai L* (Lightness).
    Berdasarkan hasil training terbaru (2.433 foto).
    """
    L = lab_values["L"]

    if L > 158:
        return "Putih"
    elif L > 124: # Diupdate jadi 124
        return "Sawo Matang"
    else:
        return "Coklat Gelap"

# ============================================================
# KLASIFIKASI UNDERTONE
# ============================================================

def classify_undertone(lab_values):
    """
    Mengklasifikasikan undertone berdasarkan selisih komponen a* dan b*.
    Nilai digeser ke 0 (dikurangi 128) sebelum dibandingkan.
    """
    A = lab_values["A"]
    B = lab_values["B"]

    a_shifted = A - 128
    b_shifted = B - 128
    diff      = b_shifted - a_shifted

    if diff > 8 and b_shifted > 4:
        return "Hangat / Warm"
    elif a_shifted > 4 and diff < -2:
        return "Dingin / Cool"
    elif b_shifted < -3:
        return "Dingin / Cool"
    else:
        return "Netral / Neutral"

# ============================================================
# MAIN — Jalankan Training
# ============================================================

if __name__ == "__main__":
    print("=" * 52)
    print("  TRAINING MODEL K-MEANS PERSONAL COLOR ANALYSIS")
    print("  Kategori: Putih | Sawo Matang | Coklat Gelap")
    print("=" * 52 + "\n")

    kmeans, mapping = train_model()

    if kmeans:
        print("\nTraining berhasil!")
        print("\nFile yang dihasilkan:")
        print("  - model_kmeans.pkl   (model K-Means terlatih)")
        print("  - label_mapping.pkl  (peta cluster → label kulit)")

        # Verifikasi threshold prediksi
        print("\nVerifikasi Threshold Skin Tone (berdasarkan nilai L*):")
        test_cases = [
            ("L*=175 (sentroid Putih)",          {"L": 175, "A": 135, "B": 140}),
            ("L*=160 (di atas batas Putih)",     {"L": 160, "A": 135, "B": 140}),
            ("L*=158 (tepat batas Putih)",        {"L": 158, "A": 135, "B": 140}),
            ("L*=141 (sentroid Sawo Matang)",     {"L": 141, "A": 135, "B": 140}),
            ("L*=124 (tepat batas Coklat)",       {"L": 124, "A": 135, "B": 140}), # Diupdate jadi 124
            ("L*=106 (sentroid Coklat Gelap)",    {"L": 106, "A": 135, "B": 140}),
        ]
        for label, val in test_cases:
            print(f"  {label:44s} → {predict_skin_tone(val)}")

        # Verifikasi undertone
        print("\nVerifikasi Undertone (berdasarkan nilai a* dan b*):")
        undertone_cases = [
            ("a*=128, b*=145 → b dominan kuning",  {"L": 140, "A": 128, "B": 145}),
            ("a*=140, b*=128 → a dominan merah",   {"L": 140, "A": 140, "B": 128}),
            ("a*=135, b*=138 → seimbang netral",   {"L": 140, "A": 135, "B": 138}),
        ]
        for label, val in undertone_cases:
            print(f"  {label:44s} → {classify_undertone(val)}")