import pandas as pd
import random
from faker import Faker
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import sqlite3
from faker import Faker
import streamlit as st

import streamlit as st

st.success("✅ Data successfully loaded!", icon="✅")

# Initialize Faker
fake = Faker()

# Sample menu items
menu_items = [
    ("Pasta", "Main Course", 12.99), 
    ("Burger", "Main Course", 10.99),
    ("Salad", "Starter", 7.99),
    ("Pizza", "Main Course", 15.99),
    ("Ice Cream", "Dessert", 5.99),
    ("Coffee", "Beverage", 3.99)
]

# Generate Sales Data
sales_data = []
for _ in range(500): 
    item, category, price = random.choice(menu_items)
    quantity = random.randint(1, 5)
    sales_data.append({
        "sale_id": fake.unique.random_int(min=100000, max=999999),
        "date": fake.date_this_year(),
        "time": fake.time(),
        "menu_item": item,
        "category": category,
        "quantity_sold": quantity,
        "price_per_item": price,
        "total_price": round(quantity * price, 2),
        "payment_method": random.choice(["Cash", "Card", "Mobile Money"])
    })
df_sales = pd.DataFrame(sales_data)

# Generate Inventory Data
inventory_data = []
for _ in range(10):
    inventory_data.append({
        "item_id": fake.random_int(min=1000, max=9999),
        "item_name": random.choice(["Tomatoes", "Lettuce", "Bread", "Pasta", "Cheese", "Tofu", "Rice", "Mushrooms"]),
        "category": random.choice(["Vegetables", "Dairy", "Grains", "Protein"]),
        "stock_quantity": random.randint(10, 200),
        "unit": random.choice(["kg", "pieces", "liters"]),
        "cost_per_unit": round(random.uniform(1.5, 10.0), 2),
        "supplier": fake.company(),
        "last_restock_date": fake.date_this_year()
    })
df_inventory = pd.DataFrame(inventory_data)

# Generate Waste Data
waste_data = []
for _ in range(10):
    waste_data.append({
        "waste_id": fake.unique.random_int(min=1000, max=9999),
        "date": fake.date_this_year(),
        "menu_item": random.choice(["Salad", "Burger", "Pasta", "Pizza", "Soup"]),
        "waste_category": random.choice(["Expired", "Overcooked", "Customer Return", "Preparation Waste"]),
        "quantity_wasted": random.randint(1, 20),
        "unit": random.choice(["kg", "pieces", "liters"]),
        "cost_of_waste": round(random.uniform(1.0, 15.0), 2)
    })
df_waste = pd.DataFrame(waste_data)

# Save to CSV
df_sales.to_csv("sales_data.csv", index=False)
df_inventory.to_csv("inventory_data.csv", index=False)
df_waste.to_csv("waste_data.csv", index=False)
print("✅ CSV files created successfully!")

# Store in SQLite
conn = sqlite3.connect("food_waste.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS sales")
cursor.execute("DROP TABLE IF EXISTS inventory")
cursor.execute("DROP TABLE IF EXISTS waste")

cursor.execute('''
    CREATE TABLE sales (
        sale_id INTEGER PRIMARY KEY,
        date TEXT,
        time TEXT,
        menu_item TEXT,
        category TEXT,
        quantity_sold INTEGER,
        price_per_item REAL,
        total_price REAL,
        payment_method TEXT
    )
''')

cursor.execute('''
    CREATE TABLE inventory (
        item_id INTEGER PRIMARY KEY,
        item_name TEXT,
        category TEXT,
        stock_quantity INTEGER,
        unit TEXT,
        cost_per_unit REAL,
        supplier TEXT,
        last_restock_date TEXT
    )
''')

cursor.execute('''
    CREATE TABLE waste (
        waste_id INTEGER PRIMARY KEY,
        date TEXT,
        menu_item TEXT,
        waste_category TEXT,
        quantity_wasted INTEGER,
        unit TEXT,
        cost_of_waste REAL
    )
''')

# Insert data into tables
df_sales.to_sql("sales", conn, if_exists="append", index=False)
df_inventory.to_sql("inventory", conn, if_exists="append", index=False)
df_waste.to_sql("waste", conn, if_exists="append", index=False)

conn.commit()
conn.close()
print("✅ Data successfully saved to SQLite database!")

# STREAMLIT DASHBOARD
st.title("Food Waste Analytics Dashboard")

# Load data
sales_df = pd.read_csv("sales_data.csv")
waste_df = pd.read_csv("waste_data.csv")
inventory_df = pd.read_csv("inventory_data.csv")

sales_df['date'] = pd.to_datetime(sales_df['date'])
waste_df['date'] = pd.to_datetime(waste_df['date'])

# Sales Over Time
st.subheader("Sales Over Time")
daily_sales = sales_df.groupby('date')['total_price'].sum()
st.line_chart(daily_sales)

# Top Wasted Items
st.subheader("Top 10 Wasted Menu Items")
top_waste = waste_df.groupby('menu_item')['quantity_wasted'].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_waste)

# Stock Levels by Category
st.subheader("Average Stock Level by Category")
category_stock = inventory_df.groupby('category')['stock_quantity'].mean()
st.bar_chart(category_stock)

st.success
