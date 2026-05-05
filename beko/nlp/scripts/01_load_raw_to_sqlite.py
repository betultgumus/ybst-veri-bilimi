import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.etl.load_raw_to_sqlite import load_raw_data


if __name__ == "__main__":
    load_raw_data()