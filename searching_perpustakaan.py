import streamlit as st
import json
import pandas as pd
import os

# Fungsi untuk membaca data dari file JSON
def baca_data_dari_file(nama_file):
    if os.path.exists(nama_file):
        with open(nama_file, 'r') as file:
            data = json.load(file)
        return data
    else:
        st.error(f"File '{nama_file}' tidak ditemukan.")
        return None

# Fungsi untuk mencari buku berdasarkan kategori
def cari_buku(kategori_dicari, data):
    for kategori in data:
        if kategori['kategori'].lower() == kategori_dicari.lower():
            return kategori['buku']
    return None

# Nama file JSON yang ingin dibaca
nama_file = 'c:\\Users\\Mega Global\\Downloads\\datajsonbuku.json'

# Pengaturan tampilan
st.set_page_config(
    page_title="Pencarian Buku Perpustakaan",
    layout="wide"
)

# Sidebar
st.sidebar.header("Pencarian Buku")
st.sidebar.markdown("""
Gunakan aplikasi ini untuk mencari lokasi buku di perpustakaan.  
Pilih kategori buku pada kolom di bawah dan tekan tombol 'Cari'.
""")

# Judul aplikasi
st.title("📚 Pencarian Buku Perpustakaan")

# Membaca data dari file JSON
data_perpustakaan = baca_data_dari_file(nama_file)

# Jika data berhasil dibaca
if data_perpustakaan:
    # Ambil daftar kategori buku
    daftar_kategori = ["Pilih kategori buku"] + [kategori['kategori'] for kategori in data_perpustakaan]

    # Input pengguna
    kategori_yang_dicari = st.selectbox("Pilih Kategori Buku:", daftar_kategori)

    # Tombol untuk mencari
    if st.button("Cari"):
        if kategori_yang_dicari != "Pilih kategori buku":
            # Cari buku berdasarkan kategori yang dipilih
            buku_ditemukan = cari_buku(kategori_yang_dicari, data_perpustakaan)
            
            # Buat DataFrame untuk menampilkan hasil
            if buku_ditemukan:
                df = pd.DataFrame(buku_ditemukan)
                df['No'] = range(1, len(df) + 1)  # Tambah kolom No dengan nomor urut dimulai dari 1
                df = df.rename(columns={'judul': 'Judul', 'pengarang': 'Pengarang', 
                                        'penerbit': 'Penerbit', 'tahun_terbit': 'Tahun Terbit',
                                        'lantai': 'Lantai', 'ruangan': 'Ruangan', 'rak': 'Rak'})
                df = df[['No', 'Judul', 'Pengarang', 'Penerbit', 'Tahun Terbit', 'Lantai', 'Ruangan', 'Rak']]  # Susun ulang kolom
                st.subheader(f"Buku-buku dalam kategori '{kategori_yang_dicari}':")
                st.write(df.to_html(index=False), unsafe_allow_html=True)  # Tampilkan tabel tanpa indeks
            else:
                st.warning("Tidak ada buku yang ditemukan dalam kategori ini.")
        else:
            st.warning("Silakan pilih kategori buku.")
else:
    st.error("Data perpustakaan tidak tersedia.")
