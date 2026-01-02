import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)
@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")
    df['datetime'] = pd.to_datetime(df['datetime'])

    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['hour'] = df['datetime'].dt.hour
    df['dayofweek'] = df['datetime'].dt.day_name()

    df['season'] = df['season'].map({
        1: 'Spring',
        2: 'Summer',
        3: 'Fall',
        4: 'Winter'
    })

    return df

df = load_data()
st.sidebar.header("Filters")

year = st.sidebar.selectbox("Select Year", sorted(df['year'].unique()))
season = st.sidebar.multiselect(
    "Select Season",
    df['season'].unique(),
    default=df['season'].unique()
)

workingday = st.sidebar.radio(
    "Working Day",
    options=["All", "Working Day", "Non-Working Day"]
)
filtered_df = df[df['year'] == year]
filtered_df = filtered_df[filtered_df['season'].isin(season)]

if workingday == "Working Day":
    filtered_df = filtered_df[filtered_df['workingday'] == 1]
elif workingday == "Non-Working Day":
    filtered_df = filtered_df[filtered_df['workingday'] == 0]
st.title("🚲 Washington DC Bike Sharing Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Total Rentals", int(filtered_df['count'].sum()))
col2.metric("Average Hourly Rentals", int(filtered_df['count'].mean()))
col3.metric("Max Hourly Rentals", int(filtered_df['count'].max()))
st.subheader("Mean Hourly Rentals")

hourly = filtered_df.groupby('hour')['count'].mean().reset_index()

fig, ax = plt.subplots()
sns.lineplot(x='hour', y='count', data=hourly, ax=ax)
ax.set_xlabel("Hour")
ax.set_ylabel("Mean Rentals")

st.pyplot(fig)
st.subheader("Mean Rentals by Month")

monthly = filtered_df.groupby('month')['count'].mean().reset_index()

fig, ax = plt.subplots()
sns.barplot(x='month', y='count', data=monthly, ax=ax)

st.pyplot(fig)
st.subheader("Working vs Non-Working Days")

work = filtered_df.groupby('workingday')['count'].mean().reset_index()

fig, ax = plt.subplots()
sns.barplot(x='workingday', y='count', data=work, ax=ax)
ax.set_xticklabels(["Non-Working", "Working"])

st.pyplot(fig)
st.subheader("Seasonal Rentals")

season_avg = filtered_df.groupby('season')['count'].mean().reset_index()

fig, ax = plt.subplots()
sns.barplot(x='season', y='count', data=season_avg, ax=ax)

st.pyplot(fig)
st.subheader("Weather Impact")

weather_avg = filtered_df.groupby('weather')['count'].mean().reset_index()

fig, ax = plt.subplots()
sns.barplot(x='weather', y='count', data=weather_avg, ax=ax)

st.pyplot(fig)
st.subheader("Correlation Heatmap")

num_cols = ['temp', 'atemp', 'humidity', 'windspeed', 'count']
corr = filtered_df[num_cols].corr()

fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)

st.pyplot(fig)