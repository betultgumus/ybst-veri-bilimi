# Titanic Veri Analizi ve Hayatta Kalma Tahmini

Bu depo, `titanic.csv` veri seti üzerinde gerçekleştirilen uçtan uca keşifçi veri analizi (EDA), özellik mühendisliği (feature engineering) ve makine öğrenmesi süreçlerini içermektedir. Projenin temel amacı, yolcuların demografik ve bilet bilgilerini kullanarak hayatta kalma durumlarını tahmin eden optimize edilmiş bir sınıflandırma modeli geliştirmektir.

## Proje Özeti

- **Veri Kaynağı:** `titanic.csv`
- **Gözlem Sayısı:** 891
- **Hedef Değişken:** `Survived` (0 = Hayatta Kalmadı, 1 = Hayatta Kaldı)
- **Proje İş Akışı:** Keşifçi Veri Analizi (EDA) -> Özellik Mühendisliği -> Veri Ön İşleme -> Modelleme -> Hiperparametre Optimizasyonu

## Keşifçi Veri Analizi (EDA) Bulguları

Veri seti üzerinde yapılan incelemeler ve görselleştirmeler sonucunda elde edilen temel bulgular aşağıda özetlenmiştir:

- **Eksik Veri Yönetimi:** `Cabin` değişkeni çok yüksek oranda eksik değere sahip olduğu için modelleme aşamasındaki etkisi sınırlı görülmüştür. `Age` ve `Embarked` değişkenlerindeki eksiklikler veri yapısına uygun stratejilerle doldurulmuştur.
- **Hayatta Kalma Belirleyicileri:** Cinsiyet (`Sex`), bilet sınıfı (`Pclass`), bilet ücreti (`Fare`) ve yaş (`Age`), hayatta kalma oranı üzerinde en yüksek istatistiksel etkiye sahip değişkenlerdir.
- **Liman Etkisi:** En çok biniş yapılan liman Southampton'dır. Ancak biniş limanının (`Embarked`) hayatta kalma üzerindeki etkisinin doğrudan değil, yolcuların bilet sınıfı (`Pclass`) dağılımı üzerinden dolaylı bir etki yarattığı saptanmıştır.
- **Aykırı Değer (Outlier) Analizi:** `Fare` ve `Age` dağılımlarında sağa çarpıklık gözlemlenmiştir. `Fare` değişkenindeki aşırı uç değerlerin `Ticket` değişkeniyle bağlantısı tespit edilmiş ve aykırı değerler azaltılmıştır.

## Özellik Mühendisliği (Feature Engineering)

Model performansını artırmak amacıyla mevcut verilerden yeni açıklayıcı değişkenler türetilmiştir:

- **`AgeGroup`:** Yaş değişkeni demografik kırılımları daha iyi yansıtması için 5 farklı kategoriye ayrılmıştır (`0-12`, `13-20`, `21-36`, `37-57`, `58-80`).
- **`Fare_Category`:** Ücret dağılımındaki çarpıklığı gidermek için `Fare` değişkeni çeyreklik dilimlere (qcut) bölünmüştür.
- **`Is_Alone`:** Yolcunun beraberinde aile üyesi (kardeş/eş veya ebeveyn/çocuk) olup olmadığını belirten mantıksal bir değişken oluşturulmuştur (`SibSp + Parch == 0` ise 1, aksi halde 0).

## Veri Ön İşleme

Modelin eğitimi öncesinde uygulanan dönüşüm ve standardizasyon adımları:

- **Eksik Değer Doldurma (Imputation):**
  - `Embarked`: Eğitim setindeki en sık tekrar eden değer (mod) ile doldurulmuştur.
  - `Age`: Tek bir sabit ortalama yerine, eğitim setindeki `Pclass` ve `Sex` gruplarının kırılımına göre elde edilen ortalamalar kullanılarak daha hassas bir doldurma işlemi uygulanmıştır.
- **Kategorik Kodlama (Encoding):** `Sex` değişkeni için Label Encoding, `Embarked` değişkeni için One-Hot Encoding uygulanmıştır.
- **Ölçeklendirme (Scaling):** Aykırı değerlere karşı daha dirençli olması amacıyla `Fare` değişkenine RobustScaler; `Age`, `SibSp` ve `Parch` değişkenlerine ise StandardScaler uygulanmıştır.

## Modelleme ve Seçim

Modelleme aşamasında öncelikle `LazyClassifier` ile geniş çaplı bir algoritma taraması yapılmış, ardından potansiyeli yüksek modeller üzerinde `RandomizedSearchCV` kullanılarak hiperparametre optimizasyonu gerçekleştirilmiştir. Analizler sonucunda nihai tahminleyici olarak **LGBMClassifier** seçilmiştir.

LGBM modelinin test seti üzerindeki genel performans değerlendirmesi aşağıda sunulmuştur:

- **Eğitim ve Tahmin Süresi:** 0.2925 saniye
- **Doğruluk (Accuracy):** 0.8539

**Karmaşıklık Matrisi (Confusion Matrix):**

| | Tahmin: 0 (Hayatta Kalmadı) | Tahmin: 1 (Hayatta Kaldı) |
|:---|---:|---:|
| **Gerçek: 0 (Hayatta Kalmadı)** | 97 | 9 |
| **Gerçek: 1 (Hayatta Kaldı)** | 17 | 55 |

**Sınıflandırma Raporu (Classification Report):**

| Sınıf | Precision | Recall | F1-Score | Support |
|:---|---:|---:|---:|---:|
| 0 (Hayatta Kalmadı) | 0.85 | 0.92 | 0.88 | 106 |
| 1 (Hayatta Kaldı) | 0.86 | 0.76 | 0.81 | 72 |
| **Accuracy** | | | **0.85** | 178 |
| **Macro Avg** | 0.86 | 0.84 | 0.85 | 178 |
| **Weighted Avg** | 0.85 | 0.85 | 0.85 | 178 |

## Sonuç

  Seçilen LGBM modeli ile veri seti üzerinde %85.39 test doğruluğuna ulaşılmış ve güçlü bir taban (baseline) model oluşturulmuştur. Özellik önem dereceleri incelendiğinde; ücret (`Fare`) ve yaş (`Age`) hayatta kalma tahminindeki en kritik belirleyiciler olduğu analitik olarak doğrulanmıştır.
