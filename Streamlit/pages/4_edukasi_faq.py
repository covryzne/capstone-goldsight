# D:\Coolyeah\Laskar AI\Capstone\fix\Streamlit\pages\4_edukasi_faq.py
import streamlit as st

if st.session_state.user_name:
    def main():
        st.title("📚 Edukasi & FAQ")
        st.markdown("""
        ### Tentang Investasi Emas
        Emas adalah aset safe-haven yang populer di tengah ketidakpastian ekonomi. Harga emas global melonjak hingga $121.06/gram pada April 2025 karena faktor seperti kebijakan tarif AS dan aksi beli bank sentral.

        ### Bagaimana GoldSight Bekerja?
        Kami menggunakan model **GRU (Gated Recurrent Unit)**, sebuah algoritma Deep Learning, untuk memprediksi harga emas berdasarkan data historis sejak 2000. Model ini dilatih dengan data dari [Kaggle](https://www.kaggle.com/datasets/romanfonel/precious-metals-history-since-2000-with-news).

        ### FAQ
        **1. Seberapa akurat prediksi kami?**  
        Akurasi prediksi tergantung pada volatilitas pasar dan kualitas data. Model kami dievaluasi dengan metrik seperti MAE dan RMSE untuk memastikan keandalan.

        **2. Apa batasan model ini?**  
        - Ketidakpastian ekonomi global dapat memengaruhi akurasi.  
        - Prediksi jangka pendek (1-30 hari) lebih andal dibandingkan jangka panjang.  
        - Model ini adalah prototipe dan bukan pengganti saran keuangan profesional.

        **3. Bagaimana cara terbaik berinvestasi di emas?**  
        - Pantau tren pasar dan sentimen berita.  
        - Pertimbangkan diversifikasi portofolio.  
        - Konsultasikan dengan ahli keuangan sebelum mengambil keputusan besar.
        """)

    if __name__ == "__main__":
        main()