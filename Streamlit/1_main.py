# D:\Coolyeah\Laskar AI\Capstone\fix\Streamlit\app.py
import streamlit as st
from pathlib import Path
import time
import pandas as pd
import os

# Konfigurasi Halaman
st.set_page_config(
    page_title="GoldSight",
    page_icon="🥇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== INISIALISASI SESSION ==========
if "user_name" not in st.session_state:
    st.session_state.user_name = None  
if "show_form" not in st.session_state:
    st.session_state.show_form = False  
if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False  

# ========== FORM AWAL (LANDING PAGE) ==========
if not st.session_state.user_name:
    placeholder = st.empty()

    with placeholder.container():
        BASE_DIR = Path(__file__).resolve().parent
        image_path = BASE_DIR / 'assets' / 'image' / 'header.png'
        st.image(image_path, use_container_width=True)
        st.title("GoldSight :blue[Navigasi Cerdas Investasi Emas Anda]")
        st.subheader("Prediksi Harga Emas Berbasis Deep Learning")
        st.markdown("""**GoldSight** membantu investor memahami tren harga emas dan membuat keputusan berbasis data di tengah volatilitas pasar global.
Dengan model GRU dan data historis sejak 2000, kami menyediakan prediksi akurat dan wawasan pasar yang mudah diakses.""")

        col1, col2, col3 = st.columns([1, 0.5, 1])  
        with col2:
            if st.button("🚀 Go to Dashboard", use_container_width=True):
                st.session_state.show_form = True  
                st.rerun()

    st.markdown("<style>[data-testid='stSidebar'] {display: none;}</style>", unsafe_allow_html=True)

# ========== POP-UP INPUT NAMA ==========
if st.session_state.show_form and not st.session_state.user_name:
    @st.dialog("🎉 Selamat Datang!")
    def get_name():
        st.write("Silakan masukkan nama kamu terlebih dahulu!")
        name = st.text_input("Nama Anda", key="user_name_input")

        if st.button("Masuk"):
            if name.strip():
                st.session_state.user_name = name.strip()
                st.session_state.welcome_shown = False  
                st.rerun()
            else:
                st.warning("Silakan isi nama terlebih dahulu!")

    get_name()
    
    
if st.session_state.user_name:
    if not st.session_state.welcome_shown:
        st.toast(f"Selamat datang, {st.session_state.user_name}! 🎉")
        time.sleep(1.5)
        st.toast("Semoga harimu menyenangkan! ☀️")
        time.sleep(1.5)
        st.toast("Ayo jelajahi dashboard ini!", icon="🚀")
        st.session_state.welcome_shown = True 
        
if st.session_state.user_name:
    def main():
        st.title("🥇 GoldSight: Navigasi Cerdas Investasi Emas Anda")
        st.header("Prediksi Harga Emas Berbasis Deep Learning")
        st.subheader(f"Halo {st.session_state.user_name}! Welcome to Dashboard! 🚀")   
        st.markdown("""
        **GoldSight** membantu investor memahami tren harga emas dan membuat keputusan berbasis data di tengah volatilitas pasar global. 
        Dengan model GRU dan data historis sejak 2000, kami menyediakan prediksi akurat dan wawasan pasar yang mudah diakses.
        """)
        
        # Visual mini: Tren harga 30 hari terakhir
        st.markdown("### Tren Harga Emas Terkini")
        data_path = r"D:\Coolyeah\Laskar AI\Capstone\fix\Dataset\final_gold_data.csv"
        try:
            # Cek apakah file ada
            if not os.path.exists(data_path):
                st.error(f"File tidak ditemukan: {data_path}")
                return
            
            # Load dataset dengan delimiter semicolon
            df = pd.read_csv(
                data_path,
                delimiter=';',  # Ganti ke semicolon
                encoding='utf-8',
                on_bad_lines='skip'  # Skip baris bermasalah
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

            # Ambil 30 hari terakhir
            recent_data = df.tail(30)[[timestamp_col, 'close']]
            st.line_chart(recent_data.set_index(timestamp_col)['close'])
        except Exception as e:
            st.error(f"Error memuat data: {str(e)}")
            st.write(f"Silakan cek file CSV di {data_path}")

        st.markdown("### Tim Pengembang")
        st.write("- Johanadi Santoso – Universitas Diponegoro")
        st.write("- Riyan Zaenal Arifin – Universitas Teknologi Yogyakarta")
        st.write("- Shendi Teuku Maulana Efendi – Universitas PGRI Madiun")
        st.write("- Wulandari – Universitas Negeri Makassar")
        
        st.markdown("**Mulai eksplorasi sekarang!**")
        if st.button("Lihat Prediksi Harga"):
            st.session_state['page'] = "Prediksi Harga"  # Redirect (opsional, sidebar udah handle)

    if __name__ == "__main__":
        main()