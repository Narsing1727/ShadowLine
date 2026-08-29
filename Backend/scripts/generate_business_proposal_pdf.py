import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# Colors based on user's exact PPTX images
C_WHITE = colors.HexColor('#FFFFFF')
C_BLACK = colors.HexColor('#000000')
C_ACCENT_PURPLE = colors.HexColor('#9b00ff') # Vivid purple from the headers

def draw_first_page(canvas, doc):
    canvas.saveState()
    # Draw the gradient image as background
    bg_img = os.path.join(os.path.dirname(__file__), "bg_gradient.jpg")
    if os.path.exists(bg_img):
        canvas.drawImage(bg_img, 0, 0, width=doc.pagesize[0], height=doc.pagesize[1])
    else:
        # Fallback purple if image not found
        canvas.setFillColor(colors.HexColor("#7a00c2"))
        canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=1, stroke=0)
    
    # Accenture ">" Logo mark at bottom left (text approximation)
    canvas.setFont("Helvetica-Bold", 36)
    canvas.setFillColor(C_WHITE)
    canvas.drawString(40, 40, ">")
    
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(doc.pagesize[0] - 40, 40, "Copyright © 2026 Accenture. All rights reserved.")
    canvas.restoreState()

def draw_later_pages(canvas, doc):
    canvas.saveState()
    # White background (default, but let's be explicit)
    canvas.setFillColor(C_WHITE)
    canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=1, stroke=0)
    
    # Left Black Sidebar
    canvas.setFillColor(C_BLACK)
    canvas.rect(0, 0, 18, doc.pagesize[1], fill=1, stroke=0)
    
    # Bottom Black Bar
    canvas.rect(0, 0, doc.pagesize[0], 18, fill=1, stroke=0)
    
    # Footer Text
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(C_WHITE)
    canvas.drawRightString(doc.pagesize[0] - 20, 5, f"{doc.page}")
    canvas.restoreState()

def build_business_proposal_pdf(output_path: str = "ShadowLine_Detailed_Business_Proposal.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36, # shift right slightly because of the 18px left border
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    # Typography & Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=36,
        leading=42,
        textColor=C_WHITE,
        spaceAfter=12,
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        fontName='Helvetica',
        fontSize=14,
        leading=18,
        textColor=C_WHITE,
        spaceAfter=12,
    )

    h1_style = ParagraphStyle(
        'SecHeading',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=C_WHITE,
        backColor=C_ACCENT_PURPLE,
        borderPadding=(4, 6, 4, 6), # top, right, bottom, left padding for the purple block
        spaceBefore=16,
        spaceAfter=12,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=10.5,
        leading=15,
        textColor=C_BLACK,
        spaceAfter=10,
    )

    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=C_WHITE,
    )

    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=C_BLACK,
    )

    story = []
    
    # Cover (Gradient)
    story.append(Spacer(1, 200))
    story.append(Paragraph("ShadowLine", title_style))
    story.append(Paragraph("Predictive Digital Twin for Zero-Downtime Automotive Manufacturing", subtitle_style))
    story.append(Paragraph("Accenture Innovation Challenge 2026", subtitle_style))
    story.append(Spacer(1, 60))
    story.append(Paragraph("Submitted By: UpStream (IIT Roorkee)", subtitle_style))
    story.append(PageBreak())

    # Inner Pages
    story.append(Paragraph("Describe the problem statement (200 words)", h1_style))
    story.append(Paragraph(
        "A vehicle assembly line is a chain where one slow station stops everything behind it. When a station begins drifting off its take time, the effect ripples downstream for thirty or forty minutes before anyone reacts, and by then the line is already down. Unplanned downtime costs automotive plants roughly $2.3 million per hour, and each hour costs about 50% more than it did in 2019 (Siemens, 2024).",
        body_style
    ))
    story.append(Paragraph(
        "Defects behave the same way. A torque setting drifts at Station 12. Nothing fails there. The fault only surfaces at final inspection, forty minutes and thirty vehicles later. Under the widely used 'rule of ten', every stage a defect passes undetected multiplies the cost of correcting it tenfold: from seconds of rework at the station, to disassembly at end of line, to a field recall.",
        body_style
    ))
    story.append(Paragraph(
        "Plants are not short of data; they are covered in sensors and PLCs. The problem is that every tool they own is retrospective. Dashboards and MES reports describe what has already happened. Nothing tells a supervisor where the line will jam in two hours, or which station is quietly producing tomorrow's warranty claims. India built 28 million vehicles in 2024. Even singleDigit throughput and rework gains are worth crores per plant annually.",
        body_style
    ))

    # Next Section
    story.append(Paragraph("The ShadowLine Solution & ROI", h1_style))
    story.append(Paragraph(
        "ShadowLine introduces a predictive digital twin that foresees bottlenecks 2 hours in advance and traces defects back to their originating stations. Utilizing telemetry from existing PLCs without hardware additions, it guarantees a $1.66M net annual saving per line.",
        body_style
    ))

    val_data = [
        [
            Paragraph("Metric", table_header),
            Paragraph("Status Quo", table_header),
            Paragraph("ShadowLine Impact", table_header),
        ],
        [
            Paragraph("<b>Downtime Reactivity</b>", table_cell),
            Paragraph("Retrospective (lag > 20 mins)", table_cell),
            Paragraph("Predictive (120-min horizon)", table_cell),
        ],
        [
            Paragraph("<b>Defect Traceability</b>", table_cell),
            Paragraph("Final Inspection", table_cell),
            Paragraph("In-station containment", table_cell),
        ]
    ]

    val_table = Table(val_data, colWidths=[140, 180, 200])
    val_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_ACCENT_PURPLE),
        ('BOX', (0,0), (-1,-1), 1, C_BLACK),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BLACK),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F9F9F9'), colors.HexColor('#FFFFFF')]),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(val_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("Commercialization & Scale", h1_style))
    story.append(Paragraph(
        "Targeting high-volume automotive OEMs and EV Battery Gigafactories. ShadowLine is deployed as an annual SaaS subscription at $180,000 per line, integrating seamlessly with Accenture Industry X practices for broad ecosystem scale.",
        body_style
    ))

    doc.build(story, onFirstPage=draw_first_page, onLaterPages=draw_later_pages)
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    build_business_proposal_pdf()
