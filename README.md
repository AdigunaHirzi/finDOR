# FinDOR Tools
## Daftar Isi

1. [Apa itu _*FinDOR Tools*_ ?](#apa-itu-FinDOR-Tools)
2. [Links](#Links)
3. [Instalasi Alat](#Instalasi-Alat)
4. [Penggunan Aplikasi](#Penggunaan-Aplikasi)

## Apa itu _*FinDOR Tools*_ ?
**_FinDOR Tools_** merupakan Tool yang didesain ini menggunakan bahasa pemrograman Python untuk mengotomatiskan fungsi pengujian kerentanan IDOR pada parameter dari URL. Pada skrip yang dibuat terdapat beberapa rules yang saling berhubungan untuk memeriksa apakah parameter tersebut rentan terhadap IDOR, sehingga nantinya dapat membantu pengguna dalam validasi IDOR

Pada _FinDOR Tools_, terdapat 2 (dua) file python yang digunakan untuk mengidentifikasi kerentanan IDOR. Secara garis besar, file dan main function python pada tool FinDOR dapat dibagi menjadi 2 (dua) bagian, yaitu file proxy yang digunakan untuk menangkap traffic request yang pengguna akses saat melakukan testing serta mengumpulkan request dari traffic yang didalamnya mengandung parameter berisi ID. Sementara file kedua berfungsi untuk memvalidasi kerentanan yang terjadi dari file terindikasi memiliki parameter berisi ID, melakukan parsing command, melakukan pengecekkan apakah indikasi kerentanan tersebut terjadi pada file, serta melakukan dumping data jika valid terjadi kerentanan IDOR.

## Links

- Bahasa pemrograman Python : https://www.python.org/downloads/
- Findor Tools : https://github.com/AdigunaHirzi/finDOR.git 
- MITM CA : http://mitm.it/

## Instalasi Alat

Untuk menggunakan tool FinDOR, pengguna dapat melakukan git clone ke repository https://github.com/AdigunaHirzi/finDOR.git dengan command “git clone https:// github.com/AdigunaHirzi/finDOR.git”. 


Di dalam folder yang telah diinstalasi file terdapat beberapa file seperti FinDOR.py, FinDORproxy.py, README.md dan Requirements.txt


Sebelum menggunakan tools pengguna diharuskan meng-install sesuai dengan Requirements.txt dengan menggunakan pip install -r Requirements.txt
	 

Setelah menginstall aplikasi, pengguna perlu melakukan instalasi CA (Certificate of Authority) self-assigned milik Mitmproxy pada browser yang digunakan. Pertama, jalankan alat FinDORproxy.py dengan command: python3 FinDORproxy.py untuk menyalakan proxy, lalu akses http://mitm.it/ pada browser yang ingin digunakan sebagai tempat melakukan testing (dalam hal ini penulis menggunakan Mozilla Firefox).

 
Pilihlah certificate untuk browser yang sedang digunakan (Mozilla Firefox) pada tampilan daftar CA yang dapat dipilih sesuai kebutuhan, kemudian lakukan pengunduhan pada pilihan browser yang akan digunakan untuk pengetesan.

 
Hasil unduh dari web tersebut akan terlihat seperti gambar ... diatas. Setelah pengguna mengunduh CA, pengguna perlu melakukan import CA tersebut ke pilihan browser yang digunakan (Mozilla Firefox) untuk melakukan testing. 


Pengguna dapat melakukan import CA seperti tampilan pada gambar .... Setelah pengguna meng-import CA pada browser, pengguna dapat menggunakan alat semi automasi IDOR yang telah dirancang penulis. Dengan menjalankan command: python3 FinDORproxy.



## Penggunaan Aplikasi

Untuk menggunakan alat semi otomatis IDOR, pengguna dapat membuka terminal dan memilih command yang telah disediakan oleh penulis dalam script Python. Sebelumnya alat semi-otomatis yang dirancang ini terdiri dari dua file yaitu file Proxy yang berguna untuk menangkap traffic request yang pengguna akses saat melakukan testing serta mengumpulkan request dari traffic yang terdapat parameter berisi ID dan file FinDOR yang berguna untuk memvalidasi kerentanan yang terjadi pada file yang terindikasi memiliki parameter berisi ID, melakukan parsing command, melakukan pengecekan apakah indikasi kerentanan tersebut terjadi pada file, serta melakukan dumping data jika valid terjadi kerentanan IDOR. Berikut adalah tabel yang berisi dari detail command yang dapat digunakan dalam alat yang dirancang:
1.	FinDOR_Proxy

Opsi	Fungsi
-h / --help	Digunakan untuk menampilkan bantuan command yang terdapat dalam script.

-p PORT_SERVICE / --port PORT_SERVICE	Digunakan untuk memasukkan target port untuk memulai service proxy.

Contoh command yang dapat digunakan pada proxy.py:
-	Python proxy.py -p 4040
-	Python proxy.py --port 8080
-	Python proxy.py -p 8081

2.	FinDOR_Main

Opsi	Fungsi
-h / --help	Digunakan untuk menampilkan bantuan command yang terdapat dalam script.

-b BEARER_TOKEN / 
--bearer-token BEARER_TOKEN	Digunakan untuk memasukkan bearer token dalam command terminal.

-c SESSION_COOKIE / 
--cookie SESSION_COOKIE	Digunakan untuk memasukkan cookie dalam command terminal.

-d DUMP / --dump DUMP	Digunakan untuk melakukan dump data apabila output adalah JSON. Untuk mejalankan fitur ini dalam terminal diperlukannya IDE Spesifik yang ingin di dump.

-f FILE_PATH / --file FILE_PATH	Digunakan untuk melakukan penginputan file text yang berisikan POST request.

-i SPECIFIED_ID / --id SPECIFIED_ID	Digunakan untuk memasukkan ide spesifik yang dibutuhkan ketika melakukan dump data.

-s SPECIFIED_PARAM / --specified_param SPECIFIED_PARAM	Digunakan untuk memasukan parameter yang ingin dilakukan percobaan. Command ini duganakan ketika pengguna ingin melakukan POST request.

-u URL / --url URL	Digunakan untuk memasukkan URL pada command.

Contoh command yang dapat digunakan pada script FinDOR.py:
-	Python FinDOR.py --url="http://localhost:3000/rest/basket/1"
-	python FinDOR.py --url="http://localhost:3000/rest/basket/1" --bearer-token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MSwidXNlcm5hbWUiOiIiLCJlbWFpbCI6ImFkbWluQGp1aWNlLXNoLm9wIiwicGFzc3dvcmQiOiIwMTkyMDIzYTdiYmQ3MzI1MDUxNmYwNjlkZjE4YjUwMCIsInJvbGUiOiJhZG1pbiIsImRlbHV4ZVRva2VuIjoiIiwibGFzdExvZ2luSXAiOiIiLCJwcm9maWxlSW1hZ2UiOiJhc3NldHMvcHVibGljL2ltYWdlcy91cGxvYWRzL2RlZmF1bHRBZG1pbi5wbmciLCJ0b3RwU2VjcmV0IjoiIiwiaXNBY3RpdmUiOnRydWUsImNyZWF0ZWRBdCI6IjIwMjQtMDUtMDkgMDQ6NDM6NTIuMTQzICswMDowMCIsInVwZGF0ZWRBdCI6IjIwMjQtMDUtMDkgMDQ6NDM6NTIuMTQzICswMDowMCIsImRlbGV0ZWRBdCI6bnVsbH0sImlhdCI6MTcxNTIzMDIxMn0.DIHjVQcZ0g8xDaEwgGX8QOCQrYAMbc-T4YDGKzdRuk8CrA9K7Q-Rauv6LCCNB5itKTQPvgPUftD0KtTwUwcCMx3pUFlHr-C25bAhEIW2UYeNUfX-p8ZKJYHM1h4Fm3awq--IowCChKJ1aY2duwSphOS9aEiLwH_UPAeCDHOwDgU”
-	python FinDOR.py --url="http://localhost:3000/rest/basket/1" --bearer-token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MSwidXNlcm5hbWUiOiIiLCJlbWFpbCI6ImFkbWluQGp1aWNlLXNoLm9wIiwicGFzc3dvcmQiOiIwMTkyMDIzYTdiYmQ3MzI1MDUxNmYwNjlkZjE4YjUwMCIsInJvbGUiOiJhZG1pbiIsImRlbHV4ZVRva2VuIjoiIiwibGFzdExvZ2luSXAiOiIiLCJwcm9maWxlSW1hZ2UiOiJhc3NldHMvcHVibGljL2ltYWdlcy91cGxvYWRzL2RlZmF1bHRBZG1pbi5wbmciLCJ0b3RwU2VjcmV0IjoiIiwiaXNBY3RpdmUiOnRydWUsImNyZWF0ZWRBdCI6IjIwMjQtMDUtMDkgMDQ6NDM6NTIuMTQzICswMDowMCIsInVwZGF0ZWRBdCI6IjIwMjQtMDUtMDkgMDQ6NDM6NTIuMTQzICswMDowMCIsImRlbGV0ZWRBdCI6bnVsbH0sImlhdCI6MTcxNTIzMDIxMn0.DIHjVQcZ0g8xDaEwgGX8QOCQrYAMbc-T4YDGKzdRuk8CrA9K7Q-Rauv6LCCNB5itKTQPvgPUftD0KtTwUwcCMx3pUFlHr-C25bAhEIW2UYeNUfX-p8ZKJYHM1h4Fm3awq--IowCChKJ1aY2duwSphOS9aEiLwH_UPAeCDHOwDgU” –dump”1-22”
-	python FinDOR.py -f “C:\Users\MSI\Documents\Potential IDOR\potential_idor_request27.txt” --s specified-param=”userid”
-	python FinDOR.py -f “C:\Users\MSI\Documents\Potential IDOR\potential_idor_request30.txt” --s specified-param=”transactionid"

