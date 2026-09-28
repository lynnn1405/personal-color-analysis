# ============================================================
# DATABASE REKOMENDASI PERSONAL COLOR
# Disesuaikan dengan konteks warna kulit Indonesia
#
# Key kombinasi menggunakan label Bahasa Indonesia:
#   Skin Tone : "Putih" | "Sawo Matang" | "Coklat Gelap"
#   Undertone : "Hangat / Warm" | "Sejuk / Cool" | "Netral / Neutral"
#
# Struktur tiap entri rekomendasi:
#   description              : Deskripsi karakteristik warna kulit
#   foundation               : Rekomendasi produk foundation
#   lipstick                 : Rekomendasi warna lipstik
#   blush                    : Rekomendasi warna blush on
#   clothing_colors_primary  : 3 WARNA UTAMA terkuat yang paling direkomendasikan
#   clothing_colors_additional: Warna pakaian tambahan yang juga cocok
#   hijab_colors             : Rekomendasi warna hijab
#   colors_to_avoid          : Warna yang sebaiknya dihindari (spesifik)
#
# Dasar ilmiah rekomendasi warna:
#   - Caygill, S. (1980). "Color: The Essence of You." Celestial Arts.
#     (Teori Seasonal Color Analysis — dasar klasifikasi undertone warm/cool)
#   - Itten, J. (1970). "The Art of Color." John Wiley & Sons.
#     (Teori harmoni warna dan kontras yang menjadi dasar personal color)
#   - Kobayashi, S. (1990). "Color Image Scale." Kodansha International.
#     (Skala citra warna untuk rekomendasi kombinasi warna personal)
#   - Zyla, D. (2010). "Color Your Style." Dutton.
#     (Adaptasi personal color analysis untuk beragam tipe kulit Asia)
#   - Fatimah, S., et al. (2021). "Analisis Warna Kulit Wajah Orang
#     Indonesia Menggunakan Color Space CIE L*a*b*."
#     Jurnal Nasional Teknik Elektro dan Teknologi Informasi (JNTEITI).
# ============================================================

