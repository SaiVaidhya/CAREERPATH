# CareerPath AI – Intelligent Career Recommendation System

**Academic Capstone Project | B.Tech Computer Science & Engineering**

---

## 🌟 Executive Summary

**CareerPath AI** is an advanced, production-grade Artificial Intelligence and Machine Learning web platform designed to solve one of higher education's most pressing challenges: **objective, personalized, and skill-aligned career guidance for engineering students**.

Moving beyond static quiz questionnaires or heuristic decision trees, CareerPath AI implements a **hybrid machine learning architecture** combining:
1. **Random Forest Classifier (150 Estimators)** for multi-class non-linear probability mapping.
2. **K-Nearest Neighbors (k=7, Distance-Weighted Cosine Metric)** for proximity clustering against successful student archetypes.
3. **Cosine Similarity Vector Alignment** against canonical industry competency benchmark vectors.

The platform provides end-to-end functionality including a 27-question multi-dimensional assessment, skills gap analysis with interactive radar charts, personalized progressive learning roadmaps, an NLP-based PDF resume analyzer, an interactive career guidance chatbot, a full administrator analytics portal, and downloadable PDF career reports.

---

## 🏗️ Technology Stack

| Layer | Technologies Used |
| :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, Bootstrap Icons, Chart.js 4.4 |
| **Backend** | Python 3.13, Flask 3.1, Werkzeug Security, Jinja2 Templating |
| **Machine Learning** | Scikit-learn 1.9, Pandas 3.1, NumPy 2.5, Joblib |
| **ML Algorithms** | Random Forest Classifier, K-Nearest Neighbors (KNN), Cosine Similarity |
| **Database** | SQLite3 Relational Database (11 normalized relational tables) |
| **Document Processing** | ReportLab (Custom PDF generator), PyPDF (PDF text & NLP keyword extractor) |
| **Testing** | Python `unittest` framework |

---

## 🎯 Supported 15 Tech Career Pathways

1. **Data Scientist** (Data & AI)
2. **Data Analyst** (Data & Analytics)
3. **AI/ML Engineer** (Artificial Intelligence)
4. **Software Developer** (Core Engineering)
5. **Web Developer** (Web & Interactive)
6. **Cyber Security Analyst** (Security & Defense)
7. **Network Engineer** (Infrastructure)
8. **Cloud Engineer** (Cloud & Distributed)
9. **Database Administrator** (Data Management)
10. **UI/UX Designer** (Design & Product)
11. **Business Analyst** (Strategy & Management)
12. **Digital Marketer** (Growth & Marketing)
13. **DevOps Engineer** (Cloud & Operations)
14. **Mobile App Developer** (Mobile Engineering)
15. **IT Support Engineer** (IT Operations)

---

## 📐 Machine Learning Pipeline & Architecture

```
Student Profile & Ratings (10 Skills) ──┐
                                       ├──► 18-Dimensional Normalized Vector
Assessment Scores (9 Dimensions) ──────┘           │
                                                   ▼
                                       StandardScaler Preprocessing
                                                   │
          ┌────────────────────────────────────────┼───────────────────────────────────────┐
          │                                        │                                       │
          ▼                                        ▼                                       ▼
Random Forest Classifier               K-Nearest Neighbors                   Cosine Similarity Engine
(Multi-class Probability: 40%)          (Archetype Proximity: 25%)            (Benchmark Vector Fit: 35%)
          │                                        │                                       │
          └────────────────────────────────────────┼───────────────────────────────────────┘
                                                   │
                                                   ▼
                               Composite Hybrid Ranking Formula
                                                   │
                                                   ▼
                         Top 5 Career Recommendations + Match Scores (%)
                                                   │
                        ┌──────────────────────────┴──────────────────────────┐
                        ▼                                                     ▼
         Matching Strengths Identification                     Priority Skills Gap Analysis
         (Skills ≥ 75% of Benchmark)                           (Interactive Radar & Action Plan)
```

### ML Performance Benchmark (Test Split: 20% Stratified)
- **Random Forest Accuracy:** `95.56%`
- **Random Forest F1-Score (Weighted):** `95.55%`
- **KNN Accuracy:** `89.84%`
- **Dataset Size:** `1,575 Synthetic Student Observations across 15 Classes`

---

## 📂 Project Directory Structure

