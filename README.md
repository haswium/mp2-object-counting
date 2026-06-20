# Mini Project 2 – Object Counting

## Nama

Hasna Widyaningrum

## NRP

5024241004

## Mata Kuliah

Pengolahan Citra dan Video

---

# Deskripsi

Mini Project 2 bertujuan untuk menghitung jumlah kendaraan pada citra aerial area parkir menggunakan teknik pengolahan citra digital tanpa menggunakan deep learning maupun model pre-trained. Pada proyek ini dilakukan tiga pendekatan berbeda yang mewakili materi yang telah dipelajari, yaitu:

1. Color-Based Detection (HSV Segmentation)
2. Edge-Based Detection (Canny Edge Detection)
3. Thresholding + Morphology + Connected Components

Tujuan utama proyek ini adalah mengeksplorasi kemampuan berbagai teknik pengolahan citra dalam melakukan object counting serta membandingkan kelebihan dan kekurangan masing-masing metode.

---

# Dataset

Input citra:

![Original](output/steps/00_original.png)

Citra merupakan foto aerial area parkir yang berisi sejumlah kendaraan dengan berbagai warna, ukuran, dan posisi parkir.

---

# Percobaan 1 – HSV Segmentation (Color-Based)

## Tujuan

Percobaan ini bertujuan mendeteksi kendaraan berdasarkan informasi warna menggunakan ruang warna HSV (Hue, Saturation, Value). Pendekatan ini dipilih karena HSV memisahkan informasi warna dan kecerahan sehingga diharapkan kendaraan dapat dibedakan dari latar belakang area parkir.

## Pipeline

```text
RGB → HSV → Threshold → Morphology → Connected Components → Counting
```

---

## Tahap 1 – Konversi RGB ke HSV

### Hue Channel

![Hue](output/steps/01_hue.png)

Kanal Hue merepresentasikan jenis warna pada citra. Nilai Hue digunakan untuk membedakan warna objek tanpa dipengaruhi oleh tingkat kecerahan.

### Saturation Channel

![Saturation](output/steps/02_saturation.png)

Kanal Saturation menunjukkan tingkat kejenuhan warna. Nilai yang tinggi menunjukkan warna yang lebih kuat, sedangkan nilai rendah menunjukkan warna yang mendekati abu-abu.

### Value Channel

![Value](output/steps/03_value.png)

Kanal Value merepresentasikan tingkat kecerahan piksel. Objek yang lebih terang akan memiliki nilai Value yang lebih tinggi dibandingkan area yang lebih gelap.

### Histogram HSV

![Histogram HSV](output/steps/04_histogram_hsv.png)

Histogram digunakan untuk melihat distribusi nilai piksel pada masing-masing kanal HSV. Informasi ini membantu memahami karakteristik citra sebelum dilakukan proses segmentasi.

### Analisis Tahap 1

Dari visualisasi HSV terlihat bahwa kanal Value memberikan kontras yang cukup baik antara kendaraan dan aspal. Kanal Hue juga menunjukkan perbedaan warna antar objek, sedangkan Saturation cenderung kurang memberikan pemisahan yang jelas pada citra ini.

---

## Tahap 2 – Thresholding pada Kanal HSV

### Hue Mask

![Hue Mask](output/steps/05_hue_mask.png)

Hasil thresholding pada kanal Hue.

### Saturation Mask

![Saturation Mask](output/steps/06_saturation_mask.png)

Hasil thresholding pada kanal Saturation.

### Value Mask

![Value Mask](output/steps/07_value_mask.png)

Hasil thresholding pada kanal Value.

### Analisis Tahap 2

Thresholding dilakukan untuk memisahkan piksel yang dianggap sebagai objek dari latar belakang. Dari ketiga kanal, terlihat bahwa setiap kanal memberikan hasil segmentasi yang berbeda. Kanal Value cenderung mempertahankan objek terang, sedangkan Hue dan Saturation memberikan hasil yang lebih bervariasi tergantung warna kendaraan.

---

## Tahap 3 – HSV Segmentation

![HSV Segmentation](output/steps/08_hsv_segmentation.png)

Segmentasi dilakukan menggunakan fungsi `cv2.inRange()` dengan rentang HSV tertentu. Piksel yang memenuhi rentang tersebut akan dianggap sebagai objek, sedangkan piksel lainnya dianggap sebagai latar belakang.

### Analisis Tahap 3

Pada tahap ini sebagian besar kendaraan berwarna terang berhasil dipisahkan dari area aspal. Namun masih terdapat area non-kendaraan yang ikut tersegmentasi dan beberapa kendaraan berwarna gelap yang tidak terdeteksi dengan baik.

---

## Tahap 4 – Morphology

![Morphology Result](output/steps/09_hsv_morphology.png)

Operasi Morphological Opening digunakan untuk menghilangkan noise kecil, sedangkan Morphological Closing digunakan untuk menyambungkan bagian objek yang terputus.

### Analisis Tahap 4

Morphology membantu membersihkan hasil segmentasi sehingga objek menjadi lebih jelas dan lebih mudah dihitung. Beberapa noise berhasil dihilangkan, namun masih terdapat objek yang saling menempel dan beberapa kendaraan yang hanya tersegmentasi sebagian.

---

## Tahap 5 – Connected Components dan Counting

![HSV Bounding Box](output/steps/10_hsv_bounding_box.png)

