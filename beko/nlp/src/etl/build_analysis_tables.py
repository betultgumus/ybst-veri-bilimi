import pandas as pd

from src.config import (
    RAW_COMPLAINTS_TABLE,
    RAW_PRODUCTS_TABLE,
    COMPLAINT_ANALYSIS_TABLE,
    MERGED_ANALYSIS_TABLE,
    PROCESSED_DIR
)
from src.database import read_table, write_df_to_table
from src.preprocessing.text_cleaner import clean_text, combine_text_fields


REPLY_COLUMNS = [
    "Reply_to_Response_1_Message",
    "Reply_to_Response_2_Message",
    "Reply_to_Response_3_Message",
    "Reply_to_Response_4_Message",
    "Reply_to_Response_5_Message"
]

BASE_TEXT_COLUMNS = [
    "Complaint_Title",
    "Complaint",
    "Update_Comment",
    "Response_Message",
    "Reply_to_Response_1_Message",
    "Reply_to_Response_2_Message",
    "Reply_to_Response_3_Message",
    "Reply_to_Response_4_Message",
    "Reply_to_Response_5_Message"
]


def count_non_empty_replies(row):
    count = 0

    for col in REPLY_COLUMNS:
        if col in row.index and pd.notna(row[col]) and str(row[col]).strip():
            count += 1

    return count


def build_customer_reply_text(row):
    reply_parts = []

    for col in REPLY_COLUMNS:
        if col in row.index:
            value = row[col]
            if pd.notna(value) and str(value).strip():
                reply_parts.append(str(value))

    return " ".join(reply_parts)


def build_complaint_analysis_table():
    complaints = read_table(RAW_COMPLAINTS_TABLE)

    required_cols = [
        "Comment_Link",
        "Complaint_Title",
        "Complaint",
        "View_Count",
        "Support_Count",
        "Category",
        "Product_Name",
        "Company_Response",
        "Update_Comment",
        "Response_Message"
    ]

    for col in required_cols + REPLY_COLUMNS:
        if col not in complaints.columns:
            complaints[col] = None

    df = pd.DataFrame()

    df["comment_link"] = complaints["Comment_Link"]
    df["complaint_title"] = complaints["Complaint_Title"]
    df["complaint_text"] = complaints["Complaint"]
    df["category"] = complaints["Category"]
    df["product_name"] = complaints["Product_Name"]

    df["view_count"] = complaints["View_Count"]
    df["support_count"] = complaints["Support_Count"]

    df["company_response_flag"] = complaints["Company_Response"]
    df["brand_response_text"] = complaints["Response_Message"].fillna("")
    df["update_comment"] = complaints["Update_Comment"].fillna("")

    df["customer_reply_text"] = complaints.apply(build_customer_reply_text, axis=1)
    df["response_depth"] = complaints.apply(count_non_empty_replies, axis=1)

    df["has_brand_response"] = df["brand_response_text"].apply(
        lambda x: 1 if str(x).strip() else 0
    )

    df["has_customer_reply_after_response"] = df["customer_reply_text"].apply(
        lambda x: 1 if str(x).strip() else 0
    )

    df["complaint_context"] = complaints.apply(
        lambda row: combine_text_fields(row, ["Complaint_Title", "Complaint"]),
        axis=1
    )

    df["after_response_context"] = complaints.apply(
        lambda row: combine_text_fields(
            row,
            [
                "Update_Comment",
                "Reply_to_Response_1_Message",
                "Reply_to_Response_2_Message",
                "Reply_to_Response_3_Message",
                "Reply_to_Response_4_Message",
                "Reply_to_Response_5_Message"
            ]
        ),
        axis=1
    )

    df["full_context"] = complaints.apply(
        lambda row: combine_text_fields(row, BASE_TEXT_COLUMNS),
        axis=1
    )

    df["clean_complaint_text"] = df["complaint_context"].apply(clean_text)
    df["clean_after_response_text"] = df["after_response_context"].apply(clean_text)
    df["clean_full_context"] = df["full_context"].apply(clean_text)

    df["legal_risk"] = 0
    df["detected_department"] = "Belirsiz"
    df["detected_fault_type"] = "Belirsiz"
    df["rule_resolution_status"] = "Belirsiz"
    df["rule_satisfaction_score"] = 3
    df["recommended_action"] = ""

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DIR / "complaint_analysis.csv", index=False, encoding="utf-8-sig")

    write_df_to_table(df, COMPLAINT_ANALYSIS_TABLE)

    print("complaint_analysis tablosu oluşturuldu.")
    print(df.shape)
    print(df.head())


def build_merged_analysis_table():
    complaints = read_table(COMPLAINT_ANALYSIS_TABLE)
    products = read_table(RAW_PRODUCTS_TABLE)

    products.columns = [str(col).strip() for col in products.columns]

    if "Product_Name" not in products.columns:
        print("Ürün tablosunda Product_Name kolonu bulunamadı. Birleştirme sadece complaint_analysis üzerinden devam edecek.")
        merged = complaints.copy()
    else:
        merged = complaints.merge(
            products,
            left_on="product_name",
            right_on="Product_Name",
            how="left",
            suffixes=("", "_product")
        )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    merged.to_csv(PROCESSED_DIR / "merged_analysis.csv", index=False, encoding="utf-8-sig")

    write_df_to_table(merged, MERGED_ANALYSIS_TABLE)

    print("merged_analysis tablosu oluşturuldu.")
    print(merged.shape)


def main():
    build_complaint_analysis_table()
    build_merged_analysis_table()


if __name__ == "__main__":
    main()