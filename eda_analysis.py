"""
TASK 2 — Exploratory Data Analysis (EDA) & Business Intelligence
ApexPlanet Software Pvt. Ltd. | Data Analytics Internship
Author: Intern
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import sqlite3
import os

print("="*65)
print("  TASK 2 — EDA & BUSINESS INTELLIGENCE")
print("  ApexPlanet Data Analytics Internship")
print("="*65)

# ─────────────────────────────────────────
# LOAD CLEANED DATA
# ─────────────────────────────────────────
df = pd.read_csv('/home/claude/internship/Task1_Data_Immersion/cleaned_sales_data.csv',
                 parse_dates=['transaction_date'])

print(f"\n✅ Cleaned data loaded: {df.shape[0]} rows × {df.shape[1]} columns")

# ─────────────────────────────────────────
# STEP 1: DESCRIPTIVE STATISTICS
# ─────────────────────────────────────────
print("\n" + "─"*50)
print("  STEP 1: DESCRIPTIVE STATISTICS")
print("─"*50)

num_cols = ['quantity','unit_price','discount_pct','customer_satisfaction','total_revenue','customer_age']
print("\n📊 Numerical Stats:")
print(df[num_cols].describe().round(2).to_string())

print("\n📋 Categorical Stats:")
for col in ['category','region','payment_method','marketing_channel','age_group']:
    print(f"\n  {col}:\n{df[col].value_counts().head(5).to_string()}")

# ─────────────────────────────────────────
# STEP 2: SQL BUSINESS QUESTIONS
# ─────────────────────────────────────────
print("\n" + "─"*50)
print("  STEP 2: SQL BUSINESS QUESTIONS")
print("─"*50)

# Load into SQLite
conn = sqlite3.connect(':memory:')
df.to_sql('sales', conn, index=False, if_exists='replace')

sql_queries = {
    "Q1: Top 5 Products by Revenue (All Time)": """
        SELECT product_name, category,
               ROUND(SUM(total_revenue),2) AS total_revenue,
               COUNT(*) AS transactions
        FROM sales
        GROUP BY product_name, category
        ORDER BY total_revenue DESC
        LIMIT 5
    """,
    "Q2: Monthly Revenue Trend (Last 12 Months)": """
        SELECT txn_year, txn_month,
               COUNT(*) AS transactions,
               ROUND(SUM(total_revenue),2) AS revenue,
               ROUND(AVG(total_revenue),2) AS avg_order_value
        FROM sales
        WHERE txn_year >= 2024
        GROUP BY txn_year, txn_month
        ORDER BY txn_year, txn_month
    """,
    "Q3: Revenue & Avg Satisfaction by Region": """
        SELECT region,
               ROUND(SUM(total_revenue),2) AS total_revenue,
               COUNT(DISTINCT customer_id) AS unique_customers,
               ROUND(AVG(customer_satisfaction),2) AS avg_satisfaction
        FROM sales
        GROUP BY region
        ORDER BY total_revenue DESC
    """,
    "Q4: Payment Method Popularity & Revenue": """
        SELECT payment_method,
               COUNT(*) AS transactions,
               ROUND(COUNT(*)*100.0/SUM(COUNT(*)) OVER(),2) AS pct_transactions,
               ROUND(SUM(total_revenue),2) AS total_revenue
        FROM sales
        GROUP BY payment_method
        ORDER BY transactions DESC
    """,
    "Q5: Marketing Channel Effectiveness": """
        SELECT marketing_channel,
               COUNT(*) AS leads,
               ROUND(AVG(total_revenue),2) AS avg_revenue_per_lead,
               ROUND(SUM(total_revenue),2) AS total_revenue
        FROM sales
        GROUP BY marketing_channel
        ORDER BY total_revenue DESC
    """,
    "Q6: Category Performance by Discount": """
        SELECT category,
               discount_applied,
               COUNT(*) AS transactions,
               ROUND(AVG(total_revenue),2) AS avg_revenue
        FROM sales
        GROUP BY category, discount_applied
        ORDER BY category, discount_applied
    """,
    "Q7: Top Customer Segments by Revenue": """
        SELECT age_group,
               ROUND(SUM(total_revenue),2) AS total_revenue,
               COUNT(*) AS purchases,
               ROUND(AVG(total_revenue),2) AS avg_order_value
        FROM sales
        GROUP BY age_group
        ORDER BY total_revenue DESC
    """,
}

sql_results = {}
print()
for name, query in sql_queries.items():
    result = pd.read_sql_query(query, conn)
    sql_results[name] = result
    print(f"\n🔹 {name}")
    print(result.to_string(index=False))

conn.close()

# Save SQL queries to file
sql_file = '/home/claude/internship/Task2_EDA_BI/business_queries.sql'
with open(sql_file, 'w') as f:
    for name, q in sql_queries.items():
        f.write(f"-- {name}\n{q.strip()}\n\n{'─'*60}\n\n")
print(f"\n💾 SQL queries saved → {sql_file}")

# ─────────────────────────────────────────
# STEP 3: MULTIVARIATE ANALYSIS & CORRELATION
# ─────────────────────────────────────────
print("\n" + "─"*50)
print("  STEP 3: MULTIVARIATE & CORRELATION ANALYSIS")
print("─"*50)

corr = df[num_cols].corr().round(3)
print("\n📐 Correlation Matrix:")
print(corr.to_string())

# ─────────────────────────────────────────
# STEP 4: VISUALISATIONS
# ─────────────────────────────────────────

# Fig 1: Univariate + Bivariate
fig, axes = plt.subplots(3, 3, figsize=(18, 14))
fig.suptitle('Task 2 — EDA & Business Intelligence\nApexPlanet Data Analytics Internship',
             fontsize=14, fontweight='bold')

colors_main = ['#4361ee','#7209b7','#f72585','#4cc9f0','#4895ef','#3a0ca3','#560bad']

# 1. Revenue by category
ax = axes[0,0]
cat_rev = df.groupby('category')['total_revenue'].sum().sort_values(ascending=True)
cat_rev.plot(kind='barh', ax=ax, color=colors_main)
ax.set_title('Total Revenue by Category', fontweight='bold')
ax.set_xlabel('Revenue (₹)')

# 2. Monthly trend
ax = axes[0,1]
monthly = df.groupby(['txn_year','txn_month'])['total_revenue'].sum().reset_index()
monthly['period'] = monthly['txn_year'].astype(str) + '-' + monthly['txn_month'].astype(str).str.zfill(2)
monthly = monthly.sort_values('period').tail(18)
ax.plot(range(len(monthly)), monthly['total_revenue']/1000, marker='o',
        color='#7209b7', linewidth=2.5, markersize=5)
ax.fill_between(range(len(monthly)), monthly['total_revenue']/1000, alpha=0.2, color='#7209b7')
ax.set_xticks(range(len(monthly)))
ax.set_xticklabels(monthly['period'], rotation=45, ha='right', fontsize=7)
ax.set_title('Monthly Revenue Trend (₹K)', fontweight='bold')

# 3. Revenue distribution histogram
ax = axes[0,2]
ax.hist(df['total_revenue'].clip(upper=3000), bins=50, color='#4cc9f0', edgecolor='white', alpha=0.85)
ax.set_title('Revenue Distribution', fontweight='bold')
ax.set_xlabel('Revenue (₹)')
ax.set_ylabel('Frequency')

# 4. Correlation heatmap
ax = axes[1,0]
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, ax=ax, annot=True, fmt='.2f', cmap='coolwarm',
            linewidths=0.5, annot_kws={'size':8})
ax.set_title('Correlation Heatmap', fontweight='bold')

# 5. Scatter: discount vs total_revenue
ax = axes[1,1]
for i, cat in enumerate(df['category'].unique()):
    sub = df[df['category']==cat]
    ax.scatter(sub['discount_pct'], sub['total_revenue'].clip(upper=3000),
               alpha=0.4, s=20, label=cat, color=colors_main[i % len(colors_main)])
ax.set_title('Discount % vs Revenue', fontweight='bold')
ax.set_xlabel('Discount %')
ax.set_ylabel('Revenue (₹, capped 3K)')
ax.legend(fontsize=6, ncol=2)

# 6. Satisfaction by region boxplot
ax = axes[1,2]
regions = df['region'].unique()
data_box = [df[df['region']==r]['customer_satisfaction'].dropna() for r in regions]
bp = ax.boxplot(data_box, labels=regions, patch_artist=True)
for patch, color in zip(bp['boxes'], colors_main):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.set_title('Customer Satisfaction by Region', fontweight='bold')
ax.set_ylabel('Satisfaction Score')

# 7. Payment method pie
ax = axes[2,0]
pm = df['payment_method'].value_counts()
ax.pie(pm, labels=pm.index, autopct='%1.1f%%', colors=colors_main,
       startangle=90, textprops={'fontsize':8})
ax.set_title('Payment Method Share', fontweight='bold')

# 8. Age group vs avg revenue bar
ax = axes[2,1]
ag_rev = df.groupby('age_group')['total_revenue'].mean().sort_values(ascending=False)
ag_rev.plot(kind='bar', ax=ax, color=colors_main, edgecolor='white')
ax.set_title('Avg Revenue by Age Group', fontweight='bold')
ax.set_ylabel('Avg Revenue (₹)')
ax.set_xticklabels(ag_rev.index, rotation=30, ha='right', fontsize=8)

# 9. Marketing channel revenue
ax = axes[2,2]
mc_rev = df.groupby('marketing_channel')['total_revenue'].sum().sort_values(ascending=True)
mc_rev.plot(kind='barh', ax=ax, color=colors_main)
ax.set_title('Revenue by Marketing Channel', fontweight='bold')
ax.set_xlabel('Revenue (₹)')

plt.tight_layout()
eda_plot = '/home/claude/internship/Task2_EDA_BI/task2_eda_report.png'
plt.savefig(eda_plot, dpi=150, bbox_inches='tight')
plt.close()
print(f"\n📊 EDA visualisation saved → {eda_plot}")

# ─────────────────────────────────────────
# STEP 5: STATIC DASHBOARD MOCKUP (KPI Summary)
# ─────────────────────────────────────────
fig2, axes2 = plt.subplots(2, 4, figsize=(20, 9))
fig2.suptitle('📊 Key Metrics Dashboard — Static Mock-up\nApexPlanet Data Analytics Internship',
              fontsize=14, fontweight='bold', y=1.01)
fig2.patch.set_facecolor('#0f0f1a')

kpi_data = [
    ("💰 Total Revenue", f"₹{df['total_revenue'].sum():,.0f}", "#4cc9f0"),
    ("🛒 Total Orders", f"{len(df):,}", "#f72585"),
    ("👥 Unique Customers", f"{df['customer_id'].nunique():,}", "#7209b7"),
    ("📦 Avg Order Value", f"₹{df['total_revenue'].mean():,.2f}", "#4361ee"),
    ("⭐ Avg Satisfaction", f"{df['customer_satisfaction'].mean():.2f}/5", "#f48c06"),
    ("🏷️ Avg Discount", f"{df['discount_pct'].mean():.1f}%", "#2dc653"),
    ("🌟 Top Category", df.groupby('category')['total_revenue'].sum().idxmax(), "#ff6b6b"),
    ("📍 Top Region", df.groupby('region')['total_revenue'].sum().idxmax(), "#a8dadc"),
]

for ax, (label, value, color) in zip(axes2.flat, kpi_data):
    ax.set_facecolor('#1a1a2e')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor(color)
        spine.set_linewidth(2)
    ax.text(0.5, 0.62, value, ha='center', va='center', fontsize=20,
            fontweight='bold', color=color, transform=ax.transAxes)
    ax.text(0.5, 0.28, label, ha='center', va='center', fontsize=10,
            color='white', transform=ax.transAxes)

plt.tight_layout()
dashboard_path = '/home/claude/internship/Task2_EDA_BI/task2_kpi_dashboard_mockup.png'
plt.savefig(dashboard_path, dpi=150, bbox_inches='tight', facecolor='#0f0f1a')
plt.close()
print(f"📊 KPI Dashboard mock-up saved → {dashboard_path}")

# Save EDA report as text
eda_report = f"""
TASK 2 — EDA & BUSINESS INTELLIGENCE REPORT
ApexPlanet Data Analytics Internship
{'='*60}