RECOMMENDATIONS = {

    # ==================== PUTIH ====================

    ("Putih", "Hangat / Warm"): {
        "description": (
            "Kulit putih/cerah dengan nuansa kekuningan dan keemasan. "
            "Undertone hangat membuat warna earth tone dan warna-warna "
            "bernuansa emas sangat mempercantik penampilan."
        ),
        "foundation": [
            "Wardah Exclusive Liquid Foundation shade 01W",
            "Make Over Powerstay Foundation N10 - warm undertone",
            "NYX Can't Stop Won't Stop shade Pale - yellow base",
            "Maybelline Fit Me Matte + Poreless shade 110 - warm"
        ],
        "lipstick": [
            "Peach",
            "Coral",
            "Nude kecoklatan",
            "Terracotta",
            "Salmon",
            "Apricot"
        ],
        "blush": [
            "Peach",
            "Apricot",
            "Coral muda",
            "Bronze tipis"
        ],
        # 3 warna utama paling direkomendasikan untuk kulit Putih - Hangat
        "clothing_colors_primary": [
            "Cream / Krem Hangat",
            "Terracotta / Merah Bata",
            "Olive Green / Hijau Zaitun"
        ],
        # Warna tambahan yang juga cocok
        "clothing_colors_additional": [
            "Off white",
            "Camel",
            "Mustard",
            "Earth tone",
            "Coklat muda",
            "Amber",
            "Burnt orange",
            "Peach",
            "Salmon",
            "Warm beige"
        ],
        "hijab_colors": [
            "Cream",
            "Camel",
            "Dusty peach",
            "Olive",
            "Coklat muda",
            "Terracotta",
            "Mustard",
            "Salmon",
            "Off white",
            "Warm beige"
        ],
        # Warna yang dihindari — spesifik dengan penjelasan
        "colors_to_avoid": [
            "Abu-abu kebiruan / cool grey (contoh: abu-abu besi, abu-abu silver dingin)",
            "Hitam pekat murni — membuat kontras terlalu kuat dan menyerap cahaya wajah",
            "Fuchsia terang (pink keunguan menyala, seperti pink magenta mencolok)",
            "Silver metalik (warna logam perak dingin, bukan gold)",
            "Biru icy / biru es (biru muda sangat dingin, seperti biru langit pucat)",
            "Putih bersih / pure white — terlalu kontras dan bisa membuat wajah tampak pucat"
        ]
    },

    ("Putih", "Sejuk / Cool"): {
        "description": (
            "Kulit putih/cerah dengan nuansa kemerahan dan kebiruan. "
            "Undertone sejuk membuat warna jewel tone dan pastel dingin "
            "sangat menonjolkan kecantikan alami."
        ),
        "foundation": [
            "Wardah Exclusive Liquid Foundation shade 01C",
            "Make Over Powerstay Foundation N10 - cool undertone",
            "Maybelline Fit Me shade 110 Porcelain - pink base",
            "L'Oreal True Match shade W1 - cool"
        ],
        "lipstick": [
            "Pink soft",
            "Mauve",
            "Berry",
            "Rose",
            "Raspberry",
            "Cool red"
        ],
        "blush": [
            "Pink",
            "Rose",
            "Plum muda",
            "Cool pink"
        ],
        "clothing_colors_primary": [
            "Navy Blue / Biru Tua",
            "Lavender / Ungu Muda Dingin",
            "Soft Pink / Pink Lembut"
        ],
        "clothing_colors_additional": [
            "Putih bersih",
            "Abu-abu muda",
            "Mint",
            "Icy blue",
            "Cobalt blue",
            "Emerald",
            "Cool purple",
            "Dusty blue",
            "Silver grey",
            "Mauve"
        ],
        "hijab_colors": [
            "Putih bersih",
            "Baby pink",
            "Lavender",
            "Dusty blue",
            "Silver grey",
            "Icy pink",
            "Mint",
            "Cool lilac",
            "Mauve",
            "Soft purple"
        ],
        "colors_to_avoid": [
            "Orange terang / oranye mencolok (seperti oranye traffic cone atau oranye buah)",
            "Kuning mencolok / kuning chrome (kuning cerah jenuh, bukan kuning pastel)",
            "Coklat tua hangat / coklat tanah (seperti coklat kopi tua, coklat kayu gelap)",
            "Mustard / kuning kecoklatan hangat (kuning tua keemasan)",
            "Terracotta / merah bata hangat (merah kecoklatan bernuansa tanah)"
        ]
    },

    ("Putih", "Netral / Neutral"): {
        "description": (
            "Kulit putih/cerah dengan undertone seimbang — sangat fleksibel "
            "dalam memilih warna. Hampir semua palet warna akan cocok, "
            "baik yang hangat maupun yang sejuk."
        ),
        "foundation": [
            "Wardah Exclusive Liquid Foundation shade 01N",
            "Make Over Powerstay Foundation N12 - neutral",
            "Maybelline Fit Me shade 115 - neutral",
            "Wardah Lightening Liquid Foundation shade Natural"
        ],
        "lipstick": [
            "Nude pink",
            "Mauve",
            "Peach",
            "MLBB (My Lips But Better)",
            "Rose nude",
            "Dusty rose"
        ],
        "blush": [
            "Soft peach",
            "Dusty rose",
            "Light coral",
            "Nude blush"
        ],
        "clothing_colors_primary": [
            "Putih Bersih / White",
            "Navy Blue / Biru Tua",
            "Dusty Pink / Pink Abu-abu"
        ],
        "clothing_colors_additional": [
            "Cream",
            "Pastel lembut (baby blue, mint muda, lavender muda)",
            "Nude",
            "Sage green",
            "Lavender",
            "Soft blue",
            "Taupe",
            "Mushroom grey",
            "Camel muda"
        ],
        "hijab_colors": [
            "Putih",
            "Cream",
            "Nude",
            "Dusty pink",
            "Sage green",
            "Lavender muda",
            "Soft grey",
            "Taupe",
            "Baby blue",
            "Mauve"
        ],
        "colors_to_avoid": [
            "Hijau neon / lime neon (hijau stabilo, hijau menyala seperti warna rompi proyek)",
            "Kuning neon / kuning fosfor (kuning stabilo, sangat terang dan menyilaukan)",
            "Pink neon / fuchsia neon (pink menyala seperti warna highlighter)",
            "Oranye neon (oranye sangat terang, lebih terang dari warna buah jeruk)",
            "Merah neon (merah fluorescent, bukan merah biasa)"
        ]
    },

    # ==================== SAWO MATANG ====================

    ("Sawo Matang", "Hangat / Warm"): {
        "description": (
            "Kulit sawo matang dengan nuansa kekuningan dan keemasan — "
            "tipe warna kulit paling umum di Indonesia. "
            "Earth tone dan warna hangat akan menonjolkan kecantikan alami."
        ),
        "foundation": [
            "Wardah Exclusive Liquid Foundation shade 03W",
            "Make Over Powerstay Foundation W30 - warm",
            "NYX Can't Stop Won't Stop shade Natural - warm",
            "Maybelline Fit Me shade 220 - warm beige"
        ],
        "lipstick": [
            "Terracotta",
            "Brick red",
            "Nude coklat",
            "Coral",
            "Peach tua",
            "Burnt orange",
            "Warm mauve"
        ],
        "blush": [
            "Peach",
            "Coral",
            "Bronze",
            "Warm peach",
            "Apricot"
        ],
        "clothing_colors_primary": [
            "Olive Green / Hijau Zaitun",
            "Mustard / Kuning Keemasan",
            "Terracotta / Merah Bata"
        ],
        "clothing_colors_additional": [
            "Coklat kayu",
            "Burnt orange",
            "Cream hangat",
            "Camel",
            "Amber",
            "Teal blue",
            "Oker / Ochre",
            "Rust / Karat",
            "Hijau lumut",
            "Coklat madu"
        ],
        "hijab_colors": [
            "Olive",
            "Mustard",
            "Coklat kayu",
            "Dusty orange",
            "Earth tone",
            "Terracotta",
            "Peach",
            "Camel",
            "Marun",
            "Burgundy",
            "Teal",
            "Hijau zaitun"
        ],
        "colors_to_avoid": [
            "Pastel sangat pucat (baby pink pucat, biru sangat muda, lavender hampir putih) — membuat kulit tampak kusam",
            "Abu-abu kebiruan / steel grey (abu-abu dingin metalik, bukan abu-abu hangat)",
            "Silver metalik (warna logam perak dingin)",
            "Biru icy / biru es (biru muda sangat dingin pucat seperti warna langit berangin)",
            "Hijau neon / lime neon (hijau stabilo menyala)",
            "Kuning neon / kuning fosfor (kuning stabilo, sangat jenuh dan terang)"
        ]
    },

    ("Sawo Matang", "Sejuk / Cool"): {
        "description": (
            "Kulit sawo matang dengan nuansa kemerahan dan keunguan. "
            "Jewel tone dan warna sejuk akan membuat wajah tampak lebih "
            "cerah dan segar."
        ),
        "foundation": [
            "Wardah Exclusive Liquid Foundation shade 03C",
            "Make Over Powerstay Foundation C30 - cool",
            "Maybelline Fit Me shade 220 - cool pink",
            "L'Oreal True Match shade C3 - cool beige"
        ],
        "lipstick": [
            "Mauve",
            "Berry",
            "Fuchsia",
            "Rose tua",
            "Wine",
            "Plum",
            "Cool pink"
        ],
        "blush": [
            "Dusty rose",
            "Mauve",
            "Berry muda",
            "Cool pink",
            "Soft plum"
        ],
        "clothing_colors_primary": [
            "Navy Blue / Biru Tua",
            "Emerald Green / Hijau Zamrud",
            "Burgundy / Merah Anggur Tua"
        ],
        "clothing_colors_additional": [
            "Purple / Ungu",
            "Dusty pink",
            "Grey / Abu-abu netral",
            "Cobalt blue",
            "Magenta",
            "Dusty mauve",
            "Lavender tua",
            "Maroon",
            "Royal blue",
            "Plum"
        ],
        "hijab_colors": [
            "Dusty purple",
            "Navy",
            "Dusty pink",
            "Grey",
            "Emerald",
            "Mauve",
            "Maroon",
            "Dusty blue",
            "Cool lavender",
            "Burgundy",
            "Ash blue",
            "Soft fuchsia"
        ],
        "colors_to_avoid": [
            "Orange mencolok / oranye jenuh (seperti warna oranye buah, oranye traffic cone)",
            "Kuning terang / kuning chrome (kuning cerah jenuh seperti kuning taksi)",
            "Coklat tua hangat / coklat kayu tua (coklat tanah gelap bernuansa hangat)",
            "Mustard / kuning kecoklatan (kuning tua keemasan hangat)",
            "Camel / krem kecoklatan hangat (warna unta, beige kecoklatan)",
            "Earth tone jenuh (coklat karat, oker tua, burnt sienna)"
        ]
    },

    ("Sawo Matang", "Netral / Neutral"): {
        "description": (
            "Kulit sawo matang dengan undertone seimbang — sangat versatile! "
            "Bisa mix warna hangat maupun sejuk, "
            "menjadikanmu bebas bereksperimen dengan banyak pilihan warna."
        ),
        "foundation": [
            "Wardah Exclusive Liquid Foundation shade 03N",
            "Make Over Powerstay Foundation N30 - neutral",
            "Maybelline Fit Me shade 230 - natural beige",
            "Wardah Exclusive Matte Foundation shade Beige"
        ],
        "lipstick": [
            "MLBB (My Lips But Better)",
            "Nude medium",
            "Rose",
            "Dusty mauve",
            "Peach rose",
            "Coklat rose"
        ],
        "blush": [
            "Peach rose",
            "Dusty coral",
            "Soft mauve",
            "Warm nude blush"
        ],
        "clothing_colors_primary": [
            "Navy Blue / Biru Tua",
            "Olive Green / Hijau Zaitun",
            "Dusty Pink / Pink Abu-abu"
        ],
        "clothing_colors_additional": [
            "Putih / White",
            "Camel",
            "Sage green",
            "Dusty blue",
            "Taupe",
            "Maroon",
            "Teal",
            "Coklat nude",
            "Warm grey",
            "Mocha"
        ],
        "hijab_colors": [
            "Earth tone hangat",
            "Dusty rose",
            "Navy",
            "Olive",
            "Taupe",
            "Sage green",
            "Mocha",
            "Coklat latte",
            "Cream",
            "Abu-abu hangat",
            "Dusty mauve",
            "Warm grey"
        ],
        "colors_to_avoid": [
            "Hijau neon / lime neon (hijau stabilo, hijau menyala seperti warna rompi proyek)",
            "Kuning neon / kuning fosfor (kuning stabilo sangat terang, bukan kuning mustard)",
            "Pink neon / fuchsia neon (pink menyala, lebih terang dari fuchsia biasa)",
            "Oranye neon (oranye fluorescent sangat terang, bukan oranye hangat biasa)",
            "Biru neon / biru elektrik (biru menyala sangat jenuh seperti warna lampu neon)"
        ]
    },

    # ==================== COKLAT GELAP ====================

    ("Coklat Gelap", "Hangat / Warm"): {
        "description": (
            "Kulit coklat gelap dengan nuansa keemasan dan kecoklatan. "
            "Warna cerah dan bold akan sangat menonjolkan kecantikan "
            "kulit yang kaya dan hangat."
        ),
        "foundation": [
            "Wardah Exclusive Liquid Foundation shade 05W",
            "Make Over Powerstay Foundation W50 - warm deep",
            "NYX Can't Stop Won't Stop shade Mahogany - warm",
            "Maybelline Fit Me shade 330 - warm toffee"
        ],
        "lipstick": [
            "Burnt orange",
            "Coklat tua",
            "Brick red",
            "Nude gelap",
            "Copper",
            "Warm brown",
            "Terracotta gelap"
        ],
        "blush": [
            "Bronze",
            "Copper",
            "Warm brown",
            "Deep peach",
            "Amber blush"
        ],
        "clothing_colors_primary": [
            "Putih Bersih / White",
            "Kuning Cerah / Bright Yellow",
            "Orange / Oranye Hangat"
        ],
        "clothing_colors_additional": [
            "Merah cerah",
            "Hijau toska",
            "Gold / Emas",
            "Mustard cerah",
            "Coral terang",
            "Fuchsia",
            "Turquoise",
            "Amber",
            "Warna-warna bold dan jenuh"
        ],
        "hijab_colors": [
            "Putih",
            "Kuning cerah",
            "Gold",
            "Merah",
            "Toska",
            "Coral",
            "Fuchsia",
            "Turquoise",
            "Mustard",
            "Orange hangat",
            "Amber",
            "Merah marun"
        ],
        "colors_to_avoid": [
            "Coklat tua senada kulit (coklat gelap seperti coklat dark chocolate — melebur dengan warna kulit)",
            "Abu-abu gelap / charcoal (abu-abu sangat gelap, hampir hitam — menyerap cahaya wajah)",
            "Coklat karat / rust gelap (coklat kemerahan tua yang terlalu dekat dengan warna kulit)",
            "Hitam murni tanpa aksesori cerah — membuat penampilan tampak berat dan flat",
            "Warna muted/kusam sangat gelap (seperti olive sangat tua, hijau lumut gelap pekat)"
        ]
    },

    ("Coklat Gelap", "Sejuk / Cool"): {
        "description": (
            "Kulit coklat gelap dengan nuansa keunguan dan kebiruan. "
            "Jewel tone dan warna vibrant akan membuat kulit bersinar "
            "dan tampak memukau."
        ),
        "foundation": [
            "Wardah Exclusive Liquid Foundation shade 05C",
            "Make Over Powerstay Foundation C50 - cool deep",
            "Maybelline Fit Me shade 370 - cool espresso",
            "L'Oreal True Match shade C6 - cool deep"
        ],
        "lipstick": [
            "Berry gelap",
            "Plum",
            "Wine",
            "Dark fuchsia",
            "Deep burgundy",
            "Blackberry",
            "Deep mauve"
        ],
        "blush": [
            "Deep rose",
            "Plum",
            "Berry",
            "Deep fuchsia",
            "Cool burgundy"
        ],
        "clothing_colors_primary": [
            "Royal Blue / Biru Kerajaan",
            "Emerald / Hijau Zamrud",
            "Purple / Ungu Tua"
        ],
        "clothing_colors_additional": [
            "Putih bersih",
            "Hot pink",
            "Silver",
            "Cobalt blue",
            "Magenta",
            "Violet",
            "Icy lavender",
            "Deep teal",
            "Cool grey",
            "Fuchsia"
        ],
        "hijab_colors": [
            "Putih",
            "Royal blue",
            "Purple",
            "Emerald",
            "Hot pink",
            "Cobalt",
            "Fuchsia",
            "Violet",
            "Silver",
            "Magenta",
            "Cool lavender",
            "Deep teal"
        ],
        "colors_to_avoid": [
            "Coklat tua senada kulit (coklat dark chocolate, coklat espresso — melebur dengan warna kulit)",
            "Coklat kayu hangat (coklat kemerahan hangat — bertabrakan dengan undertone sejuk)",
            "Warna muted/kusam dan redup (seperti olive tua, coklat khaki, warna tanah kusam)",
            "Beige kecoklatan hangat / camel — terlalu dekat dengan warna kulit, tidak kontras",
            "Kuning mustard tua (kuning kecoklatan hangat — bertabrakan dengan undertone sejuk)"
        ]
    },

    ("Coklat Gelap", "Netral / Neutral"): {
        "description": (
            "Kulit coklat gelap dengan undertone seimbang — punya keistimewaan "
            "bisa memakai hampir semua warna bold dan cerah dengan percaya diri! "
            "Kunci utama: pilih warna yang kontras dan bercahaya."
        ),
        "foundation": [
            "Wardah Exclusive Liquid Foundation shade 05N",
            "Make Over Powerstay Foundation N50 - neutral deep",
            "Maybelline Fit Me shade 360 - neutral deep",
            "NYX Can't Stop Won't Stop shade Espresso - neutral"
        ],
        "lipstick": [
            "Nude gelap",
            "Coklat rose",
            "Berry medium",
            "MLBB gelap",
            "Deep mauve",
            "Warm plum"
        ],
        "blush": [
            "Warm brown",
            "Deep peach",
            "Soft berry",
            "Bronze neutral",
            "Deep coral"
        ],
        "clothing_colors_primary": [
            "Putih Bersih / White",
            "Merah Cerah / Bright Red",
            "Kuning Cerah / Bright Yellow"
        ],
        "clothing_colors_additional": [
            "Hijau toska / Teal",
            "Biru cerah",
            "Fuchsia",
            "Turquoise",
            "Gold / Emas",
            "Coral terang",
            "Mustard cerah",
            "Emerald",
            "Semua warna bold dan jenuh"
        ],
        "hijab_colors": [
            "Putih",
            "Warna-warna cerah dan bold",
            "Fuchsia",
            "Kuning cerah",
            "Turquoise",
            "Coral",
            "Gold",
            "Merah",
            "Emerald",
            "Metalik (gold, silver, bronze)"
        ],
        "colors_to_avoid": [
            "Coklat tua sangat gelap (coklat dark chocolate, coklat espresso, coklat hitam — melebur dengan warna kulit)",
            "Abu-abu sangat gelap / charcoal (abu-abu nyaris hitam — membuat penampilan flat)",
            "Warna muted/kusam dan gelap (olive sangat tua, hijau lumut pekat, coklat khaki gelap)",
            "Hitam total tanpa aksesori warna cerah — menyerap cahaya dan membuat wajah tampak berat"
        ]
    }
}


