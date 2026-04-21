# The Customer Revenue & Retention Engine
## End-to-End Data Analytics Project | SQL Server · Python · Tableau

An end-to-end analytics portfolio project showing how a UK wine retailer can identify profit leakage, prioritise customer retention, and recover growth using SQL, Python, and Tableau.

---

## Executive Summary

This project simulates a UK wine retailer facing a commercially important problem: revenue performance looks healthy on the surface, but deeper analysis shows profit leakage driven by service issues, complaint-linked churn risk, and uneven customer value concentration.

I built an end-to-end analytics solution that connects:

- commercial performance
- customer service quality
- complaint behaviour
- churn risk
- product affinity

into one structured decision-support workflow.

The final output is a two-layer Tableau solution:

- **Dashboard 1 – CFO Lens**: profit leakage, margin pressure, and commercial exposure
- **Dashboard 2 – Growth & Retention Engine**: customer prioritisation, service-risk signals, and intervention workflow

This project was designed to demonstrate senior-style analytical thinking across data modelling, metric design, business framing, dashboard development, and recommendations.

---

## Business Problem

The retailer lacks a joined-up view of:

- where value is leaking
- which customers matter most commercially
- how service quality affects churn risk
- which operational hotspots drive financial loss
- where recovery opportunities exist

The goal was not simply to build a dashboard, but to build an analytics product that helps leadership make better decisions.

---

## Main Business Questions

1. Where is the business currently losing value?
2. Which customer segments matter most commercially?
3. Which customers should be prioritised for intervention?
4. How is service experience affecting churn risk?
5. Which commercial levers could help recover value?

---

## Sub-Business Questions

- Is profit concentrated in fewer customers than expected?
- Which regions show the greatest complaint-linked revenue loss?
- Which complaint patterns are linked to financial exposure?
- Which customers combine high churn risk with high commercial value?
- Which product pairings offer the strongest recovery potential?

---

## Project Outcome

This project delivers a structured analytics workflow that supports both executive and operational decision-making:

- an executive dashboard for financial risk and profit leakage
- an operational dashboard for intervention and retention
- reusable SQL semantic views
- a Python-based churn scoring workflow
- a recruiter-friendly GitHub portfolio project showing end-to-end analytical thinking

---

## What This Project Demonstrates

This project reflects the expectations of a mid-senior to senior Data Analyst role.

It demonstrates my ability to:

- translate an ambiguous business problem into a structured analytics workflow
- build relational datasets and reusable SQL views
- design customer-level commercial and operational metrics
- generate synthetic data and predictive features in Python
- build stakeholder-specific Tableau dashboards
- communicate insight in clear business language
- shift analytics from reporting to decision support

---

## Tools Used

- **SQL Server** – schema design, views, and business logic
- **Python** – synthetic data generation, feature engineering, and churn scoring
- **Tableau** – dashboard design and stakeholder-facing decision tools
- **GitHub** – project presentation and portfolio documentation

---

## Data Structure and Analytical Layers

The project uses a synthetic but relational SQL Server model built around four core entities:

- **Dim_Customers** – customer profile, region, and tier
- **Dim_Products** – product category, price, and cost
- **Fact_Sales** – order-line level transactions
- **Fact_Support_Tickets** – complaints linked to sales

Additional semantic layers were created using SQL views, including:

- customer insights
- revenue leakage
- market basket analysis
- time intelligence
- retention action base

The project is built on a relational SQL Server structure, with Tableau connected primarily to curated analytical views rather than raw fact tables.

---

## Workflow

The project was built in the following sequence:

1. Create the schema in SQL Server
2. Generate synthetic data in Python
3. Build reusable SQL semantic views
4. Score churn probability in Python
5. Connect Tableau to curated analytical views
6. Build two dashboards for different decision layers
7. Package the work as a recruiter-friendly portfolio project

---

## Dashboard 1 – CFO Lens

This dashboard was designed for executive commercial stakeholders.

It helps answer:

- How much profit is being generated?
- How much revenue is at risk?
- How much value has already been lost?
- Where is value concentrated?
- Where is profit leakage most visible?

Core visuals include:

- KPI cards
- profit share vs customer share by tier
- regional complaint-linked revenue loss
- issue-category risk view
- market basket opportunity context

![Dashboard 1](dashboards/dashboard_1_cfo_lens.png)

---

## Dashboard 2 – Growth & Retention Engine

This dashboard was designed for operational and retention-focused stakeholders.

It helps answer:

- Which customers need intervention now?
- How is service quality linked to churn risk?
- Who should be prioritised first?
- What type of action should be taken?

Core visuals include:

- retention priority matrix
- service experience quality vs churn risk
- customer intervention queue
- priority-customer filtering logic

![Dashboard 2](dashboards/dashboard_2_growth_retention_engine.png)

---

## Techniques Used

### SQL
- schema creation
- customer and product dimensions
- customer-level aggregation
- revenue leakage logic
- market basket logic
- time-intelligence logic
- retention action base view

### Python
- synthetic data generation
- basket affinity logic
- repeat complaint behaviour logic
- feature engineering
- logistic regression churn model

### Tableau
- parameter-driven KPI controls
- stakeholder-specific dashboard design
- priority segmentation
- executive vs operational separation
- action-focused visual layout

---

## Key Insights

- Commercial value is concentrated in a relatively small customer segment.
- Complaint-linked revenue loss is uneven across regions.
- Service experience quality is directionally linked to churn risk.
- Targeted intervention is more effective than broad monitoring.
- Some product pairings offer stronger commercial recovery potential than others.

---

## Recommendations

### 1. Prioritise high-value at-risk customers
Use the retention layer to focus proactive outreach on customers with the strongest mix of commercial value and churn risk.

### 2. Target operational hotspots
Complaint-linked leakage should be treated as a targeted operational problem rather than a generic service issue.

### 3. Use service quality as a risk signal
Treat service experience as a leading indicator of commercial risk, not just a support metric.

### 4. Pair operational fixes with commercial recovery
Use stronger product affinity pairings to support revenue recovery while service issues are being addressed.


---

## Repository Structure

```text
sql/        -> schema, views, and business logic
python/     -> data generation and churn scoring scripts
dashboards/ -> dashboard screenshots
docs/       -> supporting project notes
deck/       -> executive summary deck
assets/     -> images and supporting visuals
```

---

## How to Reproduce
- Run the SQL schema setup script
- Run the Python data generation script
- Run the SQL view scripts
- Run the churn prediction script
- Connect Tableau to the curated views
- Rebuild or review the dashboards using the screenshots and documentation provided


---

## Why This Project Matters
This project was built to demonstrate more than technical tool usage.
It shows how analytics can help a business:
- identify where value is leaking
- understand which customers matter most
- connect operational friction to financial impact
- convert analysis into prioritised action

---

## About This Portfolio Project
This is one project in a broader analytics portfolio designed to demonstrate senior-level thinking across:
- commercial analytics
- customer experience analytics
- metric design
- dashboard product design
- executive communication
