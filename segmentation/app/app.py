import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SAYFA AYARLARI
st.set_page_config(layout="wide", page_title="Beko Segmentasyon")

# 2. RENKLER
BEKO_BLUE = "#0057B8"
BEKO_DARK = "#062B5F"
BEKO_CYAN = "#00AEEF"
BEKO_GRAY = "#F8FBFF"
TEXT_DARK = "#172033"
WARNING_BG = "#FFF7E6"

# 3. CSS ENJEKSİYONU
def inject_css():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(180deg, #F7FAFF 0%, #FFFFFF 42%, #F7FAFF 100%);
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {BEKO_DARK} 0%, {BEKO_BLUE} 100%);
        }}

        section[data-testid="stSidebar"] * {{
            color: white !important;
        }}

        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stMultiSelect label,
        section[data-testid="stSidebar"] .stTextInput label,
        section[data-testid="stSidebar"] .stSlider label {{
            color: white !important;
            font-weight: 600;
        }}

        section[data-testid="stSidebar"] div[data-baseweb="select"] span {{
            color: #172033 !important;
        }}

        section[data-testid="stSidebar"] input {{
            color: #172033 !important;
        }}

        .main-header {{
            background: linear-gradient(135deg, {BEKO_DARK} 0%, {BEKO_BLUE} 55%, {BEKO_CYAN} 100%);
            padding: 28px 32px;
            border-radius: 26px;
            color: white;
            margin-bottom: 22px;
            box-shadow: 0 18px 45px rgba(0, 87, 184, 0.22);
        }}
        
        .complaint-box,
        .response-box,
        .customer-box {{
            color: #172033 !important;
        }}

        .complaint-box div,
        .response-box div,
        .customer-box div {{
            color: #172033 !important;
        }}
        
        .complaint-box .box-title,
        .response-box .box-title,
        .customer-box .box-title {{
            color: #062B5F !important;
        }}
        
        .complaint-text-content {{
            color: #172033 !important;
            font-size: 14px;
            line-height: 1.55;
        }}
        
                /* =========================
           TABS - Genel Görünüm / Öncelikli Aksiyonlar
        ========================== */

        div[data-testid="stTabs"] button {{
            background: #F8FBFF !important;
            color: #062B5F !important;
            border-radius: 14px 14px 0 0 !important;
            border: 1px solid #D6E9FF !important;
            padding: 10px 16px !important;
            font-weight: 800 !important;
        }}

        div[data-testid="stTabs"] button p {{
            color: #062B5F !important;
            font-weight: 800 !important;
        }}

        div[data-testid="stTabs"] button[aria-selected="true"] {{
            background: #0057B8 !important;
            color: white !important;
            border-color: #0057B8 !important;
        }}

        div[data-testid="stTabs"] button[aria-selected="true"] p {{
            color: white !important;
            font-weight: 900 !important;
        }}

        div[data-testid="stTabs"] {{
            color: #172033 !important;
        }}


        /* =========================
           GRAPH / CHART TEXT FIX
        ========================== */

        .js-plotly-plot,
        .plotly,
        .plot-container,
        .svg-container {{
            color: #172033 !important;
        }}

        .js-plotly-plot text {{
            fill: #172033 !important;
        }}

        .gtitle {{
            fill: #062B5F !important;
            font-weight: 800 !important;
        }}

        .xtitle,
        .ytitle {{
            fill: #172033 !important;
            font-weight: 700 !important;
        }}

        .xtick text,
        .ytick text {{
            fill: #172033 !important;
        }}

        .legendtext {{
            fill: #172033 !important;
        }}


        /* =========================
           EXPANDER / RADIO / SELECTBOX LABEL FIX
        ========================== */

        label,
        .stMarkdown,
        .stText,
        .stCaption {{
            color: #172033;
        }}

        div[data-testid="stMarkdownContainer"] p {{
            color: #172033;
        }}

        div[data-testid="stMarkdownContainer"] h1,
        div[data-testid="stMarkdownContainer"] h2,
        div[data-testid="stMarkdownContainer"] h3 {{
            color: #062B5F;
        }}

        .main-title {{
            font-size: 34px;
            font-weight: 800;
            margin-bottom: 6px;
            letter-spacing: -0.5px;
        }}

        .main-subtitle {{
            font-size: 16px;
            opacity: 0.92;
            max-width: 1100px;
        }}

        .badge {{
            display: inline-block;
            background: rgba(255,255,255,0.18);
            border: 1px solid rgba(255,255,255,0.25);
            color: white;
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 12px;
        }}

        .metric-card {{
            background: white;
            border: 1px solid #E6EEF8;
            border-radius: 22px;
            padding: 20px 20px;
            box-shadow: 0 10px 25px rgba(16, 24, 40, 0.055);
            min-height: 124px;
        }}

        .metric-title {{
            color: #667085;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 8px;
        }}

        .metric-value {{
            color: {TEXT_DARK};
            font-size: 30px;
            font-weight: 800;
            line-height: 1.1;
        }}

        .metric-help {{
            color: #667085;
            font-size: 12px;
            margin-top: 8px;
        }}

        .section-card {{
            background: white;
            border: 1px solid #E6EEF8;
            border-radius: 24px;
            padding: 20px 22px;
            box-shadow: 0 10px 25px rgba(16, 24, 40, 0.055);
            margin-bottom: 18px;
        }}

        .section-title {{
            color: {BEKO_DARK};
            font-size: 22px;
            font-weight: 800;
            margin-bottom: 4px;
        }}

        .section-desc {{
            color: #667085;
            font-size: 14px;
            margin-bottom: 16px;
        }}

        .empty-state {{
            background: {WARNING_BG};
            border: 1px solid #FEDF89;
            color: #7A4B00;
            border-radius: 24px;
            padding: 28px 30px;
            margin-top: 18px;
            box-shadow: 0 10px 25px rgba(255, 193, 7, 0.10);
        }}

        .empty-title {{
            font-size: 24px;
            font-weight: 800;
            margin-bottom: 8px;
        }}

        .empty-text {{
            font-size: 15px;
            line-height: 1.55;
        }}

        .risk-high {{
            background: #FEF3F2;
            color: #B42318;
            border: 1px solid #FECDCA;
            border-radius: 999px;
            padding: 5px 10px;
            font-weight: 700;
            font-size: 12px;
        }}

        .risk-low {{
            background: #ECFDF3;
            color: #027A48;
            border: 1px solid #ABEFC6;
            border-radius: 999px;
            padding: 5px 10px;
            font-weight: 700;
            font-size: 12px;
        }}

        .complaint-box {{
            background: #F8FBFF;
            border: 1px solid #D6E9FF;
            border-radius: 20px;
            padding: 18px 20px;
            min-height: 180px;
        }}

        .response-box {{
            background: #F9FAFB;
            border: 1px solid #EAECF0;
            border-radius: 20px;
            padding: 18px 20px;
            min-height: 180px;
        }}

        .customer-box {{
            background: #F0F9FF;
            border: 1px solid #BAE6FD;
            border-radius: 20px;
            padding: 18px 20px;
            min-height: 180px;
        }}

        .box-title {{
            color: {BEKO_DARK};
            font-weight: 800;
            margin-bottom: 10px;
            font-size: 16px;
        }}

        .small-note {{
            font-size: 13px;
            color: #9aa2b1;
        }}

        div[data-testid="stTabs"] button {{
            font-weight: 700;
        }}

        .stDataFrame {{
            border-radius: 18px;
            overflow: hidden;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

inject_css()

# ==========================================

# 3. RENK VE SEGMENT HARİTASI
BEKO_COLOR_MAP = {
    "Düşük Segment (Giriş Seviyesi)": "#002252",
    "Niş / Aşırı Fiyatlandırılmış": "#81B3CE",
    "Popüler Ekonomik": "#015EC7",
    "Keşfedilmemiş Teknoloji": "#C1E6FB",
    "Premium / Lüks": "#313BFB",
    "Fırsat / Yıldız Ürünler": "#FD4040"
}

# 4. VERİYİ YÜKLE
@st.cache_data
def load_data():
    import os
    # Alternatif yolları dene
    paths = [
        "web-scraping-data/data/claned/beko_segmentasyon_sonuc.csv", # Kök dizinden çalıştırılırsa
        "../web-scraping-data/data/claned/beko_segmentasyon_sonuc.csv", # segmentation/app/ içinden çalıştırılırsa
        "../../web-scraping-data/data/claned/beko_segmentasyon_sonuc.csv" # Alternatif
    ]
    for p in paths:
        if os.path.exists(p):
            return pd.read_csv(p)
            
    # Eğer hiçbiri bulunamazsa hata mesajı için bir deneme yap (hata fırlatması için)
    return pd.read_csv(paths[1])

df = load_data()

# 5. KENAR ÇUBUĞU (SIDEBAR) FİLTRELERİ
st.sidebar.header("Kategori Filtreleri")

# Hiyerarşik Filtreleme Mantığı
# 1. Ana Kategori Seçimi
main_cat_options = df['Main_Category'].dropna().unique()
main_cat = st.sidebar.multiselect("Ana Kategori", options=main_cat_options)

# 2. Alt Kategori Seçimi (Ana kategoriye göre filtrele)
sub_cat_df = df[df['Main_Category'].isin(main_cat)] if main_cat else df
sub_cat_options = sub_cat_df['Subcategory'].dropna().unique()
sub_cat = st.sidebar.multiselect("Alt Kategori", options=sub_cat_options)

# 3. Ürün Grubu Seçimi (Alt kategoriye göre filtrele)
prod_group_df = sub_cat_df[sub_cat_df['Subcategory'].isin(sub_cat)] if sub_cat else sub_cat_df
prod_group_options = prod_group_df['Product_Group'].dropna().unique()
prod_group = st.sidebar.multiselect("Ürün Grubu", options=prod_group_options)

# 4. Ürün Adı Seçimi (Ürün grubuna göre filtrele)
prod_name_df = prod_group_df[prod_group_df['Product_Group'].isin(prod_group)] if prod_group else prod_group_df
prod_name_options = prod_name_df['Product_Name'].dropna().unique()
prod_name = st.sidebar.multiselect("Ürün Adı", options=prod_name_options)

st.sidebar.markdown("---")
st.sidebar.header("Metrik Filtreleri")

# Sayısal Değerler İçin Sürgüler (Slider)
# min ve max değerlerini verisetinden otomatik alır
tech_range = st.sidebar.slider(
    "Teknoloji Skoru Aralığı", 
    float(df['Relative_Feature_Score'].min()), float(df['Relative_Feature_Score'].max()), 
    (float(df['Relative_Feature_Score'].min()), float(df['Relative_Feature_Score'].max()))
)

price_range = st.sidebar.slider(
    "Fiyat Aralığı", 
    float(df['Scaled_Price'].min()), float(df['Scaled_Price'].max()), 
    (float(df['Scaled_Price'].min()), float(df['Scaled_Price'].max()))
)

fav_range = st.sidebar.slider(
    "Favori Sayısı Aralığı", 
    float(df['Scaled_Favorite'].min()), float(df['Scaled_Favorite'].max()), 
    (float(df['Scaled_Favorite'].min()), float(df['Scaled_Favorite'].max()))
)


# 6. FİLTRELEME MANTIĞI
filtered_df = df.copy()

# Sayısal değerlerdeki NaN (boş) satırları temizle (Grafiğin çizilmesi için kritik)
numeric_cols = ['Relative_Feature_Score', 'Scaled_Price', 'Scaled_Favorite']
filtered_df = filtered_df.dropna(subset=numeric_cols)

# Kategori filtrelerini uygula
if main_cat: filtered_df = filtered_df[filtered_df['Main_Category'].isin(main_cat)]
if sub_cat: filtered_df = filtered_df[filtered_df['Subcategory'].isin(sub_cat)]
if prod_group: filtered_df = filtered_df[filtered_df['Product_Group'].isin(prod_group)]
if prod_name: filtered_df = filtered_df[filtered_df['Product_Name'].isin(prod_name)]

# Sürgü filtrelerini uygula
filtered_df = filtered_df[
    (filtered_df['Relative_Feature_Score'] >= tech_range[0]) & (filtered_df['Relative_Feature_Score'] <= tech_range[1]) &
    (filtered_df['Scaled_Price'] >= price_range[0]) & (filtered_df['Scaled_Price'] <= price_range[1]) &
    (filtered_df['Scaled_Favorite'] >= fav_range[0]) & (filtered_df['Scaled_Favorite'] <= fav_range[1])
]


# 7. GÖRSELLEŞTİRME (3D GRAFİK)
st.markdown(f"""
    <div class="main-header">
        <div class="badge">Veri Odaklı Ürün Stratejisi</div>
        <div class="main-title">Beko Ürün Segmentasyon ve Konumlandırma Paneli</div>
        <div class="main-subtitle">Ürünlerin teknoloji donanımı, fiyat seviyesi ve tüketici popülaritesine (favori skoru) göre analiz edilerek stratejik segmentlere ayrıldığı etkileşimli pazar görünürlük ekranı.</div>
    </div>
""", unsafe_allow_html=True)

# Grafik eksenleri için ölçeklenmiş verileri kullanmak 3D görünümü daha dengeli yapar
if not filtered_df.empty:
    fig = px.scatter_3d(
        filtered_df, 
        x='Relative_Feature_Score',  # Teknoloji
        y='Scaled_Price',            # Fiyat
        z='Scaled_Favorite',         # Favori
        color='Segmentation_Name',   # Verideki gerçek sütun ismi
        color_discrete_map=BEKO_COLOR_MAP,
        hover_name='Product_Name',
        hover_data={'Price': True, 'Segmentation_Name': True, 'Relative_Feature_Score': False, 'Scaled_Price': False, 'Scaled_Favorite': False}
    )

    # Grafiğin arka planını transparan veya koyu tema yapmak istersen:
    fig.update_layout(
        scene=dict(
            xaxis_title='Teknoloji',
            yaxis_title='FİYAT (Ağırlıklı)',
            zaxis_title='Popülarite',
            xaxis=dict(backgroundcolor=BEKO_GRAY, gridcolor='white', showbackground=True),
            yaxis=dict(backgroundcolor=BEKO_GRAY, gridcolor='white', showbackground=True),
            zaxis=dict(backgroundcolor=BEKO_GRAY, gridcolor='white', showbackground=True),
            camera=dict(eye=dict(x=1.2, y=2.0, z=0.9))
        ),
        paper_bgcolor=BEKO_GRAY,
        plot_bgcolor=BEKO_GRAY,
        font=dict(color=BEKO_DARK),
        legend=dict(title='Cluster', orientation='h', y=0.98, x=0.02),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    fig.update_traces(marker=dict(size=6)) 
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Seçilen filtrelere uygun veri bulunamadı veya sayısal değerler eksik.")


# 8. VERİ TABLOSU VE LİNKLER
st.subheader(f"Listelenen Ürün Sayısı: {len(filtered_df)}")

# Ekranda gösterilecek sütunlar
display_columns = ['Product_Name', 'Price', 'Favorite_Count', 'Segmentation_Name', 'Product_Link']

st.dataframe(
    filtered_df[display_columns].sort_values(by="Price", ascending=False),
    column_config={
        "Price": st.column_config.NumberColumn("Fiyat (TL)", format="%d ₺"),
        "Product_Link": st.column_config.LinkColumn("🔗 Ürün Sayfası", display_text="Siteye Git")
    },
    use_container_width=True,
    hide_index=True
)

# 9. ALT NOT
st.markdown("---")
st.markdown(
    '<p class="small-note">Bu panelde yer alan veriler 2 Mayıs 2026 tarihine aittir.</p>', 
    unsafe_allow_html=True
)