import pandas as pd
# import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re

# CSV dosyasını oku
csv_file = 'sikayet_var_urun_linki.csv'
df = pd.read_csv(csv_file)

# Ürün linklerini ve bilgilerini al
urun_linkleri = df['Urun Linki'].unique()

print(f"Toplam {len(urun_linkleri)} adet ürün bulundu.\n")

# Sonuçları saklamak için liste
sonuclar = []

# CSV dosyası için header tanımla
csv_file_out = 'sikayet_var_yorum_linki.csv'
is_first_write = True
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# Şikayetvar'ın bot sanmasını engellemek için standart bir tarayıcı kimliği ekliyoruz
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36')

# Standart sürücüyü başlatıyoruz (version_main vs. gerek yok)
driver = webdriver.Chrome(options=options)

try:
    for idx, link in enumerate(urun_linkleri, 1):
        try:
            print(f"[{idx}/{len(urun_linkleri)}] Ziyaret ediliyor: {link}")
            
            # CSV'den ilgili ürün bilgisini al
            urun_bilgisi = df[df['Urun Linki'] == link].iloc[0]
            urun_adi = urun_bilgisi['Urun Adi']
            
            # Linke git
            driver.get(link)
            
            # Sayfanın yüklenmesi için bekle
            time.sleep(3)
            
            # Ekstra veriler için değişkenleri başlat
            urun_adi_cekilen = ""
            urun_puan_yuzdelik = ""
            anahtar_etiket = ""
            yorum_linkleri_str = ""
            sikayet_sayisi = 0

            # 1. urun_adi çek
            try:
                elem_h1 = driver.find_element(By.CSS_SELECTOR, "h1.model-name")
                urun_adi_cekilen = elem_h1.text.strip()
            except:
                pass

            # 2. urun_puan_yuzdelik çek
            try:
                # <div class="rate-num"><span>40</span><span>100</span></div> yapısından ilk span'ı (örn: 40) çeker
                elem_puan = driver.find_element(By.CSS_SELECTOR, "div.rate-num span:first-child")
                urun_puan_yuzdelik = elem_puan.text.strip()
            except:
                pass

            # 3. anahtar_etiket çek (yetkili servis vs.)
            try:
                elem_etiketler = driver.find_elements(By.CSS_SELECTOR, "a.search-item")
                anahtar_etiket = ", ".join([el.text.strip() for el in elem_etiketler if el.text.strip()])
            except:
                pass

            # 4. yorum_linki çek (sayfadaki tüm şikayet linklerini virgülle ayırarak al)
            try:
                # 'complaint-description' sınıfına sahip tüm a etiketlerinden href'leri çekiyoruz
                elem_yorumlar = driver.find_elements(By.CSS_SELECTOR, "a.complaint-description")
                yorum_linkleri_str = ", ".join([el.get_attribute("href") for el in elem_yorumlar if el.get_attribute("href")])
            except:
                pass

            # 5. Şikayet sayısını içeren elemanı bul
            try:
                complaint_element = driver.find_element(By.CLASS_NAME, "complaint-count")
                complaint_text = complaint_element.text
                match = re.search(r'(\d+)', complaint_text)
                if match:
                    sikayet_sayisi = int(match.group(1))
                    print(f"   ✓ Sayfadan: {urun_adi_cekilen} | Puan: {urun_puan_yuzdelik} | Şikayet: {sikayet_sayisi}")
                else:
                    print(f"   ✗ Şikayet sayısı bulunamadı: {complaint_text}")
            except Exception as e:
                print(f"   ✗ Hata (şikayet sayısı): {str(e)}")
            
            # Sonucu kaydet
            row_data = {
                'Urun_Adi_CSV': urun_adi,
                'Urun_Linki': link,
                'Urun_Adi_Sayfadan': urun_adi_cekilen,
                'Urun_Puan_Yuzdelik': urun_puan_yuzdelik,
                'Anahtar_Etiketler': anahtar_etiket,
                'Yorum_Linkleri': yorum_linkleri_str,
                'Sikayet_Sayisi': sikayet_sayisi
            }
            sonuclar.append(row_data)
            
            # Hemen CSV'ye kaydet
            sonuc_df_temp = pd.DataFrame([row_data])
            sonuc_df_temp.to_csv(csv_file_out, mode='a', header=is_first_write, 
                                index=False, encoding='utf-8-sig')
            is_first_write = False
            
        except Exception as e:
            print(f"   ✗ Link ziyareti hatası: {str(e)}")
            hata_row = {
                'Urun_Adi_CSV': '',
                'Urun_Linki': link,
                'Urun_Adi_Sayfadan': '',
                'Urun_Puan_Yuzdelik': '',
                'Anahtar_Etiketler': '',
                'Yorum_Linkleri': '',
                'Sikayet_Sayisi': None
            }
            sonuclar.append(hata_row)
            
            # Hata kaydını da CSV'ye kaydet
            sonuc_df_temp = pd.DataFrame([hata_row])
            sonuc_df_temp.to_csv(csv_file_out, mode='a', header=is_first_write, 
                                index=False, encoding='utf-8-sig')
            is_first_write = False
        
        # Rate limiting
        time.sleep(2)

finally:
    driver.quit()

# Sonuçları DataFrame'e dönüştür (özet istatistikler için)
sonuc_df = pd.DataFrame(sonuclar)

print(f"\n✅ Tüm veriler '{csv_file_out}' dosyasına kaydedildi.")
