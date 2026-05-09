import pandas as pd
import time
import os
import random
import json
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc # Gizli sürücümüz

# Kodun bulunduğu klasörün yolunu al
script_dir = os.path.dirname(os.path.abspath(__file__))
 
# CSV dosyasının tam yolunu oluştur
csv_okunacak_yol = r'...\web-scraping-data\data\raw\beko\beko_urun_linki.csv'
csv_kaydedilecek_yol = r'...\web-scraping-data\data\raw\beko\beko_buzdolabi_fiyat.csv'

# URL'leri oku
df_urls = pd.read_csv(csv_okunacak_yol)
urun_linkleri = df_urls['urun_linki'].tolist()[:84]  # Sadece ilk 84 linki al

# Tekrar eden değer kontrolü ve silinmesi (kalıcı olarak, sırayı koruyarak)
eski_uzunluk = len(urun_linkleri)
urun_linkleri = list(dict.fromkeys(urun_linkleri))
tekrar_eden_sayisi = eski_uzunluk - len(urun_linkleri)

if tekrar_eden_sayisi > 0:
    print(f"Bilgi: {tekrar_eden_sayisi} adet tekrar eden link bulundu ve tekilleştirildi.")
    # Temizlenmiş listeyi ana dosyaya da geri yansıt
    df_urls = pd.DataFrame(urun_linkleri, columns=['urun_linki'])
    df_urls.to_csv(csv_okunacak_yol, index=False)
    print("Bilgi: 'beko_urun_linki.csv' dosyası tekrar edenlerden arındırılarak güncellendi.")
else:
    print("Bilgi: Tekrar eden link bulunmuyor.")


# Sonuçların kaydedileceği değişken
csv_file = csv_kaydedilecek_yol
try:
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        df_sonuc = pd.read_csv(csv_file)
        print(f"Mevcut {len(df_sonuc)} ürün yüklendi")
    else:
        df_sonuc = pd.DataFrame(columns=['urun_linki', 'urun_adi', 'fiyat'])
        print("Yeni CSV dosyası oluşturulacak")
except Exception:
    df_sonuc = pd.DataFrame(columns=['urun_linki', 'urun_adi', 'fiyat'])
    print("Yeni CSV dosyası oluşturulacak (Mevcut dosya boş veya hatalı)")

# Undetected Chromedriver ayarları fonksiyonu
def get_driver():
    options = uc.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return uc.Chrome(options=options, version_main=147)

driver = get_driver()
wait = WebDriverWait(driver, 15)

try:
    for idx, url in enumerate(tqdm(urun_linkleri, desc="Ürünler İşleniyor", unit="ürün"), 1):
        print(f"\nİşleniyor: {idx}/{len(urun_linkleri)} - {url}")
        
        # Her 20 üründe bir sürücüyü yenile
        if idx > 1 and idx % 20 == 0:
            print("\nOturum yenileniyor...")
            try:
                driver.quit()
            except:
                pass
            time.sleep(2)
            driver = get_driver()
            wait = WebDriverWait(driver, 15)

        try:
            driver.get(url)
            
            # Sayfanın yüklenmesini bekle
            wait = WebDriverWait(driver, 15) 
            
            # Çerez kabul butonuna bas
            try:
                cookie_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
                )
                cookie_button.click()
                print("  ✓ Çerez kabul edildi")
            except TimeoutException:
                pass 
            except Exception:
                pass 
            
            # Ürün adını çek 
            try:
                urun_adi_element = wait.until(
                    EC.visibility_of_element_located((By.ID, "product-title"))
                )
                urun_adi = urun_adi_element.text.replace('\n', ' ').strip()
            except TimeoutException:
                urun_adi = "Başlık Bulunamadı"
            
            # Fiyatı çek 
            try:
                # Önce itemprop="price" olan span'ı dene, bulamazsa sınıfa göre ara
                fiyat_element = None
                try:
                    fiyat_element = wait.until(
                        EC.visibility_of_element_located((By.XPATH, "//span[@itemprop='price']"))
                    )
                except:
                    fiyat_element = wait.until(
                        EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'prc-last')]"))
                    )
                
                fiyat = fiyat_element.text.strip().replace('\xa0', ' ')
            except TimeoutException:
                fiyat = "Fiyat Bulunamadı"

            # Veriyi anlık olarak kaydet
            yeni_urun = pd.DataFrame([{
                'urun_linki': url,
                'urun_adi': urun_adi,
                'fiyat': fiyat
            }])
            
            # Dosyaya ekleme modunda yaz (header sadece dosya yoksa yazılır)
            file_exists = os.path.isfile(csv_file)
            yeni_urun.to_csv(csv_file, mode='a', index=False, header=not file_exists, encoding='utf-8-sig')
            
            # Bellekteki df_sonuc'u da güncelle (görsel takip için)
            df_sonuc = pd.concat([df_sonuc, yeni_urun], ignore_index=True)
            
            print(f"  ✓ Kaydedildi: {urun_adi[:30]}... ({fiyat})")
            
            # DİKKAT: İnsan gibi davranmak için rastgele bekleme
            bekleme_suresi = random.uniform(2, 5)
            time.sleep(bekleme_suresi) 
            
        except Exception as e:
            print(f"  ✗ Hata (URL: {url}): {str(e)}")
            yeni_urun = pd.DataFrame([{
                'urun_linki': url,
                'urun_adi': 'Hata',
                'fiyat': 'Hata'
            }])
            file_exists = os.path.isfile(csv_file)
            yeni_urun.to_csv(csv_file, mode='a', index=False, header=not file_exists, encoding='utf-8-sig')
            df_sonuc = pd.concat([df_sonuc, yeni_urun], ignore_index=True)

finally:
    driver.quit()

print(f"\n✓ Tamamlandı! Toplam {len(df_sonuc)} ürün kaydedildi.")