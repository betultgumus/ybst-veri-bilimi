import pandas as pd
# import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re
import os 

import undetected_chromedriver as uc

# Kodun çalıştığı klasörün yolunu otomatik bul
calisma_dizini = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(calisma_dizini, 'sikayet_var_urun_linki.csv')

# CSV dosyasını oku
df = pd.read_csv(csv_file)

# Ürün linklerini ve bilgilerini al
urun_linkleri = df['Urun Linki'].unique()

print(f"Toplam {len(urun_linkleri)} adet ürün bulundu.\n")

# Sonuçları saklamak için liste
sonuclar = []

# CSV dosyası için header tanımla
csv_file_out = 'sikayet_var_yorum_linki.csv'
is_first_write = True


def start_driver():
    options = uc.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Buraya version_main=147 parametresini ekliyoruz!
    driver = uc.Chrome(options=options, version_main=147)
    return driver

driver = start_driver()

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

            # 4. Yorumları çek - Sayfalama (Pagination) ve Güvenli Filtre ile
            try:
                yorum_linkleri = []
                sayfa_no = 1
                
                while True:
                    print(f"   🔍 Sayfa {sayfa_no} taranıyor...")
                    
                    # Sayfalama butonunun (İleri oku) DOM'a yüklenmesi için EN DİBE inmemiz şart!
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    
                    # Sayfa sonu tembel yüklemesini (lazy load) tetiklemek için ufak bir yukarı-aşağı manevrası
                    driver.execute_script("window.scrollBy(0, -500);")
                    time.sleep(0.5)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1.5)
                    
                    # Sadece senin bulduğun net sınıfı alıyoruz
                    yorum_elemanlari = driver.find_elements(By.CSS_SELECTOR, "a.complaint-layer")
                    
                    yeni_bulunan = 0
                    for elem in yorum_elemanlari:
                        href = elem.get_attribute("href")
                        
                        # Link Beko şikayeti ise ve ürünün kendi ana linki değilse
                        if href and href.startswith("https://www.sikayetvar.com/beko/"):
                            if href != link and href not in yorum_linkleri:
                                yorum_linkleri.append(href)
                                yeni_bulunan += 1
                                
                    print(f"      > Bu sayfadan {yeni_bulunan} net şikayet alındı.")
                    
                    # İLERİ BUTONUNA BASIP DİĞER SAYFAYA GEÇME KISMI
                    try:
                        # 1. XPath karmaşasını bıraktık, en sade haliyle sadece 'icomoon-paginate-next' ikonunu arıyoruz.
                        next_icon = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".icomoon-paginate-next"))
                        )
                        
                        # 2. İkonun içinde bulunduğu asıl baba <a> (link) etiketine (.. ile) çıkıyoruz.
                        next_button = next_icon.find_element(By.XPATH, "..")
                        next_url = next_button.get_attribute("href")
                        
                        if next_url:
                            print(f"      > Sonraki sayfa bulundu! Geçiliyor: {next_url}") 
                            driver.get(next_url)
                            sayfa_no += 1
                            time.sleep(3.5) # Yeni sayfanın yüklenmesi için bekle
                        else:
                            break # Link yoksa döngüyü bitir
                            
                    except Exception as e:
                        # 3. KÖR UÇUŞU BİTİRDİK: Neden geçemediğini konsola yazdırıyoruz!
                        print(f"      > İleri butonu bulunamadı. (Sebep: {type(e).__name__})")
                        break # İleri butonu bulunamadıysa döngüyü bitir

                    
                yorum_linkleri_str = ", ".join(yorum_linkleri)
                
                if yorum_linkleri_str:
                    print(f"   ✅ Toplam {sayfa_no} sayfa gezildi, {len(yorum_linkleri)} adet şikayet linki çekildi.")
                else:
                    print("   ⚠️ Link bulunamadı.")
                    
                # ÇOK ÖNEMLİ: İşlem bitince ürünün ilk sayfasına dön. 
                # (Yoksa 5. adımdaki 'Toplam Şikayet Sayısı' kodun son sayfada patlar)
                if sayfa_no > 1:
                    driver.get(link)
                    time.sleep(2)
                    
            except Exception as e:
                print(f"   ✗ Yorum çekme hatası: {e}")
                yorum_linkleri_str = ", ".join(yorum_linkleri) if 'yorum_linkleri' in locals() else ""


            

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
            err_msg = str(e)
            print(f"   ✗ Link ziyareti hatası: {err_msg}")
            
            # Eğer session düştüyse (tarayıcı kapandıysa) yeniden başlat
            if "invalid session id" in err_msg.lower() or "target window already closed" in err_msg.lower():
                print("   ➔ Tarayıcı oturumu koptu, yeniden başlatılıyor...")
                try:
                    driver.quit()
                except:
                    pass
                driver = start_driver()
                
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
        time.sleep(3)

finally:
    driver.quit()

# Sonuçları DataFrame'e dönüştür (özet istatistikler için)
sonuc_df = pd.DataFrame(sonuclar)

print(f"\n✅ Tüm veriler '{csv_file_out}' dosyasına kaydedildi.")
