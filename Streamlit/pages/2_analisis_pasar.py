# D:\Coolyeah\Laskar AI\Capstone\fix\Streamlit\pages\2_analisis_pasar.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Inisialisasi session state
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "page" not in st.session_state:
    st.session_state.page = "landing"

if st.session_state.user_name:
    def main():
        st.title("📊 Analisis Pasar & Wawasan Historis")
        st.write("Eksplorasi tren harga emas dan wawasan berbasis data historis sejak 2000.")

        # Load dataset
        data_path = r"D:\Coolyeah\Laskar AI\Capstone\fix\Dataset\final_gold_data.csv"
        try:
            # Cek apakah file ada
            if not os.path.exists(data_path):
                st.error(f"File tidak ditemukan: {data_path}")
                return
            
            # Load dataset dengan delimiter semicolon
            df = pd.read_csv(
                data_path,
                delimiter=';',
                encoding='utf-8',
                on_bad_lines='skip'
            )

            # Cek kolom yang tersedia
            # st.write("Kolom yang tersedia di dataset:", list(df.columns))

            # Cek apakah kolom 'timestamp' ada
            timestamp_col = None
            for col in df.columns:
                if col.lower() in ['timestamp', 'date', 'time']:
                    timestamp_col = col
                    break
            
            if timestamp_col is None:
                st.error("Kolom 'timestamp' tidak ditemukan di dataset. Silakan cek nama kolom di file CSV.")
                return
            
            # Convert ke datetime
            try:
                df[timestamp_col] = pd.to_datetime(df[timestamp_col])
            except Exception as e:
                st.error(f"Error saat mengonversi kolom {timestamp_col} ke datetime: {str(e)}")
                return

            # Filter periode
            st.subheader("Filter Data")
            year_range = st.slider("Pilih rentang tahun:", 2000, 2025, (2020, 2025))
            filtered_df = df[(df[timestamp_col].dt.year >= year_range[0]) & (df[timestamp_col].dt.year <= year_range[1])]

            # Grafik harga (pake Plotly biar interaktif)
            st.subheader("Tren Harga Emas (Close)")
            fig = px.line(filtered_df, x=timestamp_col, y='close', title="Harga Emas (Close) per Hari")
            st.plotly_chart(fig, use_container_width=True)

            # Statistik sederhana
            st.subheader("Statistik Harga")
            st.write(f"Harga rata-rata: ${filtered_df['close'].mean():.2f}")
            st.write(f"Volatilitas (std): ${filtered_df['close'].std():.2f}")

            # Grafik volume
            st.subheader("Volume Perdagangan")
            fig_volume = px.line(filtered_df, x=timestamp_col, y='volume', title="Volume Perdagangan per Hari")
            st.plotly_chart(fig_volume, use_container_width=True)

        except Exception as e:
            st.error(f"Error memuat data: {str(e)}")
            st.write(f"Silakan cek file CSV di {data_path}")

    if __name__ == "__main__":
        main()