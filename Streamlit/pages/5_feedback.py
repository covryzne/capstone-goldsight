import streamlit as st
import pandas as pd
import os
from pathlib import Path
from datetime import datetime

# Inisialisasi session state
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

    st.title("⚙️ Feedback")
    st.write(f"Selamat datang, {st.session_state.user_name}! Kami menghargai masukan Anda untuk meningkatkan GoldSight.")

    # Feedback Pengguna
    st.write("### Feedback Pengguna")
    with st.form("feedback_form"):
        feedback = st.text_area("Tulis umpan balik atau saran di sini:")
        submit = st.form_submit_button("Kirim Feedback")

        if submit:
            if feedback.strip():
                # Simpan feedback ke file
                BASE_DIR = Path(__file__).resolve().parent.parent.parent
                feedback_path = BASE_DIR / 'Dataset' / 'feedback.csv'
                feedback_data = {
                    'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                    'User': [st.session_state.user_name],
                    'Feedback': [feedback.strip()]
                }
                feedback_df = pd.DataFrame(feedback_data)
                if os.path.exists(feedback_path):
                    feedback_df.to_csv(feedback_path, mode='a', header=False, index=False)
                else:
                    feedback_df.to_csv(feedback_path, index=False)
                st.success("Terima kasih atas umpan balik Anda!")
            else:
                st.warning("Feedback tidak boleh kosong!")

if __name__ == "__main__":
    main()