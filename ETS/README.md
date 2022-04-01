# Evaluasi Tengah Semester

Dengan menggunakan contoh program pada  [{repo}/progjar1a](https://github.com/rm77/progjar/tree/master/progjar1a)
- buatlah susunan koneksi client server

## Soal 1
Dari client, jalankan client dengan multithread
- Nomor pemain secara random, tambahkanlah data nama pemain jika diperlukan. 
- Dengan menggunakan contoh multithread pada [{repo}/progjar3/concurrency/multi_thread.py](https://github.com/rm77/progjar/blob/master/progjar3/concurrency/multi_thread.py), lakukan request dengan jumlah thread berikut ini 1,5,10,20
- Catatlah hasilnya dari sisi clien dalam bentuk tabel, dalam metrik:
    - Jumlah request dikirim
    - Jumlah respon (respon dicatat ketika data diterima, jika hang/tidak ada jawaban, tidak dihitung)
    - latency, waktu mulai kirim request sampai response data diterima (opsional)
- Buatlah screenshot tampilan di sisi server dan client
- Laporkan deskripsi hasil pengamatan untuk melengkapi screenshot tersebut

## Soal 2
Dari client, jalankan client dengan multithread, server multithread
- Dengan menggunakan contoh multithread pada [{repo}/progjar3/concurrency/multi_thread.py](https://github.com/rm77/progjar/blob/master/progjar3/concurrency/multi_thread.py)
- Modifikasilah program server pada [{repo}/progjar1a/server_side/tcp_server.py](https://github.com/rm77/progjar/blob/master/progjar1a/server_side/tcp_server.py), agar dapat menghandle request secara multithread
- Dari sisi client, jalankan request untuk mendapat data pemain secara random,  tambahkanlah data nama pemain jika diperlukan, dan lakukan request dengan jumlah thread berikut ini 1,5,10,20
- Catatlah hasilnya dari sisi clien dalam bentuk tabel seperti contoh tabel pada halaman 3, dalam metrik
    - Jumlah request dikirim
    - Jumlah respon (respon dicatat ketika data diterima, jika hang/tidak ada jawaban, tidak dihitung)
    - latency, waktu mulai kirim request sampai response data diterima (opsional)
- Buatlah screenshot tampilan di sisi server dan client
- Laporkan deskripsi hasil pengamatan untuk melengkapi screenshot tersebut

## soal 3
Jalankan lagi soal nomor 2, namun untuk mode secure

## Soal 4
Berikan opini anda tentang perbandingan performa komunikasi pada soal 1, soal 2 , dan soal 3 dalam 1 paragraf, minimal 10 kalimat

