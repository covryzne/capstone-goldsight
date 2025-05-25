# D:\Coolyeah\Laskar AI\Capstone\fix\Streamlit\pages\3_prediksi_harga.py
import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import plotly.express as px
import os

if st.session_state.user_name:
    def main():
        st.title("📈 Prediksi Harga Emas")
        st.write("Gunakan model Deep Learning GRU kami untuk memprediksi harga emas jangka pendek.")

        # Inisialisasi session state untuk horizon
        if 'horizon' not in st.session_state:
            st.session_state.horizon = 7  # Default 7 hari

        # Load model dan scaler
        model_path = r"D:\Coolyeah\Laskar AI\Capstone\fix\Model\best_model_gru_5th.h5"
        scaler_path = r"D:\Coolyeah\Laskar AI\Capstone\fix\Model\scaler_close_gru_5th.pkl"
        data_path = r"D:\Coolyeah\Laskar AI\Capstone\fix\Dataset\final_gold_data.csv"
        
        try:
            # Cek apakah file model dan scaler ada
            if not os.path.exists(model_path):
                st.error(f"File model tidak ditemukan: {model_path}")
                return
            if not os.path.exists(scaler_path):
                st.error(f"File scaler tidak ditemukan: {scaler_path}")
                return
            
            # Load model dengan custom_objects
            model = tf.keras.models.load_model(
                model_path,
                custom_objects={
                    'mse': tf.keras.losses.MeanSquaredError(),
                    'mean_squared_error': tf.keras.losses.MeanSquaredError()
                }
            )
            scaler = joblib.load(scaler_path)
            # st.write("Model dan scaler berhasil dimuat.")

            # Load dataset
            if not os.path.exists(data_path):
                st.error(f"File dataset tidak ditemukan: {data_path}")
                return
            
            df = pd.read_csv(
                data_path,
                delimiter=';',
                encoding='utf-8',
                on_bad_lines='skip'
            )

            # Cek kolom yang tersedia
            # st.write("Kolom yang tersedia di dataset:", list(df.columns))

            # Cek apakah kolom 'timestamp' dan 'close' ada
            timestamp_col = None
            for col in df.columns:
                if col.lower() in ['timestamp', 'date', 'time']:
                    timestamp_col = col
                    break
            
            if timestamp_col is None:
                st.error("Kolom 'timestamp' tidak ditemukan di dataset. Silakan cek nama kolom di file CSV.")
                return
            
            if 'close' not in df.columns:
                st.error("Kolom 'close' tidak ditemukan di dataset. Silakan cek nama kolom di file CSV.")
                return

            # Convert timestamp ke datetime
            try:
                df[timestamp_col] = pd.to_datetime(df[timestamp_col])
            except Exception as e:
                st.error(f"Error saat mengonversi kolom {timestamp_col} ke datetime: {str(e)}")
                return

            close_prices = df['close'].values

            # Pilih mode prediksi
            st.subheader("Pilih Mode Prediksi")
            mode = st.radio("Pilih cara menentukan horizon prediksi:", ("Custom via Slider", "Preset"))

            # Input horizon prediksi
            if mode == "Custom via Slider":
                st.session_state.horizon = st.slider("Pilih horizon prediksi (hari):", 1, 90, st.session_state.horizon)
            else:
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

            # Debug horizon
            st.write(f"Horizon yang dipilih: {st.session_state.horizon} hari")

            # Tombol untuk jalankan prediksi
            if st.button("Dapatkan Prediksi"):
                horizon = st.session_state.horizon
                # Preprocessing untuk prediksi
                if len(close_prices) < 60:
                    st.error("Data tidak cukup untuk prediksi (minimum 60 hari).")
                    return
                last_sequence = close_prices[-60:]  # Sesuai WINDOW=60
                last_sequence_scaled = scaler.transform(last_sequence.reshape(-1, 1))
                X = last_sequence_scaled.reshape(1, 60, 1)

                # Prediksi
                predictions = []
                for _ in range(horizon):
                    pred = model.predict(X, verbose=0)
                    predictions.append(pred[0, 0])
                    X = np.roll(X, -1)
                    X[0, -1, 0] = pred

                predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()

                # Tampilkan hasil
                st.subheader(f"Prediksi Harga untuk {horizon} Hari ke Depan")

                # Grafik prediksi vs historis
                last_30_days = close_prices[-30:]
                future_dates = pd.date_range(start=df[timestamp_col].iloc[-1] + pd.Timedelta(days=1), periods=horizon, freq='D')
                pred_df = pd.DataFrame({
                    'timestamp': np.concatenate([df[timestamp_col].tail(30).values, future_dates]),
                    'price': np.concatenate([last_30_days, predictions]),
                    'type': ['Historis']*30 + ['Prediksi']*horizon
                })
                
                st.subheader("Grafik Prediksi vs Historis")
                fig = px.line(pred_df, x='timestamp', y='price', color='type', title=f"Prediksi {horizon} Hari vs Harga Historis")
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error memuat data atau model: {str(e)}")
            st.write(f"Silakan cek file di {data_path}, {model_path}, dan {scaler_path}")

    if __name__ == "__main__":
        main()