import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
import streamlit as st

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

from src.config import COMPLAINT_ANALYSIS_TABLE
from src.database import read_table


# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="Beko Müşteri Sesi Zekâ Platformu",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==============================
# THEME CONSTANTS
# ==============================

BEKO_BLUE = "#0057B8"
BEKO_DARK = "#062B5F"
BEKO_LIGHT = "#EAF3FF"
BEKO_CYAN = "#00AEEF"
BEKO_GRAY = "#F5F7FA"
TEXT_DARK = "#172033"
WARNING_BG = "#FFF7E6"
DANGER = "#D92D20"
SUCCESS = "#12B76A"


# ==============================
# CSS
# ==============================

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
            color: #667085;
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


# ==============================
# HELPERS
# ==============================

def safe_text(value, default=""):
    if value is None:
        return default

    try:
        if pd.isna(value):
            return default
    except Exception:
        pass

    text = str(value).strip()

    if text.lower() in ["nan", "none", "nat"]:
        return default

    return text


def safe_int(value, default=0):
    try:
        if pd.isna(value):
            return default
        return int(value)
    except Exception:
        return default


def safe_float(value, default=0.0):
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def to_python_value(value):
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except Exception:
        pass

    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            return value

    return value


def ensure_columns(df):
    defaults = {
        "comment_link": "",
        "complaint_title": "",
        "complaint_text": "",
        "category": "Belirsiz",
        "product_name": "Belirsiz",
        "view_count": 0,
        "support_count": 0,
        "company_response_flag": 0,
        "brand_response_text": "",
        "update_comment": "",
        "customer_reply_text": "",
        "response_depth": 0,
        "has_brand_response": 0,
        "has_customer_reply_after_response": 0,
        "complaint_context": "",
        "after_response_context": "",
        "full_context": "",
        "legal_risk": 0,
        "detected_department": "Belirsiz",
        "detected_fault_type": "Belirsiz",
        "rule_resolution_status": "Belirsiz",
        "rule_satisfaction_score": 3,
        "recommended_action": "Şikayet manuel incelemeye yönlendirilmeli."
    }

    for col, default in defaults.items():
        if col not in df.columns:
            df[col] = default

    return df


