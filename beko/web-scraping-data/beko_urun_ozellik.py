import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# URL'leri oku
df_urls = pd.read_csv('beko_urun_linki.csv')
urun_linkileri = df_urls['urun_linki'].tolist()

# CSV dosya yolu
csv_file = 'beko_urun_ozellik.csv'

# CSV dosya varsa oku, yoksa boş DataFrame oluştur
if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
    df_sonuc = pd.read_csv(csv_file)
    print(f"Mevcut {len(df_sonuc)} ürün yüklendi")
else:
    df_sonuc = pd.DataFrame(columns=['urun_linki', 'urun_adi', 'fiyat'])
    print("Yeni CSV dosyası oluşturulacak")

# Selenium driver setup
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

try:
    for idx, url in enumerate(urun_linkileri, 1):
        print(f"\nİşleniyor: {idx}/{len(urun_linkileri)} - {url}")
        
        try:
            driver.get(url)
            
            # Sayfanın yüklenmesini bekle
            wait = WebDriverWait(driver, 15)
            
            # Çerez kabul butonuna bas
            try:
                cookie_button = wait.until(
                    EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
                )
                cookie_button.click()
                print("  ✓ Çerez kabul edildi")
                time.sleep(2)
            except TimeoutException:
                print("  ⚠ Çerez butonu bulunamadı")
            except Exception as e:
                print(f"  ⚠ Çerez hatası: {str(e)}")
            
            # Sayfanın tam yüklenmesini bekle
            time.sleep(2)
            
            # Ürün adını çek
            try:
                urun_adi_element = wait.until(
                    EC.presence_of_element_located((By.ID, "product-title"))
                )
                urun_adi = urun_adi_element.text.replace('\n', ' ').strip()
            except TimeoutException:
                urun_adi = "Bulunamadı"
            
            # Fiyatı çek
            try:
                fiyat_element = driver.find_element(By.XPATH, "//span[@class='prc prc-last']")
                fiyat = fiyat_element.text.strip()
            except NoSuchElementException:
                fiyat = "Bulunamadı"
            
            # Yeni ürünü DataFrame'e ekle
            yeni_urun = pd.DataFrame([{
                'urun_linki': url,
                'urun_adi': urun_adi,
                'fiyat': fiyat
            }])
            df_sonuc = pd.concat([df_sonuc, yeni_urun], ignore_index=True)
            
            # Hemen CSV'ye kaydet
            df_sonuc.to_csv(csv_file, index=False, encoding='utf-8')
            
            print(f"  ✓ Ürün: {urun_adi}")
            print(f"  ✓ Fiyat: {fiyat}")
            print(f"  ✓ CSV'ye kaydedildi (Toplam: {len(df_sonuc)} ürün)")
            
            # Sayfalar arasında bekle
            time.sleep(1)
            
        except Exception as e:
            print(f"  ✗ Hata: {str(e)}")
            yeni_urun = pd.DataFrame([{
                'urun_linki': url,
                'urun_adi': 'Hata',
                'fiyat': 'Hata'
            }])
            df_sonuc = pd.concat([df_sonuc, yeni_urun], ignore_index=True)
            df_sonuc.to_csv(csv_file, index=False, encoding='utf-8')

finally:
    driver.quit()

print(f"\n✓ Tamamlandı! Toplam {len(df_sonuc)} ürün kaydedildi.")
print(f"Dosya: {csv_file}")
print("\nÖnizleme:")
print(df_sonuc.head(10))
