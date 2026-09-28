from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO

# ============================================================
# PALET WARNA PDF
# ============================================================
SAGE_GREEN    = colors.HexColor("#4a7040")
SAGE_LIGHT    = colors.HexColor("#7a9870")
SAGE_BG       = colors.HexColor("#f4f8f0")
SAGE_BORDER   = colors.HexColor("#c8dac4")
SAGE_DARK     = colors.HexColor("#2a4a28")

PRIMARY_GREEN = colors.HexColor("#3a8040")
PRIMARY_BG    = colors.HexColor("#e8f4e4")
PRIMARY_BORDER= colors.HexColor("#88c888")

DARK          = colors.HexColor("#1a2818")
GREY          = colors.HexColor("#8aa088")

WARM_COLOR    = colors.HexColor("#8a4a00")
WARM_BG       = colors.HexColor("#fffbf0")
WARM_BORDER   = colors.HexColor("#e8c878")

COOL_COLOR    = colors.HexColor("#1a3a7a")
COOL_BG       = colors.HexColor("#f0f6ff")
COOL_BORDER   = colors.HexColor("#a0c0f0")

NETRAL_COLOR  = colors.HexColor("#2a4a28")
NETRAL_BG     = colors.HexColor("#f4f8f0")
NETRAL_BORDER = colors.HexColor("#a8c8a0")

AVOID_COLOR   = colors.HexColor("#8a2010")
AVOID_BG      = colors.HexColor("#fff8f6")
AVOID_BORDER  = colors.HexColor("#f0c8c0")

LAB_COLOR     = colors.HexColor("#1a3a5a")
LAB_BG        = colors.HexColor("#f0f6ff")
LAB_BORDER    = colors.HexColor("#a0b8d8")

WHITE         = colors.white


# ============================================================
# HELPER: Warna badge undertone
# ============================================================
def get_undertone_colors(undertone):
    """
    Mengembalikan tuple (text_color, bg_color, border_color)
    sesuai kategori undertone.
    """
    ut = undertone.lower()
    if "hangat" in ut or "warm" in ut:
        return WARM_COLOR, WARM_BG, WARM_BORDER
    elif "sejuk" in ut or "dingin" in ut or "cool" in ut:
        return COOL_COLOR, COOL_BG, COOL_BORDER
    else:
        return NETRAL_COLOR, NETRAL_BG, NETRAL_BORDER


# ============================================================
# HELPER: ParagraphStyle singkat
# ============================================================
def s(name, **kw):
    base = getSampleStyleSheet()["Normal"]
    return ParagraphStyle(name, parent=base, **kw)


# ============================================================
# HELPER: Bullet list dalam cell tabel
# ============================================================
def list_cell(items, color=None, font_size=8):
    if color is None:
        color = DARK
    return Paragraph(
        "".join([f"• {i}<br/>" for i in items]),
        s("li", fontSize=font_size, textColor=color,
          fontName="Helvetica", leading=13, leftIndent=4)
    )

def primary_list_cell(items):
    return Paragraph(
        "".join([f"★ {i}<br/>" for i in items]),
        s("pri", fontSize=9, textColor=PRIMARY_GREEN,
          fontName="Helvetica-Bold", leading=16, leftIndent=4)
    )


# ============================================================
# HELPER: Box kartu info (header + konten)
# ============================================================
def info_box(label, content_para, bg, border, width=5.2*cm):
    return Table([
        [Paragraph(label, s("bl", fontSize=7.5, textColor=GREY,
                            fontName="Helvetica-Bold", alignment=TA_CENTER,
                            letterSpacing=1.5))],
        [content_para]
    ], colWidths=[width], style=TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), bg),
        ("BOX",           (0,0),(-1,-1), 1.5, border),
        ("TOPPADDING",    (0,0),(-1,0),  10),
        ("BOTTOMPADDING", (0,0),(-1,0),  6),
        ("TOPPADDING",    (0,1),(-1,1),  6),
        ("BOTTOMPADDING", (0,1),(-1,1),  12),
        ("ROUNDEDCORNERS",(0,0),(-1,-1), 8),
    ]))


