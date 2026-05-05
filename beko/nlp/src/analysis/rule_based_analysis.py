import pandas as pd

from src.config import COMPLAINT_ANALYSIS_TABLE, REPORTS_DIR
from src.database import read_table, write_df_to_table


LEGAL_KEYWORDS = [
    "tüketici hakem heyeti", "hakem heyeti", "thh", "mahkeme",
    "dava", "avukat", "ihtarname", "cimer", "yasal süreç",
    "hukuki", "savcılık", "şikayet edeceğim", "yasal hak",
    "tüketici mahkemesi", "noter", "icra"
]


POSITIVE_RESOLUTION_KEYWORDS = [
    "teşekkür ederim", "teşekkürler", "sorunum çözüldü", "çözüldü",
    "yardımcı oldular", "memnun kaldım", "ürün değiştirildi",
    "para iadesi yapıldı", "iadem yapıldı", "servis geldi",
    "problem giderildi", "şikayetim çözüldü"
]


NEGATIVE_RESOLUTION_KEYWORDS = [
    "çözülmedi", "sorun devam ediyor", "hala çözülmedi", "geri dönüş yapılmadı",
    "aranmadım", "servis gelmedi", "mağdurum", "hiçbir çözüm",
    "çözüm sunulmadı", "ilgilenilmedi", "bekliyorum", "dönüş yok",
    "tekrar arıza", "aynı sorun", "sonuç alamadım"
]


PARTIAL_RESOLUTION_KEYWORDS = [
    "kısmen", "servis geldi ama", "arıza tekrar etti", "geçici olarak",
    "bir süre düzeldi", "tam çözülmedi", "beklemedeyim"
]


DEPARTMENT_RULES = {
    "Teknik Servis": [
        "servis", "teknik", "tamir", "onarım", "montaj", "kurulum",
        "arıza", "parça", "usta", "yetkili servis", "randevu"
    ],
    "Lojistik": [
        "kargo", "teslimat", "geç geldi", "hasarlı geldi",
        "nakliye", "sevkiyat", "teslim edilmedi", "lojistik",
        "kırık geldi", "çizik geldi"
    ],
    "İade / Değişim": [
        "iade", "değişim", "para iadesi", "ürün değişimi",
        "cayma", "iptal", "değişim talebi", "iade talebi"
    ],
    "Garanti": [
        "garanti", "garanti dışı", "ücretli servis", "kapsam dışı",
        "garanti kapsamı", "ek garanti"
    ],
    "Çağrı Merkezi": [
        "müşteri hizmetleri", "çağrı merkezi", "aranmadım",
        "iletişim", "telefon", "kayıt açıldı", "geri dönüş"
    ],
    "Bayi / Satış": [
        "bayi", "satıcı", "mağaza", "satış", "kampanya", "fiyat",
        "fatura", "sipariş"
    ],
    "Hukuk / Uyum": LEGAL_KEYWORDS
}


FAULT_RULES = {
    "Soğutmama Problemi": [
        "soğutmuyor", "soğutma", "buzdolabı soğutmuyor",
        "dolap soğutmuyor", "yiyecekler bozuldu", "dondurmuyor"
    ],
    "Su Alma Problemi": [
        "su almıyor", "su dolmuyor", "su gelmiyor"
    ],
    "Su Boşaltma Problemi": [
        "su boşaltmıyor", "tahliye", "suyu atmıyor", "su akıtıyor"
    ],
    "Sıkma Problemi": [
        "sıkma yapmıyor", "sıkmıyor", "çamaşır ıslak"
    ],
    "Ses / Gürültü Problemi": [
        "ses yapıyor", "gürültü", "çok ses", "uğultu", "takırtı"
    ],
    "Ekran / Panel Problemi": [
        "ekran", "panel", "görüntü yok", "ekran karardı", "ışık yanmıyor"
    ],
    "Isıtma Problemi": [
        "ısıtmıyor", "ısıtma yapmıyor", "sıcak su vermiyor"
    ],
    "Koku Problemi": [
        "koku", "yanık kokusu", "kötü koku", "plastik kokusu"
    ],
    "Kurutma Problemi": [
        "kurutmuyor", "kurutma yapmıyor", "ıslak çıkarıyor"
    ],
    "Çekim Gücü Problemi": [
        "çekmiyor", "çekim gücü", "emiş gücü", "süpürge çekmiyor"
    ]
}


def normalize(text):
    if pd.isna(text):
        return ""
    return str(text).lower()


