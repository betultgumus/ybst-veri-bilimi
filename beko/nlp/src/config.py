from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
DATABASE_DIR = DATA_DIR / "database"

REPORTS_DIR = BASE_DIR / "reports"
MODELS_DIR = BASE_DIR / "models"

COMMENTS_CSV_PATH = RAW_DIR / "sikayetvar_yorumlar.csv"
PRODUCTS_CSV_PATH = RAW_DIR / "beko_urun_ozellikleri.csv"

DB_PATH = DATABASE_DIR / "beko_nlp.db"

RAW_COMPLAINTS_TABLE = "raw_complaints"
RAW_PRODUCTS_TABLE = "raw_products"
COMPLAINT_ANALYSIS_TABLE = "complaint_analysis"
MERGED_ANALYSIS_TABLE = "merged_analysis"