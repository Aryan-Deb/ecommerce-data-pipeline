-- ============================================
-- E-COMMERCE DATA PIPELINE
-- ANALYTICS QUERIES
-- ============================================


-- ============================================
-- 1. TOTAL REVENUE
-- ============================================

SELECT
    ROUND(
        SUM(oi.quantity * p.price)::numeric,
        2
    ) AS total_revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'completed';


-- ============================================
-- 2. AVERAGE ORDER VALUE
-- ============================================

SELECT
    ROUND(
        SUM(oi.quantity * p.price)::numeric
        / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
WHERE o.status = 'completed';


-- ============================================
-- 3. REVENUE BY CATEGORY
-- ============================================

SELECT
    p.category,
    ROUND(
        SUM(oi.quantity * p.price)::numeric,
        2
    ) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY revenue DESC;


-- ============================================
-- 4. TOP 10 PRODUCTS BY REVENUE
-- ============================================

SELECT
    p.product_id,
    p.product_name,
    SUM(oi.quantity) AS units_sold,
    ROUND(
        SUM(oi.quantity * p.price)::numeric,
        2
    ) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY
    p.product_id,
    p.product_name
ORDER BY revenue DESC
LIMIT 10;


-- ============================================
-- 5. TOP 10 CUSTOMERS BY SPENDING
-- ============================================

SELECT
    c.customer_id,
    c.name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(
        SUM(oi.quantity * p.price)::numeric,
        2
    ) AS total_spend
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY
    c.customer_id,
    c.name
ORDER BY total_spend DESC
LIMIT 10;


-- ============================================
-- 6. MONTHLY REVENUE
-- ============================================

SELECT
    TO_CHAR(
        DATE_TRUNC('month', o.order_date::date),
        'YYYY-MM'
    ) AS month,
    ROUND(
        SUM(oi.quantity * p.price)::numeric,
        2
    ) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY
    DATE_TRUNC('month', o.order_date::date)
ORDER BY
    DATE_TRUNC('month', o.order_date::date);


-- ============================================
-- 7. ORDER STATUS DISTRIBUTION
-- ============================================

SELECT
    status,
    COUNT(*) AS order_count
FROM orders
GROUP BY status
ORDER BY order_count DESC;


-- ============================================
-- 8. TOTAL UNITS SOLD
-- ============================================

SELECT
    SUM(oi.quantity) AS total_units_sold
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'completed';


-- ============================================
-- 9. DAILY REVENUE
-- ============================================

SELECT
    o.order_date::date AS order_date,
    ROUND(
        SUM(oi.quantity * p.price)::numeric,
        2
    ) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY o.order_date::date
ORDER BY o.order_date::date;


-- ============================================
-- 10. CUSTOMER ORDER FREQUENCY
-- ============================================

SELECT
    c.customer_id,
    c.name,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.status = 'completed'
GROUP BY
    c.customer_id,
    c.name
ORDER BY total_orders DESC;