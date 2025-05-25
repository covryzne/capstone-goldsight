import streamlit as st

if st.session_state.user_name:
    def main():
        st.title("⚙️ Feedback")

        # Feedback Pengguna
        st.write("### Feedback Pengguna")
        feedback = st.text_area("Tulis umpan balik atau saran di sini:")
        if feedback:
            st.write("Terima kasih atas umpan balik Anda!")
        
    if __name__ == "__main__":
        main()