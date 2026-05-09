import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.analysis.lda_topic_modeling import run_lda_topic_modeling

if __name__ == "__main__":
    run_lda_topic_modeling(n_topics=10, n_words=15)