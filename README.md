# GoldSight: Navigasi Cerdas Investasi Emas
## LAI25-SM048
### Anggota Tim
![image](https://github.com/user-attachments/assets/ece0cda1-75ef-4251-b5cb-dca032e11e11)

* A200YBF237 – Johanadi Santoso – Universitas Diponegoro - [Aktif]
* A327YBF437 – Riyan Zaenal Arifin  – Universitas Teknologi Yogyakarta - [Aktif]
* A463YBM456 – Shendi Teuku Maulana Efendi – Universitas PGRI Madiun - [Aktif]
* A278XAM502 – Wulandari – Universitas Negeri Makassar - [Aktif]
---

**GoldSight** adalah aplikasi web buat investor yang pengen paham tren harga emas dan bikin keputusan cerdas di tengah pasar yang naik-turun. Pake model *Deep Learning* **GRU (Gated Recurrent Unit)** dan data harga emas dari tahun 2000, GoldSight kasih prediksi harga yang akurat, visualisasi tren pasar, sama wawasan edukasi biar lo bisa investasi dengan percaya diri. 

Proyek ini dibikin sama tim **Laskar AI** buat Capstone Project

## Fitur Keren
- **Prediksi Harga Emas**: Ramal harga emas 1-90 hari ke depan pake model GRU.
- **Analisis Pasar**: Grafik interaktif buat lihat tren harga dan volume perdagangan emas sejak 2000.
- **Dashboard Gampang**: Antarmuka yang gampang dipake buat eksplor data dan prediksi.
- **Edukasi & FAQ**: Info soal investasi emas dan cara kerja model prediksi.
- **Feedback**: Feedback.

## Teknologi yang Dipake
- **Streamlit**: Buat bikin aplikasi web yang interaktif.
- **Pandas & Plotly**: Buat olah data dan bikin grafik yang kece.
- **TensorFlow**: Buat model *Deep Learning* GRU.
- **Joblib**: Buat nyimpen dan load scaler model.
- **Python**: Bahasa utama yang ngejalanin semuanya.

## Apa yang Lo Butuhin
- Python 3.10 atau lebih baru
- Dependensi di `requirements.txt`
- File dataset: `final_gold_data.csv`
- File model: `best_model_gru.h5` dan `scaler_close_gru.pkl`

## Cara Install
1. Clone repo ini:
   ```bash
   git clone https://github.com/covryzne/capstone-goldsight.git
   cd capstone-goldsight
   ```
2. Bikin virtual environment (conda):
   ```bash
   conda create -n capstone python=3.10
   conda activate capstone
   ```
3. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
4. Pastiin file ini ada di tempatnya:
   - `Dataset/final_gold_data.csv`
   - `Model/best_model_gru.h5`
   - `Model/scaler_close_gru.pkl`

## Cara Jalanin
1. Masuk ke folder `capstone-goldsight`.
2. Jalanin Streamlit:
   ```bash
   streamlit run Streamlit/app.py
   ```
3. Buka browser di `http://localhost:8501`.
4. Masukin nama lo di pop-up login buat masuk ke dashboard.

## Struktur Folder
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
│   ├── best_model_gru.h5     # Model GRU buat prediksi
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

## Dataset
Data harga emas (`final_gold_data.csv`) diambil dari [Kaggle: Precious Metals History Since 2000](https://www.kaggle.com/datasets/romanfonel/precious-metals-history-since-2000-with-news).

## Catatan Penting
- Prediksi harga emas cuma buat jangka pendek dan bisa dipengaruhi gejolak pasar. Jadi, pake sebagai referensi aja, bukan pengganti saran keuangan pro.
- Aplikasi ini prototipe, bisa dikembangin lagi, misalnya nambahin integrasi berita pasar atau model yang lebih canggih.

## Mau Kontribusi?
Kami seneng banget kalau lo mau bantu! Fork repo ini, bikin pull request, atau kasih saran lewat issue.

## Lisensi
Proyek ini pake [MIT License](LICENSE).

---
Dibikin sama **Laskar AI** – Dicoding: @shendyeff @johanadisantoso

