# SQL Scripts

This folder contains all SQL logic used in the Customer Revenue Retention Model.  
Each script builds a different part of the analytical layer — from customer insights to revenue leakage, market basket analysis, time‑based metrics, and the final retention action base.

Although the project’s data is generated in Python, the SQL layer defines the semantic model that powers the dashboards, KPIs, and retention strategy.

Scripts are ordered to reflect the logical flow of the analysis.

---

## 1. `01_schema_setup.sql`  
Creates the core dimensional and fact tables:

- `Dim_Products`
- `Dim_Customers`
- `Fact_Sales`
- `Fact_Support_Tickets`

Includes constraints, foreign keys, and basic indexing.  
This is the foundation for all downstream views.

---

## 2. `02_customer_insights_view.sql` — Customer Insights (RFM + Behaviour)  
Builds the main customer‑level analytical view:

- Recency, Frequency, Monetary (RFM)
- Net profit allocation
- CSAT and ticket behaviour
- Customer status (Active, At‑Risk, Churned)
- Revenue and profit buckets
- Customer tier and region

This is the primary customer profile view used across the project.

---

## 3. `03_revenue_leakage_view.sql` — Revenue Leakage Analysis  
Analyses support tickets to quantify:

- Revenue at risk  
- Revenue lost  
- CSAT impact  
- Issue category performance  
- % of total business revenue affected  

This view identifies where the business is losing money due to service issues.

---

## 4. `04_market_basket_view.sql` — Market Basket Analysis (MBA)  
Generates product‑pair insights:

- Support  
- Confidence  
- Lift  
- Pair‑level net profit  

This view helps identify cross‑sell opportunities and profitable product associations.

---

## 5. `05_time_intelligence_view.sql` — Time Intelligence Metrics  
Daily‑level metrics for KPI dashboards:

- Daily revenue  
- Daily net profit  

Used for trendlines, period comparisons, and executive KPI visuals.

---

## 6. `06_retention_action_base_view.sql` — Retention Action Base  
Final consolidated view combining:

- Customer insights  
- Churn probability (from Python model)  
- Basket size  
- Profit banding  
- Ticket burden banding  

This is the core dataset used to prioritise customer retention actions.

---

### Notes

- These scripts are not intended to be run manually in sequence.  
- They document the analytical layer that powers the dashboards and retention engine.  
- Data generation and churn modelling are handled in the `/python` folder.

