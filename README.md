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

```text
input/parking.jpg
```

Citra merupakan foto aerial area parkir yang berisi sejumlah kendaraan dengan berbagai warna, ukuran, dan posisi parkir.

---

# Percobaan 1 – HSV Segmentation (Color-Based)

## Tujuan

Memisahkan objek kendaraan dari latar belakang menggunakan informasi warna pada ruang warna HSV.

## Pipeline

RGB Image
→ HSV Conversion
→ Analisis H, S, V
→ HSV Thresholding
→ Morphological Opening
→ Morphological Closing
→ Connected Components
→ Bounding Box
→ Counting

## Visualisasi Tahapan

* 01_hue.png
* 02_saturation.png
* 03_value.png
* 04_histogram_hsv.png
* 05_hue_mask.png
* 06_saturation_mask.png
* 07_value_mask.png
* 08_hsv_segmentation.png
* 09_hsv_morphology.png
* 10_hsv_bounding_box.png

## Analisis

Konversi ke ruang warna HSV dilakukan untuk memisahkan informasi warna dan intensitas. Histogram H, S, dan V digunakan untuk memahami distribusi piksel pada citra sebelum dilakukan segmentasi.

Segmentasi HSV mampu mendeteksi sebagian besar objek berwarna terang yang memiliki kontras cukup tinggi terhadap aspal. Setelah dilakukan operasi Opening dan Closing, noise berukuran kecil dapat dikurangi sehingga objek menjadi lebih mudah dihitung menggunakan Connected Components.

Namun hasil deteksi masih belum sempurna. Beberapa kendaraan hanya terdeteksi sebagian, misalnya hanya bagian atap atau kap kendaraan. Selain itu terdapat kendaraan yang saling berdekatan sehingga tergabung menjadi satu komponen besar. Oleh karena itu jumlah objek yang terdeteksi tidak selalu merepresentasikan jumlah kendaraan sebenarnya secara akurat.

## Hasil

Jumlah objek terdeteksi:

```text
HSV = 31
```

Metode ini memberikan hasil yang paling mendekati jumlah kendaraan pada citra dibandingkan dua metode lainnya.

---

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
