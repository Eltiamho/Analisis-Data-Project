
# E-Commerce Public Dataset Analysis Project

## Setup Environment
1. Pastikan Anda berada di direktori utama proyek (folder root).
2. Install library yang dibutuhkan:
   ```bash
   pip install -r requirements.txt


## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard.py
```

## Cara Menjalankan Dashboard
1. Pastikan file `main_data.csv` berada di dalam folder yang sama dengan `dashboard.py`.
2. Buka terminal atau command prompt.
3. Masuk ke direktori folder dashboard:
    ```bash
   cd dashboard
4. Jalankan Perintah berikut
    ```bash
    streamlit run dashboard.py
Jika Anda menggunakan Windows dan menemui error 'streamlit is not recognized', silakan gunakan perintah alternatif berikut:
    ```bash
    python -m streamlit run dashboard.py