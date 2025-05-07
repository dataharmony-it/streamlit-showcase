import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data

def load_data():
    url = "https://raw.githubusercontent.com/owid/co2-data/refs/heads/master/owid-co2-data.csv"
    df = pd.read_csv(url, encoding='ISO-8859-1')
    df = df[df['year'] >= 1950]
    df = df[df['co2'].notna()]
    return df

df = load_data()

st.title("🌍 Global CO₂ Emissions Dashboard")
st.markdown("Explore historical CO₂ emissions by country and region from 1950 onwards.")

# Sidebar filters
st.sidebar.header("Filter Options")
selected_year = st.sidebar.slider("Select Year", int(df['year'].min()), int(df['year'].max()), 2020)
selected_countries = st.sidebar.multiselect("Select Countries", df['country'].unique(), default=["United States", "China", "India", "Germany"])

# Filter data
filtered_df = df[df['year'] == selected_year]
country_df = df[df['country'].isin(selected_countries)]

# Global bar chart
st.subheader(f"Top 10 Emitters in {selected_year}")
top_emitters = filtered_df.sort_values('co2', ascending=False).head(10)
st.plotly_chart(px.bar(top_emitters, x='country', y='co2', title=f"Top 10 CO₂ Emitters in {selected_year}", color='country'))

# Line chart for selected countries
st.subheader("CO₂ Emissions Over Time")
st.plotly_chart(px.line(country_df, x='year', y='co2', color='country', title="CO₂ Emissions by Country Over Time"))

# World map
st.subheader("CO₂ Emissions Map")
st.plotly_chart(px.choropleth(filtered_df, locations='country', locationmode='country names',
                              color='co2', hover_name='country',
                              color_continuous_scale='Reds',
                              title=f"CO₂ Emissions by Country in {selected_year}"))

