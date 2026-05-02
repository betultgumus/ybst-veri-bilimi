import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Site listesini tanımla
site = ["https://www.beko.com.tr/"]

# Link listesi
kategori_links = []
tur_listesi = []

def get_driver():
    """Selenium driver yapılandırması"""
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Arka planda çalışması için aktif edilebilir
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def kategori_linklerini_cek(driver):
    """Kategori linklerini Selenium ile çıkart - Ürünler menüsünden"""
    try:
        # Menünün yüklenmesi için bekle
        wait = WebDriverWait(driver, 20)
        
        # Beko sayfasında "Ürünler" listesindeki linkleri bul
        li_elements = driver.find_elements(By.CSS_SELECTOR, "ul[title='Ürünler'] li a.link")
        
        for link in li_elements:
            href = link.get_attribute('href')
            title = link.get_attribute('title')
            if href and title:
                kategori_links.append({
                    'kategori': title,
                    'href': href,
                })
        
        print(f"\n✓ {len(kategori_links)} kategori linki çekildi:")
        for item in kategori_links:
            print(f"  - {item['kategori']}")
            
    except Exception as e:
        print(f"✗ Kategoriler çekilirken hata: {e}")

def kategori_linklerini_kaydet():
    """Kategorileri CSV dosyasına kaydet"""
    if not kategori_links:
        print("✗ Kaydedecek kategori yok")
        return
    
    csv_path = "beko/web-scraping-data/data/raw/beko/beko_kategori.csv"
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['kategori', 'href'])
            writer.writeheader()
            writer.writerows(kategori_links)
        print(f"✓ {len(kategori_links)} kategori {csv_path} dosyasına kaydedildi.")
    except Exception as e:
        print(f"✗ CSV dosyasına kaydedilirken hata: {e}")

def tur_listesini_kaydet():
    """Türleri CSV dosyasına kaydet"""
    if not tur_listesi:
        print("✗ Kaydedecek tür yok")
        return
    
    csv_path = "beko/web-scraping-data/data/raw/beko/beko_turleri.csv"
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['kategori', 'urun_adi'])
            writer.writeheader()
            writer.writerows(tur_listesi)
        print(f"✓ {len(tur_listesi)} tür {csv_path} dosyasına kaydedildi.")
    except Exception as e:
        print(f"✗ CSV dosyasına kaydedilirken hata: {e}")

def tur_linklerini_cek(driver, kategori_url, kategori_adi):
    """Kategori sayfasından alt türleri (Buzdolabı, Çamaşır Makinesi vb.) çıkart"""
    try:
        print(f"\n  📦 '{kategori_adi}' kategorisi içinden ürün grupları çekiliyor...")
        driver.get(kategori_url)
        time.sleep(3)
        
        # plp-sub-categories div'ini bekle
        try:
            wait = WebDriverWait(driver, 10)
            plp_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "plp-sub-categories")))
            
            a_tags = plp_div.find_elements(By.TAG_NAME, "a")
            
            urun_sayisi = 0
            
            for a in a_tags:
                try:
                    span = a.find_element(By.TAG_NAME, "span")
                    urun_adi = span.text.strip()
                    
                    if urun_adi:
                        tur_listesi.append({
                            'kategori': kategori_adi,
                            'urun_adi': urun_adi
                        })
                        print(f"    ✓ {urun_adi}")
                        urun_sayisi += 1
                except:
                    continue
            
            print(f"  → {urun_sayisi} ürün grubu eklendi")
            return urun_sayisi
        except:
            print(f"  ✗ '{kategori_adi}' için alt ürün grubu bulunamadı")
            return 0
        
    except Exception as e:
        print(f"  ✗ Hata: {e}")
        return 0


# Ana akışı başlat
driver = get_driver()
try:
    for url in site:
        print(f"\n{url} sitesine bağlanılıyor...")
        driver.get(url)
        time.sleep(2)
        
        try:
            cookie_btn = driver.find_element(By.ID, "onetrust-accept-btn-handler")
            cookie_btn.click()
            print("  ✓ Çerez uyarısı kabul edildi.")
            time.sleep(1)
        except:
            pass
        
        kategori_linklerini_cek(driver)
        
        # Her kategori için türleri çek
        for kategori in kategori_links:
            tur_linklerini_cek(driver, kategori['href'], kategori['kategori'])
    
    # Kategorileri ve türleri CSV'ye kaydet
    print("\n" + "="*50)
    kategori_linklerini_kaydet()
    tur_listesini_kaydet()
    print("="*50)
        
finally:
    driver.quit()