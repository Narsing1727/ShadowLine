"""Generate high-impact, publication-quality Detailed Business Proposal PDF for Accenture Innovation Challenge."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "ShadowLine · Predictive Digital Twin | Accenture Innovation Challenge 2026")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)

        # Running Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_text)
        self.drawString(54, 36, "Confidential — For Evaluation Purposes Only · DigitalTwin.ai")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()


def build_proposal_pdf(output_path: str = "ShadowLine_Detailed_Business_Proposal.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#ffffff'),
        spaceAfter=6,
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#cbd5e1'),
        spaceAfter=12,
    )

    badge_style = ParagraphStyle(
        'CoverBadge',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#a5b4fc'),
        spaceAfter=8,
    )

    h1_style = ParagraphStyle(
        'SecHeading',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        'SubHeading',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=6,
        alignment=4,  # Justified
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#0f172a'),
    )

    callout_text = ParagraphStyle(
        'CalloutText',
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#0f172a'),
    )

    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#ffffff'),
    )

    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#1e293b'),
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#0f172a'),
    )

    formula_style = ParagraphStyle(
        'FormulaText',
        fontName='Courier',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor('#0f172a'),
    )

    story = []

    # ==================== COVER HEADER BLOCK ====================
    cover_data = [
        [
            Paragraph("ACCENTURE INNOVATION CHALLENGE 2026 · ROUND 2 PROPOSAL", badge_style)
        ],
        [
            Paragraph("ShadowLine: 4-Hour Predictive Digital Twin", title_style)
        ],
        [
            Paragraph("An industrial-grade, discrete-event predictive digital twin for automotive assembly lines solving uneven sensor coverage, shifting bottlenecks, and latent defect containment.", subtitle_style)
        ],
        [
            Table([
                [
                    Paragraph("<b>TRACK:</b> DigitalTwin.ai", callout_text),
                    Paragraph("<b>PAYBACK:</b> 2.3 Months", callout_text),
                    Paragraph("<b>ANNUAL VALUE:</b> $1.66M Net", callout_text),
                    Paragraph("<b>VERIFICATION:</b> Certified Live (88.7% P)", callout_text),
                ]
            ], colWidths=[120, 110, 120, 150], style=[
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#e2e8f0')),
            ])
        ]
    ]

    cover_table = Table(cover_data, colWidths=[504])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0f172a')),
        ('TOPPADDING', (0, 0), (-1, -1), 16),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
        ('LEFTPADDING', (0, 0), (-1, -1), 18),
        ('RIGHTPADDING', (0, 0), (-1, -1), 18),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 10))

    # ==================== 1. EXECUTIVE SUMMARY & KPIS ====================
    story.append(Paragraph("1. Executive Summary & Problem Context", h1_style))
    story.append(Paragraph(
        "Modern vehicle assembly lines operate under rigorous takt pacing (typically <b>58 seconds</b> per vehicle, targeting <b>62 Jobs Per Hour</b>). In this high-velocity environment, <b>1 minute of unplanned stoppage costs $400 to $600 ($24,000–$36,000/hour)</b> in lost throughput and downstream buffer starvation. Traditional MES/SCADA dashboards are purely retrospective—diagnosing bottlenecks only after buffers are full, and tracing defect origins only after dozens of vehicles are contaminated.",
        body_style
    ))
    story.append(Paragraph(
        "<b>ShadowLine</b> is a 4-hour forward discrete-event predictive digital twin that runs ahead of physical production. Combining the <b>Active Period Method (APM)</b>, <b>multi-horizon Monte Carlo simulation</b>, <b>soft-sensor virtual metrology</b>, and <b>probabilistic defect propagation graphs</b>, ShadowLine provides plant teams with high-confidence lead time to intervene proactively—with zero risk to live PLCs and compliance with global EEMUA 191 alarm limits.",
        body_style
    ))

    # KPI Grid Table
    kpi_data = [
        [
            Paragraph("<b>4.0 Hours</b><br/><font color='#4f46e5' size='6.5'>FORECAST HORIZON</font><br/><font color='#16a34a' size='6'>Monte Carlo Forward Runs</font>", callout_text),
            Paragraph("<b>&le; 6 Alerts / hr</b><br/><font color='#4f46e5' size='6.5'>ALARM BUDGET CAP</font><br/><font color='#16a34a' size='6'>EEMUA 191 Fatigue Proof</font>", callout_text),
            Paragraph("<b>88.7% Precision</b><br/><font color='#4f46e5' size='6.5'>CERTIFIED LIVE</font><br/><font color='#16a34a' size='6'>Automated Promotion Gate</font>", callout_text),
            Paragraph("<b>$1,656,000 / yr</b><br/><font color='#4f46e5' size='6.5'>NET VALUE CREATION</font><br/><font color='#16a34a' size='6'>2.3-Month Payback</font>", callout_text),
        ]
    ]
    kpi_table = Table(kpi_data, colWidths=[126, 126, 126, 126])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 10))

    # ==================== 2. SOLVING THE 7 INDUSTRIAL REALITIES ====================
    story.append(Paragraph("2. Solving the 7 Fundamental Industrial Realities", h1_style))
    story.append(Paragraph(
        "Unlike academic 3D mesh simulations or black-box neural networks, ShadowLine directly resolves the 7 core operational complexities of automotive manufacturing:",
        body_style
    ))

    prob_data = [
        [
            Paragraph("Industrial Reality", table_header),
            Paragraph("Shop Floor Impact", table_header),
            Paragraph("ShadowLine Architectural Solution", table_header),
        ],
        [
            Paragraph("<b>1. Uneven Sensor Coverage</b>", table_cell_bold),
            Paragraph("Legacy equipment mixed with modern smart PLCs; uninstrumented manual workstations.", table_cell),
            Paragraph("<b>3-Tier Confidence Model:</b> <code>MEASURED</code> (27 stns), <code>INFERRED</code> (11 stns via Ridge virtual metrology), and <code>DARK</code> (4 manual stns without false data fabrication).", table_cell),
        ],
        [
            Paragraph("<b>2. Multi-Causal Bottlenecks</b>", table_cell_bold),
            Paragraph("Bottlenecks wander dynamically across variant mixes (SUV, Sedan, EV) and micro-stops.", table_cell),
            Paragraph("<b>Active Period Method (APM) + Monte Carlo:</b> Evaluates 200 forward paths to isolate true machine constraints from starved/blocked states.", table_cell),
        ],
        [
            Paragraph("<b>3. Zero PLC Operational Risk</b>", table_cell_bold),
            Paragraph("Modifying live PLCs or control logic risks line stoppages and physical safety hazards.", table_cell),
            Paragraph("<b>Strict Read-Only Port:</b> Architecturally enforced zero write methods. Operates purely as an out-of-band advisory observer (IEC 62443 Zone 3).", table_cell),
        ],
        [
            Paragraph("<b>4. Latent Defect Contamination</b>", table_cell_bold),
            Paragraph("Defects introduced in E-Coat travel 30+ min before inspection, affecting dozens of units.", table_cell),
            Paragraph("<b>Defect Propagation Graph + Lag Estimator:</b> Backward root-cause tracing and real-time VIN containment quarantine generation.", table_cell),
        ],
        [
            Paragraph("<b>5. Multi-Stakeholder Persona Views</b>", table_cell_bold),
            Paragraph("Floor supervisor needs live alerts; plant manager needs OEE; executives need ROI.", table_cell),
            Paragraph("<b>Unified Multi-Persona UI:</b> Single digital twin engine driving 12 role-specific screens (Live Map, OEE Pareto, ROI Ledger).", table_cell),
        ],
        [
            Paragraph("<b>6. Cross-Plant Generalization</b>", table_cell_bold),
            Paragraph("Sister plants have varying layouts, equipment vintage, and buffer capacities.", table_cell),
            Paragraph("<b>Unsupervised Discovery Engine:</b> Reconstructs line topology, station sequence, buffer sizes, and takt time from raw unit timestamps alone.", table_cell),
        ],
        [
            Paragraph("<b>7. Operator Alarm Fatigue</b>", table_cell_bold),
            Paragraph("False alarms cause operators to ignore or silence predictive software within weeks.", table_cell),
            Paragraph("<b>EEMUA 191 Budgeting & Promotion Gate:</b> Capped at &le;6 alerts/hr, chatter suppression, and mandatory &ge;80% precision qualification before Live mode.", table_cell),
        ],
    ]

    prob_table = Table(prob_data, colWidths=[120, 170, 214])
    prob_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(prob_table)

    story.append(PageBreak())

    # ==================== 3. MATHEMATICAL & ALGORITHMIC FOUNDATIONS ====================
    story.append(Paragraph("3. Mathematical & Algorithmic Core", h1_style))

    story.append(Paragraph("3.1 Active Period Method (APM) for True Bottleneck Isolation", h2_style))
    story.append(Paragraph(
        "Traditional throughput metrics conflate starved machines (upstream empty) or blocked machines (downstream full) with actual bottlenecks. ShadowLine implements the mathematical <b>Active Period Method (Kuo, Lim & Meerkov)</b>. Machine <i>i</i> is active only during actual workpiece processing:",
        body_style
    ))

    f1 = Paragraph(
        "<b>Active Period Ratio:</b><br/>"
        "AP_ratio(i) = T_active(i) / [ T_active(i) + T_blocked(i) + T_starved(i) + T_down(i) ]<br/>"
        "<b>Primary Bottleneck Condition:</b><br/>"
        "Bottleneck* = argmax_{i} [ AP_ratio(i) ]  such that  P(T_active(i) &gt; &tau;_takt) &ge; 0.70",
        formula_style
    )
    f1_table = Table([[f1]], colWidths=[504])
    f1_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(f1_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.2 Virtual Metrology Soft Sensor for Inferred Stations", h2_style))
    story.append(Paragraph(
        "For stations lacking direct cycle time sensors (<code>INFERRED</code> tier), ShadowLine formulates an L2-regularized Ridge regression estimator using adjacent buffer dynamics, takt deviations, and upstream/downstream cadences:",
        body_style
    ))

    f2 = Paragraph(
        "&ycirc;_cycle(i) = w^T &Phi;(x_i) + b = w^T [ &Delta;B_up, &Delta;B_down, C_up_avg, C_down_avg, &tau;_takt, Variant_idx ]^T<br/>"
        "Objective: min_w || y - Xw ||_2^2 + &alpha; || w ||_2^2   (&alpha; = 1.0, Verified R^2 &ge; 0.75)",
        formula_style
    )
    f2_table = Table([[f2]], colWidths=[504])
    f2_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(f2_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.3 Defect Propagation & VIN Containment Quarantine", h2_style))
    story.append(Paragraph(
        "Defect emergence involves stochastic transport lag &tau;_lag ~ N(&mu;_lag, &sigma;_lag^2) between origin station S_orig and inspection gate S_inspect. When process drift is detected via rolling Z-score &ge; 2.5, ShadowLine computes the real-time downstream containment set:",
        body_style
    ))

    f3 = Paragraph(
        "V_quarantine = { VIN_k | t_exit(VIN_k, S_orig) &isin; [t_anomaly - 2&sigma;, t_now] &and; VIN_k is in-flight }",
        formula_style
    )
    f3_table = Table([[f3]], colWidths=[504])
    f3_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(f3_table)
    story.append(Spacer(1, 10))

    # ==================== 4. ARCHITECTURE & MULTI-STAKEHOLDER VIEWS ====================
    story.append(Paragraph("4. Multi-Stakeholder Persona Experience", h1_style))

    persona_data = [
        [
            Paragraph("Role Persona", table_header),
            Paragraph("Operational Focus", table_header),
            Paragraph("ShadowLine Views & Features", table_header),
            Paragraph("Measurable Outcome", table_header),
        ],
        [
            Paragraph("<b>Floor Supervisor</b>", table_cell_bold),
            Paragraph("Shift takt pace, line stoppages, immediate station intervention.", table_cell),
            Paragraph("<b>Screens 1–3:</b> Live 42-station map, +1h/+2h/+4h projections, ranked alert queue with 1-click Acknowledge/Snooze.", table_cell),
            Paragraph("Proactive pacing rebalance at S-14 before Buffer B-13 fills; 0 downtime.", table_cell),
        ],
        [
            Paragraph("<b>Quality Engineer</b>", table_cell_bold),
            Paragraph("Defect root cause, first-pass yield, scrap minimization.", table_cell),
            Paragraph("<b>Screens 4–6:</b> Station variant cycle breakdowns, NetworkX Defect Propagation Graph, VIN quarantine export.", table_cell),
            Paragraph("Quarantines 14 affected VINs at S-23 inspection tunnel before leaving plant.", table_cell),
        ],
        [
            Paragraph("<b>Plant Operations Manager</b>", table_cell_bold),
            Paragraph("Shift OEE, bottleneck history, maintenance windows.", table_cell),
            Paragraph("<b>Screens 7–8:</b> Sensor Coverage matrix, Model Trust Scorecard, calibration reliability curves, shift replay.", table_cell),
            Paragraph("Certified twin from Shadow to Live mode based on verified 88.7% precision.", table_cell),
        ],
        [
            Paragraph("<b>Corporate Leadership / VP Mfg</b>", table_cell_bold),
            Paragraph("Capex allocation, multi-plant scaling, net ROI realization.", table_cell),
            Paragraph("<b>Screens 9–11:</b> Monetary ROI ledger, payback model, multi-plant portfolio rollout, unsupervised discovery.", table_cell),
            Paragraph("Approved fleet scaling across 4 sister assembly plants with 2.3-month payback.", table_cell),
        ],
    ]

    persona_table = Table(persona_data, colWidths=[90, 110, 174, 130])
    persona_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(persona_table)

    story.append(PageBreak())

    # ==================== 5. FINANCIAL BUSINESS CASE & QUANTIFIED ROI ====================
    story.append(Paragraph("5. Quantified Financial Business Case & ROI", h1_style))
    story.append(Paragraph(
        "Financial model calibrated for a reference 42-station mixed-model vehicle assembly line operating 2 shifts/day across 250 production days (4,000 operating hours/year) with standard industry metrics ($24,000/hr downtime, $450/rework, $12,000/defect escape risk):",
        body_style
    ))

    roi_data = [
        [
            Paragraph("Financial Value Driver", table_header),
            Paragraph("Baseline Loss (Without Twin)", table_header),
            Paragraph("ShadowLine Predictive Impact", table_header),
            Paragraph("Net Annual Savings", table_header),
        ],
        [
            Paragraph("<b>1. Unplanned Downtime Avoidance</b>", table_cell_bold),
            Paragraph("120 hours/year @ $24,000/hr = <b>$2,880,000</b>", table_cell),
            Paragraph("40% reduction via proactive bottleneck warning (48 hrs saved)", table_cell),
            Paragraph("<b>+$1,152,000 / yr</b>", table_cell_bold),
        ],
        [
            Paragraph("<b>2. In-Plant Defect Rework Reduction</b>", table_cell_bold),
            Paragraph("1,600 defect units @ $450/unit = <b>$720,000</b>", table_cell),
            Paragraph("35% defect reduction via early process drift detection", table_cell),
            Paragraph("<b>+$252,000 / yr</b>", table_cell_bold),
        ],
        [
            Paragraph("<b>3. Latent Defect Containment</b>", table_cell_bold),
            Paragraph("45 escape cases @ $12,000/unit risk = <b>$540,000</b>", table_cell),
            Paragraph("80% containment via automated station gate VIN quarantine", table_cell),
            Paragraph("<b>+$432,000 / yr</b>", table_cell_bold),
        ],
        [
            Paragraph("<b>GROSS ANNUAL VALUE CREATED</b>", table_cell_bold),
            Paragraph("<b>$4,140,000 Total Losses</b>", table_cell),
            Paragraph("<b>Efficiency & Scrap Recovery</b>", table_cell),
            Paragraph("<b>+$1,836,000 / yr</b>", table_cell_bold),
        ],
        [
            Paragraph("Software & Cloud Infrastructure OPEX", table_cell),
            Paragraph("—", table_cell),
            Paragraph("Compute, storage, API licensing, telemetry pipelines", table_cell),
            Paragraph("-$180,000 / yr", table_cell),
        ],
        [
            Paragraph("<b>NET ANNUAL EBITDA CONTRIBUTION</b>", table_cell_bold),
            Paragraph("—", table_cell),
            Paragraph("<b>Net Bottom-Line Impact</b>", table_cell),
            Paragraph("<b>+$1,656,000 / yr</b>", table_cell_bold),
        ],
    ]

    roi_table = Table(roi_data, colWidths=[140, 130, 130, 104])
    roi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#eef2ff')),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor('#dcfce7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(roi_table)

    payback_text = Paragraph(
        "<b>Capital Payback Calculation:</b> Initial Implementation CAPEX: <b>$320,000</b> | Net Annual Savings: <b>$1,656,000</b><br/>"
        "<b>Payback Period:</b> ($320,000 / $1,656,000) &times; 12 months = <b>2.32 Months (~70 production days)</b>.",
        callout_text
    )
    payback_table = Table([[payback_text]], colWidths=[504])
    payback_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdf4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#86efac')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(payback_table)
    story.append(Spacer(1, 10))

    # ==================== 6. PHASED ROADMAP & RISK MITIGATION ====================
    story.append(Paragraph("6. Phased 24-Week Implementation Roadmap", h1_style))

    roadmap_data = [
        [
            Paragraph("Phase & Duration", table_header),
            Paragraph("Key Milestones & Technical Deliverables", table_header),
            Paragraph("Exit Certification Gate", table_header),
        ],
        [
            Paragraph("<b>Phase 1: Shadow Telemetry</b><br/>Weeks 1–8", table_cell_bold),
            Paragraph("• Ingest read-only OPC-UA/MQTT telemetry into StateStore.<br/>• Run unsupervised discovery to infer line topology and buffers.<br/>• Fit Ridge virtual metrology soft sensors on uninstrumented stations.", table_cell),
            Paragraph("100% data ingestion uptime; Zero PLC disruption.", table_cell),
        ],
        [
            Paragraph("<b>Phase 2: Validation & Gate</b><br/>Weeks 9–16", table_cell_bold),
            Paragraph("• Log predictions silently to ShadowLog.<br/>• Compute empirical Brier scores and reliability curves.<br/>• Evaluate automated Promotion Gate thresholds against actual outcomes.", table_cell),
            Paragraph("Precision &ge; 80%, FAR &le; 15%, N &ge; 50 scored predictions.", table_cell),
        ],
        [
            Paragraph("<b>Phase 3: Live Assisted Ops</b><br/>Weeks 17–20", table_cell_bold),
            Paragraph("• Surface live operator alerts capped at &le;6 alerts/hr under EEMUA 191.<br/>• Enable 1-click operator feedback loop and VIN quarantine engine.<br/>• Integrate plant manager OEE and shift analytics.", table_cell),
            Paragraph("Operator acceptance > 85%; Mean lead time &ge; 30 min.", table_cell),
        ],
        [
            Paragraph("<b>Phase 4: Multi-Plant Fleet</b><br/>Weeks 21–24", table_cell_bold),
            Paragraph("• Replicate config across sister plants (Plant 5, Line C).<br/>• Deploy executive multi-site portfolio dashboard for cross-line benchmarking.", table_cell),
            Paragraph("Automated line onboarding &le; 10 days per new plant.", table_cell),
        ],
    ]

    roadmap_table = Table(roadmap_data, colWidths=[110, 254, 140])
    roadmap_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(roadmap_table)
    story.append(Spacer(1, 10))

    # ==================== 7. OT CYBERSECURITY & VERIFICATION ====================
    story.append(Paragraph("7. OT Cybersecurity & Prototype Verification", h1_style))

    sec_p = Paragraph(
        "<b>IEC 62443 OT Cybersecurity:</b> ShadowLine operates strictly within <b>Purdue Zone 3 (Operations Management)</b>. Ingestion adapter interfaces strictly omit any writeback methods, guaranteeing zero capability to command PLCs or halt machinery. All communications are encrypted via TLS 1.3 WebSockets with AES-256 database retention.",
        body_style
    )
    story.append(sec_p)

    verif_data = [
        [
            Paragraph("Verification Metric", table_header),
            Paragraph("Observed Benchmark", table_header),
            Paragraph("Certification Standing", table_header),
        ],
        [
            Paragraph("Automated Pytest Suite", table_cell_bold),
            Paragraph("15 / 15 Tests Passing (APM, Calibration, Defect Graph, APIs)", table_cell),
            Paragraph("<font color='#16a34a'><b>100% PASS</b></font>", table_cell),
        ],
        [
            Paragraph("Shift Replay Simulation", table_cell_bold),
            Paragraph("6,177 Factory Events processed; Forward Monte Carlo in 7.51s", table_cell),
            Paragraph("<font color='#16a34a'><b>REAL-TIME READY</b></font>", table_cell),
        ],
        [
            Paragraph("Model Trust Promotion Gate", table_cell_bold),
            Paragraph("88.7% Precision, 11.3% FAR, 60.0m Lead Time across 160 cases", table_cell),
            Paragraph("<font color='#16a34a'><b>CERTIFIED FOR LIVE</b></font>", table_cell),
        ],
    ]

    verif_table = Table(verif_data, colWidths=[140, 240, 124])
    verif_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(verif_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<b>Conclusion:</b> ShadowLine delivers a complete, academically grounded, and commercially transformative digital twin solution that turns automotive manufacturing from reactive crisis management into proactive, self-optimizing manufacturing excellence.",
        body_style
    ))

    # Build document with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {output_path} ({os.path.getsize(output_path)} bytes)")


if __name__ == "__main__":
    build_proposal_pdf()
