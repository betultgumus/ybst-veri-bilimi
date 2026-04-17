from bs4 import BeautifulSoup
import requests
import time

# Site listesini tanımla
site = ["https://www.beko.com.tr/"]

# Link listesi
kategori_links = []
urun_listesi = []

# Headers ayarla (bazı siteler bot tarafından engellenir)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def site_ye_gir(url):
    """BeautifulSoup ile site ye erişim"""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # HTML'i parse et
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print(f"✓ Siteye başarıyla girildi: {url}")
        print(f"Sayfa başlığı: {soup.title.string if soup.title else 'Başlık bulunamadı'}")
        
        return soup
    except requests.exceptions.RequestException as e:
        print(f"✗ Hata: {e}")
        return None

def kategori_linklerini_cek(soup):
    """Kategori linklerini BeautifulSoup ile çıkart - title='Ürünler' olan <ul> içinden"""
    # title="Ürünler" olan ul'i bul
    urun_ul = soup.find('ul', {'class': 'ul-clear', 'role': 'region', 'title': 'Ürünler'})
    
    if not urun_ul:
        print("✗ 'Ürünler' kategorisi bulunamadı")
        return
    
    # Bu ul'in içindeki tüm li'leri bul
    li_elements = urun_ul.find_all('li')
    
    for li in li_elements:
        link = li.find('a', class_='link')
        if link:
            href = link.get('href')
            title = link.get('title')
            if href and title:
                kategori_links.append({
                    'kategori': title,
                    'link': href,
                    'full_url': f"https://www.beko.com.tr{href}" if href.startswith('/') else href
                })
    
    print(f"\n✓ {len(kategori_links)} kategori linki çekildi:")
    for item in kategori_links:
        print(f"  - {item['kategori']}: {item['full_url']}")

def urunleri_cek(kategori_url, kategori_adi):
    """Kategori sayfasından ürünleri çıkart - sadece <div class="plp-sub-categories"> içinden"""
    try:
        print(f"\n  📦 '{kategori_adi}' kategorisi içinden ürünler çekiliyor...")
        response = requests.get(kategori_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Kategori linklerinin full_url'lerini al (bu linkler ürün değil kategori linki)
        kategori_full_urls = [k['full_url'] for k in kategori_links]
        
        # <div class="plp-sub-categories mt-10"> bul
        plp_div = soup.find('div', {'class': 'plp-sub-categories'})
        
        if not plp_div:
            print(f"  ✗ 'plp-sub-categories' div'i bulunamadı")
            return 0
        
        # Bu div'in içindeki <a> taglarını bul
        a_tags = plp_div.find_all('a', href=True)
        
        urun_sayisi = 0
        for a in a_tags:
            img = a.find('img', class_='lazy')
            span = a.find('span')
            
            if img and span:
                urun_adi = span.get_text(strip=True)
                urun_linki = a.get('href')
                
                # Full URL'yi oluştur
                full_url = f"https://www.beko.com.tr{urun_linki}" if urun_linki.startswith('/') else urun_linki
                
                # Kontrol: bu link kategori linki mi?
                if full_url not in kategori_full_urls:
                    # Ürün linki, kategori linki değil - kaydet
                    if urun_adi and urun_linki:
                        urun_listesi.append({
                            'kategori': kategori_adi,
                            'urun_adi': urun_adi,
                            'urun_linki': urun_linki,
                            'full_url': full_url
                        })
                        print(f"    ✓ {urun_adi}")
                        urun_sayisi += 1
        
        print(f"  → {urun_sayisi} ürün eklendi")
        return urun_sayisi
        
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Hata: {e}")
        return 0



# Siteler üzerinde döngü yap
for url in site:
    print(f"\n{url} sitesine bağlanılıyor...")
    soup = site_ye_gir(url)
    
    if soup:
        # Kategori linklerini çek
        kategori_linklerini_cek(soup)
        
        # TEST: Sadece ilk kategoriyi çek
        if kategori_links:
            print(f"\n--- TEST: İlk Kategori ({kategori_links[0]['kategori']}) ---")
            urunleri_cek(kategori_links[1]['full_url'], kategori_links[0]['kategori'])
    
    time.sleep(2)  # İki istek arasında 2 saniye bekle
