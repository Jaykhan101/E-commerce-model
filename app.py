import math
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Function for Price Elasticity of Demand (PED)
def calculate_PED(price, new_price, quantity, PED):
    return quantity * (1 + PED * ((new_price - price) / price))

# Function for Sales Forecasting based on PED
def sales_forecasting(price, new_price, quantity, PED):
    new_quantity = calculate_PED(price, new_price, quantity, PED)
    return round(new_quantity)

# Function for Cross-Price Elasticity of Demand (XED)
def calculate_XED(price_1, new_price_1, quantity_2, XED):
    return round(quantity_2 * (1 + XED * ((new_price_1 - price_1) / price_1)))

# Function for Profitability Analysis
def profitability_analysis(price, COGS, quantity):
    profit_per_unit = price - COGS
    total_profit = profit_per_unit * quantity
    return total_profit

# Function for Reorder Point (ROP)
def calculate_ROP(demand_per_week, lead_time, safety_stock):
    return (demand_per_week * lead_time) + safety_stock

# Function for Cash Flow Forecasting
def cash_flow_forecasting(revenue, inventory_cost):
    return revenue - inventory_cost

# --- Streamlit App for Interactivity ---
st.title("E-Commerce Financial Modeling Dashboard")

# Input fields for product details
st.header("Product Data Input")

# Product 1 Inputs
product_name = st.text_input("Product Name:", value="Herbal Body Lotion")
price = st.number_input(f"Current price for {product_name} ($):", value=100.0)
new_price = st.number_input(f"New price for {product_name} ($):", value=110.0)
units_sold = st.number_input(f"Current units sold for {product_name}:", value=1000, min_value=0, step=1)
PED = st.number_input(f"Price Elasticity of Demand (PED) for {product_name}:", value=-0.4, format="%.2f")

# Related Product Inputs
related_product_name = st.text_input("Related Product Name (optional):", value="Organic Exfoliating Scrub")
related_product_price = st.number_input(f"Current price for {related_product_name} ($):", value=50.0)
related_product_units_sold = st.number_input(f"Current units sold for {related_product_name}:", value=500, min_value=0, step=1)
XED = st.number_input(f"Cross-Price Elasticity of Demand (XED) for {related_product_name}:", value=0.2, format="%.2f")

# Costs
COGS = st.number_input(f"Cost of Goods Sold (COGS) for {product_name} ($):", value=40.0)
related_product_COGS = st.number_input(f"COGS for {related_product_name} ($):", value=20.0)

# Supply and ROP for Product 1
lead_time = st.number_input(f"Lead time in weeks for {product_name} supply:", value=3)
demand_per_week = st.number_input(f"Demand per week for {product_name}:", value=250)
safety_stock = st.number_input(f"Safety stock level for {product_name}:", value=50)

# Supply and ROP for Related Product
related_lead_time = st.number_input(f"Lead time in weeks for {related_product_name} supply:", value=3)
related_demand_per_week = st.number_input(f"Demand per week for {related_product_name}:", value=100)
related_safety_stock = st.number_input(f"Safety stock level for {related_product_name}:", value=30)

# --- Model Calculations ---

# Calculate new quantity sold for the product using PED
new_quantity = sales_forecasting(price, new_price, units_sold, PED)

# Calculate new quantity for related product using XED
new_quantity_related = calculate_XED(price, new_price, related_product_units_sold, XED)

# Calculate profitability for both products
product_profit = profitability_analysis(new_price, COGS, new_quantity)
related_product_profit = profitability_analysis(related_product_price, related_product_COGS, new_quantity_related)

# Calculate total revenue
total_revenue = (new_quantity * new_price) + (new_quantity_related * related_product_price)

# Calculate inventory cost (including buffer stock)
inventory_cost = (new_quantity * COGS) + (new_quantity_related * related_product_COGS) + (safety_stock * COGS) + (related_safety_stock * related_product_COGS)

# Calculate cash flow
cash_flow = cash_flow_forecasting(total_revenue, inventory_cost)

# Calculate ROP (Reorder Point) for both products
ROP = calculate_ROP(demand_per_week, lead_time, safety_stock)
related_ROP = calculate_ROP(related_demand_per_week, related_lead_time, related_safety_stock)

# --- Display Results ---
st.header("Key Financial Metrics")

# Display key metrics with professional tone
st.subheader("Sales and Profit Forecasts")
st.write(f"New units sold for {product_name}: **{new_quantity}**")
st.write(f"New units sold for {related_product_name} (XED effect): **{new_quantity_related}**")
st.write(f"Total profit for {product_name}: **${product_profit:.2f}**")
st.write(f"Total profit for {related_product_name}: **${related_product_profit:.2f}**")

st.subheader("Revenue and Inventory Costs")
st.write(f"Total projected revenue: **${total_revenue:.2f}**")
st.write(f"Inventory cost (including buffer stock): **${inventory_cost:.2f}**")
st.write(f"Net cash flow: **${cash_flow:.2f}**")

st.subheader("Supply Chain Metrics")
st.write(f"Reorder Point (ROP) for {product_name}: **{ROP} units**")
st.write(f"Reorder Point (ROP) for {related_product_name}: **{related_ROP} units**")

# --- Professional Visualizations ---

# Seaborn styling for more professional look
sns.set(style="whitegrid")

# Sales Forecasting - Bar Chart using Seaborn
st.subheader("Sales Forecasting Comparison")
fig, ax = plt.subplots()
sns.barplot(x=[product_name, related_product_name], y=[new_quantity, new_quantity_related], ax=ax, palette="Blues_d")
ax.set_xlabel("Products")
ax.set_ylabel("Units Sold")
ax.set_title("Forecasted Units Sold")
st.pyplot(fig)

# Profitability Analysis - Bar Chart using Seaborn
st.subheader("Profitability Comparison")
fig2, ax2 = plt.subplots()
sns.barplot(x=[product_name, related_product_name], y=[product_profit, related_product_profit], ax=ax2, palette="Greens_d")
ax2.set_xlabel("Products")
ax2.set_ylabel("Profit ($)")
ax2.set_title("Forecasted Profit")
st.pyplot(fig2)

# Cash Flow Projection - Line Chart using Seaborn (Simulation over 6 months)
st.subheader("Cash Flow Projection (6 Months)")
months = ["Month 1", "Month 2", "Month 3", "Month 4", "Month 5", "Month 6"]
cash_flows = [cash_flow * (1 + 0.05 * i) for i in range(6)]  # Simulating growth of cash flow over 6 months

fig3, ax3 = plt.subplots()
sns.lineplot(x=months, y=cash_flows, marker='o', ax=ax3, color='#4c72b0')
ax3.set_xlabel("Months")
ax3.set_ylabel("Cash Flow ($)")
ax3.set_title("Projected Cash Flow Over 6 Months")
st.pyplot(fig3)
