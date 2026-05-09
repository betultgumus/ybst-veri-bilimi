import pandas as pd

from src.config import COMPLAINT_ANALYSIS_TABLE, REPORTS_DIR
from src.database import read_table


def save_value_counts(df, column, filename, new_col_name):
    if column not in df.columns:
        return

    result = df[column].value_counts(dropna=False).reset_index()
    result.columns = [column, new_col_name]
    result.to_csv(REPORTS_DIR / filename, index=False, encoding="utf-8-sig")


def basic_analysis():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    df = read_table(COMPLAINT_ANALYSIS_TABLE)

    summary = {
        "total_complaints": len(df),
        "unique_products": df["product_name"].nunique(),
        "unique_categories": df["category"].nunique(),
        "brand_response_count": int(df["has_brand_response"].sum()),
        "customer_reply_after_response_count": int(df["has_customer_reply_after_response"].sum()),
        "legal_risk_count": int(df["legal_risk"].sum()),
        "average_view_count": float(df["view_count"].mean()),
        "average_support_count": float(df["support_count"].mean()),
        "average_response_depth": float(df["response_depth"].mean())
    }

    summary_df = pd.DataFrame([summary])
    summary_df.to_csv(REPORTS_DIR / "summary_report.csv", index=False, encoding="utf-8-sig")

    save_value_counts(df, "product_name", "product_complaint_counts.csv", "complaint_count")
    save_value_counts(df, "category", "category_complaint_counts.csv", "complaint_count")
    save_value_counts(df, "detected_department", "department_counts.csv", "complaint_count")
    save_value_counts(df, "detected_fault_type", "fault_type_counts.csv", "complaint_count")
    save_value_counts(df, "rule_resolution_status", "resolution_status_counts.csv", "complaint_count")
    save_value_counts(df, "rule_satisfaction_score", "satisfaction_score_counts.csv", "complaint_count")

    product_resolution = df.groupby("product_name").agg(
        complaint_count=("comment_link", "count"),
        avg_satisfaction=("rule_satisfaction_score", "mean"),
        legal_risk_count=("legal_risk", "sum"),
        avg_view_count=("view_count", "mean"),
        avg_support_count=("support_count", "mean")
    ).reset_index().sort_values("complaint_count", ascending=False)

    product_resolution.to_csv(
        REPORTS_DIR / "product_level_insights.csv",
        index=False,
        encoding="utf-8-sig"
    )

    category_resolution = df.groupby("category").agg(
        complaint_count=("comment_link", "count"),
        avg_satisfaction=("rule_satisfaction_score", "mean"),
        legal_risk_count=("legal_risk", "sum"),
        avg_view_count=("view_count", "mean"),
        avg_support_count=("support_count", "mean")
    ).reset_index().sort_values("complaint_count", ascending=False)

    category_resolution.to_csv(
        REPORTS_DIR / "category_level_insights.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("Temel analiz tamamlandı.")
    print(summary_df)


if __name__ == "__main__":
    basic_analysis()