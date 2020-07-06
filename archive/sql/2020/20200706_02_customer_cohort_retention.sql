-- Archive task: Customer Cohort Retention
-- Generated for 2020-07-06

WITH first_seen AS (
    SELECT customer_id, MIN(DATE_TRUNC('month', event_date)) AS cohort_month
    FROM product_events
    GROUP BY customer_id
),
activity AS (
    SELECT customer_id, DATE_TRUNC('month', event_date) AS activity_month
    FROM product_events
    GROUP BY customer_id, DATE_TRUNC('month', event_date)
)
SELECT
    first_seen.cohort_month,
    activity.activity_month,
    COUNT(*) AS retained_customers
FROM first_seen
JOIN activity USING (customer_id)
GROUP BY first_seen.cohort_month, activity.activity_month;
