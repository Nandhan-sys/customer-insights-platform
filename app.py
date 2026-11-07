import os
import json
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, redirect, url_for
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

app = Flask(__name__)

# --- Model & Data Pipeline Initialization ---
DATA_PATH = os.path.join(os.path.dirname(__file__), 'mall_customer_segmentation.csv')
if not os.path.exists(DATA_PATH):
    DATA_PATH = os.path.join(os.path.dirname(__file__), 'Mall_Customer_Advanced_Dataset.csv')

df = pd.read_csv(DATA_PATH)
df.fillna(df.mean(numeric_only=True), inplace=True)

numeric_cols = ['Visit_Frequency', 'Avg_Spending', 'Time_Spent_Minutes', 'Spending_Score']

# Fit scaler
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df[numeric_cols]), columns=numeric_cols)

# Fit PCA
pca = PCA(n_components=2)
df_pca = pca.fit_transform(df_scaled)
pca_df = pd.DataFrame(df_pca, columns=['PC1', 'PC2'])

# Fit KMeans
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(pca_df)
df['Cluster'] = cluster_labels
pca_df['Cluster'] = cluster_labels

# Simple & Clear Persona Definitions & Marketing Strategies
PERSONAS = {
    0: {
        "id": 0,
        "name": "Regular Fashion Shoppers",
        "badge": "VIP Regular Customer",
        "color": "#4f46e5",
        "bg_color": "rgba(79, 70, 229, 0.1)",
        "tagline": "Loyal customers who visit often and love buying clothes at regular prices.",
        "avg_spend": 2468.43,
        "visit_freq": 14.83,
        "dwell_time": 99.61,
        "spending_score": 34.75,
        "top_category": "Fashion & Clothes",
        "offer_usage": "Only 32% (Rarely use coupons)",
        "lead_tier": "High Priority: Keep Them Loyal (VIP)",
        "characteristics": [
            "Visits about 15 times every month (our most frequent visitors).",
            "Spends around $2,468 each month consistently.",
            "Loves shopping for fashion, shoes, and clothing.",
            "Rarely asks for discounts — they buy because they love the styles and new arrivals."
        ],
        "marketing_strategy": "Do not give them big discounts—they already buy at full price! Instead, make them feel special with VIP early previews of new clothes, private fitting sessions, and loyalty points.",
        "promotional_action": "VIP Early Access & Loyalty Points (No heavy price cuts).",
        "roi_potential": "Guaranteed recurring profit because they visit and spend every single week."
    },
    1: {
        "id": 1,
        "name": "Big Spenders (Food & Dining)",
        "badge": "Highest Spenders",
        "color": "#0d9488",
        "bg_color": "rgba(13, 148, 136, 0.1)",
        "tagline": "People who come for great food and spend the most money per trip.",
        "avg_spend": 3561.21,
        "visit_freq": 6.30,
        "dwell_time": 57.88,
        "spending_score": 37.33,
        "top_category": "Food & Restaurants",
        "offer_usage": "72% (Love good deals & bundles)",
        "lead_tier": "Top Priority: High-Value Growth",
        "characteristics": [
            "Spends $3,561 every month (highest spenders in the whole mall!).",
            "Visits about 6 times a month for focused meals and dinner meetings (~58 minutes).",
            "Their favorite spend is on premium restaurants and food.",
            "72% use deals when available — smart offers make them spend even more!"
        ],
        "marketing_strategy": "Give them high-value bundle deals (like 'Spend $150 on dinner, get a $30 gift card'). Great for targeting business lunches, family gatherings, and weekend dining.",
        "promotional_action": "Dinner Combos, Chef Specials & High-Spend Gift Cards.",
        "roi_potential": "Brings in the most money per visit; high return on every marketing dollar spent."
    },
    2: {
        "id": 2,
        "name": "Movie & Hangout Visitors",
        "badge": "Long-Stay Visitors",
        "color": "#f59e0b",
        "bg_color": "rgba(245, 158, 11, 0.1)",
        "tagline": "People who hang out for over 2 hours for movies, games, and entertainment.",
        "avg_spend": 2338.03,
        "visit_freq": 6.90,
        "dwell_time": 131.26,
        "spending_score": 71.09,
        "top_category": "Movies & Entertainment",
        "offer_usage": "75% (Very deal-friendly)",
        "lead_tier": "Medium Priority: Fun & Cross-Selling",
        "characteristics": [
            "Stays the longest in the mall — over 2 hours per visit (131 minutes).",
            "Spends around $2,338 a month on activities.",
            "Highest spending score (71/100) — eager to participate in events and games.",
            "75% love coupons and special offers."
        ],
        "marketing_strategy": "Since they are hanging out for hours, send them quick flash deals on their phones (e.g. 'Show your movie ticket for 20% off snacks or arcade games') to get them to spend more.",
        "promotional_action": "Movie + Snack Combo Passes & Weekend Fun Deals.",
        "roi_potential": "Great for getting people to spend money across different stores while hanging out."
    }
}

