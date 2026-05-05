# Beko Müşteri Memnuniyeti ve Şikayet Analizi (NLP)

Bu çalışma, **Şikayetvar** platformu üzerinden web scraping yöntemiyle toplanan **Beko** markasına ait müşteri geri bildirimlerini Doğal Dil İşleme (NLP) teknikleriyle analiz eden kapsamlı bir veri bilimi projesidir.

## Projenin Amacı ve Veri Kaynağı
Müşteri sesini (Voice of Customer) veriye dayalı bir şekilde anlamlandırmayı hedefleyen bu çalışmada şu temel esaslar benimsenmiştir:

*   **Veri Kaynağı:** Analizde kullanılan ham veriler, Türkiye'nin en büyük tüketici platformu olan `sikayetvar.com` adresinden scraping yöntemleriyle elde edilmiştir.
*   **Temel Hedef:** Şikayet metinlerinin içinde yatan asıl problemleri makine öğrenmesi algoritmalarıyla otomatik olarak tespit etmek. Yalnızca "kaç şikayet var?" sorusuna değil, "insanlar tam olarak neden şikayet ediyor?" sorusuna eyleme dönüştürülebilir (actionable) yanıtlar bulmak.
*   **Odak Çıktılar:** Markanın müşteri deneyimini iyileştirmesine yardımcı olmak adına; ürün bazlı kronik arızaları saptamak, hukuki risk (hakem heyeti, mahkeme vb.) taşıyan metinleri ayrıştırmak ve departman (çağrı merkezi, yetkili servis vb.) performanslarını metin üzerinden ölçümlemek.

---

## Canlı Pano (Dashboard)
Analiz sonuçlarını, oluşturduğumuz etkileşimli grafikler üzerinden incelemek için geliştirdiğimiz web uygulamasına buradan ulaşabilirsiniz:  
🔗 **[Beko NLP Dashboard'a Gitmek İçin Tıklayın](https://beko-customer-satisfaction.streamlit.app/)**

---

## 💡 Panodaki Temel Metrikler ve Çıktılar
Geliştirilen boru hattının (pipeline) sonuçları Streamlit panosunda şu başlıklar altında görselleştirilmiştir:
*   **Kategori ve Ürün Analizi:** Hangi ürün grubunda (beyaz eşya, küçük ev aletleri vb.) şikayetlerin daha yoğun olduğu.
*   **Konu Modelleme (Topic Modeling):** Scikit-learn üzerinden kurulan LDA modeli ile karmaşık metinlerin "servis gecikmesi", "yedek parça bekleme" gibi ana başlıklara otomatik kümelenmesi.
*   **Hukuki Risk Analizi:** Tüketicinin yasal yollara başvurma eğiliminde olduğu kritik vakaların önceliklendirilmesi.
*   **Çözüm ve Memnuniyet Skorları:** Şikayetin çözülme durumları ve süreç sonunda müşterinin markaya verdiği memnuniyet puanlarının dağılımı.
*   **Arıza ve Departman Kırılımı:** Şikayetlerin ağırlıklı olarak teknik bir arızadan mı, yoksa müşteri hizmetleri/servis davranışından mı kaynaklandığının tespiti.

---

## 🛠️ Kullanılan Teknolojiler
Projenin uçtan uca geliştirilmesi sürecinde kullanılan ana araçlar:
*   **Veri İşleme:** `pandas`, `numpy`
*   **Makine Öğrenmesi & NLP:** `scikit-learn` (LDA Modelleme), `joblib`
*   **Görselleştirme:** `plotly`, `matplotlib`
*   **Web Arayüzü:** `streamlit`
*   **Dosya/Veritabanı İşlemleri:** `SQLite`, `openpyxl`

---
## 📂 Proje Dizin Yapısı
Proje, sürdürülebilir ve temiz kod prensiplerine uygun, ETL ve Modelleme süreçlerinin ayrıştırıldığı modüler bir mimaride tasarlanmıştır:

```text
nlp/
├── app/                    # Streamlit web arayüzü ve asset dosyaları
├── data/                   # SQLite veritabanı (.db), raw (ham) ve işlenmiş NLP verileri
├── reports/                # Modelden çıkan ve panoyu besleyen metriklerin CSV dosyaları
├── scripts/                # Pipeline adımlarını (ETL, LDA, kural tabanlı analiz) tetikleyen çalıştırıcılar
├── src/                    # NLP temizleme, veritabanı yönetimi ve analiz için çekirdek kaynak kodları
├── .gitattributes          # LFS ayarları
├── requirements.txt        # Proje bağımlılıkları
└── README.md
