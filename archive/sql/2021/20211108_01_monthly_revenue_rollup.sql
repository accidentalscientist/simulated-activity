-- Archive task: Monthly Revenue Rollup
-- Generated for 2021-11-08

SELECT
    DATE_TRUNC('month', invoice_date) AS revenue_month,
    SUM(amount) AS gross_revenue,
    COUNT(DISTINCT customer_id) AS paying_customers
FROM invoices
GROUP BY DATE_TRUNC('month', invoice_date)
ORDER BY revenue_month;
