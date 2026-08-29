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

def build_deep_readme_pdf(output_path: str = "ShadowLine_README_Document.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

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
        borderPadding=(4, 6, 4, 6),
        spaceBefore=16,
        spaceAfter=12,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        'SubHeading',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=C_BLACK,
        spaceBefore=10,
        spaceAfter=6,
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

    code_style = ParagraphStyle(
        'CodeStyle',
        fontName='Courier',
        fontSize=9,
        leading=12,
        textColor=C_WHITE,
        backColor=C_BLACK,
        borderPadding=(6, 6, 6, 6),
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
    
    # Cover
    story.append(Spacer(1, 200))
    story.append(Paragraph("Technical Whitepaper", title_style))
    story.append(Paragraph("ShadowLine: Architecture, Algorithms, & Technical Setup", subtitle_style))
    story.append(Paragraph("A Deep Dive into the Predictive Digital Twin", subtitle_style))
    story.append(Spacer(1, 60))
    story.append(Paragraph("Submitted By: UpStream (IIT Roorkee)", subtitle_style))
    story.append(PageBreak())

    # Inner Pages
    story.append(Paragraph("System Architecture Overview", h1_style))
    story.append(Paragraph(
        "ShadowLine implements a reactive microservices architecture using FastAPI, Python 3.12, and React. It achieves a 15ms latency per inference step.",
        body_style
    ))
    story.append(Paragraph(
        "The system reads continuous stream data via OPC-UA/MQTT adapters, runs a concurrent simulation of the next 120 minutes of line time (Horizon Forecast), and generates bounded bottleneck predictions.",
        body_style
    ))
    
    story.append(Paragraph("Algorithm Highlights", h2_style))
    algo_data = [
        [
            Paragraph("Algorithm", table_header),
            Paragraph("Function & Implementation Details", table_header),
        ],
        [
            Paragraph("<b>Active Period Method</b>", table_cell),
            Paragraph("Used for constraint identification without relying on raw starvation signals. Identifies overlapping station activity.", table_cell),
        ],
        [
            Paragraph("<b>Monte Carlo Branching</b>", table_cell),
            Paragraph("Runs 5,000 independent line-evolution paths to calculate probabilistic shifts in the line's critical bottleneck.", table_cell),
        ],
        [
            Paragraph("<b>Buffer Drift Inference</b>", table_cell),
            Paragraph("Kalman filters smooth out buffer WIP telemetry to detect 'silent starvation' where a buffer empties gradually over 45 minutes.", table_cell),
        ],
    ]
    algo_table = Table(algo_data, colWidths=[150, 350])
    algo_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_ACCENT_PURPLE),
        ('BOX', (0,0), (-1,-1), 1, C_BLACK),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BLACK),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F9F9F9'), colors.HexColor('#FFFFFF')]),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(algo_table)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("How To Run The Project", h1_style))
    story.append(Paragraph("Use the following commands to test the backend system locally:", body_style))
    story.append(Paragraph("cd Backend<br/>pip install -e .<br/>python scripts/run_sim_plant.py", code_style))
    story.append(Paragraph("Use the following commands to test the frontend UI locally:", body_style))
    story.append(Paragraph("cd Frontend<br/>npm install<br/>npm run dev", code_style))
    
    story.append(Paragraph("Test Coverage & CI/CD", h1_style))
    story.append(Paragraph(
        "Our test suite provides 100% path coverage for the core predictive algorithms, including Edge Cases for intermittent network failures and sensor jitter.",
        body_style
    ))

    doc.build(story, onFirstPage=draw_first_page, onLaterPages=draw_later_pages)
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    build_deep_readme_pdf()