# ============================================================
# FUNGSI GET RECOMMENDATION
# ============================================================

def get_recommendation(skin_tone, undertone):
    """
    Mengambil data rekomendasi warna berdasarkan kombinasi
    skin tone dan undertone yang terdeteksi.

    Args:
        skin_tone (str): "Putih" | "Sawo Matang" | "Coklat Gelap"
        undertone (str): "Hangat / Warm" | "Sejuk / Cool" | "Netral / Neutral"

    Return:
        dict: Data rekomendasi lengkap untuk kombinasi tersebut.
              Jika kombinasi tidak ditemukan, return rekomendasi default.
    """
    key = (skin_tone, undertone)
    if key in RECOMMENDATIONS:
        return RECOMMENDATIONS[key]
    else:
        # Fallback default jika kombinasi tidak ditemukan
        return {
            "description": "Kombinasi warna kulit unik — warna netral dan natural cocok untukmu.",
            "foundation": ["Konsultasikan ke beauty advisor untuk shade yang tepat"],
            "lipstick": ["Nude", "MLBB", "Rose"],
            "blush": ["Peach", "Rose", "Coral muda"],
            "clothing_colors_primary": ["Putih", "Navy", "Olive"],
            "clothing_colors_additional": ["Camel", "Grey", "Taupe"],
            "colors_to_avoid": [
                "Warna neon (hijau stabilo, kuning fosfor, pink menyala)",
                "Warna terlalu gelap senada kulit"
            ],
            "hijab_colors": ["Putih", "Cream", "Nude", "Navy", "Olive"]
        }


# ============================================================
# MAIN — Test semua 9 kombinasi
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  TEST SEMUA 9 KOMBINASI REKOMENDASI PERSONAL COLOR")
    print("=" * 60 + "\n")

    combos = [
        ("Putih",        "Hangat / Warm"),
        ("Putih",        "Sejuk / Cool"),
        ("Putih",        "Netral / Neutral"),
        ("Sawo Matang",  "Hangat / Warm"),
        ("Sawo Matang",  "Sejuk / Cool"),
        ("Sawo Matang",  "Netral / Neutral"),
        ("Coklat Gelap", "Hangat / Warm"),
        ("Coklat Gelap", "Sejuk / Cool"),
        ("Coklat Gelap", "Netral / Neutral"),
    ]

    for skin, under in combos:
        rec = get_recommendation(skin, under)
        print(f"✅ {skin} + {under}")
        print(f"   Deskripsi : {rec['description'][:60]}...")
        print(f"   3 Warna Utama Pakaian: {', '.join(rec['clothing_colors_primary'])}")
        print()