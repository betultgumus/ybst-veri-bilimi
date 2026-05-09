from src.etl.load_raw_to_sqlite import load_raw_data
from src.etl.build_analysis_tables import main as build_tables
from src.analysis.rule_based_analysis import apply_rule_based_analysis
from src.analysis.basic_analysis import basic_analysis
from src.analysis.lda_topic_modeling import run_lda_topic_modeling


def main():
    load_raw_data()
    build_tables()
    apply_rule_based_analysis()
    basic_analysis()
    run_lda_topic_modeling(n_topics=10, n_words=15)

    print("Tüm pipeline başarıyla tamamlandı.")


if __name__ == "__main__":
    main()