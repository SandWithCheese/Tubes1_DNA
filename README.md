# Tugas Besar 1 Strategi Algoritma

## Pemanfaatan Algoritma Greedy dalam pembuatan bot permainan Diamonds

Bot permainan Diamonds yang kami buat mengimplementasikan algoritma greedy untuk mendapatkan diamond paling banyak dalam waktu yang terbatas. Bot yang kami buat pada dasarnya sama-sama mengimplementasikan algoritma greedy, hanya saja implementasi algoritma greedy pada bot-bot yang telah kami buat mengambil sudut pandang yang berbeda dalam strateginya. Bot-bot yang kami buat adalah sebagai berikut:

- Greedy (Logika greedy utama)
- GreedyDense (Logika greedy by density)
- Circular (Logika pergerakan bot secara melingkar)
- Chaser (Logika pergerakan bot mengejar bot lain)
- WASD (Bot yang dapat dimainkan dengan keyboard)
- Sandwich (Logika greedy dasar yang memilih preferensi terhadap teleporter dan red button secara acak)
- DewoDT (Logika greedy dasar yang ditambah tambahan strategi)
- Aggresive (Logika greedy yang lebih menjaga jarak dari bot lain karena ada bug dari game Diamonds)

## Requirements

- colorama
- requests
- dacite
- keyboard

## How to Run

1. To run one bot

    ```bash
    python src/main.py --logic Random --email=your_email@example.com --name=your_name --password=your_password --team etimo
    ```

2. To run multiple bots simultaneously

    Change directory to src

    ```bash
    cd src
    ```

    For Windows

    ```bash
    ./run-bots.bat
    ```

    For Linux / (possibly) macOS

    ```bash
    ./run-bots.sh
    ```

    **Before executing the script, make sure to change the permission of the shell script to enable executing the script (for linux/macOS)**

    ```bash
    chmod +x run-bots.sh
    ```

## Anggota

- Ahmad Naufal Ramadan - 13522005
- Dewantoro Triatmojo - 13522011
- Azmi Mahmud Bazeid - 13522109
