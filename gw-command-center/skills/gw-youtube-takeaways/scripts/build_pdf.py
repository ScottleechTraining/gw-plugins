#!/usr/bin/env python3
"""
GW Video Takeaways — PDF builder.

Usage:
    python build_pdf.py <input.json> <output.pdf>

The input JSON has this shape:

    {
      "title": "YouTube Videos Notebook — V3",
      "subtitle": "Per-video takeaways and 10x business insights for Scott Leech<br/>Source: ...",
      "intro": "This report breaks down...",
      "videos": [
        {
          "n": 1,
          "title": "...",
          "creator": "...",
          "takeaways": ["...", "..."],
          "tenx": "...",
          "watch": "..."
        }
      ],
      "summary": {
        "themes_html": "...",
        "priority_rows": [
          ["Watch first", "1 — ...", "Why..."],
          ...
        ],
        "cross_video_html": "..."
      },
      "signoff": "Keep the Fire Burning,<br/>Leech"
    }

The script applies GW brand styling, paginates, and writes the PDF.
"""

import json
import sys
from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether,
)


GW_RED = HexColor("#9E1B1B")
GW_BLACK = HexColor("#111111")
GW_GRAY = HexColor("#3A3A3A")
GW_LIGHT = HexColor("#F2EFEA")


def make_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="GWTitle", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=24, textColor=GW_BLACK, leading=28, spaceAfter=8, alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        name="GWSubtitle", parent=styles["Normal"], fontName="Helvetica",
        fontSize=11, textColor=GW_GRAY, leading=14, spaceAfter=18, alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        name="VideoHeader", parent=styles["Heading1"], fontName="Helvetica-Bold",
        fontSize=15, textColor=GW_RED, leading=18, spaceBefore=14, spaceAfter=2, keepWithNext=1,
    ))
    styles.add(ParagraphStyle(
        name="VideoSubheader", parent=styles["Normal"], fontName="Helvetica-Oblique",
        fontSize=10, textColor=GW_GRAY, leading=12, spaceAfter=10,
    ))
    styles.add(ParagraphStyle(
        name="SectionLabel", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=10.5, textColor=GW_BLACK, leading=13, spaceBefore=6, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="BodyTake", parent=styles["Normal"], fontName="Helvetica",
        fontSize=10, textColor=GW_BLACK, leading=13, leftIndent=14, bulletIndent=0, spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        name="TenX", parent=styles["Normal"], fontName="Helvetica",
        fontSize=10, textColor=GW_BLACK, leading=13.5, leftIndent=8, rightIndent=8,
        spaceBefore=4, spaceAfter=6, backColor=GW_LIGHT, borderPadding=8,
    ))
    styles.add(ParagraphStyle(
        name="Verdict", parent=styles["Normal"], fontName="Helvetica",
        fontSize=10, textColor=GW_BLACK, leading=13, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="SectionH", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=14, textColor=GW_BLACK, leading=17, spaceBefore=14, spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="Body", parent=styles["Normal"], fontName="Helvetica",
        fontSize=10.5, textColor=GW_BLACK, leading=14, spaceAfter=6,
    ))

    return styles


def build_pdf(data, output_path):
    styles = make_styles()

    doc = SimpleDocTemplate(
        output_path,
        pagesize=LETTER,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title=data.get("title", "GW Video Takeaways"),
        author="Gridiron Warrior",
    )

    story = []

    # Cover
    story.append(Paragraph(data["title"], styles["GWTitle"]))
    if data.get("subtitle"):
        story.append(Paragraph(data["subtitle"], styles["GWSubtitle"]))
    if data.get("intro"):
        story.append(Paragraph(data["intro"], styles["Body"]))
        story.append(Spacer(1, 6))

    # Per-video sections
    for v in data["videos"]:
        block = []
        block.append(Paragraph(f"Video {v['n']}: {v['title']}", styles["VideoHeader"]))
        block.append(Paragraph(f"Creator: {v['creator']}", styles["VideoSubheader"]))
        block.append(Paragraph("Takeaways", styles["SectionLabel"]))
        for i, t in enumerate(v["takeaways"], 1):
            block.append(Paragraph(f"{i}. {t}", styles["BodyTake"]))
        block.append(Paragraph("The 10x Move for GW", styles["SectionLabel"]))
        block.append(Paragraph(v["tenx"], styles["TenX"]))
        block.append(Paragraph("Watch the full video?", styles["SectionLabel"]))
        block.append(Paragraph(v["watch"], styles["Verdict"]))

        # Keep the header + subheader + first label together so we don't get
        # an orphan red header at the bottom of a page
        story.append(KeepTogether(block[:3]))
        for p in block[3:]:
            story.append(p)
        story.append(Spacer(1, 10))

    # Final summary on a new page
    summary = data.get("summary", {})
    if summary:
        story.append(PageBreak())
        story.append(Paragraph("Final Summary", styles["GWTitle"]))
        if summary.get("subtitle"):
            story.append(Paragraph(summary["subtitle"], styles["GWSubtitle"]))

        if summary.get("themes_html"):
            story.append(Paragraph("Themes", styles["SectionH"]))
            story.append(Paragraph(summary["themes_html"], styles["Body"]))

        if summary.get("priority_rows"):
            story.append(Paragraph("Watch Priority", styles["SectionH"]))
            rows = [["Tier", "Video", "Why"]] + summary["priority_rows"]
            t = Table(rows, colWidths=[1.0 * inch, 2.5 * inch, 3.5 * inch], repeatRows=1)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), GW_BLACK),
                ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#FFFFFF")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 9.5),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#FFFFFF"), HexColor("#F7F4EE")]),
                ("LINEBELOW", (0, 0), (-1, 0), 0.5, GW_BLACK),
                ("LINEBELOW", (0, -1), (-1, -1), 0.5, GW_BLACK),
            ]))
            story.append(t)

        if summary.get("cross_video_html"):
            story.append(Spacer(1, 14))
            story.append(Paragraph("The Highest-Leverage Move Across All Videos", styles["SectionH"]))
            story.append(Paragraph(summary["cross_video_html"], styles["Body"]))

    # Signoff
    story.append(Spacer(1, 18))
    story.append(Paragraph(data.get("signoff", "Keep the Fire Burning,<br/>Leech"), styles["Body"]))

    doc.build(story)
    return output_path


def main():
    if len(sys.argv) != 3:
        print("Usage: python build_pdf.py <input.json> <output.pdf>", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    data = json.loads(input_path.read_text(encoding="utf-8"))
    build_pdf(data, str(output_path))
    print(f"PDF written to: {output_path}")


if __name__ == "__main__":
    main()
