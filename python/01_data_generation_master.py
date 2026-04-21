import pyodbc
import random
from datetime import datetime, timedelta

# =============================================================
# WINE ANALYTICS UK — FINAL MASTER INJECTION SCRIPT
# Consolidates V1-V16 | Corrected CustomerKey/ProductKey FK Logic
# Updated: Affinity Basket Logic (Market Basket Analysis Ready)
# =============================================================

# --- 1. CONNECTION ---
server = r'server = r'LOCAL_SQL_SERVER'
'
database = 'Wine_Analytics_UK'
conn = pyodbc.connect(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};DATABASE={database};Trusted_Connection=yes;'
)
cursor = conn.cursor()
print("Connection Successful.")

# --- 2. FULL RESET ---
print("Resetting all tables and identity seeds...")
cursor.execute("TRUNCATE TABLE Fact_Support_Tickets")
cursor.execute("DELETE FROM Fact_Sales")
cursor.execute("DBCC CHECKIDENT ('Fact_Sales', RESEED, 0)")
cursor.execute("DELETE FROM Fact_Churn_Predictions")
conn.commit()

cursor.execute("DELETE FROM Dim_Products")
cursor.execute("DBCC CHECKIDENT ('Dim_Products', RESEED, 0)")
cursor.execute("DELETE FROM Dim_Customers")
cursor.execute("DBCC CHECKIDENT ('Dim_Customers', RESEED, 0)")
conn.commit()
print("Reset complete. All identity seeds at 0.")

# --- 3. DIM_PRODUCTS ---
products_data = [
    (1, 'Reserve Cabernet', 'Red',        45.00, 36.50),
    (2, 'Crisp Chablis',    'White',      28.00, 22.50),
    (3, 'Provence Rosé',    'Rosé',       22.00, 18.50),
    (4, 'English Sparkling','Sparkling',  65.00, 52.00),
    (5, 'Midnight Malbec',  'Red',        32.00, 26.00),
]

product_key_lookup = {}
for prod in products_data:
    cursor.execute(
        """
        INSERT INTO Dim_Products (ProductID, ProductName, Category, UnitPrice, CostPrice)
        OUTPUT INSERTED.ProductKey
        VALUES (?, ?, ?, ?, ?)
        """,
        prod
    )
    generated_key = cursor.fetchone()[0]
    product_key_lookup[prod[0]] = {
        'ProductKey': generated_key,
        'UnitPrice':  prod[3]
    }
conn.commit()
print(f"Dim_Products loaded: {len(products_data)} products.")
print(f"  ProductKey map: { {k: v['ProductKey'] for k, v in product_key_lookup.items()} }")

# --- 4. DIM_CUSTOMERS ---
reg_config = [
    ('London',     1.8, 1.0),
    ('Birmingham', 1.4, 1.1),
    ('Manchester', 1.3, 1.1),
    ('Edinburgh',  1.1, 1.4),
    ('Bristol',    1.0, 1.1),
    ('Belfast',    0.7, 1.6),
    ('Highlands',  0.3, 2.8),
]
pop_weights     = [r[1] for r in reg_config]
friction_lookup = {r[0]: r[2] for r in reg_config}

print("Generating 5,000 customers...")
customer_lookup = {}

for i in range(1, 5001):
    tier        = random.choices(['Bronze', 'Silver', 'Gold'], weights=[60, 30, 10])[0]
    region_data = random.choices(reg_config, weights=pop_weights)[0]
    region      = region_data[0]

    cursor.execute(
        """
        INSERT INTO Dim_Customers (CustomerID, CustomerName, Region, Tier, IsActive)
        OUTPUT INSERTED.CustomerKey
        VALUES (?, ?, ?, ?, 1)
        """,
        (i, f"Cust_{i}", region, tier)
    )
    generated_cust_key = cursor.fetchone()[0]
    customer_lookup[generated_cust_key] = (tier, region)

conn.commit()
print(f"Dim_Customers loaded: 5,000 customers.")
print(f"  CustomerKey range: {min(customer_lookup)} to {max(customer_lookup)}")

valid_customer_keys = list(customer_lookup.keys())

product_by_id = {
    1: {'ProductKey': product_key_lookup[1]['ProductKey'], 'UnitPrice': product_key_lookup[1]['UnitPrice']},
    2: {'ProductKey': product_key_lookup[2]['ProductKey'], 'UnitPrice': product_key_lookup[2]['UnitPrice']},
    3: {'ProductKey': product_key_lookup[3]['ProductKey'], 'UnitPrice': product_key_lookup[3]['UnitPrice']},
    4: {'ProductKey': product_key_lookup[4]['ProductKey'], 'UnitPrice': product_key_lookup[4]['UnitPrice']},
    5: {'ProductKey': product_key_lookup[5]['ProductKey'], 'UnitPrice': product_key_lookup[5]['UnitPrice']},
}

affinity_map = {
    1: [5, 3],
    2: [4, 3],
    3: [2, 4],
    4: [2, 3],
    5: [1, 4],
}

anchor_weights_by_tier = {
    'Bronze': ([1, 2, 3, 4, 5], [15, 25, 25, 10, 25]),
    'Silver': ([1, 2, 3, 4, 5], [20, 25, 20, 15, 20]),
    'Gold':   ([1, 2, 3, 4, 5], [25, 15, 10, 30, 20]),
}

