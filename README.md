# 🌟 GoldSight: Navigasi Cerdas Investasi Emas
## 📌 ID Grup Capstone LAI25-SM048
### Anggota Tim
![image](https://github.com/user-attachments/assets/ece0cda1-75ef-4251-b5cb-dca032e11e11)

* A200YBF237 – Johanadi Santoso – Universitas Diponegoro - [Aktif]
* A327YBF437 – Riyan Zaenal Arifin  – Universitas Teknologi Yogyakarta - [Aktif]
* A463YBM456 – Shendi Teuku Maulana Efendi – Universitas PGRI Madiun - [Aktif]
* A278XAM502 – Wulandari – Universitas Negeri Makassar - [Aktif]
---
## 🚀 Tentang Proyek

**GoldSight** adalah platform berbasis web yang dirancang untuk mempermudah investor dalam memahami dan memprediksi pergerakan harga emas. Dengan mengintegrasikan teknologi **Deep Learning** (GRU) dan analisis visual berbasis data historis sejak tahun 2000, GoldSight hadir sebagai asisten digital yang membantu pengguna membuat keputusan investasi yang lebih bijak dan berbasis data.

🔗 **Akses Aplikasi**
👉 [goldsight-capstone.streamlit.app](https://goldsight-capstone.streamlit.app/)
---

## 💡 Fitur Unggulan

| Fitur                       | Deskripsi                                                                           |
| --------------------------- | ----------------------------------------------------------------------------------- |
| 🔮 **Prediksi Harga**       | Model GRU memprediksi harga emas hingga 90 hari ke depan.                           |
| 📈 **Analisis Pasar**       | Visualisasi interaktif untuk mengeksplorasi tren harga dan volume sejak tahun 2000. |
| 🧠 **Edukasi & FAQ**        | Penjelasan mudah dipahami tentang konsep investasi emas dan algoritma prediksi.     |
| 📊 **Dashboard Responsif**  | Antarmuka intuitif berbasis Streamlit, siap pakai di berbagai perangkat.            |
| ✉️ **Formulir Umpan Balik** | Pengguna dapat menyampaikan saran dan evaluasi langsung di aplikasi.                |

---

## 🛠️ Teknologi yang Digunakan

* **Python 3.10+** – Bahasa pemrograman utama
* **TensorFlow** – Arsitektur model GRU untuk prediksi deret waktu
* **Streamlit** – Framework antarmuka web interaktif
* **Pandas & Plotly** – Analisis dan visualisasi data
* **Joblib** – Serialisasi model dan preprocessing

---

## ⚙️ Persyaratan Sistem

* Python 3.10 atau lebih baru
* File dependensi: `requirements.txt`
* Dataset: `Dataset/final_gold_data.csv`
* Model:

  * `Model/best_model_gru.h5`
  * `Model/scaler_close_gru.pkl`

---

## 🔧 Cara Instalasi

1. **Clone repositori**

   ```bash
   git clone https://github.com/covryzne/capstone-goldsight.git
   cd capstone-goldsight
   ```

2. **Buat environment**

   ```bash
   conda create -n capstone python=3.10
   conda activate capstone
   ```

3. **Install dependensi**

   ```bash
   pip install -r requirements.txt
   ```

4. **Pastikan file berikut tersedia:**

   * `Dataset/final_gold_data.csv`
   * `Model/best_model_gru.h5`
   * `Model/scaler_close_gru.pkl`

---

## ▶️ Cara Menjalankan Aplikasi

1. Navigasikan ke direktori proyek:

   ```bash
   cd capstone-goldsight
   ```

2. Jalankan aplikasi menggunakan **Streamlit**:

   ```bash
   streamlit run Streamlit/app.py
   ```

3. Setelah aplikasi berjalan, buka browser dan akses:

   ```
   http://localhost:8501
   ```

4. Masukkan nama Anda pada pop-up login untuk mengakses dashboard utama.

## 🗂️ Struktur Folder
```
capstone-goldsight/
├── Dataset/
│   └── final_gold_data.csv       # Data harga emas
├── Dokumen/
│   ├── Project Brief - LAI25-SM048.docx
│   ├── Project Plan - LAI25-SM048.docx
│   ├── Project Plan - LAI25-SM048.pdf
│   ├── Schedule Progress.xlsx
│   ├── [Laskar Ai] Pakta Integritas LAI25-SM048.docx
│   └── [Laskar Ai] Pakta Integritas LAI25-SM048.pdf
├── Model/
│   ├── best_model_gru.h5     # Model GRU terbaik untuk prediksi
│   └── scaler_close_gru.pkl  # Scaler buat preprocessing
├── Notebook/
│   └── notebook.ipynb             # Notebook buat olah data
├── Streamlit/
│   ├── app.py                    # Landing page & dashboard
│   ├── assets/
│   │   └── image/
│   │       └── header.png        # Gambar header landing page
│   └── pages/
│       ├── 2_analisis_pasar.py   # Tren dan statistik pasar
│       ├── 3_prediksi_harga.py   # Prediksi harga emas
│       ├── 4_edukasi_faq.py      # Edukasi dan FAQ
│       └── 5_feedback.py         # Feedback
├── .gitignore                    # File yang di-skip git
├── README.md                     # Dokumentasi proyek ini
└── requirements.txt              # Daftar dependensi
```

## 🗃️ Dataset
Data harga emas (`final_gold_data.csv`) diambil dari [Kaggle: Precious Metals History Since 2000](https://www.kaggle.com/datasets/romanfonel/precious-metals-history-since-2000-with-news).

## ⚠️ Catatan Penting
- Prediksi harga emas cuma buat jangka pendek dan bisa dipengaruhi gejolak pasar. Jadi, gunakan sebagai referensi aja, bukan pengganti saran keuangan pro.
- Aplikasi ini adalah prototipe yang masih dapat dikembangkan lebih lanjut, seperti integrasi berita pasar dan peningkatan model.

## 🤝 Mau Kontribusi?
Terbuka untuk kontribusi!
Silakan fork, buat pull request, atau kirim masukan lewat issue.

## Lisensi
Proyek ini pake [MIT License](LICENSE).

---
Dibuat dengan dedikasi **Laskar AI** – Dicoding: @shendyeff @johanadisantoso @riyan_zaenal_arifin @wulandari_vhfz