def normalize_numeric_columns(df):
    numeric_cols = [
        "view_count",
        "support_count",
        "company_response_flag",
        "response_depth",
        "has_brand_response",
        "has_customer_reply_after_response",
        "legal_risk",
        "rule_satisfaction_score"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["legal_risk"] = df["legal_risk"].astype(int)
    df["rule_satisfaction_score"] = df["rule_satisfaction_score"].astype(int)

    return df


def minmax(series):
    series = pd.to_numeric(series, errors="coerce").fillna(0)

    min_value = series.min()
    max_value = series.max()

    if max_value == min_value:
        return pd.Series([0] * len(series), index=series.index)

    return (series - min_value) / (max_value - min_value)


def add_priority_score(df):
    unresolved = df["rule_resolution_status"].isin(["Çözülmedi"]).astype(int)
    partial = df["rule_resolution_status"].isin(["Kısmen Çözüldü"]).astype(int)
    no_reply = df["rule_resolution_status"].isin(["Müşteri Dönüşü Yok"]).astype(int)
    low_satisfaction = (df["rule_satisfaction_score"] <= 2).astype(int)

    view_score = minmax(df["view_count"])
    support_score = minmax(df["support_count"])

    df["priority_score"] = (
        df["legal_risk"] * 35
        + unresolved * 30
        + low_satisfaction * 20
        + partial * 8
        + no_reply * 5
        + view_score * 5
        + support_score * 5
    ).round(2)

    return df


@st.cache_data(show_spinner=False)
def load_data():
    df = read_table(COMPLAINT_ANALYSIS_TABLE)
    df = ensure_columns(df)
    df = normalize_numeric_columns(df)
    df = add_priority_score(df)

    text_cols = [
        "comment_link",
        "complaint_title",
        "complaint_text",
        "category",
        "product_name",
        "brand_response_text",
        "customer_reply_text",
        "detected_department",
        "detected_fault_type",
        "rule_resolution_status",
        "recommended_action"
    ]

    for col in text_cols:
        df[col] = df[col].fillna("").astype(str)

    return df


def metric_card(title, value, help_text=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-help">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_header(title, desc=""):
    st.markdown(
        f"""
        <div class="section-title">{title}</div>
        <div class="section-desc">{desc}</div>
        """,
        unsafe_allow_html=True
    )


def empty_state():
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-title">Bu filtre kombinasyonunda veri bulunamadı</div>
            <div class="empty-text">
                Seçtiğin kategori, ürün, departman, çözüm durumu veya arama metni birlikte eşleşen sonuç üretmedi.
                Filtreleri biraz genişletip tekrar deneyebilirsin. Uygulama hata vermedi; sadece seçili koşullara uygun kayıt yok.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def value_counts_df(df, column, top_n=15, name="count"):
    if column not in df.columns or df.empty:
        return pd.DataFrame(columns=[column, name])

    result = (
        df[column]
        .fillna("Belirsiz")
        .replace("", "Belirsiz")
        .value_counts()
        .head(top_n)
        .reset_index()
    )

    result.columns = [column, name]
    return result


def plot_bar(data, x, y, title, x_title="", y_title="Şikayet Sayısı"):
    if data.empty:
        st.info("Bu grafik için gösterilecek veri bulunamadı.")
        return

    if PLOTLY_AVAILABLE:
        fig = px.bar(
            data,
            x=x,
            y=y,
            text=y,
            color_discrete_sequence=[BEKO_BLUE]
        )

        fig.update_traces(
            textposition="outside",
            marker_line_width=0,
            opacity=0.92
        )

        fig.update_layout(
            title={
                "text": title,
                "font": {"size": 18, "color": BEKO_DARK},
                "x": 0.02,
                "xanchor": "left"
            },
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis_title=x_title,
            yaxis_title=y_title,
            margin=dict(l=20, r=20, t=70, b=100),
            height=430,
            font=dict(color=TEXT_DARK, size=13),
            xaxis=dict(
                tickangle=-35,
                title_font=dict(color=TEXT_DARK, size=14),
                tickfont=dict(color=TEXT_DARK, size=11),
                gridcolor="#E6EEF8",
                linecolor="#D0D5DD"
            ),
            yaxis=dict(
                title_font=dict(color=TEXT_DARK, size=14),
                tickfont=dict(color=TEXT_DARK, size=12),
                gridcolor="#E6EEF8",
                linecolor="#D0D5DD"
            ),
            legend=dict(
                font=dict(color=TEXT_DARK)
            )
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.bar_chart(data.set_index(x)[y])


def plot_donut(data, names, values, title):
    if data.empty:
        st.info("Bu grafik için gösterilecek veri bulunamadı.")
        return

    if PLOTLY_AVAILABLE:
        fig = px.pie(
            data,
            names=names,
            values=values,
            hole=0.55,
            color_discrete_sequence=[
                BEKO_BLUE,
                BEKO_CYAN,
                "#6BA3FF",
                "#98D9FF",
                "#B6D7FF",
                "#D6E9FF"
            ]
        )

        fig.update_layout(
            title={
                "text": title,
                "font": {"size": 18, "color": BEKO_DARK},
                "x": 0.02,
                "xanchor": "left"
            },
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=70, b=20),
            height=430,
            font=dict(color=TEXT_DARK, size=13),
            legend=dict(
                font=dict(color=TEXT_DARK, size=12)
            )
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            textfont=dict(color="white", size=12)
        )

        fig.update_traces(textposition="inside", textinfo="percent+label")

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.dataframe(data, use_container_width=True)


def plot_score_gauge(score):
    score = safe_float(score, 0)

    if not PLOTLY_AVAILABLE:
        st.metric("Ortalama Memnuniyet", round(score, 2))
        return

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"font": {"size": 40, "color": BEKO_DARK}},
            gauge={
                "axis": {"range": [0, 5]},
                "bar": {"color": BEKO_BLUE},
                "steps": [
                    {"range": [0, 2], "color": "#FEE4E2"},
                    {"range": [2, 3.5], "color": "#FEF0C7"},
                    {"range": [3.5, 5], "color": "#D1FADF"}
                ],
                "threshold": {
                    "line": {"color": BEKO_DARK, "width": 4},
                    "thickness": 0.8,
                    "value": score
                }
            },
            title={"text": "Ortalama Memnuniyet", "font": {"size": 18, "color": BEKO_DARK}}
        )
    )

    fig.update_layout(
        height=330,
        margin=dict(l=20, r=20, t=70, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=TEXT_DARK)
    )

    st.plotly_chart(fig, use_container_width=True)


