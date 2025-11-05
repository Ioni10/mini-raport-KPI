from create_database import con

#Daily sales 30 zile
# print(con.execute("""
#     SELECT
#            CAST(order_date AS DATE) AS day,
#            COUNT(order_id) AS orders,
#            SUM(amount) AS revenue
#     FROM orders
#     WHERE status = 'paid'
#       AND order_date >= CURRENT_DATE - INTERVAL '30 days'
#       GROUP BY day
#       ORDER BY day;
#""").fetchdf())

#Top 5 categorii (90 zile):
# print(con.execute("""
#     SELECT i.category,
#     SUM(i.unit_price * i.qty) AS Total_Money_Collected
#     FROM orders o
#     JOIN order_items i
#         ON o.order_id = i.order_id
#     WHERE o.status = 'paid'
#       AND o.order_date >= CURRENT_DATE - INTERVAL '90 days'
#     GROUP BY i.category
#     ORDER BY Total_Money_Collected DESC
#     LIMIT 5
# """).fetchdf())

#Refund rate lunar = 'refunded_orders / paid_orders'

print(con.execute("""
    SELECT
        STRFTIME('%Y-%m', order_date) AS month,
        SUM(CASE WHEN status='refunded' THEN 1 ELSE 0 END) * 1.0/
        SUM(CASE WHEN status='paid' THEN 1 ELSE 0 END) AS refund_rate
    FROM orders
    GROUP BY month
    ORDER BY month""").fetchdf())

#ROAS zilnic = join 'marketing_spend' + revenue ('paid').