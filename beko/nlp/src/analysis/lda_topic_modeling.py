import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from src.config import COMPLAINT_ANALYSIS_TABLE, REPORTS_DIR
from src.database import read_table


def run_lda_topic_modeling(n_topics=10, n_words=15):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    df = read_table(COMPLAINT_ANALYSIS_TABLE)

    texts = df["clean_complaint_text"].fillna("")

    vectorizer = CountVectorizer(
        max_df=0.90,
        min_df=5,
        max_features=7000
    )

    X = vectorizer.fit_transform(texts)

    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42,
        learning_method="batch"
    )

    topic_matrix = lda.fit_transform(X)

    words = vectorizer.get_feature_names_out()

    topic_rows = []

    for topic_idx, topic in enumerate(lda.components_):
        top_indices = topic.argsort()[-n_words:][::-1]
        top_words = [words[i] for i in top_indices]

        topic_rows.append({
            "topic_id": topic_idx,
            "top_words": ", ".join(top_words)
        })

    topic_df = pd.DataFrame(topic_rows)
    topic_df.to_csv(REPORTS_DIR / "topic_results.csv", index=False, encoding="utf-8-sig")

    df["dominant_topic"] = topic_matrix.argmax(axis=1)
    df[[
        "comment_link",
        "product_name",
        "category",
        "complaint_title",
        "dominant_topic",
        "detected_department",
        "detected_fault_type",
        "rule_resolution_status",
        "rule_satisfaction_score"
    ]].to_csv(REPORTS_DIR / "complaints_with_topics.csv", index=False, encoding="utf-8-sig")

    print("LDA konu modelleme tamamlandı.")
    print(topic_df)


if __name__ == "__main__":
    run_lda_topic_modeling()