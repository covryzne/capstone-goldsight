import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pathlib import Path

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
            delimiter=';',
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
        year_range = st.slider("Pilih rentang tahun:",
                               2000, 2025, (2020, 2025))
        filtered_df = df[(df[timestamp_col].dt.year >= year_range[0]) & (
            df[timestamp_col].dt.year <= year_range[1])]

        # Grafik harga
        st.subheader("Tren Harga Emas (Close)")
        fig = px.line(filtered_df, x=timestamp_col, y='close',
                      title="Harga Emas (Close) per Hari")
        st.plotly_chart(fig, use_container_width=True)

        # Statistik sederhana
        st.subheader("Statistik Harga (USD)")
        stats_df = pd.DataFrame({
            'Metrik': ['Harga Rata-rata', 'Volatilitas (Std)'],
            'Nilai': [filtered_df['close'].mean(), filtered_df['close'].std()]
        })
        fig_stats = px.bar(
            stats_df,
            x='Metrik',
            y='Nilai',
            title="Statistik Harga Emas",
            text_auto='.2f',
            color='Metrik',
            color_discrete_sequence=['#1f77b4', '#ff7f0e'],
            labels={'Nilai': 'Harga (USD)'}
        )
        fig_stats.update_traces(textposition='outside')
        fig_stats.update_layout(
            yaxis_title="Harga (USD)",
            xaxis_title="Metrik",
            showlegend=False
        )
        st.plotly_chart(fig_stats, use_container_width=True)

        # Grafik volume
        st.subheader("Volume Perdagangan")
        fig_volume = px.line(filtered_df, x=timestamp_col,
                             y='volume', title="Volume Perdagangan per Hari")
        st.plotly_chart(fig_volume, use_container_width=True)

    except Exception as e:
        st.error(f"Error memuat data: {str(e)}")
        st.write(f"Silakan cek file CSV di {data_path}")


if __name__ == "__main__":
    main()
