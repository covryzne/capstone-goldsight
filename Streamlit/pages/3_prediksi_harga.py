import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import plotly.express as px
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os
from pathlib import Path
from datetime import datetime, timedelta

# Inisialisasi Session State
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "show_form" not in st.session_state:
    st.session_state.show_form = False

# Redirect ke app.py kalau user_name kosong
if st.session_state.user_name is None:
    st.warning("Silakan login terlebih dahulu!")
    st.query_params["page"] = "login"
    st.markdown('<a href="/" target="_self">Kembali ke Halaman Login</a>', unsafe_allow_html=True)
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

    st.title("📈 Prediksi Harga Emas")
    st.write(f"Selamat datang, {st.session_state.user_name}! Gunakan model Deep Learning GRU untuk memprediksi harga emas jangka pendek.")

    # Inisialisasi session state untuk horizon
    if 'horizon' not in st.session_state:
        st.session_state.horizon = 7

    # Load model dan scaler
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    model_path = BASE_DIR / 'Model' / 'best_model_gru_5th.h5'
    scaler_path = BASE_DIR / 'Model' / 'scaler_close_gru_5th.pkl'
    data_path = BASE_DIR / 'Dataset' / 'final_gold_data.csv'

    try:
        if not os.path.exists(model_path):
            st.error(f"File model tidak ditemukan: {model_path}")
            return
        if not os.path.exists(scaler_path):
            st.error(f"File scaler tidak ditemukan: {scaler_path}")
            return
        
        model = tf.keras.models.load_model(
            model_path,
            custom_objects={
                'mse': tf.keras.losses.MeanSquaredError(),
                'mean_squared_error': tf.keras.losses.MeanSquaredError()
            }
        )
        scaler = joblib.load(scaler_path)

        if not os.path.exists(data_path):
            st.error(f"File dataset tidak ditemukan: {data_path}")
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
        
        if 'close' not in df.columns:
            st.error("Kolom 'close' tidak ditemukan di dataset.")
            return

        try:
            df[timestamp_col] = pd.to_datetime(df[timestamp_col])
        except Exception as e:
            st.error(f"Error saat mengonversi kolom {timestamp_col} ke datetime: {str(e)}")
            return

        close_prices = df['close'].values
        last_date = df[timestamp_col].iloc[-1]

        # Evaluasi model
        st.subheader("Performa Model")
        WINDOW = 60
        close_scaled = scaler.transform(close_prices.reshape(-1, 1))
        X, y = [], []
        for i in range(len(close_scaled) - WINDOW):
            X.append(close_scaled[i:i + WINDOW])
            y.append(close_scaled[i + WINDOW])
        X = np.array(X).reshape(-1, WINDOW, 1)
        y = np.array(y).flatten()
        
        total = len(X)
        val_end = int(total * 0.85)
        X_test = X[val_end:]
        y_test = y[val_end:]
        
        y_pred_s = model.predict(X_test, verbose=0).flatten()
        y_test_true = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()
        y_pred_true = scaler.inverse_transform(y_pred_s.reshape(-1, 1)).flatten()
        
        rmse = np.sqrt(mean_squared_error(y_test_true, y_pred_true))
        mae = mean_absolute_error(y_test_true, y_pred_true)
        mape = np.mean(np.abs((y_test_true - y_pred_true) / y_test_true)) * 100
        r2 = r2_score(y_test_true, y_pred_true)
        
        metrics_df = pd.DataFrame({
            'Metrik': ['RMSE', 'MAE', 'MAPE', 'R2'],
            'Nilai': [rmse, mae, mape, r2]
        })
        # Format nilai ke dua angka di belakang koma tanpa pembulatan
        def format_trunc(val):
            return f"{int(val * 100) / 100:.2f}"

        metrics_df['Nilai'] = metrics_df['Nilai'].apply(format_trunc)

        fig_metrics = px.bar(metrics_df, x='Metrik', y='Nilai', 
                   labels={'Nilai': 'Nilai Metrik'},
                   text_auto=True,
                   color='Metrik',
                   color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        fig_metrics.update_traces(textposition='outside')
        st.plotly_chart(fig_metrics, use_container_width=True)

        # Pilih mode prediksi
        st.subheader("Pilih Mode Prediksi")
        mode = st.radio("Pilih cara menentukan horizon prediksi:", 
                      ("Custom via Slider", "Preset", "Pilih Tanggal"))

        if mode == "Custom via Slider":
            st.session_state.horizon = st.slider("Pilih horizon prediksi (hari):", 
                                              1, 90, st.session_state.horizon)
        elif mode == "Preset":
            st.write("Pilih preset horizon:")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("3 Hari"):
                    st.session_state.horizon = 3
            with col2:
                if st.button("7 Hari"):
                    st.session_state.horizon = 7
            with col3:
                if st.button("60 Hari"):
                    st.session_state.horizon = 60
            with col4:
                if st.button("90 Hari"):
                    st.session_state.horizon = 90
        else:
            st.write(f"Tanggal terakhir di dataset: {last_date.strftime('%Y-%m-%d')}")
            selected_date = st.date_input("Pilih tanggal untuk prediksi:", 
                                        min_value=last_date.date() + timedelta(days=1),
                                        max_value=datetime(2025, 12, 31))
            horizon = (selected_date - last_date.date()).days
            if horizon <= 0:
                st.error("Tanggal yang dipilih harus setelah tanggal terakhir di dataset!")
                return
            st.session_state.horizon = horizon

        st.write(f"Horizon yang dipilih: {st.session_state.horizon} hari")

        if st.button("Dapatkan Prediksi"):
            horizon = st.session_state.horizon
            if len(close_prices) < WINDOW:
                st.error(f"Data tidak cukup untuk prediksi (minimum {WINDOW} hari).")
                return
            last_sequence = close_prices[-WINDOW:]
            last_sequence_scaled = scaler.transform(last_sequence.reshape(-1, 1))
            X = last_sequence_scaled.reshape(1, WINDOW, 1)

            predictions = []
            current_sequence = X.copy()
            for _ in range(horizon):
                pred = model.predict(current_sequence, verbose=0)
                predictions.append(pred[0, 0])
                current_sequence = np.roll(current_sequence, -1)
                current_sequence[0, -1, 0] = pred

            predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
            predictions = np.maximum(predictions, 0)

            last_close = close_prices[-1]
            last_pred = predictions[-1]
            percent_change = ((last_pred - last_close) / last_close) * 100
            
            st.subheader("Perubahan Harga Prediksi")
            st.metric(
                label="Perubahan Harga (%)",
                value=f"{percent_change:.2f}%",
                delta=f"{percent_change:.2f}% {'naik' if percent_change >= 0 else 'turun'}"
            )

            future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), 
                                       periods=horizon, freq='D')
            pred_df = pd.DataFrame({
                'Tanggal': future_dates,
                'Prediksi Harga (USD)': predictions
            })
            # st.write("**Tabel Prediksi Harga**")
            # st.dataframe(pred_df)

            last_30_days = close_prices[-30:]
            pred_df_plot = pd.DataFrame({
                'timestamp': np.concatenate([df[timestamp_col].tail(30).values, future_dates]),
                'price': np.concatenate([last_30_days, predictions]),
                'type': ['Historis'] * 30 + ['Prediksi'] * horizon
            })
            
            st.subheader("Grafik Prediksi vs Historis")
            fig = px.line(pred_df_plot, x='timestamp', y='price', color='type', 
                         title=f"Prediksi {horizon} Hari vs Harga Historis",
                         labels={'timestamp': 'Tanggal', 'price': 'Harga (USD)', 'type': 'Tipe'})
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error memuat data atau model: {str(e)}")
        st.write(f"Silakan cek file di {data_path}, {model_path}, dan {scaler_path}")

if __name__ == "__main__":
    main()