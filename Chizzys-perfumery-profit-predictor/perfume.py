# Chizzy's Perfumery Profit Predictor with Multi-size Profit Comparison
# Requirements: pip install pandas streamlit matplotlib

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Chizzy's Perfumery Profit Predictor", page_icon="💎")

st.title("💎 Chizzy's Perfumery – Expense & Profit Predictor")
st.markdown("""
Easily calculate expenses and profit for each fragrance.  
✅ Set a selling price per bottle size.  
✅ Compare profit across different bottle sizes.
""")

# Bottle sizes and costs
bottle_cost_map = {
    "3ml": 125,
    "6ml": 150,
    "10ml": 500,
    "12ml": 500,
    "15ml": 500,
    "20ml": 670,
    "30ml": 1000,
    "50ml": 1100,
    "100ml": 1300
}

# Sample data
sample_data = {
    "Fragrance": [
        "Royal Black", "Bombshell", "Attractive", "Sweet Temptation", "Black Orchid",
        "Sugar Baby", "Pink Sugar", "Black Oud", "Good Girl", "Pure Seduction",
        "Gucci Bamboo", "Giorgio Armani", "Dunhil", "Creed Aventus", "Signature"
    ],
    "CostPrice": [
        8300, 8500, 8800, 6800, 7200,
        7500, 7500, 9200, 8500, 6800,
        8500, 6800, 8500, 8500, 8500
    ],
    "Quantity": [1]*15
}
base_df = pd.DataFrame(sample_data)

# User input
st.write("---")
selected_size = st.selectbox("Select a bottle size for detailed view:", list(bottle_cost_map.keys()))
custom_price = st.number_input(
    f"Set selling price for {selected_size} bottle (₦):",
    min_value=0,
    value=1500
)

# ---- Calculations for selected size
size_ml = int(selected_size.replace("ml", ""))
df = base_df.copy()
df["FragranceCostForSize"] = (df["CostPrice"] / 100) * size_ml
df["BottleCost"] = bottle_cost_map[selected_size]
df["LabelCost"] = 10
df["UnitTotalCost"] = df["FragranceCostForSize"] + df["BottleCost"] + df["LabelCost"]
df["TotalCost"] = df["UnitTotalCost"] * df["Quantity"]
df["SellPrice"] = custom_price
df["ExpectedRevenue"] = df["SellPrice"] * df["Quantity"]
df["ExpectedProfit"] = df["ExpectedRevenue"] - df["TotalCost"]
df["ProfitMargin%"] = (df["ExpectedProfit"] / df["TotalCost"]) * 100

# Show table
st.write("---")
st.subheader(f"📊 Calculations for {selected_size} bottles")
st.dataframe(df[[
    "Fragrance", "UnitTotalCost", "Quantity",
    "TotalCost", "SellPrice", "ExpectedRevenue", "ExpectedProfit", "ProfitMargin%"
]])

# Summary
st.write("---")
st.subheader("📌 Summary")
st.write("✅ **Total Expenses:** ₦", df["TotalCost"].sum())
st.write("✅ **Expected Total Revenue:** ₦", df["ExpectedRevenue"].sum())
st.write("✅ **Expected Total Profit:** ₦", df["ExpectedProfit"].sum())

total_cost = df["TotalCost"].sum()
break_even_units = total_cost / custom_price if custom_price > 0 else 0
st.write("📌 **Break-Even Units:**", round(break_even_units, 2))

# Bar chart for profit (selected size)
st.write("---")
st.subheader(f"💹 Expected Profit per Fragrance ({selected_size})")
fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(df["Fragrance"], df["ExpectedProfit"], color="green")
ax1.set_title(f"Expected Profit per Fragrance ({selected_size})")
ax1.set_ylabel("Profit (₦)")
ax1.set_xlabel("Fragrance")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig1)

# ---- NEW SECTION: Compare profit across multiple sizes
st.write("---")
st.subheader("📊 Compare Profit Across Bottle Sizes")

# Let user choose which sizes to compare
sizes_to_compare = st.multiselect(
    "Select bottle sizes to compare:",
    list(bottle_cost_map.keys()),
    default=["6ml", "12ml", "30ml"]
)

# Dictionary to store custom prices for each size
size_price_map = {}

# Show input boxes dynamically for each chosen size
if sizes_to_compare:
    st.markdown("### 💰 Enter selling price for each size")
    for size in sizes_to_compare:
        price = st.number_input(
            f"Set selling price for {size} bottle (₦):",
            min_value=0,
            value=1500,
            key=f"price_{size}"
        )
        size_price_map[size] = price

# Only calculate when user has selected sizes and set prices
if sizes_to_compare:
    comparison_data = []
    for size in sizes_to_compare:
        size_ml = int(size.replace("ml", ""))
        sell_price = size_price_map[size]
        temp_df = base_df.copy()
        temp_df["UnitTotalCost"] = (temp_df["CostPrice"] / 100) * size_ml + bottle_cost_map[size] + 10
        temp_df["ExpectedProfit"] = sell_price - temp_df["UnitTotalCost"]
        temp_df["BottleSize"] = size
        comparison_data.append(temp_df[["Fragrance", "BottleSize", "ExpectedProfit"]])

    compare_df = pd.concat(comparison_data)

    # Pivot for plotting
    pivot_df = compare_df.pivot(index="Fragrance", columns="BottleSize", values="ExpectedProfit")
    st.write("---")
    st.markdown("### 📋 Profit Comparison Table")
    st.dataframe(pivot_df)

    # Grouped bar chart
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    pivot_df.plot(kind="bar", ax=ax2)
    ax2.set_title("Profit Comparison Across Bottle Sizes")
    ax2.set_ylabel("Expected Profit (₦)")
    ax2.set_xlabel("Fragrance")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig2)