def contains_any(text, keywords):
    text = normalize(text)
    return any(keyword in text for keyword in keywords)


def detect_legal_risk(text):
    return 1 if contains_any(text, LEGAL_KEYWORDS) else 0


def detect_resolution_status(after_response_text, full_context):
    after_response_text = normalize(after_response_text)
    full_context = normalize(full_context)

    if contains_any(after_response_text, POSITIVE_RESOLUTION_KEYWORDS):
        return "Çözüldü"

    if contains_any(after_response_text, PARTIAL_RESOLUTION_KEYWORDS):
        return "Kısmen Çözüldü"

    if contains_any(after_response_text, NEGATIVE_RESOLUTION_KEYWORDS):
        return "Çözülmedi"

    if after_response_text.strip() == "":
        return "Müşteri Dönüşü Yok"

    if contains_any(full_context, NEGATIVE_RESOLUTION_KEYWORDS):
        return "Çözülmedi"

    return "Belirsiz"


def detect_satisfaction_score(resolution_status, after_response_text, full_context):
    text = normalize(after_response_text + " " + full_context)

    if resolution_status == "Çözüldü":
        return 5

    if resolution_status == "Kısmen Çözüldü":
        return 3

    if resolution_status == "Çözülmedi":
        return 1

    if contains_any(text, ["teşekkür", "memnun", "çözüldü"]):
        return 4

    if contains_any(text, ["mağdur", "rezalet", "şikayetçiyim", "pişman", "asla", "çözüm yok"]):
        return 1

    return 3


def detect_department(text):
    text = normalize(text)
    scores = {}

    for department, keywords in DEPARTMENT_RULES.items():
        score = sum(1 for keyword in keywords if keyword in text)
        scores[department] = score

    best_department = max(scores, key=scores.get)

    if scores[best_department] == 0:
        return "Belirsiz"

    return best_department


def detect_fault_type(text):
    text = normalize(text)

    for fault_type, keywords in FAULT_RULES.items():
        if any(keyword in text for keyword in keywords):
            return fault_type

    return "Belirsiz"


def recommend_action(row):
    department = row["detected_department"]
    legal_risk = row["legal_risk"]
    resolution = row["rule_resolution_status"]
    fault = row["detected_fault_type"]

    if legal_risk == 1:
        return "Hukuk/Uyum birimine öncelikli inceleme ve müşteriyle hızlı iletişim önerilir."

    if resolution == "Çözülmedi" and department == "Teknik Servis":
        return "Teknik servis süreci hızlandırılmalı ve müşteri yeniden aranmalı."

    if resolution == "Çözülmedi" and department == "İade / Değişim":
        return "İade/değişim talebi operasyon ekibi tarafından yeniden değerlendirilmeli."

    if department == "Lojistik":
        return "Teslimat/hasar süreci lojistik birimi tarafından kontrol edilmeli."

    if fault != "Belirsiz":
        return f"{fault} için teknik kök neden analizi yapılmalı."

    return "Şikayet manuel incelemeye yönlendirilmeli."


def apply_rule_based_analysis():
    df = read_table(COMPLAINT_ANALYSIS_TABLE)

    df["legal_risk"] = df["full_context"].apply(detect_legal_risk)

    df["rule_resolution_status"] = df.apply(
        lambda row: detect_resolution_status(
            row["after_response_context"],
            row["full_context"]
        ),
        axis=1
    )

    df["rule_satisfaction_score"] = df.apply(
        lambda row: detect_satisfaction_score(
            row["rule_resolution_status"],
            row["after_response_context"],
            row["full_context"]
        ),
        axis=1
    )

    df["detected_department"] = df["full_context"].apply(detect_department)
    df["detected_fault_type"] = df["full_context"].apply(detect_fault_type)

    df["recommended_action"] = df.apply(recommend_action, axis=1)

    write_df_to_table(df, COMPLAINT_ANALYSIS_TABLE)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    legal_df = df[df["legal_risk"] == 1]
    legal_df.to_csv(REPORTS_DIR / "legal_risk_complaints.csv", index=False, encoding="utf-8-sig")

    print("Kural tabanlı analiz tamamlandı.")
    print(df[[
        "product_name",
        "rule_resolution_status",
        "rule_satisfaction_score",
        "detected_department",
        "detected_fault_type",
        "legal_risk",
        "recommended_action"
    ]].head())


if __name__ == "__main__":
    apply_rule_based_analysis()