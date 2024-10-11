import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

df = pd.read_csv('melbourne.csv')
df['Date'] = pd.to_datetime(df['Date'], format = 'mixed')
df['M/Y'] = df['Date'].dt.to_period('M')
df['M/Y'] = df['M/Y'].astype(str)

df['Date1'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
df['Year'] = df['Date1'].dt.year


df_new = df[['Suburb', 'Rooms', 'Type', 'Price', 'Distance', 'Bathroom', 'Landsize', 'YearBuilt', 'Regionname', 'M/Y', 'Year']]

st.markdown("""
    <style>
        /* Increase the overall width of the app's main content area */
        [data-testid="stAppViewContainer"] {
            max-width: 100%;  /* Utilize the full width of the screen */
            padding: 0rem 0rem; /* Remove padding to free up more space */
        }
        /* Adjust sidebar width to give more space to main content */
        [data-testid="stSidebar"] {
            width: 180px;  /* Reduce the width of the sidebar */
        }
        /* Set the background color for the app */
        [data-testid="stAppViewContainer"] {
            background-color: #f5f5f5; /* Lighter background for better contrast */
        }
        /* Adjust font and size of headers */
        h1 {
            font-size: 36px; /* Title font size */
            color: #333; /* Title color */
        }
        h2 {
            font-size: 30px; /* Subheader font size */
            color: #333; /* Subheader color */
        }
        h3 {
            font-size: 24px; /* Smaller header font size */
            color: #333; /* Smaller header color */
        }
        h4 {
            font-size: 20px; /* Even smaller header font size */
            color: #333; /* Even smaller header color */
        }
    </style>
    """, unsafe_allow_html=True)

st.title("Melbourne Housing Data Dashboard")
st.sidebar.header("Filter Options")

regions = df['Regionname'].unique()
selected_regions = st.sidebar.multiselect("Select Region", regions, default=regions)

types = df['Type'].unique()
selected_type = st.sidebar.multiselect("Select Property Type", types, default=types)

year = df['Year'].unique()
select_year = st.sidebar.multiselect("Select Year", year, default=year)

rooms = df['Rooms'].unique()
selected_rooms = st.sidebar.multiselect("Select Number of Rooms", rooms, default=rooms)

bathroom = df['Bathroom'].unique()
select_bathroom = st.sidebar.multiselect("Select Number of Bathrooms", bathroom, default=bathroom)

filtered_data = df[
    (df['Regionname'].isin(selected_regions)) &
    (df['Type'].isin(selected_type)) &
    (df['Rooms'].isin(selected_rooms)) &
    (df['Year'].isin(select_year)) &
    (df['Bathroom'].isin(select_bathroom))
]

filtered_data['Date'] = pd.to_datetime(filtered_data['Date'], format='%d-%m-%Y')

col1, col2 = st.columns([4,4])

with col1:
    st.subheader("Price Trending")
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.lineplot(x=filtered_data['Date'], y=filtered_data['Price'], ax=ax)
    ax.set_title("Price Trend Over Time", fontsize=18)
    ax.set_xlabel("Date", fontsize=18)
    ax.set_ylabel("Price", fontsize=18)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Price by Region")
    fig3, ax3 = plt.subplots(figsize=(14, 8))
    avg_price_region = filtered_data.groupby('Regionname')['Price'].mean().sort_values()
    sns.barplot(x=avg_price_region.index, y=avg_price_region.values, ax=ax3, palette="viridis")
    ax3.set_title("Average Price by Region", fontsize=18)
    ax3.set_xlabel("Region", fontsize=14)
    ax3.set_ylabel("Average Price", fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    st.pyplot(fig3)

with col2:
    st.subheader("Price Vs Land Size")
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.scatterplot(x=filtered_data['Landsize'], y=filtered_data['Price'], hue=filtered_data['Type'], ax=ax)
    ax.set_title("Price Variation According to the Land Size", fontsize=18)
    ax.set_xlabel("Land Size", fontsize=18)
    ax.set_ylabel("Price", fontsize=18)
    st.pyplot(fig)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Properties by Type")
    fig4, ax4 = plt.subplots(figsize=(14, 8))
    property_count = filtered_data['Type'].value_counts()
    sns.barplot(x=property_count.index, y=property_count.values, ax=ax4, palette="coolwarm")
    ax4.set_title("Count of Properties by Type", fontsize=18)
    ax4.set_xlabel("Property Type", fontsize=14)
    ax4.set_ylabel("Count", fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    st.pyplot(fig4)



