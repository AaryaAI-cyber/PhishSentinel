# PhishSentinel 🛡️
### India's #1 AI-Powered Cybersecurity Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://python.org)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react)](https://react.dev)
[![XGBoost](https://img.shields.io/badge/XGBoost-ML-red?style=for-the-badge)](https://xgboost.readthedocs.io)
[![SHAP](https://img.shields.io/badge/SHAP-XAI-orange?style=for-the-badge)](https://shap.readthedocs.io)
[![Flask](https://img.shields.io/badge/Flask-API-green?style=for-the-badge)](https://flask.palletsprojects.com)

> **"Every Scam Has a Tell. We Find It in Under 400 Milliseconds."**

**Team Name:** CyberTechie | **Member:** Aarya Shinde (160624747002)
**Branch:** AI & Data Science — A | Stanley College of Engineering & Technology for Women, Hyderabad
**Event:** EPL '26 | Cyber Crusaders | Problem Code: **CC-02-S1**
**SDGs:** SDG 9 | SDG 16 | SDG 4

---

## What Is PhishSentinel?

PhishSentinel is India's most comprehensive AI-powered cybersecurity platform with 20+ tools. It detects phishing links, scam messages, fake jobs, AI-generated content, and account breaches — then explains exactly WHY something is dangerous using SHAP Explainable AI, suggests safe alternatives, guides users on what to do next, and delivers all results in 10 Indian languages.

**The problem:** India lost Rs 1,750 crore to cyber fraud in 2023. 1.39 million phishing attacks were recorded (CERT-In). Most victims had no tool to check suspicious links — and existing tools only say safe/unsafe without any explanation.

**The solution:** PhishSentinel does what no other free tool does — it explains every threat in plain language, in your language, with specific action steps.

---

## UN Sustainable Development Goals

| SDG | How PhishSentinel Contributes |
|-----|-------------------------------|
| **SDG 9** — Industry & Innovation | Free tool protecting 120M+ new Indian internet users with no technical knowledge required |
| **SDG 16** — Peace & Justice | Combats phishing fraud. SHAP explainability makes AI accountable — EU AI Act 2024 compliant |
| **SDG 4** — Quality Education | Explanations teach users to identify phishing patterns themselves over time |

---

## 20+ Tools Across 4 Categories

### Detection Tools
| Tool | What It Does |
|------|-------------|
| URL Scanner | Analyzes 15 URL features with RF+XGBoost+SHAP. Cross-references VirusTotal (70+ engines) + Google Safe Browsing |
| Email Analyzer | BERT semantic analysis + keyword detection. Highlights suspicious phrases. AI-generation detection |
| WhatsApp/SMS Scanner | Auto-extracts all URLs from pasted messages and scans each one |
| QR Code Scanner | Decodes QR images, extracts URL, runs full scan + brand logo detection |
| Bulk URL Scanner | Scan 10 URLs simultaneously. Results table with CSV export |
| Phone Scam Check | IPQualityScore API + number pattern analysis. Links to Truecaller verification |

### Analysis Tools
| Tool | What It Does |
|------|-------------|
| Fake Job Detector | NLP analysis of job offers. Detects Aadhaar requests, unrealistic salaries, missing registration details |
| Conversation Analyzer | Detects manipulation patterns across multi-turn WhatsApp/SMS conversations |
| Email Header Analyzer | SPF/DKIM/DMARC verification. Visual email journey map |
| AI Text Detector | GPTZero API. Detects AI-generated phishing emails via perplexity and burstiness scoring |
| Password Analyzer | k-anonymity HaveIBeenPwned check. Entropy scoring. Time-to-crack estimate |
| File Safety Scanner | VirusTotal 70+ engine scan. Behavior report in plain English |
| Dark Pattern Detector | Identifies deceptive UI patterns. Legal reference to Consumer Protection Act 2019 |
| Digital Footprint | HaveIBeenPwned breach timeline. Data exposure analysis |
| App Safety Scanner | Permission risk analysis. Developer reputation scoring |
| Deepfake Detector | Sensity API. Facial inconsistency detection. Educational mode |

### Education Tools
| Tool | What It Does |
|------|-------------|
| Cyber Jargon Translator | 500+ cyber terms explained in 10 Indian languages with real examples |
| Scam News Feed | NewsAPI — latest India scam alerts filtered by state and type |
| AI Safety Quiz | 8 scenario-based questions. SHAP-style explanations after each answer |

### Business Tools
| Tool | What It Does |
|------|-------------|
| Session Dashboard | Real-time analytics. Donut chart. Coordinated campaign detection |

---

## What Makes It Different

| Feature | Basic Tools | Competitors | PhishSentinel |
|---------|-------------|-------------|---------------|
| Explains WHY | ❌ | ❌ | ✅ SHAP XAI |
| Safe Alternative | ❌ | ❌ | ✅ |
| What To Do Next | ❌ | ❌ | ✅ |
| Indian Languages | ❌ | Some | ✅ 10 languages |
| AI Text Detection | ❌ | ❌ | ✅ |
| Multiple scan modes | URL only | 2-3 modes | ✅ 20+ tools |
| Zero data storage | ❌ | Varies | ✅ By design |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│              React Frontend (Vercel)                     │
│   20 Tool Interfaces | SHAP Visualizations | i18n        │
│   Framer Motion | Three.js Globe | CipherCat Bot         │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS POST (JSON)
                       ▼
┌─────────────────────────────────────────────────────────┐
│           Flask REST API (Render.com)                    │
│     Input Validation (5 layers) | Rate Limiting         │
└──────────┬────────────────────────────┬─────────────────┘
           │                            │
    ┌──────┴──────┐              ┌──────┴──────┐
    │  ML Pipeline │              │  API Gateway │
    │  RF+XGBoost  │              │  VirusTotal  │
    │  BERT NLP    │              │  Google SB   │
    │  SHAP Engine │              │  IPQualScore │
    │  235,795 URLs│              │  URLScan.io  │
    └──────┬───────┘              │  HaveIBeenPwned│
           │                     │  GPTZero     │
           └──────────┬──────────┘
                      ▓
           ┌──────────▼──────────┐
           │   Unified Result    │
           │   Verdict + Score   │
           │   SHAP Reasons      │
           │   Safe Alternative  │
           │   What To Do Next   │
           │   10 Language i18n  │
           └─────────────────────┘
```

---

## Performance Benchmarks

| Metric | Value |
|--------|-------|
| Model Accuracy | 97.2% |
| False Positive Rate | 0.8% |
| Prediction Latency (optimized) | 91.9 ms |
| Prediction Latency (before optimization) | 1,064.2 ms |
| Speed Improvement | **11.6x faster** |
| Training Dataset | 235,795 URLs (UCI + PhiUSIIL) |
| Features Extracted | 15 per URL |
| External APIs | 8 real-time sources |

*Benchmarked on development machine — Python 3.13, Windows, averaged over 5 runs.*

---

## Installation Guide

### Prerequisites
```
Python 3.9+
Node.js 18+
Git
```

### Clone Repository
```bash
git clone https://github.com/AaryaAI-cyber/PhishSentinel.git
cd PhishSentinel
```

### Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
python train_model.py    # First run only — trains and saves model
python app.py            # Starts Flask server on http://localhost:5000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev              # Starts React app on http://localhost:3000
```

### Environment Variables
```bash
# Create backend/.env
VIRUSTOTAL_API_KEY=your_key
GOOGLE_SAFE_BROWSING_KEY=your_key
IPQS_API_KEY=your_key
URLSCAN_API_KEY=your_key
HIBP_API_KEY=your_key
GPTZERO_API_KEY=your_key
NEWSAPI_KEY=your_key
```

---

## API Reference

### POST /predict-url
```json
Request:  { "url": "http://paypa1-secure.xyz/login" }
Response: {
  "label": "PHISHING",
  "confidence": 99.9,
  "risk_score": 94,
  "virustotal_detections": "12/70 engines",
  "google_safe_browsing": "SOCIAL_ENGINEERING",
  "shap_reasons": [
    { "feature": "domain_age", "display": "Domain registered 2 days ago", "score": 0.84 },
    { "feature": "no_https", "display": "No HTTPS certificate", "score": 0.71 }
  ],
  "safe_alternative": "paypal.com",
  "what_to_do": ["Do NOT click", "Report at cybercrime.gov.in", "Call 1930"]
}
```

---

## Repository Structure

```
PhishSentinel/
├── backend/
│   ├── app.py                    # Flask API — all endpoints
│   ├── models/
│   │   ├── train_model.py        # RF + XGBoost training
│   │   ├── features.py           # 15-feature URL extractor
│   │   ├── predict.py            # Ensemble prediction pipeline
│   │   └── explain.py            # SHAP explainer
│   ├── apis/
│   │   ├── virustotal.py         # VirusTotal integration
│   │   ├── google_sb.py          # Google Safe Browsing
│   │   ├── ipqualityscore.py     # Phone + IP fraud scoring
│   │   └── hibp.py               # HaveIBeenPwned breach check
│   ├── validation/
│   │   └── validators.py         # 5-layer input validation
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Scanner/          # All 20 tool components
│   │   │   ├── Results/          # SHAP visualization
│   │   │   ├── Globe/            # 3D Earth threat map
│   │   │   └── CipherCat/        # AI mascot bot
│   │   ├── i18n/                 # 10 Indian language translations
│   │   └── App.jsx
│   ├── public/
│   │   └── manifest.json         # PWA manifest
│   └── package.json
├── docs/
│   ├── architecture.png          # System diagram
│   └── screenshots/              # UI gallery
└── README.md
```

---

---

## Tech Stack

```
AI & ML:      Python, scikit-learn, Random Forest, XGBoost, SHAP, BERT, NLP
              Computer Vision, OpenCV, GPTZero
Backend:      Flask, pandas, numpy, tldextract, python-whois, joblib
Frontend:     React, Tailwind CSS, Framer Motion, Three.js, Recharts
Security APIs: VirusTotal, Google Safe Browsing, IPQualityScore
              URLScan.io, HaveIBeenPwned, GPTZero, NewsAPI, AbuseIPDB
Deployment:   Vercel (frontend) + Render.com (backend)
PWA:          Service Worker, Web Manifest — Play Store ready
```

---

## Business Model

| Tier | Price | Features |
|------|-------|---------|
| Free | Rs 0/month | 10 scans/day, 6 core tools, 3 languages |
| Pro | Rs 299/month | Unlimited scans, all 20 tools, 10 languages, API access |
| Enterprise | Rs 2,999/month | Team dashboard, white-label, compliance reports, SLA |

---

## About

**Mission:** We built PhishSentinel because phishing victims in India are not hackers — they are parents, students, and small business owners who just needed one tool that could tell them the truth in plain language.

**Team:** Aarya Shinde | Roll No: 160624747002 | AI & Data Science — A
Stanley College of Engineering & Technology for Women, Hyderabad

**Event:** EPL '26 | Cyber Crusaders | CC-02-S1

**Cybercrime Reporting:** cybercrime.gov.in | National Helpline: **1930**

---

*PhishSentinel — Detect. Explain. Protect.*
*Built with purpose for every Indian internet user.*
