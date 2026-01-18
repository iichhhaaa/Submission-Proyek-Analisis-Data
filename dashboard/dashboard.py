import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="darkgrid")

# ===============================
# LOAD DATA
# ===============================
day_df = pd.read_csv("dashboard/day.csv")

# ===============================
# DATA CLEANING & PREPARATION
# ===============================
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weather_map = {1: 'Clear', 2: 'Mist', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow/Fog'}
year_map = {0: '2011', 1: '2012'}
workingday_map = {0: 'Holiday', 1: 'Working Day'}

day_df['season'] = day_df['season'].map(season_map)
day_df['weathersit'] = day_df['weathersit'].map(weather_map)
day_df['yr'] = day_df['yr'].map(year_map)
day_df['workingday'] = day_df['workingday'].map(workingday_map)
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# ===============================
# SIDEBAR FILTER (GLOBAL)
# ===============================
st.sidebar.header("📅 Filter Data")

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

start_date, end_date = st.sidebar.date_input(
    "Rentang Waktu",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

filtered_df = day_df[
    (day_df["dteday"] >= pd.to_datetime(start_date)) &
    (day_df["dteday"] <= pd.to_datetime(end_date))
]

if filtered_df.empty:
    st.warning("Tidak ada data pada rentang waktu yang dipilih.")
    st.stop()

# ===============================
# HEADER
# ===============================
st.title("🚲 Bike Sharing Dashboard")
st.markdown("**Analisis Penyewaan Sepeda Harian (2011–2012)**")

st.info(
    "Seluruh visualisasi pada dashboard ini bersifat interaktif "
    "dan akan menyesuaikan dengan rentang waktu yang dipilih."
)

# ===============================
# METRICS
# ===============================
col1, col2, col3 = st.columns(3)

col1.metric("Total Penyewaan", int(filtered_df["cnt"].sum()))
col2.metric("Rata-rata Harian", int(filtered_df["cnt"].mean()))
col3.metric("Penyewaan Tertinggi (1 Hari)", int(filtered_df["cnt"].max()))

st.divider()

# ===============================
# TREN BULANAN
# ===============================
st.subheader("📈 Tren Penyewaan Sepeda per Bulan")

monthly_df = (
    filtered_df
    .resample("M", on="dteday")["cnt"]
    .sum()
    .reset_index()
)

monthly_df["year_month"] = monthly_df["dteday"].dt.strftime("%Y-%m")

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(monthly_df["year_month"], monthly_df["cnt"], marker="o")
ax.set_title("Total Penyewaan Sepeda per Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penyewaan")
ax.grid(axis="y", linestyle="--", alpha=0.6)
plt.xticks(rotation=45)
st.pyplot(fig)

st.divider()

# ===============================
# FAKTOR YANG MEMENGARUHI PENYEWAAN
# ===============================
st.subheader("🔍 Pengaruh Faktor terhadap Rata-rata Penyewaan")

season_avg = (
    filtered_df.groupby("season")["cnt"]
    .mean()
    .reset_index()
    .sort_values("cnt", ascending=False)
)

weather_avg = (
    filtered_df.groupby("weathersit")["cnt"]
    .mean()
    .reset_index()
    .sort_values("cnt", ascending=False)
)

workingday_avg = (
    filtered_df.groupby("workingday")["cnt"]
    .mean()
    .reset_index()
    .sort_values("cnt", ascending=False)
)

col1, col2, col3 = st.columns(3)

with col1:
    fig, ax = plt.subplots(figsize=(4,4))
    sns.barplot(
        data=season_avg,
        x="season",
        y="cnt",
        hue="season",
        palette=sns.light_palette("#72BCD4", n_colors=4, reverse=True),
        legend=False,
        ax=ax
    )
    ax.set_title("Musim")
    ax.set_xlabel("")
    ax.set_ylabel("Rata-rata")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(4,4))
    sns.barplot(
        data=weather_avg,
        x="weathersit",
        y="cnt",
        hue="weathersit",
        palette=sns.light_palette("#72BCD4", n_colors=len(weather_avg), reverse=True),
        legend=False,
        ax=ax
    )
    ax.set_title("Cuaca")
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.xticks(rotation=30)
    st.pyplot(fig)

with col3:
    fig, ax = plt.subplots(figsize=(4,4))
    sns.barplot(
        data=workingday_avg,
        x="workingday",
        y="cnt",
        hue="workingday",
        palette=sns.light_palette("#72BCD4", n_colors=2, reverse=True),
        legend=False,
        ax=ax
    )
    ax.set_title("Jenis Hari")
    ax.set_xlabel("")
    ax.set_ylabel("")
    st.pyplot(fig)

st.divider()

# ===============================
# DEMAND CLUSTERING
# ===============================
st.header("📌 Analisis Lanjutan: Kategori Permintaan (Demand)")

df_demand = filtered_df.copy()

df_demand["demand_category"] = pd.qcut(
    df_demand["cnt"],
    q=3,
    labels=["Low Demand", "Medium Demand", "High Demand"]
)

demand_palette = {
    "Low Demand": "#D3D3D3",
    "Medium Demand": "#72BCD4",
    "High Demand": "#FFA07A"
}

fig, ax = plt.subplots(figsize=(6,4))
sns.countplot(
    data=df_demand,
    x="season",
    hue="demand_category",
    order=["Spring", "Summer", "Fall", "Winter"],
    palette=demand_palette,
    ax=ax
)
ax.set_title("Kategori Demand berdasarkan Musim")
ax.set_xlabel("")
ax.set_ylabel("Jumlah Hari")
st.pyplot(fig)

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(5,4))
    sns.countplot(
        data=df_demand,
        x="workingday",
        hue="demand_category",
        order=["Holiday", "Working Day"],
        palette=demand_palette,
        ax=ax
    )
    ax.set_title("Kategori Demand: Hari Kerja vs Libur")
    ax.set_xlabel("")
    ax.set_ylabel("Jumlah Hari")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(5,4))
    sns.countplot(
        data=df_demand,
        x="weathersit",
        hue="demand_category",
        order=["Clear", "Mist", "Light Snow/Rain", "Heavy Rain/Snow/Fog"],
        palette=demand_palette,
        ax=ax
    )
    ax.set_title("Kategori Demand berdasarkan Kondisi Cuaca")
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.xticks(rotation=30)
    st.pyplot(fig)

st.divider()

# ===============================
# ANALISIS JENIS PENGGUNA
# ===============================
st.header("👥 Analisis Lanjutan: Jenis Pengguna")

user_total = filtered_df[['casual', 'registered']].sum()

fig, ax = plt.subplots(figsize=(6,6))
ax.pie(
    user_total,
    labels=user_total.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=sns.light_palette('#72BCD4', n_colors=2),
    wedgeprops={'edgecolor': 'white'}
)

ax.set_title(
    "Proporsi Total Penyewaan Sepeda\nBerdasarkan Jenis Pengguna",
    fontsize=13
)

st.pyplot(fig)

# ===============================
# FOOTER
# ===============================
st.caption("© 2026 – Proyek Analisis Data | Hoerunnisa")