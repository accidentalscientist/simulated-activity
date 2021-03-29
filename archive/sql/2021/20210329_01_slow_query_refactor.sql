-- Archive task: Slow Query Refactor
-- Generated for 2021-03-29

WITH ranked_orders AS (
    SELECT
        customer_id,
        order_id,
        order_total,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY order_total DESC
        ) AS order_rank
    FROM orders
)
SELECT customer_id, order_id, order_total
FROM ranked_orders
WHERE order_rank <= 3;
