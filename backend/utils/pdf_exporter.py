"""
utils/pdf_exporter.py — Génération du CDC en format PDF

Produit un PDF professionnel avec :
  - Page de garde
  - En-tête et pied de page sur chaque page
  - Toutes les sections du CDC
  - Tableau des exigences coloré
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, PageBreak, HRFlowable, KeepTogether
)

# ── Couleurs ──────────────────────────────────────────────────────────────────
BLUE       = colors.HexColor("#1B4F8A")
LIGHT_BLUE = colors.HexColor("#D5E8F5")
DARK_GRAY  = colors.HexColor("#2C2C2C")
MED_GRAY   = colors.HexColor("#555555")
LIGHT_GRAY = colors.HexColor("#F5F5F5")
WHITE      = colors.white
RED_BG     = colors.HexColor("#FFF0F0")
RED_TEXT   = colors.HexColor("#C53030")
AMBER_BG   = colors.HexColor("#FFFBEA")
AMBER_TEXT = colors.HexColor("#B7791F")
GREEN_BG   = colors.HexColor("#F0FDF4")
GREEN_TEXT = colors.HexColor("#276749")

W, H       = A4
MARGIN     = 2.2 * cm
CONTENT_W  = W - 2 * MARGIN
OUTPUT_DIR = "/tmp/systemreq_exports"


# ── Styles ────────────────────────────────────────────────────────────────────
def make_styles():
    return {
        "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13,
                             textColor=BLUE, spaceBefore=14, spaceAfter=4),
        "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11,
                             textColor=DARK_GRAY, spaceBefore=10, spaceAfter=4),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.5,
                               textColor=MED_GRAY, leading=14, spaceAfter=4,
                               alignment=TA_JUSTIFY),
        "cover_title": ParagraphStyle("ct", fontName="Helvetica-Bold", fontSize=26,
                                      textColor=BLUE, alignment=TA_CENTER, spaceAfter=8),
        "cover_sub": ParagraphStyle("cs", fontName="Helvetica", fontSize=12,
                                    textColor=MED_GRAY, alignment=TA_CENTER, spaceAfter=6),
        "cover_ref": ParagraphStyle("cr", fontName="Helvetica", fontSize=9,
                                    textColor=MED_GRAY, alignment=TA_CENTER),
    }


# ── En-tête et pied de page ───────────────────────────────────────────────────
def make_page_template(client_name, ref, date_str):
    def on_page(canvas, doc):
        canvas.saveState()

        # Header
        canvas.setFillColor(BLUE)
        canvas.rect(MARGIN, H - 1.4 * cm, CONTENT_W, 0.65 * cm, fill=1, stroke=0)
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.drawString(MARGIN + 6, H - 1.08 * cm, "EPS SARL")
        canvas.setFont("Helvetica", 7.5)
        canvas.drawRightString(MARGIN + CONTENT_W - 6, H - 1.08 * cm,
                               f"Réf. {ref}  ·  {date_str}")

        # Footer
        canvas.setFillColor(LIGHT_GRAY)
        canvas.rect(MARGIN, 0.7 * cm, CONTENT_W, 0.55 * cm, fill=1, stroke=0)
        canvas.setFillColor(MED_GRAY)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawCentredString(W / 2, 0.92 * cm,
                                 f"Cahier des charges — {client_name}  ·  Page {doc.page}")

        canvas.restoreState()

    return on_page


# ── Export principal ──────────────────────────────────────────────────────────
async def export_to_pdf(cdc: dict) -> str:
    """
    Génère le fichier PDF et retourne son chemin.

    Args:
        cdc : dict complet issu du GeneratorAgent

    Returns:
        str : chemin absolu vers le fichier .pdf généré
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    session_id   = cdc.get("session_id", "unknown")
    client_name  = cdc.get("client_name", "Client")
    project_name = cdc.get("project_name", "Projet web")
    services     = ", ".join(cdc.get("services", []))
    budget       = cdc.get("budget", "N/A")
    sections     = cdc.get("sections", [])
    requirements = cdc.get("requirements", [])
    date_str     = datetime.now().strftime("%d/%m/%Y")
    ref          = f"CDC-{session_id[:6].upper()}"

    filename = f"CDC_{client_name.replace(' ', '_')}_{session_id[:6]}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    S  = make_styles()
    on_page = make_page_template(client_name, ref, date_str)

    doc = SimpleDocTemplate(
        filepath, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=2 * cm, bottomMargin=2 * cm,
    )

    story = []

    # ── Page de garde ─────────────────────────────────────────────────────────
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph("EPS SARL", ParagraphStyle(
        "eps", fontName="Helvetica-Bold", fontSize=11,
        textColor=BLUE, alignment=TA_CENTER)))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("CAHIER DES CHARGES PRÉLIMINAIRE", S["cover_title"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=2, color=LIGHT_BLUE,
                             spaceAfter=12))
    story.append(Paragraph(f"Client : {client_name}", S["cover_sub"]))
    story.append(Paragraph(f"Services : {services}", S["cover_sub"]))
    story.append(Paragraph(f"Budget : {budget} EUR  ·  {date_str}", S["cover_sub"]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(f"Réf. {ref}", S["cover_ref"]))
    story.append(PageBreak())

    # ── Informations client ───────────────────────────────────────────────────
    story.append(Paragraph("1. Informations du client", S["h1"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1.5, color=BLUE, spaceAfter=8))

    info_data = [
        ["Champ", "Valeur"],
        ["Nom & Prénom",  client_name],
        ["Email",         cdc.get("email", "—")],
        ["Téléphone",     cdc.get("telephone", "—")],
        ["Ville / Pays",  f"{cdc.get('ville', '')} — {cdc.get('pays', '')}"],
        ["Budget",        f"{budget} EUR"],
        ["Services",      services],
        ["Référence",     ref],
    ]

    info_table = Table(info_data, colWidths=[4 * cm, CONTENT_W - 4 * cm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  BLUE),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0),  9),
        ("BACKGROUND",    (0, 1), (0, -1),  LIGHT_BLUE),
        ("FONTNAME",      (0, 1), (0, -1),  "Helvetica-Bold"),
        ("TEXTCOLOR",     (0, 1), (0, -1),  BLUE),
        ("FONTNAME",      (1, 1), (1, -1),  "Helvetica"),
        ("FONTSIZE",      (0, 1), (-1, -1), 9),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, colors.HexColor("#EFF6FC")]),
        ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.5 * cm))

    # ── Sections du CDC ───────────────────────────────────────────────────────
    for section in sections:
        block = []
        block.append(Paragraph(section.get("title", ""), S["h1"]))
        block.append(HRFlowable(width=CONTENT_W, thickness=1, color=LIGHT_BLUE,
                                 spaceAfter=6))
        content = section.get("content", "")
        for line in content.split("\n"):
            if line.strip():
                block.append(Paragraph(line.strip(), S["body"]))
        block.append(Spacer(1, 0.4 * cm))
        story.append(KeepTogether(block))

    story.append(PageBreak())

    # ── Tableau des exigences ─────────────────────────────────────────────────
    story.append(Paragraph("Tableau des exigences", S["h1"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1.5, color=BLUE, spaceAfter=8))

    if requirements:
        req_data = [["ID", "Description", "Catégorie", "Priorité", "MoSCoW"]]
        for req in requirements:
            req_data.append([
                req.get("id", ""),
                req.get("description", ""),
                req.get("category", ""),
                req.get("priority", ""),
                req.get("moscow", ""),
            ])

        col_widths = [1.4*cm, 8.5*cm, 2.5*cm, 2*cm, 1.8*cm]
        req_table  = Table(req_data, colWidths=col_widths, repeatRows=1)

        table_style = [
            ("BACKGROUND",    (0, 0), (-1, 0),  BLUE),
            ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
            ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",      (0, 0), (-1, 0),  8.5),
            ("ALIGN",         (0, 0), (-1, 0),  "CENTER"),
            ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE",      (0, 1), (-1, -1), 8.5),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING",    (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING",   (0, 0), (-1, -1), 6),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
            ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
            ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, colors.HexColor("#F7F7F5")]),
        ]

        # Couleurs priorité
        for i, req in enumerate(requirements, start=1):
            p = req.get("priority", "")
            if p == "Haute":
                table_style.append(("BACKGROUND", (3, i), (3, i), RED_BG))
                table_style.append(("TEXTCOLOR",  (3, i), (3, i), RED_TEXT))
            elif p == "Moyenne":
                table_style.append(("BACKGROUND", (3, i), (3, i), AMBER_BG))
                table_style.append(("TEXTCOLOR",  (3, i), (3, i), AMBER_TEXT))
            else:
                table_style.append(("BACKGROUND", (3, i), (3, i), GREEN_BG))
                table_style.append(("TEXTCOLOR",  (3, i), (3, i), GREEN_TEXT))

        req_table.setStyle(TableStyle(table_style))
        story.append(req_table)

    # ── Build ─────────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return filepath