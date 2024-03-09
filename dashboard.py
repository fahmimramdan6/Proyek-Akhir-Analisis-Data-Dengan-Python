import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Menyiapkan Data Frame

# Data Frame montly_bike_data()
def create_montly_bike_data(df):
    monthly_bike_data = bike_day_df.groupby(bike_day_df['dteday'].dt.to_period("M")).agg({
        "cnt" : "sum",
        "casual" : "sum",
        "registered" : "sum"
    }).reset_index()

    return monthly_bike_data

# Data Frame weekday_bike()
def create_weekday_bike(df):
    weekday_bike = bike_day_df.groupby(by="weekday").agg({
        "cnt" : "sum",
        "casual" : "sum",
        "registered" : "sum"
    }).reset_index()

    return weekday_bike

# Data Frame by_weathersit_df()
def create_by_weathersit_df(df):
    by_weathersit_bike = bike_day_df.groupby(by="weathersit").agg({
        "cnt" : "sum",
        "casual" : "sum",
        "registered" : "sum"
    }).reset_index()

    return by_weathersit_bike

# Load berkas bike_day.csv
bike_day_df = pd.read_csv("bike_day.csv")

# datetime
datetime_columns = ["dteday"]
bike_day_df.sort_values(by = "dteday", inplace = True)
bike_day_df.reset_index(inplace = True)
 
for column in datetime_columns:
    bike_day_df[column] = pd.to_datetime(bike_day_df[column])

# Membuat Komponen Filter
min_date = bike_day_df["dteday"].min()
max_date = bike_day_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/fahmimramdan6/Proyek-Akhir-Analisis-Data-Dengan-Python/main/sepeda.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = bike_day_df[(bike_day_df["dteday"] >= str(start_date)) & 
                (bike_day_df["dteday"] <= str(end_date))]


monthly_bike_data =  create_montly_bike_data(main_df)
weekday_bike = create_weekday_bike(main_df)
by_weathersit_bike = create_by_weathersit_df(main_df)

# Melengkapi Dashboard dengan berbagain visualisasi data

# Header
st.header("Bike Sharing Dataset : Predicting Bike sharing demand")

# Visualisai Data Bulanan
st.subheader("Jumlah Peminjaman Sepeda Bulanan")

# Mengubah dteday ke timestamps
monthly_bike_data["dteday"] = monthly_bike_data["dteday"].dt.to_timestamp()

#Plot Grafik
fig = plt.figure(figsize=(10, 5))

plt.plot(
    monthly_bike_data["dteday"],
    monthly_bike_data["cnt"],
    label = "Total Peminjaman",
    color = "green",
    marker = "o"
)
plt.plot(
    monthly_bike_data["dteday"],
    monthly_bike_data["casual"],
    label = 'Peminjam Tidak Tetap',
    color = "blue",
    marker = "o"
)
plt.plot(
    monthly_bike_data["dteday"],
    monthly_bike_data["registered"],
    label = "Peminjam Terdaftar",
    color = "red",
    marker = "o"
)

# atribut plot
plt.title("Jumlah Peminjaman Sepeda Setiap Bulan", fontsize = 15)
plt.ylabel("Jumlah Peminjaman")
plt.xticks(monthly_bike_data["dteday"], labels = monthly_bike_data["dteday"].dt.strftime("%b %Y"), rotation = -90)
plt.legend()

st.pyplot(fig)


#Visualisasi Data Weekday
st.subheader("Jumlah Peminjaman Sepeda Weekday")

# Konversi berdasarkan kategori
weekday_bike["weekday"] = pd.Categorical(weekday_bike["weekday"], categories = [0, 1, 2, 3, 4, 5, 6], ordered = True)
weekday_bike["weekday"] = weekday_bike["weekday"].astype(int)

# Bar Plot
fig2, ax = plt.subplots(figsize=(10, 5))

bar_width = 0.15
index = weekday_bike["weekday"]

bar_cnt = ax.bar(
    index - bar_width,
    weekday_bike["cnt"],
    bar_width,
    label = "Total Peminjaman",
    color = "green"
)
bar_casual = ax.bar(
    index,
    weekday_bike["casual"],
    bar_width,
    label = "Peminjam Tidak Tetap",
    color = "blue"
)
bar_registered = ax.bar(
    index + bar_width,
    weekday_bike["registered"],
    bar_width,
    label = "Peminjam Terdaftar",
    color = "red"
)

# atribut plot
ax.set_ylabel("Jumlah Peminjam")
ax.set_title("Peminjaman Sepeda Berdasarkan Weekday")
ax.set_xticks(index)
ax.set_xticklabels(["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"])
plt.legend()

st.pyplot(fig2)


# Visualisasi Pengaruh Kondisi Cuaca 
st.subheader("Pengaruh Kondisi Cuaca Terhadap Peminjaman Sepeda")

# Konversi Numerik ke Dictionary
kondisi_cuaca = {
    1: "Clear, Few clouds",
    2: "Mist + Cloudy",
    3: "Light Snow, Light Rain",
    4: "Heavy Rain, Thunderstorm, Mist"
}
by_weathersit_bike["cuaca"] = by_weathersit_bike["weathersit"].map(kondisi_cuaca)

# plot grafik
fig3 = plt.figure(figsize=(10, 5))

bar_width = 0.15
posisi_bar_cnt = range(len(by_weathersit_bike))
posisi_bar_casual = [pos + bar_width for pos in posisi_bar_cnt]
posisi_bar_registered = [pos + bar_width for pos in posisi_bar_casual]

plt.bar(
    posisi_bar_cnt,
    by_weathersit_bike["cnt"],
    color="green",
    width = bar_width,
    label="Total Peminjaman"
)
plt.bar(
    posisi_bar_casual,
    by_weathersit_bike["casual"],
    color="blue",
    width = bar_width,
    label="Peminjam Tidak Tetap"
)
plt.bar(
    posisi_bar_registered,
    by_weathersit_bike["registered"],
    color="red",
    width = bar_width,
    label="Peminjam Terdaftar"
)

# atribut plot
plt.title("Pengaruh Kondisi Cuaca Terhadap Peminjaman Sepeda", fontsize=15)
plt.ylabel("Jumlah Peminjam", fontsize=12)
plt.gca().yaxis.get_major_formatter().set_scientific(False)
plt.xticks([pos + bar_width /2 for pos in posisi_bar_casual], by_weathersit_bike["cuaca"])
plt.legend()

st.pyplot(fig3)