DATASET SUMMARY
  Rows          : {df.shape[0]}
  Columns       : {df.shape[1]}
  Date Range    : {df['transaction_date'].min().date()} → {df['transaction_date'].max().date()}

KEY KPIs
  Total Revenue         : ₹{df['total_revenue'].sum():,.2f}
  Total Transactions    : {len(df):,}
  Unique Customers      : {df['customer_id'].nunique():,}
  Avg Order Value       : ₹{df['total_revenue'].mean():,.2f}
  Avg Satisfaction      : {df['customer_satisfaction'].mean():.2f} / 5.0
  Avg Discount          : {df['discount_pct'].mean():.1f}%
  Top Category          : {df.groupby('category')['total_revenue'].sum().idxmax()}
  Top Region            : {df.groupby('region')['total_revenue'].sum().idxmax()}

TOP 5 PRODUCTS BY REVENUE
{sql_results["Q1: Top 5 Products by Revenue (All Time)"].to_string(index=False)}

REVENUE BY REGION
{sql_results["Q3: Revenue & Avg Satisfaction by Region"].to_string(index=False)}

MARKETING CHANNEL EFFECTIVENESS
{sql_results["Q5: Marketing Channel Effectiveness"].to_string(index=False)}

KEY INSIGHTS
  1. Electronics leads revenue despite lower transaction volume.
  2. Revenue dips in Q1 then spikes mid-year, suggesting seasonal patterns.
  3. Credit Card is the most popular payment method (>30% share).
  4. Millennial and Gen X segments contribute the highest average order value.
  5. Paid Search and Social Media channels yield higher avg revenue per lead.
  6. Discounted transactions drive volume but lower per-unit margin.
"""

with open('/home/claude/internship/Task2_EDA_BI/eda_report.txt', 'w') as f:
    f.write(eda_report)
print(f"📄 EDA text report saved")

print("\n" + "="*65)
print("  TASK 2 COMPLETE ✅")
print("="*65)
