import os
import re

def update_file(filepath, is_readme=False):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Add draw_background function
    background_func = """
def draw_background(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#000000"))
    canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=1, stroke=0)
    
    # Header Accent line
    canvas.setFillColor(colors.HexColor("#A000FF"))
    canvas.rect(54, doc.pagesize[1] - 40, doc.pagesize[0] - 108, 2, fill=1, stroke=0)
    
    # Footer
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#05F2DB"))
    canvas.drawRightString(doc.pagesize[0] - 54, 34, f"Page {doc.page}")
    title = "ShadowLine | Technical Whitepaper" if is_readme else "ShadowLine | Accenture Innovation Challenge"
    canvas.drawString(54, 34, title)
    canvas.restoreState()
"""
    if "def draw_background" not in content:
        content = content.replace("class BusinessProposalCanvas(canvas.Canvas):", background_func + "\n\nclass BusinessProposalCanvas(canvas.Canvas):")
        content = content.replace("class DeepReadmeCanvas(canvas.Canvas):", background_func + "\n\nclass DeepReadmeCanvas(canvas.Canvas):")

    # 2. Update doc.build to use draw_background instead of canvasmaker (since custom canvas was drawing over background)
    content = re.sub(r'doc\.build\(story,\s*canvasmaker=.*?Canvas\)', 'doc.build(story, onFirstPage=draw_background, onLaterPages=draw_background)', content)

    # 3. Replace Theme Colors
    # General Text Colors
    content = content.replace("textColor=colors.HexColor('#0f172a')", "textColor=colors.HexColor('#A000FF')") # H1
    content = content.replace("textColor=colors.HexColor('#1e293b')", "textColor=colors.HexColor('#05F2DB')") # H2
    content = content.replace("textColor=colors.HexColor('#334155')", "textColor=colors.HexColor('#FFFFFF')") # Body / General
    content = content.replace("textColor=colors.HexColor('#475569')", "textColor=colors.HexColor('#C1A3FF')") # Subtext
    content = content.replace("textColor=colors.HexColor('#ffffff')", "textColor=colors.HexColor('#FFFFFF')") # Cover Title
    
    # Tables
    content = content.replace("colors.HexColor('#0f172a')", "colors.HexColor('#450073')") # Table Headers background
    content = content.replace("colors.HexColor('#cbd5e1')", "colors.HexColor('#A000FF')") # Table border
    content = content.replace("colors.HexColor('#e2e8f0')", "colors.HexColor('#7400C0')") # Table innergrid
    content = content.replace("[colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]", "[colors.HexColor('#000000'), colors.HexColor('#111111')]") # Table rows alternating
    
    # We might need to ensure table body text is white
    content = content.replace("textColor=colors.HexColor('#1e293b')", "textColor=colors.HexColor('#FFFFFF')") # Table bold text (if used)
    # The body text in the old script was using '#334155' and '#475569', which we converted to white and light purple.
    
    # Check if there's any specific black text hardcoded
    content = re.sub(r"colors\.black", "colors.white", content)
    
    # Cover text colors
    content = content.replace("textColor=colors.HexColor('#a5b4fc')", "textColor=colors.HexColor('#FF50A0')") # Cover Badge (was indigo)
    
    with open(filepath, 'w') as f:
        f.write(content.replace("is_readme", str(is_readme)))

update_file("Backend/scripts/generate_business_proposal_pdf.py", False)
update_file("Backend/scripts/generate_deep_readme_pdf.py", True)
print("Update complete.")
