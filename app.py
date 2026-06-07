import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

st.title("🎬 Netflix Data Analysis Dashboard")
st.write("Interactive Data Science Project By Ilyas Ahmad")

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")

    # Cleaning
    df['director'] = df['director'].fillna('Unknown')
    df['cast'] = df['cast'].fillna('Unknown')
    df['country'] = df['country'].fillna('Unknown')
    df['rating'] = df['rating'].fillna('Not Rated')

    df['date_added'] = df['date_added'].astype(str).str.strip()
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

    return df

df = load_data()

# -------------------------
# SIDEBAR FILTER
# -------------------------
st.sidebar.header("Filters")

type_filter = st.sidebar.multiselect(
    "Select Type",
    options=df['type'].unique(),
    default=df['type'].unique()
)

df = df[df['type'].isin(type_filter)]

# -------------------------
# KPIs
# -------------------------
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Titles", len(df))
col2.metric("Movies", (df['type'] == 'Movie').sum())
col3.metric("TV Shows", (df['type'] == 'TV Show').sum())

st.divider()

# -------------------------
# CHART 1 - TYPE DISTRIBUTION
# -------------------------
st.subheader("📊 Content Type Distribution")

fig, ax = plt.subplots()
df['type'].value_counts().plot(kind='bar', ax=ax)
st.pyplot(fig)

# -------------------------
# CHART 2 - TOP COUNTRIES
# -------------------------
st.subheader("🌍 Top 10 Countries")

fig, ax = plt.subplots()
df['country'].value_counts().head(10).plot(kind='bar', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# -------------------------
# CHART 3 - RELEASE YEAR TREND
# -------------------------
st.subheader("📅 Content Trend Over Years")

fig, ax = plt.subplots()
df['release_year'].value_counts().sort_index().plot(ax=ax)
st.pyplot(fig)

# -------------------------
# CHART 4 - RATINGS
# -------------------------
st.subheader("⭐ Ratings Distribution")

fig, ax = plt.subplots()
df['rating'].value_counts().plot(kind='bar', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# -------------------------
# CHART 5 - GENRES
# -------------------------
st.subheader("🎭 Top Genres")

fig, ax = plt.subplots()
df['listed_in'].value_counts().head(10).plot(kind='bar', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# -------------------------
# DATA VIEW
# -------------------------
st.subheader("📄 Raw Data Preview")
st.dataframe(df.head(20))