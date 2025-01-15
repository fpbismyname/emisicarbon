<h1>Emisi Karbon</h1>

<p>Web Emisi Karbon adalah platform yang dirancang untuk membantu individu, perusahaan, dan organisasi dalam mengelola, melacak, serta mengurangi emisi karbon mereka</p>

<p>Untuk mengembangkan website ini ada beberapa aplikasi yang perlu tersedia di komputer anda :</p>

- Pastikan git terinstall untuk melakukan cloning template website
- Pastikan python terinstall untuk menjalankan website di localhost
- Pastikan XAMPP terintall untuk mengelola database website
- Pastikan Postman terintall untuk melakukan testing API yang tersedia

<br/>

<p>Setelah itu, perhatikan lah beberapa step selanjutnya pada daftar berikut ini :</p>

- ### Mengaktifkan XAMPP
    - Buka xampp, aktifkan apache dan mysql.
- ### Buat database
    - Buka localhost di web browser, buatlah database.
- ### Membuat folder kosong
    - Buka vscode, buatlah folder kosong.
- ### Cloning repositori website
    - Buka new terminal di vscode, dan clone folder emisi karbon :
    - git clone https://github.com/fpbismyname/emisicarbon.git
- ### Masuk ke environtment folder python di folder website emisi karbon
    - Masukan perintah "cd .\emisi-api" lalu jalankana perintah ini :
    - .\venv\Scripts\activate
- ### Menghapus semua isi tabel dan mengisi dengan seeder
    - Masukan perintah ini untuk menjalankannya :
    - flask db-refresh
- ### Menjalankan website di localhost dengan debug mode
    - Masukan perintah ini untuk menjalankannya :
    - flask --app run run --debug
- ### Menjalankan website di localhost tanpa debug mode
    - Masukan perintah ini untuk menjalankannya :
    - flask --app run run
