# InsightIQ: Market Dynamics & Consumer Segmentation Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask%203.1-black.svg)](https://palletsprojects.com/p/flask/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)](https://scikit-learn.org/)
[![Bootstrap](https://img.shields.io/badge/UI-Bootstrap%205-purple.svg)](https://getbootstrap.com/)

A full-stack, enterprise-grade **Consumer Insights and Market Intelligence Platform** designed to transform multidimensional behavioral data into actionable consumer personas, strategic business decisions, and an interactive, **codeless lead qualification tool** for marketing and business development teams.

---

## 🌟 Key Capabilities

1. **Executive Market Dashboard**:
   - High-level KPIs: Cohort Size (120), Average Spend ($2,814), Visit Frequency (9.6 visits/mo), and Offer Adoption Rate (58.3%).
   - Interactive Chart.js visualizations for market share, spend vs visits, category affinities, and offer elasticity.

2. **Consumer Persona Hub**:
   - Quantitative synthesis of 3 distinct behavioral archetypes:
     - **High-Frequency Fashion Loyalists (Cluster 0)**: Foot-traffic anchors driving consistent organic revenue with low discount elasticity.
     - **High-Ticket Culinary Maximizers (Cluster 1)**: Premium experience seekers generating the highest monthly spend ($3,561) and responding strongly to bundle promotions.
     - **Leisure & Entertainment Explorers (Cluster 2)**: Extended dwell-time visitors (>2.1 hours) with high engagement scores who readily convert on cross-department promotions.

3. **Codeless Lead Qualifier Tool (Interactive)**:
   - Allows non-technical business development and marketing professionals to input prospective customer parameters.
   - Instantly predicts the customer persona, assigns a lead priority tier, outputs the recommended go-to-market strategy, and provides a tailored sales outreach pitch.

4. **Executive Presentation / Report View**:
   - Management-ready slide format (compatible with Gamma, Canva, and Google Slides) summarizing findings, competitor dynamics, and strategic directives. Includes one-click PDF printing.

5. **Customer Cohort Data Explorer**:
   - Searchable, filterable table covering all 120 customer profiles with category and cluster filtering.

---

## 🔬 Analytical Pipeline & Methodology

```
Data Ingestion (mall_customer_segmentation.csv)
       ↓
Data Cleaning & Quality Assurance (Mean Imputation, Deduplication)
       ↓
MinMax Normalization (0 to 1 scaling across behavioral dimensions)
       ↓
Principal Component Analysis (PCA) for Latent Dimensionality Reduction
       ↓
Mathematical Validation (Inertia Elbow Curve + Silhouette Coefficient)
       ↓
K-Means Clustering (Optimal k=3 Convergence)
       ↓
Real-Time Flask API & Web Deployment
```

---

## 🚀 Quickstart: Running Locally

1. **Clone or navigate to the directory**:
   ```bash
   cd "c:\Users\91701\Downloads\Projects\Mall Segmentation"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the web application**:
   ```bash
   python app.py
   ```

4. **Open in browser**:
   ```
   http://127.0.0.1:5000
   ```

---

## 🌐 Free Cloud Deployment (Render.com)

1. Push this folder to a GitHub repository.
2. Sign in to [Render.com](https://render.com) and create a **New Web Service**.
3. Select your repository:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Click **Deploy**. Your live web link will be generated in 2 minutes.

---

## 📂 Repository Structure

```
├── app.py                             # Core Flask application and ML inference engine
├── mall_customer_segmentation.csv     # Cleaned 120-customer observation cohort
├── Mall_Customer_Advanced_Dataset.csv # Raw baseline dataset
├── Mall_Segmentation.ipynb            # Executive, fully-rendered data science notebook
├── Executive_Market_Research_Report.md# Management presentation report / slide outline
├── DEPLOYMENT_AND_INTERVIEW_GUIDE.md  # Step-by-step deployment and interview strategy
├── requirements.txt                   # Production dependencies
├── Procfile                           # Cloud deployment configuration
├── runtime.txt                        # Python runtime specification
├── templates/                         # Modern HTML5 Jinja templates
│   ├── base.html                      # Layout, navigation sidebar, and shared styles
│   ├── dashboard.html                 # Executive metrics and Chart.js visualizations
│   ├── personas.html                  # Deep-dive customer persona cards
│   ├── lead_generator.html            # Interactive codeless lead qualification tool
│   ├── market_report.html             # Presentation slide deck view
│   └── data_explorer.html             # Searchable customer cohort table
└── static/                            # Static assets
    ├── css/style.css                  # Executive design system styling
    └── js/app.js                      # Chart.js initialization and reactive interactions
```

