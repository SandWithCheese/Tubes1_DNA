# Tugas Besar 1 Strategi Algoritma

## Deskripsi Permasalahan

Diamonds merupakan suatu programming challenge yang mempertandingkan bot yang anda buat dengan bot dari para pemain lainnya. Setiap pemain akan memiliki sebuah bot dimana tujuan dari bot ini adalah mengumpulkan diamond sebanyak-banyaknya. Cara mengumpulkan diamond tersebut tidak akan sesederhana itu, tentunya akan terdapat berbagai rintangan yang akan membuat permainan ini menjadi lebih seru dan kompleks. Untuk memenangkan pertandingan, setiap pemain harus mengimplementasikan strategi tertentu pada masing-masing bot-nya.

## Pemanfaatan Algoritma Greedy dalam pembuatan bot permainan Diamonds

Bot permainan Diamonds yang kami buat mengimplementasikan algoritma greedy untuk mendapatkan diamond paling banyak dalam waktu yang terbatas. Bot yang kami buat pada dasarnya sama-sama mengimplementasikan algoritma greedy, hanya saja implementasi algoritma greedy pada bot-bot yang telah kami buat mengambil sudut pandang yang berbeda dalam strateginya. Bot-bot yang kami buat adalah sebagai berikut:

- Greedy (Logika greedy utama)
- GreedyDense (Logika greedy by density diamond)
- Chaser (Logika pergerakan bot mengejar bot lain)
- Sandwich (Logika greedy dasar yang memilih preferensi terhadap teleporter dan red button secara acak)
- DewoDT (Logika greedy dasar yang ditambah tambahan strategi portal, diamond button dan heuristic)
- Aggresive (Logika greedy yang lebih menjaga jarak dari bot lain karena ada bug dari game diamonds)

## Persyaratan Menjalankan

Pastikan telah menginstall library berikut dengan pip:

- colorama
- requests
- dacite
- keyboard

## Cara Menjalankan

1. Clone repository ini

   ```bash
   git clone https://github.com/SandWithCheese/Tubes1_DNA.git
   ```

2. Kunjungi directory `/src`

   ```bash
   cd src
   ```

3. Untuk menjalankan 1 bot saja,

   ```bash
   python main.py --logic <LOGIC_NAME> --email=<UNIQUE_EMAIL> --name=<NAME> --password=<PASSWORD> --team <TEAM_NAME>
   ```

4. Untuk menjalankan lebih dari beberapa bot,

   - Windows

   ```bash
   ./run-bots.bat
   ```

   - Linux / (possibly) macOS

   Sebelum menjalankan script, pastikan untuk memberikan izin kepada shell script agar bisa dieksekusi

   ```bash
   chmod +x run-bots.sh
   ```

   Jalankan script untuk banyak bot dengan command

   ```bash
   ./run-bots.sh
   ```

## Anggota Kelompok

|   NIM    |         Nama         |
| :------: | :------------------: |
| 13522005 | Ahmad Naufal Ramadan |
| 13522011 | Dewantoro Triatmojo  |
| 13522109 |  Azmi Mahmud Bazeid  |
