# Bike Sharing Dashboard

Dashboard interaktif untuk analisis data **Bike Sharing Dataset** sebagai bagian dari  
**submission kelas Belajar Fundamental Analisis Data**.  
Aplikasi ini dikembangkan menggunakan **Streamlit** untuk menampilkan visualisasi
dan insight terkait pola penyewaan sepeda.

Dashboard ini menyajikan:
- Ringkasan metrik penyewaan sepeda
- Tren penyewaan sepeda per bulan
- Analisis faktor yang memengaruhi penyewaan (musim, cuaca, dan hari kerja)
- Analisis lanjutan kategori demand
- Analisis jenis pengguna (casual dan registered)

---

## 🚀 Live Demo (Streamlit Deployment)

Aplikasi ini telah berhasil dideploy menggunakan **Streamlit Community Cloud**  
dan dapat diakses melalui link berikut:

🔗 **[Lihat Dashboard](https://submissiondahsboard.streamlit.app/)**

---

## 🛠 Setup Environment

### Setup Environment – Anaconda
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

---

### Setup Environment – Shell / Terminal
```bash
pip install -r requirements.txt
```

---

### Run Streamlit App (Local)
```bash
streamlit run dashboard/dashboard.py
```
