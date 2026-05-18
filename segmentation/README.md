# BEKO Ürün Segmentasyonu ve Kümeleme Analizi

## Proje Özeti

Bu çalışma, Beko cihazlarını teknolojik donanım, fiyat ve müşteri ilgisine (popülarite/favori) göre analiz eden yapay zekâ tabanlı bir segmentasyon projesidir.

Web scraping ile toplanan veriler temizlenmiş ve 647 ana ürün K-Means algoritması ile 6 segmente ayrılmıştır.

Geleneksel yöntemlerden farklı olarak, kategori bazlı ölçeklendirme (Robust Scaler) kullanılarak ürünlerin gerçek "Fiyat/Performans" haritası çıkarılmıştır.

## Teknik Mimari

Sistem dört ana aşamadan oluşan bir veri bilimi hattı üzerine kurulmuştur:

* **Veri Toplama:** Python ve Selenium ile web scraping otomasyonu.
* **Ön İşleme:** Birim temizliği ve manuel mantıksal skorlama.
* **Analitik:** Robust Scaler, logaritmik dönüşüm ve K-Means Kümeleme.
* **Sunum:** Streamlit tabanlı interaktif dashboard.

## Analitik Çıktılar ve Segmente Özel Aksiyon Planları

Algoritma, ürünleri teknoloji, fiyat ve müşteri popülaritesine göre 6 ana stratejik gruba ayırmaktadır:

**1. Gizli Kalmış Potansiyel (Keşfedilmemiş Teknoloji)**

* Yüksek teknoloji, düşük fiyat, düşük popülarite.
* **Strateji:** Görünürlüğü düşük ancak potansiyeli yüksek olan bu ürünler için reklam bütçeleri artırılmalı ve e-ticaret platformunda öne çıkarılmalıdır. Ürün görselleri ve açıklamaları iyileştirilerek cazibesi artırılmalıdır.

**2. Fırsat / Yıldız Ürünler**

* Yüksek teknoloji, düşük fiyat, yüksek popülarite.
* **Strateji:** Satış dönüşüm oranı en yüksek olan amiral gemisi ürünlerdir. Kampanya ve indirim dönemlerinde ana sayfada ve reklamlarda doğrudan vitrine konumlandırılmalıdır.

**3. Premium / Lüks**

* Yüksek teknoloji, yüksek fiyat, değişken popülarite.
* **Strateji:** Kalite ve statü odaklı niş bir kitleye hitap eder. VIP müşteri hizmetleri ve özel hedef kitleli premium dijital reklamlarla desteklenmelidir.

**4. Popüler Ekonomik**

* Düşük teknoloji, düşük fiyat, yüksek popülarite.
* **Strateji:** Sürümden kazanılan ana akım ürünlerdir. Stoklar her zaman dolu tutulmalı ve hacimli satışlar için paket kampanyalarla desteklenmelidir.

**5. Niş / Aşırı Fiyatlandırılmış**

* Düşük teknoloji, yüksek fiyat, değişken popülarite.
* **Strateji:** Donanımına kıyasla fiyatı yüksek kalan ürünlerdir. Fiyat/performans optimizasyonu yapılmalı veya yaşam döngüsünü tamamladıysa üretimden çekilmelidir.

**6. Düşük Segment (Giriş Seviyesi)**

* Düşük teknoloji, düşük fiyat, düşük popülarite.
* **Strateji:** Temel ihtiyaçları karşılayan sade cihazlardır. Reklam bütçesi harcamak yerine, fiyat hassasiyeti yüksek kitleler için temel görünürlük çalışmaları yapılmalı ve stok verimliliği odaklı bir süreç izlenmelidir.

## İş Birimleri İçin Katma Değer

* **Pazarlama ve E-Ticaret:** İnaktif stokları nakde dönüştürmek için reklam bütçesini doğru yönlendirir.
* **Fiyatlandırma:** Fiyatı donanımına göre yüksek kalan ürünleri tespit ederek dinamik indirim stratejileri sağlar.
* **Ar-Ge:** Müşteri ilgisine göre yeni ürünlerin donanım gereksinimlerini öngörür.
* **Tedarik Zinciri:** Satış hızı yüksek segmentlere odaklanarak üretim ve lojistik verimliliğini artırır.

## Gelecek Vizyonu

* Selenium botları ile anlık fiyat ve rakip takibi yapılması.
* Doğrudan satış verilerinin entegre edilmesi.

---

**Geliştiren:** Betül Tuba Gümüş

**Tarih:** Mayıs 2026
