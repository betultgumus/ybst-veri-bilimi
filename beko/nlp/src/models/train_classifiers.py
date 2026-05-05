import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from src.config import COMPLAINT_ANALYSIS_TABLE, MODELS_DIR
from src.database import read_table


def train_single_classifier(df, target_column, model_name):
    model_df = df[["clean_full_context", target_column]].dropna()

    if len(model_df) < 50:
        print(f"{target_column} için yeterli veri yok.")
        return

    if model_df[target_column].nunique() < 2:
        print(f"{target_column} için en az 2 farklı sınıf gerekli.")
        return

    X = model_df["clean_full_context"]
    y = model_df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=15000, ngram_range=(1, 2))),
        ("model", LogisticRegression(max_iter=1500, class_weight="balanced"))
    ])

    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)

    print("\n" + "=" * 70)
    print(f"Model: {model_name}")
    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODELS_DIR / f"{model_name}.pkl")


def train_all_models():
    df = read_table(COMPLAINT_ANALYSIS_TABLE)

    train_single_classifier(
        df=df,
        target_column="rule_satisfaction_score",
        model_name="satisfaction_model"
    )

    train_single_classifier(
        df=df,
        target_column="rule_resolution_status",
        model_name="resolution_model"
    )

    train_single_classifier(
        df=df,
        target_column="detected_department",
        model_name="department_model"
    )


if __name__ == "__main__":
    train_all_models()