def make_download_csv(df):
    return df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")


def format_option(row):
    title = safe_text(row.get("complaint_title", "Başlık yok"))
    product = safe_text(row.get("product_name", "Ürün yok"))
    status = safe_text(row.get("rule_resolution_status", "Belirsiz"))

    if len(title) > 85:
        title = title[:85] + "..."

    return f"{product} | {status} | {title}"


# ==============================
# DATA LOAD
# ==============================

try:
    df = load_data()
except Exception as e:
    st.error("Veri yüklenirken hata oluştu.")
    st.code(str(e))
    st.stop()


if df.empty:
    st.warning("Veritabanında gösterilecek kayıt bulunamadı. Önce pipeline dosyalarını çalıştırmalısın.")
    st.code("python scripts/run_pipeline.py")
    st.stop()


# ==============================
# HEADER
# ==============================

logo_path = ROOT_DIR / "app" / "assets" / "beko_logo.png"

header_left, header_right = st.columns([5, 1])

with header_left:
    st.markdown(
        """
        <div class="main-header">
            <div class="badge">AI Destekli Müşteri Deneyimi Analitiği</div>
            <div class="main-title">Beko Müşteri Sesi Zekâ Platformu</div>
            <div class="main-subtitle">
                Şikayetvar verilerinden ürün, kategori, memnuniyet, çözüm durumu, departman yönlendirme,
                arıza tipi ve hukuki risk içgörüleri üreten karar destek paneli.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with header_right:
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
    else:
        st.markdown(
            f"""
            <div style="
                background:white;
                border:1px solid #D6E9FF;
                border-radius:24px;
                padding:30px 12px;
                text-align:center;
                box-shadow:0 10px 25px rgba(16,24,40,0.055);
            ">
                <div style="color:{BEKO_BLUE};font-size:30px;font-weight:900;">beko</div>
                <div style="font-size:12px;color:#667085;margin-top:4px;">logo için app/assets/beko_logo.png</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==============================
# SIDEBAR FILTERS
# ==============================

with st.sidebar:
    st.markdown("## 🔎 Filtre Paneli")
    st.caption("Boş seçimler tüm kayıtları kapsar.")

    search_text = st.text_input(
        "Metin içinde ara",
        placeholder="ör. servis, iade, soğutmuyor..."
    )

    category_options = sorted([x for x in df["category"].dropna().unique().tolist() if safe_text(x)])
    selected_categories = st.multiselect(
        "Kategori",
        options=category_options,
        default=[]
    )

    temp_for_product = df.copy()
    if selected_categories:
        temp_for_product = temp_for_product[temp_for_product["category"].isin(selected_categories)]

    product_options = sorted([x for x in temp_for_product["product_name"].dropna().unique().tolist() if safe_text(x)])
    selected_products = st.multiselect(
        "Ürün",
        options=product_options,
        default=[]
    )

    department_options = sorted([x for x in df["detected_department"].dropna().unique().tolist() if safe_text(x)])
    selected_departments = st.multiselect(
        "Departman",
        options=department_options,
        default=[]
    )

    resolution_options = sorted([x for x in df["rule_resolution_status"].dropna().unique().tolist() if safe_text(x)])
    selected_resolutions = st.multiselect(
        "Çözüm Durumu",
        options=resolution_options,
        default=[]
    )

    fault_options = sorted([x for x in df["detected_fault_type"].dropna().unique().tolist() if safe_text(x)])
    selected_faults = st.multiselect(
        "Arıza Tipi",
        options=fault_options,
        default=[]
    )

    legal_filter = st.selectbox(
        "Hukuki Risk",
        ["Tümü", "Risk Var", "Risk Yok"]
    )

    min_score, max_score = st.slider(
        "Memnuniyet Skoru Aralığı",
        min_value=1,
        max_value=5,
        value=(1, 5)
    )

    min_priority = st.slider(
        "Minimum Öncelik Skoru",
        min_value=0,
        max_value=100,
        value=0
    )

    st.markdown("---")
    st.caption("Demo önerisi: önce hukuki risk + çözülmedi filtrelerini göster, sonra tek şikayet analizi ekranına geç.")


# ==============================
# APPLY FILTERS
# ==============================

filtered = df.copy()

if selected_categories:
    filtered = filtered[filtered["category"].isin(selected_categories)]

if selected_products:
    filtered = filtered[filtered["product_name"].isin(selected_products)]

if selected_departments:
    filtered = filtered[filtered["detected_department"].isin(selected_departments)]

if selected_resolutions:
    filtered = filtered[filtered["rule_resolution_status"].isin(selected_resolutions)]

if selected_faults:
    filtered = filtered[filtered["detected_fault_type"].isin(selected_faults)]

if legal_filter == "Risk Var":
    filtered = filtered[filtered["legal_risk"] == 1]
elif legal_filter == "Risk Yok":
    filtered = filtered[filtered["legal_risk"] == 0]

filtered = filtered[
    (filtered["rule_satisfaction_score"] >= min_score)
    & (filtered["rule_satisfaction_score"] <= max_score)
]

filtered = filtered[filtered["priority_score"] >= min_priority]

if search_text.strip():
    q = search_text.lower().strip()

    search_area = (
        filtered["complaint_title"].fillna("") + " "
        + filtered["complaint_text"].fillna("") + " "
        + filtered["brand_response_text"].fillna("") + " "
        + filtered["customer_reply_text"].fillna("") + " "
        + filtered["product_name"].fillna("") + " "
        + filtered["category"].fillna("")
    ).str.lower()

    filtered = filtered[search_area.str.contains(q, na=False)]


# ==============================
# EMPTY FILTER RESULT
# ==============================

if filtered.empty:
    empty_state()

    st.markdown("### Filtreleri genişletmek için öneriler")
    st.info(
        """
        - Ürün filtresini kaldırıp sadece kategoriyle dene.
        - Hukuki risk filtresini “Tümü” yap.
        - Minimum öncelik skorunu düşür.
        - Arama kutusundaki kelimeyi daha genel yaz. Örneğin “servis gelmedi” yerine “servis”.
        """
    )

    st.markdown("### Genel veri özeti")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Toplam Şikayet", f"{len(df):,}".replace(",", "."), "Tüm veri seti")
    with col2:
        metric_card("Kategori", df["category"].nunique(), "Tüm veri seti")
    with col3:
        metric_card("Ürün", df["product_name"].nunique(), "Tüm veri seti")
    with col4:
        metric_card("Hukuki Risk", int(df["legal_risk"].sum()), "Tüm veri seti")

    st.stop()


# ==============================
# EXECUTIVE METRICS
# ==============================

total_count = len(filtered)
product_count = filtered["product_name"].nunique()
category_count = filtered["category"].nunique()
legal_count = int(filtered["legal_risk"].sum())
unresolved_count = int((filtered["rule_resolution_status"] == "Çözülmedi").sum())
avg_satisfaction = round(float(filtered["rule_satisfaction_score"].mean()), 2)
avg_priority = round(float(filtered["priority_score"].mean()), 2)

response_rate = round(float(filtered["has_brand_response"].mean() * 100), 1)
customer_reply_rate = round(float(filtered["has_customer_reply_after_response"].mean() * 100), 1)

st.markdown("## Yönetici Özeti")

m1, m2, m3, m4, m5, m6 = st.columns(6)

with m1:
    metric_card("Şikayet", f"{total_count:,}".replace(",", "."), "Filtrelenmiş kayıt")
with m2:
    metric_card("Ürün", product_count, "Etkilenen ürün")
with m3:
    metric_card("Kategori", category_count, "Ürün grubu")
with m4:
    metric_card("Hukuki Risk", legal_count, "Öncelikli takip")
with m5:
    metric_card("Çözülmedi", unresolved_count, "Negatif kapanış")
with m6:
    metric_card("Memnuniyet", avg_satisfaction, "1-5 arası skor")

st.markdown("")


# ==============================
# TABS
# ==============================

tab_overview, tab_priority, tab_explorer, tab_single, tab_download = st.tabs(
    [
        "📊 Genel Görünüm",
        "🚨 Öncelikli Aksiyonlar",
        "🔍 Şikayet Gezgini",
        "🧠 Tek Şikayet Analizi",
        "📥 Çıktılar"
    ]
)


# ==============================
# TAB 1: OVERVIEW
# ==============================

with tab_overview:
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header(
            "Kategori ve Ürün Yoğunluğu",
            "Hangi kategori ve ürünlerde şikayetlerin yoğunlaştığını gösterir."
        )

        c1, c2 = st.columns(2)

        with c1:
            category_counts = value_counts_df(filtered, "category", top_n=12, name="complaint_count")
            plot_bar(
                category_counts,
                x="category",
                y="complaint_count",
                title="Kategori Bazlı Şikayet Sayısı",
                x_title="Kategori"
            )

        with c2:
            product_counts = value_counts_df(filtered, "product_name", top_n=12, name="complaint_count")
            plot_bar(
                product_counts,
                x="product_name",
                y="complaint_count",
                title="En Çok Şikayet Alan Ürünler",
                x_title="Ürün"
            )

        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header(
            "Memnuniyet Göstergesi",
            "Filtrelenmiş veride ortalama memnuniyet skoru."
        )
        plot_score_gauge(avg_satisfaction)

        st.markdown(
            f"""
            <div class="small-note">
                Marka yanıt oranı: <b>{response_rate}%</b><br>
                Yanıt sonrası müşteri dönüş oranı: <b>{customer_reply_rate}%</b><br>
                Ortalama öncelik skoru: <b>{avg_priority}</b>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    section_header(
        "Operasyonel Dağılım",
        "Şikayetlerin departman, çözüm durumu ve arıza tipine göre dağılımı."
    )

    d1, d2, d3 = st.columns(3)

    with d1:
        department_counts = value_counts_df(filtered, "detected_department", top_n=10, name="complaint_count")
        plot_donut(
            department_counts,
            names="detected_department",
            values="complaint_count",
            title="Departman Yönlendirme"
        )

    with d2:
        resolution_counts = value_counts_df(filtered, "rule_resolution_status", top_n=10, name="complaint_count")
        plot_donut(
            resolution_counts,
            names="rule_resolution_status",
            values="complaint_count",
            title="Çözüm Durumu"
        )

    with d3:
        fault_counts = value_counts_df(filtered, "detected_fault_type", top_n=10, name="complaint_count")
        plot_donut(
            fault_counts,
            names="detected_fault_type",
            values="complaint_count",
            title="Arıza Tipi"
        )

    st.markdown('</div>', unsafe_allow_html=True)


# ==============================
# TAB 2: PRIORITY ACTIONS
# ==============================

with tab_priority:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    section_header(
        "Öncelikli İncelenmesi Gereken Şikayetler",
        "Hukuki risk, çözülmeme durumu, düşük memnuniyet, görüntülenme ve destek sayısına göre sıralanır."
    )

    priority_df = filtered.sort_values(
        by=["priority_score", "legal_risk", "support_count", "view_count"],
        ascending=[False, False, False, False]
    ).copy()

    priority_columns = [
        "priority_score",
        "product_name",
        "category",
        "complaint_title",
        "rule_resolution_status",
        "rule_satisfaction_score",
        "detected_department",
        "detected_fault_type",
        "legal_risk",
        "view_count",
        "support_count",
        "recommended_action",
        "comment_link"
    ]

    existing_priority_columns = [col for col in priority_columns if col in priority_df.columns]

    st.dataframe(
        priority_df[existing_priority_columns].head(150),
        use_container_width=True,
        hide_index=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    section_header(
        "Aksiyon Dağılımı",
        "Sistemin önerdiği aksiyonların yoğunluğunu gösterir."
    )

    action_counts = value_counts_df(filtered, "recommended_action", top_n=12, name="complaint_count")
    plot_bar(
        action_counts,
        x="recommended_action",
        y="complaint_count",
        title="Önerilen Aksiyonlar",
        x_title="Aksiyon"
    )

    st.markdown('</div>', unsafe_allow_html=True)


# ==============================
# TAB 3: EXPLORER
# ==============================

with tab_explorer:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    section_header(
        "Şikayet Gezgini",
        "Filtrelenmiş veriyi incelemek, sıralamak ve dışa aktarmak için kullanılır."
    )

    sort_column = st.selectbox(
        "Sıralama kriteri",
        [
            "priority_score",
            "view_count",
            "support_count",
            "rule_satisfaction_score",
            "response_depth"
        ],
        index=0
    )

    sort_order = st.radio(
        "Sıralama yönü",
        ["Büyükten küçüğe", "Küçükten büyüğe"],
        horizontal=True
    )

    explorer_df = filtered.sort_values(
        by=sort_column,
        ascending=True if sort_order == "Küçükten büyüğe" else False
    )

    explorer_columns = [
        "product_name",
        "category",
        "complaint_title",
        "rule_resolution_status",
        "rule_satisfaction_score",
        "detected_department",
        "detected_fault_type",
        "legal_risk",
        "priority_score",
        "view_count",
        "support_count",
        "recommended_action",
        "comment_link"
    ]

    existing_explorer_columns = [col for col in explorer_columns if col in explorer_df.columns]

    st.dataframe(
        explorer_df[existing_explorer_columns],
        use_container_width=True,
        hide_index=True,
        height=620
    )

    st.markdown('</div>', unsafe_allow_html=True)


# ==============================
# TAB 4: SINGLE COMPLAINT
# ==============================

with tab_single:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    section_header(
        "Tek Şikayet Analizi",
        "Bir şikayeti seçerek müşteri metni, Beko yanıtı, tüketici dönüşleri ve sistem çıktısını birlikte inceleyebilirsin."
    )

    single_df = filtered.sort_values("priority_score", ascending=False).copy()

    if single_df.empty:
        st.info("Tek şikayet incelemek için uygun kayıt bulunamadı.")
    else:
        option_map = {
            idx: format_option(row)
            for idx, row in single_df.iterrows()
        }

        selected_idx = st.selectbox(
            "İncelenecek şikayeti seç",
            options=list(option_map.keys()),
            format_func=lambda x: option_map[x]
        )

        row = single_df.loc[selected_idx]

        top_a, top_b, top_c, top_d = st.columns(4)

        with top_a:
            metric_card("Öncelik Skoru", safe_float(row["priority_score"]), "Risk + etkileşim")
        with top_b:
            metric_card("Memnuniyet", safe_int(row["rule_satisfaction_score"]), "1-5 arası")
        with top_c:
            metric_card("Görüntülenme", safe_int(row["view_count"]), "İtibar etkisi")
        with top_d:
            metric_card("Destek", safe_int(row["support_count"]), "Kullanıcı desteği")

        st.markdown("")

        text_col1, text_col2, text_col3 = st.columns(3)

        with text_col1:
            st.markdown(
                f"""
                <div class="complaint-box">
                    <div class="box-title">Müşteri Şikayeti</div>
                    <div>{safe_text(row["complaint_text"], "Şikayet metni bulunamadı.")}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with text_col2:
            brand_response = safe_text(row["brand_response_text"])

            if not brand_response:
                brand_response = "Beko yanıtı bulunamadı."

            st.markdown(
                f"""
                <div class="response-box">
                    <div class="box-title">Beko Yanıtı</div>
                    <div>{brand_response}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with text_col3:
            customer_reply = safe_text(row["customer_reply_text"])

            if not customer_reply:
                customer_reply = "Beko cevabından sonra tüketici dönüşü yok."

            st.markdown(
                f"""
                <div class="customer-box">
                    <div class="box-title">Tüketici Cevapları</div>
                    <div>{customer_reply}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### Sistem Çıktısı")

        system_output = {
            "Ürün": to_python_value(row["product_name"]),
            "Kategori": to_python_value(row["category"]),
            "Çözüm Durumu": to_python_value(row["rule_resolution_status"]),
            "Memnuniyet Skoru": safe_int(row["rule_satisfaction_score"]),
            "Tahmini Departman": to_python_value(row["detected_department"]),
            "Tahmini Arıza Tipi": to_python_value(row["detected_fault_type"]),
            "Hukuki Risk": "Var" if safe_int(row["legal_risk"]) == 1 else "Yok",
            "Öncelik Skoru": safe_float(row["priority_score"]),
            "Önerilen Aksiyon": to_python_value(row["recommended_action"])
        }

        st.json(system_output)

        link = safe_text(row.get("comment_link", ""))

        if link:
            st.link_button("Şikayet Kaynağını Aç", link)

    st.markdown('</div>', unsafe_allow_html=True)


# ==============================
# TAB 5: DOWNLOADS
# ==============================

with tab_download:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    section_header(
        "Çıktılar",
        "Filtrelenmiş sonuçları CSV olarak indirebilir veya demo için özet tabloyu kullanabilirsin."
    )

    export_columns = [
        "priority_score",
        "product_name",
        "category",
        "complaint_title",
        "complaint_text",
        "brand_response_text",
        "customer_reply_text",
        "rule_resolution_status",
        "rule_satisfaction_score",
        "detected_department",
        "detected_fault_type",
        "legal_risk",
        "view_count",
        "support_count",
        "recommended_action",
        "comment_link"
    ]

    existing_export_columns = [col for col in export_columns if col in filtered.columns]
    export_df = filtered[existing_export_columns].copy()

    st.download_button(
        label="Filtrelenmiş Analiz Sonuçlarını CSV İndir",
        data=make_download_csv(export_df),
        file_name="beko_musteri_sesi_analiz_sonuclari.csv",
        mime="text/csv"
    )

    st.markdown("### İndirilecek Önizleme")
    st.dataframe(export_df.head(100), use_container_width=True, hide_index=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ==============================
# FOOTER
# ==============================

st.markdown(
    f"""
    <div style="
        margin-top:28px;
        padding:18px 22px;
        border-radius:20px;
        background:{BEKO_LIGHT};
        border:1px solid #D6E9FF;
        color:#344054;
        font-size:13px;
    ">
        <b>Not:</b> Bu panel demo/prototip amaçlıdır. Kurumsal kullanımda KVKK uyumu için müşteri adı,
        telefon, adres ve kişisel bilgiler anonimleştirilmelidir. Kural tabanlı çıktılar daha sonra
        etiketli veri ve transformer tabanlı modellerle güçlendirilebilir.
    </div>
    """,
    unsafe_allow_html=True
)