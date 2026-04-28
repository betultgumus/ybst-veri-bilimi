import pandas as pd
import time
import os
import random
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc # Gizli sürücümüz

# Kodun bulunduğu klasörün yolunu al
script_dir = os.path.dirname(os.path.abspath(__file__))

# CSV dosyasının tam yolunu oluştur
csv_okunacak_yol = os.path.join(script_dir, 'beko_urun_linki.csv')
csv_kaydedilecek_yol = os.path.join(script_dir, 'beko_urun_ozellik.csv')

# URL'leri oku
df_urls = pd.read_csv(csv_okunacak_yol)
urun_linkileri = df_urls['urun_linki'].tolist()

# Sonuçların kaydedileceği değişken
csv_file = csv_kaydedilecek_yol
if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
    df_sonuc = pd.read_csv(csv_file)
    print(f"Mevcut {len(df_sonuc)} ürün yüklendi")
else:
    df_sonuc = pd.DataFrame(columns=['urun_linki', 'urun_adi', 'fiyat', 'teknik_ozellikler', 'enerji_sinifi', 'favori_sayisi', 'yorum_sayisi', 'renk_secenekleri', 'urun_ozellikleri', 'yorumlar'])
    print("Yeni CSV dosyası oluşturulacak")

# Undetected Chromedriver ayarları
options = uc.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Standart sürücü yerine 'uc' ile başlatıyoruz ve Chrome 147 sürümünü belirtiyoruz
driver = uc.Chrome(options=options, version_main=147)

