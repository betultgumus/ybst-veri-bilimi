import re
import pandas as pd


TURKISH_STOPWORDS = {
    "ve", "veya", "ile", "ama", "fakat", "çünkü", "bu", "şu", "o",
    "bir", "de", "da", "ki", "mi", "mı", "mu", "mü", "için",
    "gibi", "daha", "çok", "az", "ben", "biz", "siz", "onlar",
    "olarak", "olan", "oldu", "oluyor", "var", "yok", "her", "hiç",
    "beni", "bana", "size", "sizi", "kadar", "sonra", "önce"
}


def safe_text(value):
    if pd.isna(value):
        return ""
    return str(value)


def clean_text(text):
    text = safe_text(text).lower()

    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"[^a-zA-ZçğıöşüÇĞİÖŞÜ\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    words = text.split()
    words = [word for word in words if word not in TURKISH_STOPWORDS and len(word) > 2]

    return " ".join(words)


def combine_text_fields(row, columns):
    values = []

    for col in columns:
        if col in row.index:
            value = safe_text(row[col])
            if value.strip():
                values.append(value)

    return " ".join(values)