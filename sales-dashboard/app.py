import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Sales Dashboard Showcase - dataharmony.it")

@st.cache_data

def load_data():
    df = pd.read_csv("superstore_dataset.csv", encoding='ISO-8859-1')
    df.columns = df.columns.str.strip().str.lower()
    df.rename(columns={df.columns[0]: 'order_id'}, inplace=True)
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

st.title("📊 Sales Dashboard")
st.markdown("Explore key metrics and trends from the sales data.")

# Sidebar filters
st.sidebar.header("Filter Options")
date_range = st.sidebar.date_input("Order Date Range", [df['order_date'].min(), df['order_date'].max()])
category_filter = st.sidebar.multiselect("Category", df['category'].unique(), default=df['category'].unique())
region_filter = st.sidebar.multiselect("Region", df['region'].unique(), default=df['region'].unique())

# Apply filters
filtered_df = df[
    (df['order_date'] >= pd.to_datetime(date_range[0])) &
    (df['order_date'] <= pd.to_datetime(date_range[1])) &
    (df['category'].isin(category_filter)) &
    (df['region'].isin(region_filter))
]

# Key metrics
total_sales = filtered_df['sales'].sum()
total_profit = filtered_df['profit'].sum()
total_orders = filtered_df['order_id'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", total_orders)

# Sales by Category
st.subheader("Sales by Category")
category_sales = filtered_df.groupby('category')['sales'].sum().reset_index()
st.plotly_chart(px.bar(category_sales, x='category', y='sales', title="Sales by Category", color='category'))

# Monthly Sales Trend
st.subheader("Monthly Sales Trend")
filtered_df['month'] = filtered_df['order_date'].dt.to_period('M').dt.to_timestamp()
monthly_sales = filtered_df.groupby('month')['sales'].sum().reset_index()
st.plotly_chart(px.line(monthly_sales, x='month', y='sales', title="Monthly Sales Trend"))

# Profit by Region and Segment
st.subheader("Profit by Region and Segment")
region_segment_profit = filtered_df.groupby(['region', 'segment'])['profit'].sum().reset_index()
st.plotly_chart(px.bar(region_segment_profit, x='region', y='profit', color='segment', barmode='group',
                       title="Profit by Region and Segment"))