try:
    for idx, url in enumerate(urun_linkileri, 1):
        print(f"\nİşleniyor: {idx}/{len(urun_linkileri)} - {url}")
        
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
                fiyat_element = wait.until(
                    EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'prc-last')]"))
                )
                fiyat = fiyat_element.text.strip()
            except TimeoutException:
                fiyat = "Fiyat Bulunamadı"

            # --- TEKNİK ÖZELLİKLERİ ÇEKME BLOĞU BAŞLANGICI ---
            teknik_ozellikler = {}
            
            # Adım 1: Butonu arama ve tıklama
            try:
                # "Ürün Teknik Özellikleri" butonunu bul
                teknik_ozellikleri_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Ürün Teknik Özellikleri') or contains(text(), 'Tüm Özellikler')]"))
                )
                
                # Sayfayı butonun olduğu yere kaydır ama butonu ekranın ortasına al
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", teknik_ozellikleri_button)
                time.sleep(1)
                
                # Javascript ile kesin olarak tıkla
                driver.execute_script("arguments[0].click();", teknik_ozellikleri_button)
                print("  ✓ Teknik Özellikleri butonuna tıklandı")
                
                # Özelliklerin açılması için bekle
                time.sleep(2)
                
            except TimeoutException:
                pass # Buton yoksa hata verme, sessizce geç
            except Exception as e:
                print(f"  ⚠ Butona tıklanırken uyarı: {str(e)}")

            # Adım 2: Verileri sayfadan okuma (Buton olsun veya olmasın her türlü dener)
            try:
                # Tüm item'leri çek
                items = driver.find_elements(By.CSS_SELECTOR, "div.item")
                
                for item in items:
                    try:
                        # Başlık (özellik adı) ve değer çek
                        baslik_elem = item.find_element(By.CSS_SELECTOR, "div.t")
                        deger_elem = item.find_element(By.CSS_SELECTOR, "div.v")
                        
                        baslik = baslik_elem.text.strip()
                        deger = deger_elem.text.strip()
                        
                        if baslik and deger:
                            teknik_ozellikler[baslik] = deger
                    except:
                        continue # Eğer o item içinde t veya v yoksa sıradaki item'a geç
                
                if teknik_ozellikler:
                    print(f"  ✓ {len(teknik_ozellikler)} teknik özellik çekildi")
                else:
                    print("  ⚠ Teknik özellik bulunamadı (Özellikler bu üründe girilmemiş olabilir)")
                    
            except Exception as e:
                print(f"  ⚠ Teknik özellikleri okurken hata: {str(e)}")
            # --- TEKNİK ÖZELLİKLERİ ÇEKME BLOĞU SONU ---
            
            # Enerji Sınıfı çek
            enerji_sinifi = ""
            try:
                enerji_img = driver.find_element(By.XPATH, "//img[contains(@src, 'energy')]")
                enerji_sinifi = enerji_img.get_attribute("title").strip()
                if enerji_sinifi:
                    print(f"  ✓ Enerji Sınıfı: {enerji_sinifi}")
            except:
                print("  ⚠ Enerji sınıfı bulunamadı")
            
            # Favori Sayısı çek
            favori_sayisi = ""
            try:
                favori_elem = driver.find_element(By.CSS_SELECTOR, "span.txt.js-favorites-count")
                favori_sayisi = favori_elem.text.strip()
                if favori_sayisi:
                    print(f"  ✓ Favori Sayısı: {favori_sayisi}")
            except:
                print("  ⚠ Favori sayısı bulunamadı")
            
            # Yorum Sayısı çek
            yorum_sayisi = ""
            try:
                # Yorum sayısı genelde ikinci span olabilir veya specific selector olabilir
                yorum_elements = driver.find_elements(By.XPATH, "//span[contains(., 'Yorum') or contains(., 'yorum')]")
                if yorum_elements:
                    # İçinde sadece sayı olan span'ı bul
                    for elem in yorum_elements:
                        text = elem.text.strip()
                        if text.isdigit():
                            yorum_sayisi = text
                            break
                if yorum_sayisi:
                    print(f"  ✓ Yorum Sayısı: {yorum_sayisi}")
            except:
                print("  ⚠ Yorum sayısı bulunamadı")
            
            # Renk Seçenekleri çek
            renk_secenekleri = []
            try:
                renk_items = driver.find_elements(By.CSS_SELECTOR, "div.list a.variant-item")
                for renk_item in renk_items:
                    try:
                        renk_adi = renk_item.find_element(By.CSS_SELECTOR, "div.t").text.strip()
                        if renk_adi:
                            renk_secenekleri.append(renk_adi)
                    except:
                        pass
                if renk_secenekleri:
                    print(f"  ✓ {len(renk_secenekleri)} renk seçeneği bulundu")
            except:
                print("  ⚠ Renk seçenekleri bulunamadı")
            
            # Ürün Özellikleri çek (pdp-features)
            urun_ozellikleri = {}
            try:
                ozellik_items = driver.find_elements(By.CSS_SELECTOR, "div.pdp-features div.item")
                for item in ozellik_items:
                    try:
                        # Başlık (t) çek
                        ozellik_adi = item.find_element(By.CSS_SELECTOR, "div.t").text.strip()
                        # Değer (v) çek
                        try:
                            ozellik_deger = item.find_element(By.CSS_SELECTOR, "div.v").text.strip()
                        except:
                            # Eğer div.v yoksa tooltip'ten deneyelim
                            try:
                                ozellik_deger = item.find_element(By.CSS_SELECTOR, "div.tooltip span.cnt").text.strip()
                            except:
                                ozellik_deger = ""
                        
                        if ozellik_adi and ozellik_deger:
                            urun_ozellikleri[ozellik_adi] = ozellik_deger
                    except:
                        pass
                if urun_ozellikleri:
                    print(f"  ✓ {len(urun_ozellikleri)} ürün özelliği çekildi")
            except:
                print("  ⚠ Ürün özellikleri bulunamadı")
            
            # Yorumlar çek
            yorumlar = []
            try:
                # "Yorumlar" butonunu bul ve tıkla
                yorumlar_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Yorumlar')]"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", yorumlar_button)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", yorumlar_button)
                print("  ✓ Yorumlar butonuna tıklandı")
                
                # Yorumların yüklenmesini bekle
                time.sleep(2)
                
                # Tüm yorum öğelerini çek
                yorum_items = driver.find_elements(By.CSS_SELECTOR, "div.rvw-list-item")
                
                for yorum_item in yorum_items:
                    try:
                        yorum_dict = {}
                        
                        # Yıldız sayısı çek
                        try:
                            rating_elem = yorum_item.find_element(By.CSS_SELECTOR, "span.rating")
                            yorum_dict['yildiz'] = rating_elem.get_attribute("data-rating")
                        except:
                            yorum_dict['yildiz'] = ""
                        
                        # Başlık çek
                        try:
                            baslik_elem = yorum_item.find_element(By.CSS_SELECTOR, "div.rvw-item-title")
                            yorum_dict['baslik'] = baslik_elem.text.strip()
                        except:
                            yorum_dict['baslik'] = ""
                        
                        # Sahip adı çek
                        try:
                            sahip_elem = yorum_item.find_element(By.CSS_SELECTOR, "div.rvw-item-owner")
                            yorum_dict['sahip_adi'] = sahip_elem.text.strip()
                        except:
                            yorum_dict['sahip_adi'] = ""
                        
                        # Tarih çek
                        try:
                            tarih_elem = yorum_item.find_element(By.CSS_SELECTOR, "div.rvw-item-date")
                            yorum_dict['tarih'] = tarih_elem.text.strip()
                        except:
                            yorum_dict['tarih'] = ""
                        
                        # Yorum metni çek
                        try:
                            metin_elem = yorum_item.find_element(By.CSS_SELECTOR, "div.rvw-item-text p")
                            yorum_dict['metin'] = metin_elem.text.strip()
                        except:
                            yorum_dict['metin'] = ""
                        
                        # Evet sayısı çek
                        try:
                            evet_button = yorum_item.find_element(By.CSS_SELECTOR, "button.current-upvote")
                            evet_title = evet_button.get_attribute("title")
                            yorum_dict['evet_sayisi'] = evet_title.split()[0] if evet_title else "0"
                        except:
                            yorum_dict['evet_sayisi'] = "0"
                        
                        # Hayır sayısı çek
                        try:
                            hayir_button = yorum_item.find_element(By.CSS_SELECTOR, "button.current-downvote")
                            hayir_title = hayir_button.get_attribute("title")
                            yorum_dict['hayir_sayisi'] = hayir_title.split()[0] if hayir_title else "0"
                        except:
                            yorum_dict['hayir_sayisi'] = "0"
                        
                        # Cevap varsa çek
                        yorum_dict['cevap'] = ""
                        try:
                            cevap_elem = yorum_item.find_element(By.CSS_SELECTOR, "div.rvw-item-reply")
                            cevap_header = cevap_elem.find_element(By.CSS_SELECTOR, "div.rvw-reply-header").text.strip()
                            cevap_text = cevap_elem.find_element(By.CSS_SELECTOR, "div.rvw-reply-text p").text.strip()
                            yorum_dict['cevap'] = f"{cevap_header}: {cevap_text}"
                        except:
                            pass
                        
                        # Yorum sözlüğünü listeye ekle
                        if yorum_dict['metin']:  # Metin varsa ekle
                            yorumlar.append(yorum_dict)
                    except:
                        continue
                
                if yorumlar:
                    print(f"  ✓ {len(yorumlar)} yorum çekildi")
                else:
                    print("  ⚠ Yorum bulunamadı")
                    
            except TimeoutException:
                print("  ⚠ Yorumlar butonu bulunamadı")
            except Exception as e:
                print(f"  ⚠ Yorumları çekerken hata: {str(e)}")
            
            # Yeni ürünü DataFrame'e ekle
            yeni_urun = pd.DataFrame([{
                'urun_linki': url,
                'urun_adi': urun_adi,
                'fiyat': fiyat,
                'teknik_ozellikler': json.dumps(teknik_ozellikler, ensure_ascii=False),
                'enerji_sinifi': enerji_sinifi,
                'favori_sayisi': favori_sayisi,
                'yorum_sayisi': yorum_sayisi,
                'renk_secenekleri': json.dumps(renk_secenekleri, ensure_ascii=False),
                'urun_ozellikleri': json.dumps(urun_ozellikleri, ensure_ascii=False),
                'yorumlar': json.dumps(yorumlar, ensure_ascii=False)
            }])
            
            df_sonuc = pd.concat([df_sonuc, yeni_urun], ignore_index=True)
            df_sonuc.to_csv(csv_file, index=False, encoding='utf-8-sig') # Türkçe karakterler için utf-8-sig
            
            print(f"  ✓ Ürün: {urun_adi}")
            print(f"  ✓ Fiyat: {fiyat}")
            print(f"  ✓ Kaydedildi (Toplam: {len(df_sonuc)} ürün)")
            
            # DİKKAT: İnsan gibi davranmak için rastgele bekleme (4 ile 8 saniye arası)
            bekleme_suresi = random.uniform(4, 8)
            time.sleep(bekleme_suresi)
            
        except Exception as e:
            print(f"  ✗ Beklenmeyen Hata: {str(e)}")
            yeni_urun = pd.DataFrame([{
                'urun_linki': url,
                'urun_adi': 'Hata',
                'fiyat': 'Hata',
                'teknik_ozellikler': json.dumps({}, ensure_ascii=False),
                'enerji_sinifi': '',
                'favori_sayisi': '',
                'yorum_sayisi': '',
                'renk_secenekleri': json.dumps([], ensure_ascii=False),
                'urun_ozellikleri': json.dumps({}, ensure_ascii=False),
                'yorumlar': json.dumps([], ensure_ascii=False)
            }])
            df_sonuc = pd.concat([df_sonuc, yeni_urun], ignore_index=True)
            df_sonuc.to_csv(csv_file, index=False, encoding='utf-8-sig')

finally:
    driver.quit()

print(f"\n✓ Tamamlandı! Toplam {len(df_sonuc)} ürün kaydedildi.")