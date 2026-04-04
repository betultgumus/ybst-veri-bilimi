# GSS Veri Analizi Projesi

<p align="left">
  <img src="https://img.shields.io/badge/Notebook-Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter">
  <img src="https://img.shields.io/badge/Python-Data%20Analysis-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Focus-Health%20Income%20Education-2E7D32?style=for-the-badge" alt="Focus">
</p>

Bu klasor, GSS verisi uzerinde yapilan kesifsel veri analizi (EDA), iliski analizi ve yonetsel yorum calismalarini icerir. Odak nokta, gelir, egitim, saglik ve finansal memnuniyet degiskenlerinin birlikte nasil hareket ettigini ortaya koyarak karar destek icgorusleri uretmektir.

---

## Icerik Haritasi

- [Proje Amaci](#proje-amaci)
- [Veri Seti](#veri-seti)
- [Notebook Icerigi](#notebook-icerigi)
- [Uretilen Ana Gorseller](#uretilen-ana-gorseller)
- [Temel Bulgular](#temel-bulgular)
- [Yonetimsel Cikarimlar](#yonetimsel-cikarimlar-ybs-perspektifi)
- [Kullanilan Teknolojiler](#kullanilan-teknolojiler)
- [Calistirma](#calistirma)
- [Not](#not)

---

## Proje Amaci

| Hedef | Aciklama |
|---|---|
| Veri Kalitesi | Eksik veri ve aykiri degerleri inceleyip analize uygun bir taban kurmak |
| Iliski Analizi | income, educ, health, satfin degiskenleri arasindaki baglantilari olceklendirmek |
| Trend Analizi | Yillara gore gelir-egitim makasinin acilip acilmadigini gozlemlemek |
| Karar Destegi | Banka ve kamu tarafi icin uygulanabilir YBS cikarimlari uretmek |

## Veri Seti

| Alan | Bilgi |
|---|---|
| Dosya | gss_2010_ve_sonrasi.csv |
| Ana Degiskenler | year, educ, income, health, satfin, sex, race |
| On Isleme Karari | natfare kolonu yuksek eksiklik nedeniyle analizden cikarildi |

## Notebook Icerigi

Ana analizler [gss.ipynb](gss.ipynb) dosyasinda yapilmistir.

1. Paket kurulumu ve veri yukleme
2. Tip donusumleri ve temel veri dogrulama
3. Eksik veri analizi
4. Sayisal degiskenlerde aykiri deger incelemesi
5. Gelir-finansal memnuniyet iliskisi (scatter, regplot, boxplot)
6. Saglik-finansal memnuniyet crosstab heatmap analizi
7. Egitim ve gelirin saglik uzerindeki etkisi (heatmap tabanli segment analizi)
8. Yillara gore ortalama gelir ve egitim cizgi grafikleri
9. Normalize edilmis gelir-egitim makasi analizi

## Uretilen Ana Gorseller

- Health ve Satfin Crosstab Heatmap
- Income Band - Health Crosstab Heatmap
- Educ Band - Health Crosstab Heatmap
- Egitim x Gelir: Kotu Saglik Riski Heatmap
- Yillara Gore Ortalama Gelir ve Egitim Seviyesi (Line Plot)
- Normalize Edilmis Gelir-Egitim Makasi (Line Plot)

## Temel Bulgular

> Saglik durumu kotulestikce dusuk finansal memnuniyet oraninin arttigi gorulmektedir.

> Gelir ve egitim seviyeleri yukseldikce kotu saglik oranlari genel olarak azalmaktadir.

> Yuksek riskli segmentler, dusuk egitim ve dusuk gelir kombinasyonlarinda yogunlasmaktadir.

> Gelir-egitim makasi tek yonlu degil; yillar icinde dalgali bir yapi gostermektedir. Bu nedenle periyodik politika ve urun ayari gereklidir.

## Yonetimsel Cikarimlar (YBS Perspektifi)

### Banka Kredi Politikasi

- Kredi degerlemesinde sadece gelir degil, egitim-gelir uyumu da ikinci bir risk gostergesi olarak kullanilmalidir.
- Segmentasyon modelinde dusuk egitim-dusuk gelir grubu icin daha dikkatli limit, fiyatlama ve erken uyari kurallari tanimlanabilir.
- Dijital kanallarda riskli segmentlere finansal okuryazarlik ve butce yonetimi odakli mikro urunler sunulabilir.

### Kamu Sosyal Yardim Stratejisi

- Sosyal yardim programlari, dusuk gelir ve dusuk egitim segmentinde daha hedefli tasarlanmalidir.
- Saglik riski yuksek segmentlerde dijital erisim destekleri (online basvuru, mobil takip, yonlendirme) onceliklendirilebilir.
- Yillik trend takibi ile bolgesel veya demografik alt gruplar icin dinamik yardim planlamasi yapilabilir.

## Kullanilan Teknolojiler

| Katman | Teknoloji |
|---|---|
| Programlama | Python |
| Veri Isleme | pandas |
| Gorsellestirme | matplotlib, seaborn |
| Ortam | Jupyter Notebook |

## Calistirma

1. Gerekli paketleri yukleyin: pandas, matplotlib, seaborn
2. [gss.ipynb](gss.ipynb) dosyasini acin
3. Hucreleri sirayla calistirarak analiz ve grafik ciktilarini uretin

## Not

Bu calisma, karar destek amacli kesifsel bir analizdir. Operasyonel kararlar icin bir sonraki asamada degisken muhendisligi, istatistiksel dogrulama ve tahmin performansi olcumleri ile genisletilmesi onerilir.
