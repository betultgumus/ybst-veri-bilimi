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
                    'link': href,
                    'full_url': href
                })
        
        print(f"\n✓ {len(kategori_links)} kategori linki çekildi:")
        for item in kategori_links:
            print(f"  - {item['kategori']}: {item['full_url']}")
            
    except Exception as e:
        print(f"✗ Kategoriler çekilirken hata: {e}")

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
            
            kategori_full_urls = [k['full_url'] for k in kategori_links]
            urun_sayisi = 0
            
            for a in a_tags:
                try:
                    span = a.find_element(By.TAG_NAME, "span")
                    urun_adi = span.text.strip()
                    full_url = a.get_attribute('href')
                    
                    if full_url and full_url not in kategori_full_urls:
                        tur_listesi.append({
                            'kategori': kategori_adi,
                            'urun_adi': urun_adi,
                            'full_url': full_url
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

def urun_detay_linklerini_cek(driver, urun_grubu_url):
    """Sonsuz kaydırma ile tüm sayfa sonuna kadar inip ürün linklerini çeker"""
    try:
        print(f"\n🔍 Sayfadaki TÜM ürün detay linkleri taranıyor (Kaydırma yapılıyor): {urun_grubu_url}")
        driver.get(urun_grubu_url)
        time.sleep(3)
        
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
            last_height = new_height
            print("  ...sayfa aşağı kaydırılıyor...")

        urun_kartlari = driver.find_elements(By.CLASS_NAME, "prd-inner")
        
        detay_linkleri = []
        for kart in urun_kartlari:
            try:
                link_tag = kart.find_element(By.CSS_SELECTOR, "h2.prd-name a")
                full_url = link_tag.get_attribute('href')
                if full_url:
                    detay_linkleri.append(full_url)
            except:
                continue
        
        detay_linkleri = list(dict.fromkeys(detay_linkleri))
        
        if detay_linkleri:
            with open('urun_linki.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['urun_linki'])
                for link in detay_linkleri:
                    writer.writerow([link])
            
            print(f"✅ Toplam {len(detay_linkleri)} ürün linki 'urun_linki.csv' dosyasına kaydedildi.")
        else:
            print("⚠️ Hiç ürün linki bulunamadı.")
            
    except Exception as e:
        print(f"❌ Hata: {e}")

# Ana akışı başlat
driver = get_driver()
try:
    for url in site:
        print(f"\n{url} sitesine bağlanılıyor...")
        driver.get(url)
        time.sleep(2)
        
        kategori_linklerini_cek(driver)
        
        if kategori_links:
            print(f"\n--- TEST: İlk Kategori ({kategori_links[0]['kategori']}) ---")
            tur_linklerini_cek(driver, kategori_links[0]['full_url'], kategori_links[0]['kategori'])
            
            if tur_listesi:
                print(f"\n--- TEST: Ürün detay linklerini çekme ({tur_listesi[0]['urun_adi']}) ---")
                urun_detay_linklerini_cek(driver, tur_listesi[0]['full_url'])
finally:
    driver.quit()