```text
careerpath-ai/
├── app/
│   ├── __init__.py               # Flask application factory & blueprints
│   ├── models.py                 # SQLite schema (11 tables) & data access objects
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── career_data.py        # Canonical 15 careers, benchmarks & roadmaps
│   │   ├── data_generator.py     # Synthetic dataset generator (1,575 records)
│   │   ├── train.py              # ML training script & evaluation metrics generator
│   │   └── engine.py             # Recommendation inference engine (RF + KNN + Cosine)
│   ├── routes/
│   │   ├── __init__.py           # Route auth decorators (login_required, admin_required)
│   │   ├── main.py               # Landing page & informational routes
│   │   ├── auth.py               # Registration, login, logout & session management
│   │   ├── dashboard.py          # Student dashboard & profile management
│   │   ├── assessment.py         # 27-question timed assessment & scoring
│   │   ├── recommendations.py    # Top 5 recommendations & skills gap analysis
│   │   ├── roadmap.py            # Learning roadmaps & milestone toggle tracking
│   │   ├── resume.py             # PDF resume upload & NLP skill parsing
│   │   ├── comparison.py         # 3-way side-by-side career track comparison
│   │   ├── chatbot.py            # AI Career guidance conversational interface
│   │   ├── admin.py              # Administrator analytics & live ML metrics
│   │   └── report.py             # Downloadable ReportLab PDF report generation
│   ├── services/
│   │   ├── pdf_service.py        # Styled multi-page PDF generator
│   │   ├── resume_service.py     # PyPDF text extraction & keyword dictionary
│   │   └── chatbot_service.py    # Intent-matching & domain knowledge assistant
│   ├── static/
│   │   ├── css/style.css         # Dark navy & purple SaaS stylesheet
│   │   ├── js/                   # main.js, assessment.js, charts.js, chatbot.js, roadmap.js
│   │   └── uploads/              # Secure upload directory for student resumes
│   └── templates/                # Jinja2 templates (auth, dashboard, assessment, etc.)
├── data/
│   ├── careers_dataset.csv       # 1,575 training records
│   ├── careerpath.db             # SQLite relational database
│   └── ml_models/                # Serialized model pickles & metrics.json
├── tests/
│   └── test_app.py               # Automated unit test suite
├── seed_data.py                  # Database seeder (27 questions, careers, demo users)
├── train_model.py                # Standalone ML training pipeline script
├── run.py                        # Application entrypoint server script
├── requirements.txt              # Production Python package dependencies
├── .env.example                  # Environment variable configuration template
└── README.md                     # Comprehensive project documentation
```

---

## ⚡ Quick Start & Execution Guide

### 1. Prerequisites
- Python 3.10+ (Tested and verified on Python 3.13.7)
- Web Browser (Chrome, Firefox, Edge, Safari)

### 2. Installation
Open your terminal in the project directory:
```bash
cd c:\Users\saivaidhya\Desktop\projects\careerpath-ai
pip install -r requirements.txt
```

### 3. Initialize Database & Train Models
Run the database seeder and model trainer:
```bash
# 1. Train ML models and generate dataset
python train_model.py

# 2. Seed database with questions, careers, and demo accounts
python seed_data.py
```

### 4. Run Automated Test Suite
```bash
python -m unittest tests/test_app.py
```

### 5. Launch the Application Server
```bash
python run.py
```
Open your browser and navigate to:
👉 **`http://127.0.0.1:5000`**

---

## 🔑 Pre-Seeded Evaluation Credentials

For seamless examination and viva presentation, two pre-configured accounts are available:

### 1. Demo Student Account
- **Email:** `demo@student.edu`
- **Password:** `Student@12345`
- **Pre-populated with:** Full academic profile (Aarav Sharma, B.Tech CSE, 8.75 CGPA), completed 27-question assessment (88.9%), generated top 5 recommendations, skills gap breakdown, and roadmap milestone progress.

### 2. Administrator Account
- **Email:** `admin@careerpath.ai`
- **Password:** `Admin@12345`
- **Privileges:** Live access to `/admin/dashboard`, platform KPIs, student registry, live ML model evaluation metrics, 15x15 confusion matrix heatmap, feature importance rankings, and one-click model retraining.

---

## 🎓 Step-by-Step Viva Demonstration Workflow

1. **Homepage Walkthrough (`/`):**
   - Showcase modern SaaS dark navy/purple UI, interactive metrics, 15 tech tracks, and how-it-works overview.
2. **Student Login (`/auth/login`):**
   - Log in as `demo@student.edu` to demonstrate an existing active student, or register a new candidate.
3. **Student Profile (`/profile`):**
   - Review academic details, degree, branch, semester, CGPA, and interactive 0-100 skill proficiency sliders.
4. **Career Assessment (`/assessment/take`):**
   - Walk through the 27-question timed test across 9 aptitude categories with live jump palette and timer.
5. **AI Recommendations Dashboard (`/recommendations`):**
   - Inspect the top 5 ranked careers, hybrid match scores, personalized rationale, and matching/missing skills.
6. **Skills Gap Analysis (`/skills-gap`):**
   - Demonstrate the Chart.js radar chart comparing student proficiency against industry benchmark requirements.
7. **Personalized Learning Roadmap (`/roadmap`):**
   - Toggle step completion checkboxes and observe dynamic progress bar updates in real time.
8. **AI Resume Analyzer (`/resume/analyzer`):**
   - Upload any PDF resume and view extracted skills, ATS score, and missing keyword suggestions.
9. **Career Comparison Tool (`/compare-careers`):**
   - Compare up to 3 careers side by side across difficulty, growth, required skills, and salary benchmarks.
10. **AI Career Chatbot (`/chatbot`):**
    - Ask questions like *"What is the difference between Data Scientist and Data Analyst?"* or *"How to learn Python?"*.
11. **Official PDF Career Report (`/download-report`):**
    - Download the ReportLab-generated professional PDF summary.
12. **Admin Dashboard (`/admin/dashboard`):**
    - Log in as `admin@careerpath.ai` to present the ML model accuracy (95.56%), feature importances, and the 15x15 confusion matrix.

---

## ⚖️ Academic Disclaimer & Ethical AI Statement

- **Advisory Scope:** CareerPath AI match scores reflect mathematical alignment against sample industry archetypes and benchmark competency profiles. They do not constitute guaranteed employment outcomes.
- **Data Privacy:** Passwords are cryptographically hashed using PBKDF2 with SHA-256 via Werkzeug. Uploaded resumes are securely parsed locally without third-party data transmission.

---

**Developed for B.Tech Computer Science Engineering Capstone Examination.**
