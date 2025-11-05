import duckdb

con = duckdb.connect('ecommerce.duckdb') #Cream baza de date

#Tabelul orders, coloane[order_id ; user_id ; order_date ; status ; amount]
con.execute("""
    CREATE TABLE IF NOT EXISTS orders AS
    SELECT * FROM read_csv_auto('orders.csv');
""")

#Tabelul order_items, coloane[order_id ; product_id ; qty ; unit_price ; category]
con.execute("""
    CREATE TABLE IF NOT EXISTS order_items AS
    SELECT * FROM read_csv_auto('order_items.csv');
""")

#Tabelul events, coloane[user_id ; event_time ; event_name ; device ; page]
con.execute("""
    CREATE TABLE IF NOT EXISTS events AS
    SELECT * FROM read_csv_auto('events.csv');
""")

#Tabelul marketing_spend, coloane[day ; channel ;spend]
con.execute("""
    CREATE TABLE IF NOT EXISTS marketing_spend AS
    SELECT * FROM read_csv_auto('marketing_spend.csv');
""")

#Tabelul subscriptions, coloane[user_id ; plan ; started_at ; canceled_at ; auto_renew]
con.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions AS
    SELECT * FROM read_csv_auto('subscriptions.csv');
""")

#Tabel users coloane:[user_id ; signup_date ; country ; channel]
con.execute("""
    CREATE TABLE IF NOT EXISTS users AS
    SELECT * FROM read_csv_auto('users.csv');
""")

#print(con.execute("SHOW TABLES").fetchdf()) #Verificam daca baza de date contine tabelele noastre
con = duckdb.connect('ecommerce.duckdb') #Salvam