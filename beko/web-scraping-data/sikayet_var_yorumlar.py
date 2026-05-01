import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import os
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
input_csv = os.path.join(script_dir, 'sikayet_var_yorum_linki.csv')
output_csv = os.path.join(script_dir, 'sikayet_var_yorumlar.csv')

# Load the input csv
try:
    df = pd.read_csv(input_csv)
    links = df['Yorum_Linki'].dropna().unique()
except Exception as e:
    print(f'Hata: {e}')
    exit()

# Write headers if file doesn't exist
if not os.path.exists(output_csv):
    with open(output_csv, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Yorum_Linki', 'Sikayet_Basligi', 'Sikayet', 'Sikayet_Tarihi', 'Goruntuleme_Sayisi', 'Kategori', 'Urun_Adi', 'Sirket_Cevabi'])

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for link in links:
    try:
        response = requests.get(link, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        desc_div = soup.find('div', class_='complaint-detail-description')
        if desc_div:
            # Şikayet metni
            paragraphs = desc_div.find_all('p')
            comment_text = ' '.join([p.get_text(strip=True) for p in paragraphs])
            
            # Şikayet Başlığı
            title_h1 = soup.find('h1', class_='complaint-detail-title')
            sikayet_basligi = title_h1.get_text(strip=True) if title_h1 else ""
            
            # Şikayet Tarihi
            date_div = soup.find('div', attrs={'class': lambda e: e and 'js-tooltip' in e and 'time' in e})
            sikayet_tarihi = date_div.get_text(strip=True) if date_div else ""
            
            # Görüntüleme Sayısı
            view_span = soup.find('span', attrs={'class': lambda e: e and 'js-view-count' in e})
            goruntuleme_sayisi = view_span.get_text(strip=True) if view_span else ""
            
            # Kategori ve Ürün Adı
            breadcrumbs = soup.find_all('a', attrs={'data-ga-element': 'Breadcrumb_Link'})
            kategori = ""
            urun_adi = ""
            # İlk eleman Beko, sonrakiler Kategori ve Ürün Adı olabilir (eğer URL /beko/ ile başlıyorsa)
            beko_crumbs = [b for b in breadcrumbs if b.get('href', '').startswith('/beko/') and b.get('href') != '/beko']
            if len(beko_crumbs) >= 1:
                kategori = beko_crumbs[0].get_text(strip=True)
            if len(beko_crumbs) >= 2:
                urun_adi = beko_crumbs[1].get_text(strip=True)

            # Şirket Cevabı
            sirket_cevabi = 0
            profile_wraps = soup.find_all('div', class_='profile-name-wrap')
            for wrap in profile_wraps:
                company_div = wrap.find('div', class_='company-name')
                if company_div:
                    a_tag = company_div.find('a', href='/beko')
                    if a_tag:
                        sirket_cevabi = 1
                        break
            
            # w değiştirmeyi unutmayın konrol için bu şekilde
            # Save directly to csv
            with open(output_csv, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([link, sikayet_basligi, comment_text, sikayet_tarihi, goruntuleme_sayisi, kategori, urun_adi, sirket_cevabi])
            print(f'Başarılı: {link}')
        else:
            print(f'Şikayet bulunamadı: {link}')
        
        time.sleep(1) # Be polite to the server
    except Exception as e:
        print(f'Hata oluştu ({link}): {e}')