# ============================================================
# FUNGSI UTAMA: GENERATE PDF
# ============================================================
def generate_pdf(skin_tone, undertone, lab_values, recommendation):
    buffer = BytesIO()
    doc    = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=2.2*cm, leftMargin=2.2*cm,
        topMargin=2*cm,     bottomMargin=2*cm
    )
    elements = []

    # ──────────────────────────────────────────────────────────
    # 1. HEADER
    # ──────────────────────────────────────────────────────────
    elements.append(Paragraph(
        "Personal Color Analysis\n\n",
        s("title", fontSize=26, textColor=DARK,
          fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=14) # Menambah jarak spasi judul
    ))
    elements.append(Paragraph(
        "Sistem Diagnosis Rona Kulit Berbasis CIELAB & K-Means Clustering",
        s("sub", fontSize=10, textColor=GREY,
          fontName="Helvetica", alignment=TA_CENTER, spaceAfter=18)
    ))
    elements.append(HRFlowable(
        width="100%", thickness=2,
        color=SAGE_GREEN, spaceAfter=0.6*cm
    ))

    # ──────────────────────────────────────────────────────────
    # 2. HASIL ANALISIS UTAMA
    # ──────────────────────────────────────────────────────────
    ut_color, ut_bg, ut_border = get_undertone_colors(undertone)

    def lab_chip(key, val):
        return Table([
            [Paragraph(key, s(f"{key}k", fontSize=7, textColor=GREY,
                              fontName="Helvetica-Bold", alignment=TA_CENTER))],
            [Paragraph(str(val), s(f"{key}v", fontSize=13,
                             textColor=SAGE_GREEN, fontName="Helvetica-Bold",
                              alignment=TA_CENTER))]
        ], colWidths=[1.55*cm], style=TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), WHITE),
            ("BOX",           (0,0),(-1,-1), 1, SAGE_BORDER),
            ("TOPPADDING",    (0,0),(-1,-1), 5),
            ("BOTTOMPADDING", (0,0),(-1,-1), 5),
            ("ROUNDEDCORNERS",(0,0),(-1,-1), 5),
        ]))

    lab_chips = Table([[
        lab_chip("L*", lab_values['L']),
        lab_chip("a*", lab_values['A']),
        lab_chip("b*", lab_values['B']),
    ]], colWidths=[1.65*cm, 1.65*cm, 1.65*cm], style=TableStyle([
        ("ALIGN",        (0,0),(-1,-1), "CENTER"),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
        ("LEFTPADDING",  (0,0),(-1,-1), 2),
        ("RIGHTPADDING", (0,0),(-1,-1), 2),
    ]))

    main_row = Table([[
        info_box("WARNA KULIT",
            Paragraph(skin_tone, s("sv", fontSize=14, textColor=SAGE_GREEN,
                                   fontName="Helvetica-Bold", alignment=TA_CENTER)),
            SAGE_BG, SAGE_BORDER, width=5.4*cm),
        info_box("UNDERTONE",
            Paragraph(undertone, s("uv", fontSize=14, textColor=ut_color,
                                   fontName="Helvetica-Bold", alignment=TA_CENTER)),
            ut_bg, ut_border, width=5.4*cm),
        info_box("MATRIKS CIELAB",
            lab_chips,
            SAGE_BG, SAGE_BORDER, width=5.4*cm),
    ]], colWidths=[5.6*cm, 5.6*cm, 5.6*cm], style=TableStyle([
        ("ALIGN",        (0,0),(-1,-1), "CENTER"),
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0),(-1,-1), 4),
        ("RIGHTPADDING", (0,0),(-1,-1), 4),
    ]))

    desc_table = Table([[
        Paragraph(
            f'"{recommendation["description"]}"',
            s("desc", fontSize=10, textColor=SAGE_LIGHT,
              fontName="Helvetica-Oblique", alignment=TA_CENTER, leading=16)
        )
    ]], colWidths=[16.8*cm], style=TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), SAGE_BG),
        ("BOX",           (0,0),(-1,-1), 1, SAGE_BORDER),
        ("TOPPADDING",    (0,0),(-1,-1), 12),
        ("BOTTOMPADDING", (0,0),(-1,-1), 12),
        ("LEFTPADDING",   (0,0),(-1,-1), 20),
        ("RIGHTPADDING",  (0,0),(-1,-1), 20),
        ("ROUNDEDCORNERS",(0,0),(-1,-1), 8),
    ]))

    elements.append(KeepTogether([
        Paragraph("Hasil Diagnosis Wajah",
                  s("sh", fontSize=12, textColor=SAGE_GREEN,
                    fontName="Helvetica-Bold", spaceAfter=10)),
        main_row,
        Spacer(1, 0.3*cm),
        desc_table,
    ]))

    elements.append(Spacer(1, 0.4*cm))
    elements.append(HRFlowable(width="100%", thickness=1,
                               color=SAGE_BORDER, spaceAfter=0.4*cm))

    # ──────────────────────────────────────────────────────────
    # 3. PENJELASAN NILAI CIELAB
    # ──────────────────────────────────────────────────────────
    L_val = lab_values['L']
    A_val = lab_values['A']
    B_val = lab_values['B']

    a_shifted = round(A_val - 128, 1)
    b_shifted = round(B_val - 128, 1)

    if L_val > 158:
        l_interpret = f"Nilai {L_val} → Kecerahan tinggi → Kategori kulit PUTIH (L* > 158)"
    elif L_val > 123:
        l_interpret = f"Nilai {L_val} → Kecerahan sedang → Kategori kulit SAWO MATANG (123 < L* ≤ 158)"
    else:
        l_interpret = f"Nilai {L_val} → Kecerahan rendah → Kategori kulit COKLAT GELAP (L* ≤ 123)"

    if a_shifted > 4:
        a_interpret = f"Nilai {A_val} → Digeser ke 0: {a_shifted:+.1f} → Kulit sedikit kemerahan → Mendukung undertone Sejuk"
    elif a_shifted < -4:
        a_interpret = f"Nilai {A_val} → Digeser ke 0: {a_shifted:+.1f} → Kulit sedikit kehijauan"
    else:
        a_interpret = f"Nilai {A_val} → Digeser ke 0: {a_shifted:+.1f} → Netral (tidak ada dominasi spektrum)"

    if b_shifted > 4:
        b_interpret = f"Nilai {B_val} → Digeser ke 0: {b_shifted:+.1f} → Kulit sedikit kekuningan/keemasan → Mendukung undertone Hangat"
    elif b_shifted < -4:
        b_interpret = f"Nilai {B_val} → Digeser ke 0: {b_shifted:+.1f} → Kulit sedikit pucat kebiruan → Mendukung undertone Sejuk"
    else:
        b_interpret = f"Nilai {B_val} → Digeser ke 0: {b_shifted:+.1f} → Netral (tidak ada dominasi spektrum)"

    lab_explain_data = [
        [
            Paragraph("Komponen", s("lh", fontSize=9, textColor=WHITE,
                                    fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph("Fungsi Komputasi", s("lh2", fontSize=9, textColor=WHITE,
                                            fontName="Helvetica-Bold", alignment=TA_LEFT)),
            Paragraph("Interpretasi Skor Ekstraksi", s("lh3", fontSize=9, textColor=WHITE,
                                                       fontName="Helvetica-Bold", alignment=TA_LEFT)),
        ],
        [
            Paragraph("L*\n(Lightness)", s("lc1", fontSize=9, textColor=LAB_COLOR,
                                           fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph("Kecerahan kulit\n(0=hitam, 255=putih)\nTitik ekuilibrium = 128",
                      s("lc2", fontSize=8, textColor=DARK, fontName="Helvetica", leading=12)),
            Paragraph(l_interpret,
                       s("lc3", fontSize=8, textColor=DARK, fontName="Helvetica", leading=12)),
        ],
        [
            Paragraph("a*\n(Merah–Hijau)", s("ac1", fontSize=9, textColor=LAB_COLOR,
                                             fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph(">128 = kemerahan\n<128 = kehijauan\nNetral = 128",
                       s("ac2", fontSize=8, textColor=DARK, fontName="Helvetica", leading=12)),
            Paragraph(a_interpret,
                       s("ac3", fontSize=8, textColor=DARK, fontName="Helvetica", leading=12)),
        ],
        [
            Paragraph("b*\n(Kuning–Biru)", s("bc1", fontSize=9, textColor=LAB_COLOR,
                                              fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph(">128 = kekuningan (warm)\n<128 = kebiruan (cool)\nNetral = 128",
                       s("bc2", fontSize=8, textColor=DARK, fontName="Helvetica", leading=12)),
            Paragraph(b_interpret,
                       s("bc3", fontSize=8, textColor=DARK, fontName="Helvetica", leading=12)),
        ],
    ]

    lab_explain_table = Table(
        lab_explain_data,
        colWidths=[3.2*cm, 4.8*cm, 8.8*cm]
    )
    lab_explain_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  LAB_COLOR),
        ("TEXTCOLOR",     (0,0),(-1,0),  WHITE),
        ("BACKGROUND",    (0,1),(-1,-1), LAB_BG),
        ("BACKGROUND",    (0,1),(0,-1),  colors.HexColor("#ddeeff")),
        ("BOX",           (0,0),(-1,-1), 1, LAB_BORDER),
        ("INNERGRID",     (0,0),(-1,-1), 0.5, LAB_BORDER),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 10),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("ALIGN",         (0,0),(0,-1),  "CENTER"),
    ]))

    elements.append(KeepTogether([
        Paragraph("Rincian Ekstraksi Matriks CIELAB",
                  s("sh2", fontSize=12, textColor=SAGE_GREEN,
                    fontName="Helvetica-Bold", spaceAfter=6)),
        Paragraph(
            "Ruang warna CIELAB memisahkan pencahayaan (L*) dari pigmen warna murni (a* dan b*). "
            "Skala komputasi diatur pada rentang 0–255, dengan ekuilibrium (titik netral) a* dan b* berada di angka 128.",
            s("note", fontSize=8.5, textColor=GREY, fontName="Helvetica-Oblique",
              leading=12, spaceAfter=8)
        ),
        lab_explain_table,
    ]))

    elements.append(Spacer(1, 0.4*cm))
    elements.append(HRFlowable(width="100%", thickness=1,
                               color=SAGE_BORDER, spaceAfter=0.4*cm))

    # ──────────────────────────────────────────────────────────
    # 4. REKOMENDASI MAKEUP
    # ──────────────────────────────────────────────────────────
    makeup_table = Table([
        [
            Paragraph("Foundation", s("mh",  fontSize=10, textColor=SAGE_GREEN, fontName="Helvetica-Bold")),
            Paragraph("Lipstik",    s("mh2", fontSize=10, textColor=SAGE_GREEN, fontName="Helvetica-Bold")),
            Paragraph("Blush On",   s("mh3", fontSize=10, textColor=SAGE_GREEN, fontName="Helvetica-Bold")),
        ],
        [
            list_cell(recommendation["foundation"]),
            list_cell(recommendation["lipstick"]),
            list_cell(recommendation["blush"]),
        ]
    ], colWidths=[6.2*cm, 4.8*cm, 5.8*cm])
    makeup_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  SAGE_BG),
        ("BACKGROUND",    (0,1),(-1,1),  WHITE),
        ("BOX",           (0,0),(-1,-1), 1, SAGE_BORDER),
        ("INNERGRID",     (0,0),(-1,-1), 0.5, SAGE_BORDER),
        ("TOPPADDING",    (0,0),(-1,-1), 10),
        ("BOTTOMPADDING", (0,0),(-1,-1), 10),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1), 12),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("NOSPLIT",       (0,0),(-1,-1)),
    ]))

    elements.append(KeepTogether([
        Paragraph("Rekomendasi Produk Kosmetik",
                  s("sh3", fontSize=12, textColor=SAGE_GREEN,
                    fontName="Helvetica-Bold", spaceAfter=10)),
        makeup_table,
    ]))

    elements.append(Spacer(1, 0.4*cm))
    elements.append(HRFlowable(width="100%", thickness=1,
                               color=SAGE_BORDER, spaceAfter=0.4*cm))

    # ──────────────────────────────────────────────────────────
    # 5. REKOMENDASI WARNA PAKAIAN & HIJAB
    # ──────────────────────────────────────────────────────────
    warna_table = Table([
        [
            Paragraph("⭐ Spektrum Utama\n(Paling Direkomendasikan)",
                      s("wh1", fontSize=10, textColor=PRIMARY_GREEN,
                        fontName="Helvetica-Bold")),
            Paragraph("✨ Spektrum Tersier",
                       s("wh2", fontSize=10, textColor=SAGE_GREEN,
                         fontName="Helvetica-Bold")),
            Paragraph("Warna Hijab",
                       s("wh3", fontSize=10, textColor=SAGE_GREEN,
                         fontName="Helvetica-Bold")),
        ],
        [
            primary_list_cell(recommendation["clothing_colors_primary"]),
            list_cell(recommendation["clothing_colors_additional"]),
            list_cell(recommendation["hijab_colors"]),
        ]
    ], colWidths=[5.6*cm, 5.6*cm, 5.6*cm])
    warna_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,0),  PRIMARY_BG),
        ("BACKGROUND",    (1,0),(2,0),  SAGE_BG),
        ("BACKGROUND",    (0,1),(0,1),  PRIMARY_BG),
        ("BACKGROUND",    (1,1),(2,1),  WHITE),
        ("BOX",           (0,0),(-1,-1), 1, SAGE_BORDER),
        ("BOX",           (0,0),(0,-1),  2, PRIMARY_BORDER),
        ("INNERGRID",     (0,0),(-1,-1), 0.5, SAGE_BORDER),
        ("TOPPADDING",    (0,0),(-1,-1), 10),
        ("BOTTOMPADDING", (0,0),(-1,-1), 10),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1), 12),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("NOSPLIT",       (0,0),(-1,-1)),
    ]))

    elements.append(KeepTogether([
        Paragraph("Rekomendasi Palet Busana & Hijab",
                  s("sh4", fontSize=12, textColor=SAGE_GREEN,
                    fontName="Helvetica-Bold", spaceAfter=10)),
        warna_table,
    ]))

    elements.append(Spacer(1, 0.4*cm))
    elements.append(HRFlowable(width="100%", thickness=1,
                               color=AVOID_BORDER, spaceAfter=0.4*cm))

    # ──────────────────────────────────────────────────────────
    # 6. WARNA YANG PERLU DIHINDARI
    # ──────────────────────────────────────────────────────────
    avoid_rows = [
        [
            Paragraph("⚠ Warna Yang Perlu Dihindari",
                       s("ah", fontSize=10, textColor=AVOID_COLOR,
                         fontName="Helvetica-Bold")),
        ],
        [
            list_cell(recommendation["colors_to_avoid"],
                      color=AVOID_COLOR, font_size=8.5),
        ]
    ]

    avoid_table = Table(avoid_rows, colWidths=[16.8*cm])
    avoid_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  AVOID_BG),
        ("BACKGROUND",    (0,1),(-1,1),  WHITE),
        ("BOX",           (0,0),(-1,-1), 1.5, AVOID_BORDER),
        ("INNERGRID",     (0,0),(-1,-1), 0.5, AVOID_BORDER),
        ("TOPPADDING",    (0,0),(-1,-1), 10),
        ("BOTTOMPADDING", (0,0),(-1,-1), 10),
        ("LEFTPADDING",   (0,0),(-1,-1), 14),
        ("RIGHTPADDING",  (0,0),(-1,-1), 14),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("NOSPLIT",       (0,0),(-1,-1)),
    ]))

    elements.append(KeepTogether([
        avoid_table,
    ]))

    elements.append(Spacer(1, 0.8*cm))

    # ──────────────────────────────────────────────────────────
    # 7. FOOTER
    # ──────────────────────────────────────────────────────────
    elements.append(HRFlowable(width="100%", thickness=1,
                               color=SAGE_BORDER, spaceAfter=0.3*cm))
    elements.append(Paragraph(
        "Laporan Personal Color Analysis  •  Sistem Otomatis Berbasis Visi Komputer",
        s("ft", fontSize=7.5, textColor=GREY, fontName="Helvetica-Bold", alignment=TA_CENTER)
    ))
    elements.append(Spacer(1, 0.15*cm))
    elements.append(Paragraph(
        "Dokumen ini dieksekusi secara otomatis oleh algoritma sistem. Hasil analisis bersifat rekomendatif.",
        s("ft3", fontSize=7.5, textColor=GREY, fontName="Helvetica", alignment=TA_CENTER)
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer