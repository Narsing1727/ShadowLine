"""Generate an executive, commercially focused Business Proposal PDF for Accenture Innovation Challenge."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas


def draw_decorations(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#000000"))
    canvas.drawRightString(doc.pagesize[0] - 54, 34, f"Page {doc.page}")
    canvas.restoreState()


def build_business_proposal_pdf(output_path: str = "ShadowLine_Detailed_Business_Proposal.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Typography & Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=colors.HexColor('#000000'),
        spaceAfter=12,
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#FFFFFF'),
        spaceAfter=10,
    )

    badge_style = ParagraphStyle(
        'CoverBadge',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#FFFFFF'),
        spaceAfter=8,
    )

    h1_style = ParagraphStyle(
        'SecHeading',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#FFFFFF'),
        backColor=colors.HexColor('#A000FF'),
        borderPadding=(6, 10, 6, 10),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        'SubHeading',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#000000'),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#000000'),
        spaceAfter=5,
        alignment=4,  # Justified
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#FFFFFF'),
        backColor=colors.HexColor('#A000FF'),
        borderPadding=(6, 10, 6, 10),
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor('#FFFFFF'),
    )

    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#FFFFFF'),
    )

    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor('#000000'),
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor('#000000'),
    )

    story = []

    # ==================== 1. EXECUTIVE COVER BANNER ====================
    cover_data = [
        [
            Paragraph("ACCENTURE INNOVATION CHALLENGE 2026 - BUSINESS PROPOSAL", badge_style)
        ],
        [
            Paragraph("ShadowLine: Enterprise Predictive Digital Twin", title_style)
        ],
        [
            Paragraph("Transforming Automotive Assembly from Reactive Crisis Management to 4-Hour Proactive Foresight & Zero-Downtime Operations.", subtitle_style)
        ],
        [
            Table([
                [
                    Paragraph("<b>CATEGORY:</b> DigitalTwin.ai", callout_style),
                    Paragraph("<b>PAYBACK:</b> 2.3 Months", callout_style),
                    Paragraph("<b>NET SAVINGS:</b> $1.66M/yr/Line", callout_style),
                    Paragraph("<b>3-YR ROI:</b> 418% Net Return", callout_style),
                ]
            ], colWidths=[120, 110, 130, 144], style=[
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#F5EBFF')),
            ])
        ]
    ]

    cover_table = Table(cover_data, colWidths=[504])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#A000FF')),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 16),
        ('RIGHTPADDING', (0, 0), (-1, -1), 16),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 8))

    # ==================== 2. EXECUTIVE SUMMARY & PROBLEM FRAMING ====================
    story.append(Paragraph("1. Executive Summary & Market Opportunity", h1_style))
    story.append(Paragraph(
        "Global automotive manufacturers operate in a hyper-competitive, low-margin environment where vehicle assembly lines run at high velocity (<b>58-second takt time</b>, producing <b>60–65 Jobs Per Hour</b>). In this environment, <b>unplanned downtime costs $24,000 to $36,000 per hour ($400–$600/minute)</b>, and late-detected quality defects risk catastrophic multi-million-dollar vehicle warranty recalls.",
        body_style
    ))
    story.append(Paragraph(
        "Existing factory solutions fail plant leadership because they are <b>purely retrospective</b> (SCADA/MES logs report stoppages after the line is already stopped) or <b>operationally unviable</b> (3D visual CAD models that look impressive but offer no forward predictions, or black-box AI that triggers constant false alarms and risks halting live PLCs).",
        body_style
    ))
    story.append(Paragraph(
        "<b>ShadowLine</b> bridges this gap by delivering an enterprise predictive digital twin that runs continuously <b>4 hours ahead of physical assembly</b>. By providing plant managers and floor supervisors with calibrated, proactive foresight, ShadowLine eliminates bottlenecks before buffers fill, isolates quality defects at the originating station, and delivers <b>$1,656,000 in net annual savings per line with a 2.3-month payback period</b>.",
        body_style
    ))

    # KPI Metric Cards
    kpi_data = [
        [
            Paragraph("<b>$1.66M / yr</b><br/><font color='#FFE600' size='6.5'>NET ANNUAL SAVINGS</font><br/><font color='#FFFFFF' size='6'>Per 42-Station Assembly Line</font>", callout_style),
            Paragraph("<b>2.32 Months</b><br/><font color='#FFE600' size='6.5'>CAPITAL PAYBACK</font><br/><font color='#FFFFFF' size='6'>~70 Production Days</font>", callout_style),
            Paragraph("<b>418%</b><br/><font color='#FFE600' size='6.5'>3-YEAR PROJECT ROI</font><br/><font color='#FFFFFF' size='6'>EBITDA Contribution</font>", callout_style),
            Paragraph("<b>&le; 6 / hr</b><br/><font color='#FFE600' size='6.5'>EEMUA 191 BUDGET</font><br/><font color='#FFFFFF' size='6'>Zero Alarm Fatigue</font>", callout_style),
        ]
    ]
    kpi_table = Table(kpi_data, colWidths=[126, 126, 126, 126])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#A000FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#000000')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 6))

    # ==================== 3. PRODUCT VALUE PROPOSITION ====================
    story.append(Paragraph("2. Strategic Value Proposition: The 4-Hour Advantage", h1_style))
    story.append(Paragraph(
        "ShadowLine creates value through three high-impact operational pillars:",
        body_style
    ))

    val_data = [
        [
            Paragraph("Strategic Pillar", table_header),
            Paragraph("Traditional Manufacturing Approach", table_header),
            Paragraph("ShadowLine Predictive Transformation", table_header),
            Paragraph("Business Benefit", table_header),
        ],
        [
            Paragraph("<b>1. Proactive Bottleneck Prevention</b>", table_cell_bold),
            Paragraph("Reacts once intermediate buffers are completely full and upstream stations starve.", table_cell),
            Paragraph("Forks factory state every 60s to simulate the next 4 hours, identifying wandering bottlenecks 1–2 hours before occurrence.", table_cell),
            Paragraph("<b>40% Downtime Reduction</b> ($1.15M recovered per year).", table_cell_bold),
        ],
        [
            Paragraph("<b>2. Latent Defect Containment</b>", table_cell_bold),
            Paragraph("Defects introduced in E-Coat or Welding are found 30 min later at vision tunnels; 30+ cars contaminated.", table_cell),
            Paragraph("Traces defect causality backward to the origin station and instantly isolates all in-flight downstream VINs.", table_cell),
            Paragraph("<b>80% Defect Containment</b> at station gate; avoids recalls.", table_cell_bold),
        ],
        [
            Paragraph("<b>3. Zero-Risk Non-Intrusive Deploy</b>", table_cell_bold),
            Paragraph("Modifying PLC ladder logic risks catastrophic shutdowns and safety violations during production.", table_cell),
            Paragraph("Operates purely as a passive, read-only observer outside the OT control perimeter (IEC 62443 Zone 3).", table_cell),
            Paragraph("<b>Zero Production Interruption</b>; no PLC re-programming.", table_cell_bold),
        ],
    ]

    val_table = Table(val_data, colWidths=[110, 130, 164, 100])
    val_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#A000FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#000000')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#F5EBFF')]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(val_table)

    story.append(PageBreak())

    # ==================== 4. MULTI-STAKEHOLDER USER JOURNEYS ====================
    story.append(Paragraph("3. Target Stakeholders & User Experience", h1_style))
    story.append(Paragraph(
        "Different manufacturing leaders require different perspectives from the digital twin. ShadowLine provides three tailored user experiences powered by the same underlying model:",
        body_style
    ))

    stake_data = [
        [
            Paragraph("Stakeholder Persona", table_header),
            Paragraph("Key Responsibilities & Pain Points", table_header),
            Paragraph("ShadowLine Experience & Key Features", table_header),
            Paragraph("Empowered Business Decision", table_header),
        ],
        [
            Paragraph("<b>Floor Supervisor</b><br/><font color='#64748b' size='6'>Operational (Real-time)</font>", table_cell_bold),
            Paragraph("Meeting hourly takt targets, preventing line stoppages, avoiding alarm overload.", table_cell),
            Paragraph("• Real-time 42-station interactive line map.<br/>• +1h/+2h/+4h forward projection toggle.<br/>• Ranked alert queue capped at &le;6/hr.<br/>• 1-Click Acknowledge / Snooze / Feedback.", table_cell),
            Paragraph("Rebalances operator pacing at Station S-14 before Buffer B-13 backs up, preserving shift JPH.", table_cell),
        ],
        [
            Paragraph("<b>Plant Operations Manager</b><br/><font color='#64748b' size='6'>Tactical (Shift / Weekly)</font>", table_cell_bold),
            Paragraph("Overall Equipment Effectiveness (OEE), scrap rates, shift handover reviews.", table_cell),
            Paragraph("• OEE breakdown (Availability &times; Perf &times; Qual).<br/>• Bottleneck history and root-cause Pareto.<br/>• Defect propagation graph & VIN quarantine.<br/>• Shift replay simulation analyzer.", table_cell),
            Paragraph("Identifies recurring thermal drift on paint bake oven and schedules targeted maintenance during lunch window.", table_cell),
        ],
        [
            Paragraph("<b>VP Manufacturing / Corporate</b><br/><font color='#64748b' size='6'>Strategic (Quarterly / Capex)</font>", table_cell_bold),
            Paragraph("Capex allocation, multi-plant scaling, corporate EBITDA, payback velocity.", table_cell),
            Paragraph("• Monetary ROI and payback ledger.<br/>• Multi-plant line portfolio tracker.<br/>• Unsupervised automated line onboarding.<br/>• Sensor retrofit investment calculator.", table_cell),
            Paragraph("Approves multi-site expansion across 4 assembly plants based on verified 2.3-month payback.", table_cell),
        ],
    ]

    stake_table = Table(stake_data, colWidths=[105, 125, 160, 114])
    stake_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#A000FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#000000')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#F5EBFF')]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(stake_table)
    story.append(Spacer(1, 8))

    # ==================== 5. FINANCIAL BUSINESS CASE & 3-YEAR PROJECTIONS ====================
    story.append(Paragraph("4. Quantified Financial Business Case & Economic Model", h1_style))
    story.append(Paragraph(
        "The financial model evaluates a reference 42-station mixed-model vehicle assembly line operating 2 shifts per day across 250 production days (4,000 operating hours per year) targeting 248,000 vehicles annually:",
        body_style
    ))

    fin_data = [
        [
            Paragraph("Financial Value Category", table_header),
            Paragraph("Annual Baseline Loss (Status Quo)", table_header),
            Paragraph("ShadowLine Predictive Recovery", table_header),
            Paragraph("Net Annual Savings", table_header),
        ],
        [
            Paragraph("<b>1. Unplanned Downtime Avoidance</b>", table_cell_bold),
            Paragraph("120 hours/year @ $24,000/hr = <b>$2,880,000</b>", table_cell),
            Paragraph("40% downtime reduction via proactive bottleneck warning (48 hrs saved)", table_cell),
            Paragraph("<b>+$1,152,000 / yr</b>", table_cell_bold),
        ],
        [
            Paragraph("<b>2. In-Plant Defect Rework Reduction</b>", table_cell_bold),
            Paragraph("1,600 defect units @ $450/unit = <b>$720,000</b>", table_cell),
            Paragraph("35% scrap reduction via early process drift detection", table_cell),
            Paragraph("<b>+$252,000 / yr</b>", table_cell_bold),
        ],
        [
            Paragraph("<b>3. Latent Defect Containment & Recall Avoidance</b>", table_cell_bold),
            Paragraph("45 escape cases @ $12,000/unit risk = <b>$540,000</b>", table_cell),
            Paragraph("80% containment via automated station gate VIN quarantine", table_cell),
            Paragraph("<b>+$432,000 / yr</b>", table_cell_bold),
        ],
        [
            Paragraph("<b>GROSS ANNUAL VALUE CREATION</b>", table_cell_bold),
            Paragraph("<b>$4,140,000 Total Losses</b>", table_cell),
            Paragraph("<b>Efficiency & Scrap Recovery</b>", table_cell),
            Paragraph("<b>+$1,836,000 / yr</b>", table_cell_bold),
        ],
        [
            Paragraph("Annual Software & Cloud Infrastructure OPEX", table_cell),
            Paragraph("—", table_cell),
            Paragraph("Telemetry pipeline, cloud compute, and dedicated support", table_cell),
            Paragraph("-$180,000 / yr", table_cell),
        ],
        [
            Paragraph("<b>NET ANNUAL EBITDA CONTRIBUTION</b>", table_cell_bold),
            Paragraph("—", table_cell),
            Paragraph("<b>Net Bottom-Line Impact (Single Line)</b>", table_cell),
            Paragraph("<b>+$1,656,000 / yr</b>", table_cell_bold),
        ],
    ]

    fin_table = Table(fin_data, colWidths=[140, 130, 130, 104])
    fin_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#A000FF')),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#eef2ff')),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor('#dcfce7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#000000')),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))
    story.append(fin_table)

    # 3-Year Pro Forma Table
    pro_forma_data = [
        [
            Paragraph("3-Year Pro Forma Metric", table_header),
            Paragraph("Year 1 (1 Pilot Line)", table_header),
            Paragraph("Year 2 (4 Plant Lines)", table_header),
            Paragraph("Year 3 (10 Fleet Lines)", table_header),
        ],
        [
            Paragraph("Gross Value Delivered", table_cell_bold),
            Paragraph("$1,836,000", table_cell),
            Paragraph("$7,344,000", table_cell),
            Paragraph("$18,360,000", table_cell),
        ],
        [
            Paragraph("Total Implementation CAPEX & OPEX", table_cell_bold),
            Paragraph("$500,000 ($320k Capex + $180k Opex)", table_cell),
            Paragraph("$1,220,000 ($500k Capex + $720k Opex)", table_cell),
            Paragraph("$2,500,000 ($700k Capex + $1.8M Opex)", table_cell),
        ],
        [
            Paragraph("<b>Net Cumulative Value Created</b>", table_cell_bold),
            Paragraph("<b>$1,336,000</b>", table_cell_bold),
            Paragraph("<b>$7,460,000</b>", table_cell_bold),
            Paragraph("<b>$23,320,000</b>", table_cell_bold),
        ],
    ]
    pro_table = Table(pro_forma_data, colWidths=[150, 118, 118, 118])
    pro_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#A000FF')),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#000000')),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))
    story.append(pro_table)

    story.append(PageBreak())

    # ==================== 6. COMMERCIALIZATION & GTM ====================
    story.append(Paragraph("5. Commercialization & Go-To-Market (GTM) Strategy", h1_style))
    story.append(Paragraph(
        "ShadowLine’s commercialization model combines rapid software deployment with scalable recurring revenue:",
        body_style
    ))

    gtm_data = [
        [
            Paragraph("GTM Element", table_header),
            Paragraph("Strategic Approach", table_header),
            Paragraph("Commercial Model & Details", table_header),
        ],
        [
            Paragraph("<b>Target Customer Segments</b>", table_cell_bold),
            Paragraph("1. High-Volume Automotive OEMs (Body, Paint, Assembly).<br/>2. EV Battery & Vehicle Gigafactories.<br/>3. Heavy Machinery & Aerospace Assembly Plants.", table_cell),
            Paragraph("Initial focus on high-velocity lines where 1 minute of downtime exceeds $400.", table_cell),
        ],
        [
            Paragraph("<b>Pricing & Packaging</b>", table_cell_bold),
            Paragraph("<b>Tiered Annual SaaS Subscription:</b><br/>• <i>Plant Line License:</i> $180,000 / line / year.<br/>• <i>Enterprise Fleet Tier (5+ Lines):</i> $140,000 / line / year.<br/>• <i>One-time Onboarding & Discovery:</i> $80,000 / line.", table_cell),
            Paragraph("Predictable subscription pricing yielding >80% recurring software gross margins.", table_cell),
        ],
        [
            Paragraph("<b>Accenture Channel Synergy</b>", table_cell_bold),
            Paragraph("Strategic alliance with <b>Accenture Industry X & Digital Manufacturing Practice</b> to deliver ShadowLine as part of enterprise smart manufacturing transformation contracts.", table_cell),
            Paragraph("Leverages Accenture's global systems integration relationships across GM, BMW, Toyota, and Stellantis.", table_cell),
        ],
    ]

    gtm_table = Table(gtm_data, colWidths=[120, 210, 174])
    gtm_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#A000FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#000000')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#F5EBFF')]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(gtm_table)
    story.append(Spacer(1, 8))

    # ==================== 7. PHASED ROLLOUT ROADMAP ====================
    story.append(Paragraph("6. Phased 24-Week Implementation Roadmap", h1_style))

    road_data = [
        [
            Paragraph("Phase & Timeline", table_header),
            Paragraph("Key Activities & Operational Milestones", table_header),
            Paragraph("Business Exit Gate", table_header),
        ],
        [
            Paragraph("<b>Phase 1: Shadow Deployment</b><br/>Weeks 1–8", table_cell_bold),
            Paragraph("• Unidirectional telemetry connection to plant OPC-UA/MQTT.<br/>• Automated discovery of line topology, sequence, and buffers.<br/>• Fitting soft-sensor models on uninstrumented stations.", table_cell),
            Paragraph("100% telemetry uptime; Zero production disruption.", table_cell),
        ],
        [
            Paragraph("<b>Phase 2: Validation Gate</b><br/>Weeks 9–16", table_cell_bold),
            Paragraph("• Model runs in silent shadow mode logging predictions.<br/>• Retrospective scoring against actual shift stoppages.<br/>• Formal qualification through automated Promotion Gate.", table_cell),
            Paragraph("Verified Precision &ge; 80%, False Alarm Rate &le; 15%.", table_cell),
        ],
        [
            Paragraph("<b>Phase 3: Live Assisted Ops</b><br/>Weeks 17–20", table_cell_bold),
            Paragraph("• Roll out Floor Supervisor and Plant Manager dashboards.<br/>• Activate EEMUA 191 alarm budget caps (&le;6/hr).<br/>• Enable 1-click operator feedback and VIN quarantine.", table_cell),
            Paragraph("Operator alert acceptance > 85%; Mean lead time &ge; 30m.", table_cell),
        ],
        [
            Paragraph("<b>Phase 4: Enterprise Scale</b><br/>Weeks 21–24", table_cell_bold),
            Paragraph("• Expand to sister assembly lines and body/paint shops.<br/>• Deploy corporate multi-plant portfolio dashboard.", table_cell),
            Paragraph("Standardized line onboarding &le; 10 days per new line.", table_cell),
        ],
    ]

    road_table = Table(road_data, colWidths=[110, 244, 150])
    road_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#A000FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#000000')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#F5EBFF')]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(road_table)
    story.append(Spacer(1, 8))

    # ==================== 8. RISK ASSESSMENT & CONCLUSION ====================
    story.append(Paragraph("7. Strategic Risk Assessment & Governance", h1_style))

    risk_data = [
        [
            Paragraph("Risk Factor", table_header),
            Paragraph("Impact", table_header),
            Paragraph("Mitigation Strategy", table_header),
        ],
        [
            Paragraph("<b>Operator Alarm Fatigue</b>", table_cell_bold),
            Paragraph("High", table_cell),
            Paragraph("Strict EEMUA 191 limit of &le;6 alerts/hr + 5-minute chatter cooldown + Probability Calibration.", table_cell),
        ],
        [
            Paragraph("<b>Sensor Data Drop / Network Gap</b>", table_cell_bold),
            Paragraph("Medium", table_cell),
            Paragraph("Soft-sensor virtual metrology fallback instantly estimates cycle times using adjacent buffer fill levels.", table_cell),
        ],
        [
            Paragraph("<b>OT Cybersecurity Breach</b>", table_cell_bold),
            Paragraph("Critical", table_cell),
            Paragraph("Purdue Zone 3 deployment with strictly read-only ingestion ports (zero PLC writeback capability).", table_cell),
        ],
    ]

    risk_table = Table(risk_data, colWidths=[130, 60, 314])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#A000FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#000000')),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Conclusion & Executive Recommendation:</b> ShadowLine provides automotive plant leadership with an empirically proven, non-intrusive, and commercially transformative solution. Delivering <b>$1.66M in net annual savings per line</b> with a <b>2.3-month payback</b>, ShadowLine is the definitive digital twin investment for zero-downtime automotive manufacturing.",
        body_style
    ))

    # Build document
    doc.build(story, onFirstPage=draw_decorations, onLaterPages=draw_decorations)
    print(f"Successfully generated {output_path} ({os.path.getsize(output_path)} bytes)")


if __name__ == "__main__":
    build_business_proposal_pdf()