Connected Components digunakan untuk mencari komponen yang saling terhubung pada hasil segmentasi. Komponen yang memiliki luas sesuai kriteria dianggap sebagai objek kendaraan dan diberikan bounding box.

### Hasil

Jumlah objek terdeteksi:

```text
31
```

### Analisis Tahap 5

Metode HSV menghasilkan jumlah deteksi yang paling mendekati jumlah kendaraan pada citra. Akan tetapi, hasil deteksi belum sepenuhnya akurat. Beberapa kendaraan hanya terdeteksi sebagian sehingga bounding box tidak mencakup seluruh kendaraan. Selain itu terdapat kendaraan yang berdekatan dan tergabung menjadi satu komponen besar. Oleh karena itu jumlah objek yang terdeteksi tidak selalu sama dengan jumlah kendaraan sebenarnya.

---

## Kesimpulan Percobaan 1

HSV Segmentation mampu memanfaatkan informasi warna untuk membedakan kendaraan dari latar belakang. Dibandingkan metode lain yang diuji pada mini project ini, pendekatan HSV menghasilkan jumlah deteksi yang paling mendekati kondisi sebenarnya. Namun metode ini masih sensitif terhadap variasi warna kendaraan dan kondisi pencahayaan sehingga belum mampu mendeteksi seluruh kendaraan secara sempurna.

# Percobaan 2 – Edge-Based Detection

## Tujuan

Mendeteksi kendaraan berdasarkan informasi tepi (edge) pada citra.

## Pipeline

RGB Image
→ Grayscale
→ Gaussian Blur
→ Canny Edge Detection
→ Dilation
→ Contour Detection
→ Bounding Box
→ Counting

## Visualisasi Tahapan

* 11_grayscale.png
* 12_blur.png
* 13_canny.png
* 14_dilation.png
* 15_edge_bounding_box.png

## Analisis

Metode ini berhasil menampilkan bentuk kendaraan dengan cukup jelas pada hasil Canny Edge Detection. Garis-garis tepi kendaraan terlihat lebih menonjol dibandingkan metode HSV.

Namun proses counting dilakukan menggunakan contour yang membutuhkan area tertutup. Banyak kendaraan hanya menghasilkan kumpulan garis tepi tanpa membentuk region yang lengkap sehingga tidak dapat dihitung sebagai satu objek.

Akibatnya jumlah kendaraan yang berhasil dihitung jauh lebih sedikit dibandingkan kondisi sebenarnya.

## Hasil

Jumlah objek terdeteksi:

```text
Edge = 13
```

Metode ini mengalami undercounting karena banyak kendaraan tidak membentuk objek tertutup yang dapat dihitung.

---

# Percobaan 3 – Thresholding + Morphology + Connected Components

## Tujuan

Mendeteksi kendaraan menggunakan segmentasi berbasis intensitas piksel.

## Pipeline

RGB Image
→ Grayscale
→ Otsu Thresholding
→ Opening
→ Closing
→ Connected Components
→ Filtering Area dan Aspect Ratio
→ Bounding Box
→ Counting

## Visualisasi Tahapan

* 16_gray_threshold.png
* 17_otsu_threshold.png
* 18_opening.png
* 19_closing.png
* 20_threshold_bounding_box.png

## Analisis

Thresholding Otsu berhasil memisahkan area terang dan gelap secara otomatis. Setelah dilakukan Opening dan Closing, region yang dihasilkan menjadi lebih jelas dan dapat diproses menggunakan Connected Components.

Namun pada citra ini banyak kendaraan yang memiliki kombinasi area terang dan gelap sehingga satu kendaraan sering terpecah menjadi beberapa komponen berbeda. Selain itu marka parkir dan objek terang lainnya juga ikut tersegmentasi.

Akibatnya jumlah objek yang terdeteksi menjadi jauh lebih besar dibandingkan jumlah kendaraan sebenarnya.

## Hasil

Jumlah objek terdeteksi:

```text
Threshold = 47
```

Metode ini mengalami overcounting karena satu kendaraan dapat menghasilkan beberapa komponen terpisah.

---

# Perbandingan Hasil

| Metode           | Jumlah Deteksi |
| ---------------- | -------------- |
| HSV Segmentation | 31             |
| Edge Detection   | 13             |
| Thresholding     | 47             |

---

# Kesimpulan

Tiga pendekatan berbeda telah diuji untuk melakukan object counting pada citra area parkir.

Metode HSV Segmentation menghasilkan jumlah deteksi yang paling mendekati kondisi sebenarnya, meskipun masih terdapat kesalahan berupa kendaraan yang hanya terdeteksi sebagian atau beberapa kendaraan yang tergabung menjadi satu komponen.

Metode Edge Detection mampu menampilkan bentuk kendaraan dengan baik, namun kurang efektif untuk counting karena banyak kendaraan tidak membentuk region tertutup.

Metode Thresholding menghasilkan jumlah deteksi paling besar karena satu kendaraan dapat terpecah menjadi beberapa komponen dan marka parkir ikut tersegmentasi.

Berdasarkan hasil eksperimen, metode HSV Segmentation memberikan performa terbaik pada dataset yang digunakan dalam mini project ini.

---

# Cara Menjalankan

```bash
python counting.py
```

Output hasil deteksi akan disimpan pada folder:

```text
output/
```

Sedangkan seluruh tahapan proses dapat dilihat pada folder:

```text
output/steps/
```
