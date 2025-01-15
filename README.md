<h1>Emisi Karbon</h1>

<p>Web Emisi Karbon adalah platform yang dirancang untuk membantu individu, perusahaan, dan organisasi dalam mengelola, melacak, serta mengurangi emisi karbon mereka</p>

<p>Untuk mengembangkan website ini ada beberapa aplikasi yang perlu tersedia di komputer anda :</p>

- Pastikan git terinstall untuk melakukan cloning template website
- Pastikan python terinstall untuk menjalankan website di localhost
- Pastikan XAMPP terintall untuk mengelola database website
- Pastikan Postman terintall untuk melakukan testing API yang tersedia

<br/>

<p>Setelah itu, perhatikan lah beberapa step selanjutnya pada daftar berikut ini :</p>

- <h3>Cloning repositori website</h3>
    - Buka vscode, buatlah folder kosong.
- ## Cloning repositori website
    - git clone https://github.com/fpbismyname/emisicarbon.git
- ## Masuk ke environtment folder python di folder website emisi karbon
    - .\venv\Scripts\activate
- ## Menjalankan website di localhost dengan debug mode
    - flask --app run run --debug
- ## Menjalankan website di localhost tanpa debug mode
    - flask --app run run
- ## Menghapus semua isi tabel dan mengisi dengan seeder
    - flask db-refresh
