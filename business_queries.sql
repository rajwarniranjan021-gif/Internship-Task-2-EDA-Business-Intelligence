-- Q1: Top 5 Products by Revenue (All Time)
SELECT product_name, category,
               ROUND(SUM(total_revenue),2) AS total_revenue,
               COUNT(*) AS transactions
        FROM sales
        GROUP BY product_name, category
        ORDER BY total_revenue DESC
        LIMIT 5

────────────────────────────────────────────────────────────

-- Q2: Monthly Revenue Trend (Last 12 Months)
SELECT txn_year, txn_month,
               COUNT(*) AS transactions,
               ROUND(SUM(total_revenue),2) AS revenue,
               ROUND(AVG(total_revenue),2) AS avg_order_value
        FROM sales
        WHERE txn_year >= 2024
        GROUP BY txn_year, txn_month
        ORDER BY txn_year, txn_month

────────────────────────────────────────────────────────────

-- Q3: Revenue & Avg Satisfaction by Region
SELECT region,
               ROUND(SUM(total_revenue),2) AS total_revenue,
               COUNT(DISTINCT customer_id) AS unique_customers,
               ROUND(AVG(customer_satisfaction),2) AS avg_satisfaction
        FROM sales
        GROUP BY region
        ORDER BY total_revenue DESC

────────────────────────────────────────────────────────────

-- Q4: Payment Method Popularity & Revenue
SELECT payment_method,
               COUNT(*) AS transactions,
               ROUND(COUNT(*)*100.0/SUM(COUNT(*)) OVER(),2) AS pct_transactions,
               ROUND(SUM(total_revenue),2) AS total_revenue
        FROM sales
        GROUP BY payment_method
        ORDER BY transactions DESC

────────────────────────────────────────────────────────────

-- Q5: Marketing Channel Effectiveness
SELECT marketing_channel,
               COUNT(*) AS leads,
               ROUND(AVG(total_revenue),2) AS avg_revenue_per_lead,
               ROUND(SUM(total_revenue),2) AS total_revenue
        FROM sales
        GROUP BY marketing_channel
        ORDER BY total_revenue DESC

────────────────────────────────────────────────────────────

-- Q6: Category Performance by Discount
SELECT category,
               discount_applied,
               COUNT(*) AS transactions,
               ROUND(AVG(total_revenue),2) AS avg_revenue
        FROM sales
        GROUP BY category, discount_applied
        ORDER BY category, discount_applied

────────────────────────────────────────────────────────────

-- Q7: Top Customer Segments by Revenue
SELECT age_group,
               ROUND(SUM(total_revenue),2) AS total_revenue,
               COUNT(*) AS purchases,
               ROUND(AVG(total_revenue),2) AS avg_order_value
        FROM sales
        GROUP BY age_group
        ORDER BY total_revenue DESC

────────────────────────────────────────────────────────────

