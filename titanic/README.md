# Titanic - Hayatta Kalma Tahmini

Titanic veri seti üzerinde keşifçi veri analizi (EDA) ve makine öğrenmesi ile yolcuların hayatta kalma durumunu tahmin eden bir çalışmadır.

## Veri Seti

- **Kaynak:** `titanic.csv` — 891 yolcu, 11 değişken
- **Hedef Değişken:** `Survived` (0 = Hayatta Kalmadı, 1 = Hayatta Kaldı)

| Sütun | Açıklama |
|---|---|
| Pclass | Bilet sınıfı (1 = Üst, 2 = Orta, 3 = Alt) |
| Sex | Cinsiyet |
| Age | Yaş |
| SibSp | Gemideki kardeş/eş sayısı |
| Parch | Gemideki ebeveyn/çocuk sayısı |
| Fare | Bilet ücreti |
| Embarked | Biniş limanı (C = Cherbourg, Q = Queenstown, S = Southampton) |

**Eksik Veriler:** Age (%19.9), Cabin (%77.1), Embarked (%0.2)

## Kullanılan Kütüphaneler

`pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `scikit-learn`, `lazypredict`, `lightgbm`, `xgboost`

## Keşifçi Veri Analizi (EDA) — Önemli Bulgular

### Genel Dağılımlar
- Yolcuların **%61.6'sı hayatta kalmadı**.
- **%64.8'i erkek**, %35.2'si kadın.
- Neredeyse yarısı **3. sınıf** yolcu (%55.1).
- Büyük çoğunluk **Southampton** limanından binmiş (%72.3).

### Hayatta Kalma Üzerindeki Etkiler

| Değişken | Bulgu |
|---|---|
| **Cinsiyet** | Kadınların kurtulma oranı çok daha yüksek. Hayatta kalanların **%68.4'ü kadın**. |
| **Bilet Sınıfı** | 1. ve 2. sınıfların neredeyse yarısı kurtulurken, 3. sınıfların çeyreği bile kurtulamamış. |
| **Yaş** | Çocukların (0-12) kurtulma oranı en yüksek. 2. sınıftaki hayatta kalan erkeklerin tamamı 0-15 yaş arası. |
| **Ücret** | Yüksek ücret ödeyenlerin hayatta kalma oranı belirgin şekilde daha yüksek. |
| **Yalnızlık** | Ailesiyle/grubuyla binenlerin hayatta kalma oranı, yalnız binenlere göre daha yüksek. |
| **Liman** | Cherbourg'dan binenlerde hayatta kalma yüksek, ancak asıl ilişki: **Liman → Pclass → Hayatta Kalma** (dolaylı). |

### Korelasyon Özeti (Survived ile)

| Değişken | Skor | Yorum |
|---|---:|---|
| Fare | +0.262 | Yüksek ücret → daha yüksek hayatta kalma |
| Is_Alone | −0.205 | Yalnız olanlar daha az hayatta kaldı |
| Pclass | −0.334 | Alt sınıf (3) hayatta kalmayı azaltır |

## Feature Engineering

- **AgeGroup:** Yaş 5 kategoriye ayrıldı (0-12, 13-20, 21-36, 37-57, 58-80)
- **Fare_Category:** Ücret, çeyreklik gruplara (qcut) bölündü (1-4)
- **Is_Alone:** SibSp + Parch = 0 ise yalnız (1), değilse (0)

## Veri Ön İşleme

- **Fare:** Uç aykırı değer temizlendi
- **Age eksikleri:** Pclass ve Sex gruplarının ortalamasıyla dolduruldu (train'den hesaplanıp test'e uygulandı. Böylece veri sızıntısı önlendi.)
- **Embarked eksikleri:** Mode (en sık liman) ile dolduruldu
- **Cabin:** Yüksek eksiklik nedeniyle çıkarıldı
- **Sex:** Label Encoding, **Embarked:** One-Hot Encoding
- **Ölçeklendirme:** Fare → RobustScaler, Age/SibSp/Parch → StandardScaler

## Model Sonuçları

LazyPredict ile hızlı bir model taraması yapıldıktan sonra en iyi 3 model üzerinde **RandomizedSearchCV** ile hiperparametre optimizasyonu uygulandı:

| Model | CV Score | Train Acc | Test Acc |
|---|---:|---:|---:|
| LGBMClassifier | 0.8380 | 0.8944 | **0.8539** |
| XGBClassifier | 0.8507 | 0.9141 | **0.8539** |
| RandomForestClassifier | 0.8408 | 0.9085 | 0.8427 |

**Seçilen Model: LGBMClassifier** — Test doğruluğu XGBClassifier ile eşit olmasına rağmen, train-test farkının daha düşük olması (daha az overfitting) ve hız avantajı nedeniyle tercih edilmiştir.

## 📊 Model Performansı ve Sonuçlar

LightGBM modeli kullanılarak elde edilen final test sonuçları aşağıda özetlenmiştir. Model, oldukça kısa bir sürede yüksek bir doğruluk oranına ulaşmıştır.

### Genel Metrikler

| Metrik | Değer |
| :--- | :--- |
| **Genel Doğruluk Oranı (Accuracy)** | %85.39 |
| **Eğitim ve Tahmin Süresi** | 0.5104 Saniye |

---

### Karmaşıklık Matrisi (Confusion Matrix)

Modelin test verisindeki 178 yolcu üzerindeki tahmin başarı ve hata dağılımı:

| | Tahmin Edilen: Hayatta Kalmadı (0) | Tahmin Edilen: Hayatta Kaldı (1) |
| :--- | :--- | :--- |
| **Gerçek: Hayatta Kalmadı (0)** | 97 *(Doğru Negatif)* | 9 *(Yanlış Pozitif)* |
| **Gerçek: Hayatta Kaldı (1)** | 17 *(Yanlış Negatif)* | 55 *(Doğru Pozitif)* |

---

### Sınıflandırma Raporu (Classification Report)

| Sınıf | Precision (Kesinlik) | Recall (Duyarlılık) | F1-Score | Support (Kişi Sayısı) |
| :--- | :--- | :--- | :--- | :--- |
| **0 (Hayatta Kalmadı)** | 0.85 | 0.92 | 0.88 | 106 |
| **1 (Hayatta Kaldı)** | 0.86 | 0.76 | 0.81 | 72 |
| **Accuracy (Genel)** | | | **0.85** | **178** |
| **Macro Avg** | 0.86 | 0.84 | 0.85 | 178 |
| **Weighted Avg** | 0.85 | 0.85 | 0.85 | 178 |

<img width="989" height="590" alt="image" src="https://github.com/user-attachments/assets/e0998333-7ed5-4bb3-a7b2-ac9cf28d058e" />

