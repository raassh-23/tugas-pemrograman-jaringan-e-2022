# Tugas 2

- Jalankan file server_thread_http.py
- Lakukan performance test dengan menggunakan ab dalam hal jumlah request dan concurrency dengan format `ab -n <jumlah request> -c <jumlah concurrency> <url>`
- Lakukan percobaan dengan kombinasi 
    - Jumlah request 10, 50, 100,500 sampai server tidak dapat melayani
    - Jumlah konkurensi (simulasi client mengakses konkuren), 1 client - maks yang dapat dilayani
    - Tipe media (pdf, txt, jpg)
    - Catatlah hasil ab tersebut dalam metrik hasil yang tertulis di tabel
    - Jika server tidak mampu menangani request, tulislah di kolom tersebut dengan “OVERLOAD”
- Pada saat server “OVERLOAD”, berikan usulan optimasi agar server masih bisa melayani
- Capturelah semua aktifitas anda dengan screenshot, termasuk usulan optimasinya. Berikan deskripsi yang cukup untuk penjelasan screenshot. Dan satukan semua dalam file PDF maks 10 halaman
