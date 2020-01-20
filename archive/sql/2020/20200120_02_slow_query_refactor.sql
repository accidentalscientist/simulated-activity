-- Archive task: Slow Query Refactor
-- Generated for 2020-01-20

WITH monthly_activity AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', event_date) AS activity_month,
        COUNT(*) AS event_count
    FROM product_events
    GROUP BY customer_id, DATE_TRUNC('month', event_date)
),
ranked_activity AS (
    SELECT
        customer_id,
        activity_month,
        event_count,
        LAG(event_count) OVER (
            PARTITION BY customer_id
            ORDER BY activity_month
        ) AS previous_event_count
    FROM monthly_activity
)
SELECT *
FROM ranked_activity
WHERE event_count >= COALESCE(previous_event_count, 0);