def predict_single_customer(visit_freq, avg_spending, time_spent, spending_score):
    raw_point = pd.DataFrame([[visit_freq, avg_spending, time_spent, spending_score]], columns=numeric_cols)
    scaled_point = pd.DataFrame(scaler.transform(raw_point), columns=numeric_cols)
    pca_point = pca.transform(scaled_point)
    cluster_pred = int(kmeans.predict(pca_point)[0])
    return cluster_pred, pca_point[0]

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    total_customers = len(df)
    avg_spend = round(float(df['Avg_Spending'].mean()), 2)
    avg_visits = round(float(df['Visit_Frequency'].mean()), 1)
    avg_dwell = round(float(df['Time_Spent_Minutes'].mean()), 1)
    
    # Offer usage %
    yes_offers = len(df[df['Offers_Used'].str.strip().str.lower() == 'yes'])
    offer_rate = round((yes_offers / total_customers) * 100, 1)

    # Segment stats
    cluster_counts = df['Cluster'].value_counts().to_dict()
    cluster_shares = {c: round((cluster_counts.get(c, 0) / total_customers) * 100, 1) for c in range(3)}

    # Aggregates by cluster for charts
    cluster_metrics = {}
    for c in range(3):
        sub = df[df['Cluster'] == c]
        cluster_metrics[c] = {
            "count": len(sub),
            "share": cluster_shares.get(c, 0),
            "avg_spend": round(float(sub['Avg_Spending'].mean()), 2),
            "avg_visits": round(float(sub['Visit_Frequency'].mean()), 1),
            "avg_dwell": round(float(sub['Time_Spent_Minutes'].mean()), 1),
            "spending_score": round(float(sub['Spending_Score'].mean()), 1),
            "top_category": sub['Category_Preference'].mode()[0],
            "offer_yes": int((sub['Offers_Used'].str.strip().str.lower() == 'yes').sum()),
            "offer_no": int((sub['Offers_Used'].str.strip().str.lower() == 'no').sum()),
        }

    # Category counts
    cat_dist = df['Category_Preference'].value_counts().to_dict()

    # Category by cluster table
    cat_by_cluster = pd.crosstab(df['Category_Preference'], df['Cluster']).to_dict()

    return render_template(
        'dashboard.html',
        total_customers=total_customers,
        avg_spend=avg_spend,
        avg_visits=avg_visits,
        avg_dwell=avg_dwell,
        offer_rate=offer_rate,
        cluster_metrics=cluster_metrics,
        cat_dist=cat_dist,
        cat_by_cluster=cat_by_cluster,
        personas=PERSONAS
    )

@app.route('/personas')
def personas():
    return render_template('personas.html', personas=PERSONAS)

@app.route('/lead-generator')
def lead_generator():
    return render_template('lead_generator.html', personas=PERSONAS)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        data = request.get_json(force=True)
        visit_freq = float(data.get('visit_frequency', 10))
        avg_spending = float(data.get('avg_spending', 2500))
        time_spent = float(data.get('time_spent', 90))
        spending_score = float(data.get('spending_score', 50))
        category = data.get('category', 'Fashion')
        offers_used = data.get('offers_used', 'No')

        cluster_id, pca_coords = predict_single_customer(visit_freq, avg_spending, time_spent, spending_score)
        persona_info = PERSONAS[cluster_id]

        response = {
            "status": "success",
            "cluster_id": cluster_id,
            "persona_name": persona_info["name"],
            "badge": persona_info["badge"],
            "tagline": persona_info["tagline"],
            "color": persona_info["color"],
            "lead_tier": persona_info["lead_tier"],
            "strategy": persona_info["marketing_strategy"],
            "promotional_action": persona_info["promotional_action"],
            "pca_coordinates": [round(float(pca_coords[0]), 3), round(float(pca_coords[1]), 3)],
            "inputs": {
                "visit_frequency": visit_freq,
                "avg_spending": avg_spending,
                "time_spent": time_spent,
                "spending_score": spending_score,
                "category": category,
                "offers_used": offers_used
            }
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/market-report')
def market_report():
    return render_template('market_report.html', personas=PERSONAS)

@app.route('/data-explorer')
def data_explorer():
    records = df.to_dict(orient='records')
    return render_template('data_explorer.html', records=records, personas=PERSONAS)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