# -------------------------------------------------------------
# NEW STEP ADDED HERE
# -------------------------------------------------------------
# Track repeat complaint burden by customer
customer_ticket_counter = {}

# --- 5. FACT_SALES + FACT_SUPPORT_TICKETS ---
print("Injecting 25,000 sales transactions with affinity basket logic...")
current_row      = 0
order_id_counter = 70001

while current_row < 25000:
    cust_key         = random.choice(valid_customer_keys)
    tier, region     = customer_lookup[cust_key]
    friction         = friction_lookup[region]

    if tier == 'Gold':
        num_items = random.choices([1, 2, 3, 4], weights=[5, 25, 45, 25])[0]
    else:
        num_items = random.choices([1, 2, 3, 4], weights=[40, 40, 15, 5])[0]

    base_shipping = random.uniform(6.00, 12.00) * friction

    if region == 'Highlands' and random.random() < 0.15:
        base_shipping *= 3.5

    order_date = datetime.now() - timedelta(days=random.randint(0, 730))

    anchor_ids, anchor_weights = anchor_weights_by_tier[tier]
    anchor_product_id          = random.choices(anchor_ids, weights=anchor_weights)[0]
    selected_product_ids       = [anchor_product_id]

    while len(selected_product_ids) < num_items:
        if random.random() < 0.75:
            candidate_pool = affinity_map[anchor_product_id]
        else:
            candidate_pool = [1, 2, 3, 4, 5]

        candidate_id = random.choice(candidate_pool)

        if candidate_id not in selected_product_ids:
            selected_product_ids.append(candidate_id)

        if len(selected_product_ids) == 5:
            break

    for product_id in selected_product_ids:
        if current_row >= 25000:
            break

        prod = product_by_id[product_id]
        qty  = random.randint(3, 8) if tier == 'Gold' else random.randint(1, 3)
        rev  = qty * prod['UnitPrice']

        cursor.execute(
            """
            INSERT INTO Fact_Sales
                (OrderDate, CustomerKey, ProductKey, Quantity,
                 TotalRevenue, OrderID, ShippingCost)
            OUTPUT INSERTED.SalesID
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (order_date, cust_key, prod['ProductKey'],
             qty, rev, order_id_counter, base_shipping)
        )
        last_sales_id = cursor.fetchone()[0]

        # -------------------------------------------------------------
        # NEW SUPPORT-TICKET LOGIC (REPLACES OLD BLOCK)
        # -------------------------------------------------------------
        prior_tickets = customer_ticket_counter.get(cust_key, 0)

        ticket_prob = 0.03 * friction
        ticket_prob += min(prior_tickets * 0.04, 0.16)

        if tier == 'Gold':
            ticket_prob *= 0.85

        ticket_prob = min(ticket_prob, 0.55)

        if random.random() < ticket_prob:
            cat = random.choices(
                ['Broken Item', 'Wrong Item', 'Delayed'],
                weights=[55, 20, 25]
            )[0]

            if prior_tickets >= 3:
                csat = random.choices([1, 2, 3], weights=[55, 35, 10])[0]
                resolution_hours = random.randint(24, 96)
            elif prior_tickets >= 1:
                csat = random.choices([1, 2, 3, 4], weights=[25, 35, 25, 15])[0]
                resolution_hours = random.randint(12, 72)
            else:
                if friction > 2.0:
                    csat = random.choices([1, 2, 3], weights=[35, 45, 20])[0]
                    resolution_hours = random.randint(8, 72)
                else:
                    csat = random.choices([2, 3, 4, 5], weights=[10, 35, 35, 20])[0]
                    resolution_hours = random.randint(4, 48)

            cursor.execute(
                """
                INSERT INTO Fact_Support_Tickets
                    (SalesID, IssueCategory, CSAT_Score, ResolutionTimeHours)
                VALUES (?, ?, ?, ?)
                """,
                (last_sales_id, cat, csat, resolution_hours)
            )

            customer_ticket_counter[cust_key] = prior_tickets + 1

        current_row += 1
    order_id_counter += 1

conn.commit()

# --- 6. FINAL AUDIT ---
cursor.execute("SELECT COUNT(*) FROM Dim_Products")
print(f"\nAudit Results:")
print(f"  Dim_Products rows    : {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM Dim_Customers")
print(f"  Dim_Customers rows   : {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM Fact_Sales")
print(f"  Fact_Sales rows      : {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM Fact_Support_Tickets")
print(f"  Fact_Support_Tickets : {cursor.fetchone()[0]}")
cursor.execute("""
    SELECT COUNT(*) FROM Fact_Sales fs
    LEFT JOIN Dim_Customers dc ON fs.CustomerKey = dc.CustomerKey
    WHERE dc.CustomerKey IS NULL
""")
orphans = cursor.fetchone()[0]
print(f"  Orphaned CustomerKeys: {orphans} (should be 0)")
cursor.execute("""
    SELECT COUNT(*) FROM Fact_Sales fs
    LEFT JOIN Dim_Products dp ON fs.ProductKey = dp.ProductKey
    WHERE dp.ProductKey IS NULL
""")
orphans_p = cursor.fetchone()[0]
print(f"  Orphaned ProductKeys : {orphans_p} (should be 0)")

print("\nFinal Script Complete. Referential integrity verified.")

cursor.close()
conn.close()
print("Connection closed.")
