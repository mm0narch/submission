import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import logging 
from babel.numbers import format_currency
sns.set(style='dark')

payment_reviews_df = pd.read_csv('payment_reviews.csv')
customer_order_price_df = pd.read_csv('customer_order_price.csv')
all_df = pd.read_csv("all_data.csv")
logging.debug('csv read complete')

st.set_page_config(layout="wide")

st.title('Brazilian E-commerce Data Analysis Dashboard')
st.subheader('Mauritius Manurung')

st.header('Datasets')
st.subheader('Tabel harga barang dan review user')
st.dataframe(payment_reviews_df.head())

st.subheader('Tabel harga barang dan kota user')
st.dataframe(customer_order_price_df.head())

st.header('Hubungan harga barang dan review user')
col1, col2, col3 = st.columns(3)

with col1:
    average_price = format_currency(payment_reviews_df.payment_value.mean(), "BRL", locale="es_CO")
    st.metric("Rata-rata harga barang", value=average_price)

with col2:
    total_revenue = format_currency(payment_reviews_df.payment_value.sum(), "BRL", locale='es_CO') 
    st.metric("Total pengeluaran user", value=total_revenue)

with col3:
    average_score = payment_reviews_df.review_score.mean()
    st.metric("Rata-rata skor review", value=average_score)  

score_payment_correlation = {
    'review_score', 'payment_value'
}
average_payment_per_score = payment_reviews_df.groupby('review_score')['payment_value'].mean()
average_payment_per_score = average_payment_per_score.reset_index()
st.bar_chart(average_payment_per_score, x='review_score', y='payment_value')
st.markdown("Dari bar chart representasi data yang telah diproses, kita dapat melihat bahwa item yang mendapatkan nilai review 1 memiliki memiliki harga yang paling tinggi, diikuti oleh produk dengan nilai review 2, 5, 4, dan 3. Review dengan nilai 1 dan 2 ini disebabkan oleh beberapa hal, salah satu yang paling memungkinkan adalah ketidakpuasan customer dengan kualitas item tersebut, walaupun memiliki harga yang tinggi. Terdapat margin yang jauh antara item dengan nilai review 1 dan 5, dimana harga rata-ratanya tidak mencapai harga rata-rata di market. Rata-rata harga item di bisnis ini adalah 153.9 BRL, sedangkan rata-rata harga item dengan nilai 5 adalah di sekitar nilai 150 BRL. Dari analisis ini dapat disimpulkan bahwa harga barang yang tinggi belum tentu menerjemahkan kualitasnya.")

st.header('Hubungan antara harga barang dan kota user')

average_payment_per_city = customer_order_price_df.groupby('customer_city')['payment_value'].mean()
top_10_cities = average_payment_per_city.sort_values(ascending=True).head(10)
fig, ax = plt.subplots(figsize=(16, 8))
top_10_cities.plot(ax=ax, y='payment value', use_index=True, kind='bar')
st.pyplot(fig)
st.markdown("Dari bar chart yang mewakili data yang telah diproses, kita dapat melihat kota-kota yang memiliki rata-rata harga pembelian tertinggi se-Brazil. Namun, grafik tersebut tidak dapat menunjukkan kota-kota termakmur di brazil. Setelah dilihat lebih lanjut, jumlah data yang memiliki kota-kota tersebut sangat sedikit. Sebagai contoh, kota Erico Cardoso hanya memiliki sebanyak tujuh buah data dan Santo Antônio do Rio Abaixo sebanyak 12 buah data, sedangkan total data di dataset tersebut ada sebanyak lebih dari 100.000. Jadi belum terlihat korelasi antara kemakmuran rakyat dengan kota tempat tinggalnya dari dataset ini.")
