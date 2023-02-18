-- Archive task: Windowed Churn Analysis
-- Generated for 2023-02-18

SELECT
    customer_id,
    activity_month,
    active_days,
    LAG(active_days) OVER (
        PARTITION BY customer_id
        ORDER BY activity_month
    ) AS previous_active_days
FROM monthly_customer_activity
WHERE active_days = 0;
