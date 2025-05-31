import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pathlib import Path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download VADER lexicon kalau belum ada
nltk.download('vader_lexicon')

# Inisialisasi session state
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "show_form" not in st.session_state:
    st.session_state.show_form = False

# Redirect ke app.py kalau user_name kosong
if st.session_state.user_name is None:
    st.warning("Silakan login terlebih dahulu!")
    st.query_params["page"] = "login"
    st.markdown('<a href="/" target="_self">Kembali ke Halaman Login</a>',
                unsafe_allow_html=True)
    st.stop()

def renderSidebar():
    with st.sidebar:
        if st.button("Logout"):
            st.session_state.user_name = None
            st.session_state.show_form = True
            st.session_state.welcome_shown = False
            st.query_params["page"] = "login"
            st.rerun()

def main():
    # Render sidebar
    renderSidebar()

    st.title("📊 Analisis Pasar & Wawasan Historis")
    st.write(
        f"Selamat datang, {st.session_state.user_name}! Eksplorasi tren harga emas dan wawasan berbasis data historis sejak 2000.")

    # Load dataset
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    data_path = BASE_DIR / 'Dataset' / 'final_gold_data.csv'
    try:
        if not os.path.exists(data_path):
            st.error(f"File tidak ditemukan: {data_path}")
            return

        df = pd.read_csv(
            data_path,
            delimiter=',',
            encoding='utf-8',
            on_bad_lines='skip'
        )

        timestamp_col = None
        for col in df.columns:
            if col.lower() in ['timestamp', 'date', 'time']:
                timestamp_col = col
                break

        if timestamp_col is None:
            st.error("Kolom 'timestamp' tidak ditemukan di dataset.")
            return

        try:
            df[timestamp_col] = pd.to_datetime(df[timestamp_col])
        except Exception as e:
            st.error(
                f"Error saat mengonversi kolom {timestamp_col} ke datetime: {str(e)}")
            return

        # Filter periode
        st.subheader("Filter Data")
        min_year = 2000  # Set tahun minimum sesuai dataset
        max_year = 2025  # Set tahun maksimum sesuai dataset
        year_range = st.slider("Pilih rentang tahun:",
                               min_year, max_year, (2020, max_year))

        filtered_df = df[(df[timestamp_col].dt.year >= year_range[0]) & (
            df[timestamp_col].dt.year <= year_range[1])]

        # Grafik harga
        st.subheader("Tren Harga Emas (Close)")
        fig = px.line(filtered_df, x=timestamp_col, y='close',
                      title="Harga Emas (Close) per Hari")
        st.plotly_chart(fig, use_container_width=True)

        # Grafik volume
        st.subheader("Volume Perdagangan")
        fig_volume = px.line(filtered_df, x=timestamp_col,
                             y='volume', title="Volume Perdagangan per Hari")
        st.plotly_chart(fig_volume, use_container_width=True)

        # Word Cloud Headlines Berita Logam Mulia
        st.subheader("Word Cloud Headlines Berita Logam Mulia")
        try:
            if 'headlines' in filtered_df.columns:
                text = ' '.join(filtered_df['headlines'].dropna().astype(str))
                if text.strip():
                    wordcloud = WordCloud(
                        width=1000, height=500, background_color='white').generate(text)
                    fig_wc, ax = plt.subplots(figsize=(15, 6))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    st.pyplot(fig_wc)
                else:
                    st.info(
                        "Tidak ada data headlines untuk ditampilkan pada Word Cloud.")
            else:
                st.info("Kolom 'headlines' tidak ditemukan di dataset.")
        except ImportError:
            st.warning(
                "Modul wordcloud atau matplotlib belum terinstal. Silakan install dengan 'pip install wordcloud matplotlib'.")

        # Pie Chart Sentimen
        st.subheader("Distribusi Sentimen Berita Emas")
        if 'sentiment_type' in filtered_df.columns:
            gold_sent = filtered_df['sentiment_type'].value_counts()
            if not gold_sent.empty:
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    fig_sent, ax = plt.subplots(figsize=(5, 4))
                    ax.pie(gold_sent.values, labels=gold_sent.index, autopct='%1.1f%%', startangle=140,
                        colors=['#66b3ff', '#99ff99', '#ff9999'])
                    ax.set_title(f"Sentimen Berita Emas ({year_range[0]} - {year_range[1]})")
                    plt.tight_layout()
                    st.pyplot(fig_sent, use_container_width=False)
            else:
                st.info("Tidak ada data sentimen untuk ditampilkan.")
        else:
            st.info("Kolom 'sentiment_type' tidak ditemukan di dataset.")

    except Exception as e:
        st.error(f"Error memuat data: {str(e)}")
        st.write(f"Silakan cek file CSV di {data_path}")

if __name__ == "__main__":
    main()