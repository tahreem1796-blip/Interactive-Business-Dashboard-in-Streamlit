import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page title
st.title("📊 Global Superstore Business Dashboard")

# Load dataset (encoding fixed)
df = pd.read_csv("superstore.csv", encoding="latin1")

# Convert date column
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Sidebar filters
st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

sub_category = st.sidebar.multiselect(
    "Select Sub-Category",
    options=df["Sub-Category"].unique(),
    default=df["Sub-Category"].unique()
)

# Apply filters
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Sub-Category"].isin(sub_category))
]

# KPIs
st.subheader("Key Performance Indicators")

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()

st.metric("Total Sales", f"${total_sales:,.2f}")
st.metric("Total Profit", f"${total_profit:,.2f}")

# Top 5 Customers
st.subheader("Top 5 Customers by Sales")

top_customers = (
    filtered_df.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

st.dataframe(top_customers)

# Sales by Category Chart
st.subheader("Sales by Category")

sales_by_category = filtered_df.groupby("Category")["Sales"].sum()

fig, ax = plt.subplots()
sales_by_category.plot(kind='bar', ax=ax)
ax.set_xlabel("Category")
ax.set_ylabel("Sales")

st.pyplot(fig)
