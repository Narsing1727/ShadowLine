# ShadowLine: Predictive Digital Twin for Automotive Assembly

> **Accenture Innovation Challenge 2026 · Round 2 Submission (DigitalTwin.ai)**  
> *A 4-hour forward discrete-event predictive digital twin solving uneven sensor coverage, shifting bottlenecks, and latent defect propagation.*

---

## 📂 Repository Structure

```
shadowLine/
├── Backend/                                # Digital Twin Engine, Simulation & FastAPI Service
│   ├── src/
│   │   ├── sim_plant/                      # Service A: 42-Station Assembly Line Simulator (OT)
│   │   └── shadowline/                     # Service B: Predictive Twin Engine & REST/WS APIs
│   ├── scripts/                            # Replay, scoring, seed & API runner scripts
│   ├── tests/                              # Pytest test suite (15/15 passing)
│   ├── configs/                            # 42-station plant topology configurations
│   ├── data/                               # Historical SQLite databases & shadow logs
│   ├── docker/                             # Dockerfile and deployment configs
│   ├── pyproject.toml                      # Backend Python dependencies
│   └── Makefile                            # Build and test shortcuts
│
├── Frontend/                               # 12-Screen Multi-Persona React 19 Dashboard
│   ├── src/
│   │   ├── components/                     # 12 persona screens, line maps & navigation
│   │   ├── services/api.ts                 # REST client & WebSocket connector (:8000)
│   │   └── App.tsx                         # Root dashboard with live backend telemetry
│   ├── package.json                        # Node dependencies (React 19, Tailwind, Recharts)
│   └── vite.config.ts                      # Vite build configuration
│
├── ShadowLine_Detailed_Business_Proposal.pdf # Executive Business Proposal (PDF)
├── ShadowLine_Detailed_Business_Proposal.pptx# Executive Presentation Deck (16:9 PPTX)
├── ShadowLine_README_Document.pdf          # Full In-Depth Technical Specification (PDF)
├── BUSINESS_PROPOSAL.md                    # Markdown version of Business Case & ROI Model
├── ARCHITECTURE.md                         # Detailed Architectural Specification
└── README.md                               # Project Overview & Quickstart Guide
```

---

## ⚡ Quickstart Guide

### 1. Run the Backend API Server
```bash
cd Backend
python scripts/run_api.py
```
* Backend API runs at: **`http://localhost:8000`**
* Interactive Swagger Docs at: **`http://localhost:8000/docs`**
* WebSocket Stream at: **`ws://localhost:8000/ws/live`**

### 2. Run the Frontend Dashboard
```bash
cd Frontend
npm run dev
```
* Interactive UI runs at: **`http://localhost:3000`**
* Top Header will indicate **`● API: Connected (:8000)`**

### 3. Run Automated Tests
```bash
cd Backend
pytest -v
```
*(All 15 unit and integration tests pass with 100% success rate)*

---

## 📊 Key Operational & Business Metrics

| Metric | Target | ShadowLine Benchmark | Status |
|---|---|:---:|:---:|
| **Forecast Horizon** | $\ge 2.0\text{ hours}$ | **4.0 Hours (Monte Carlo)** | ✅ EXCEEDED |
| **Alert Precision** | $\ge 80.0\%$ | **88.7%** | ✅ CERTIFIED LIVE |
| **False Alarm Rate** | $\le 15.0\%$ | **11.3%** | ✅ PASSED |
| **Alarm Budget Cap** | EEMUA 191 | **$\le 6$ alerts / operator / hr** | ✅ COMPLIANT |
| **Net Annual Savings** | — | **+\$1,656,000 / year / line** | ✅ CALCULATED |
| **Capital Payback** | $\le 6\text{ months}$ | **2.32 Months (~70 Days)** | ✅ VERIFIED |
