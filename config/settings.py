import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DB_SQLITE_PATH = os.getenv("DB_SQLITE_PATH", str(BASE_DIR / "data" / "erp.db"))
DB_POSTGRES_URL = os.getenv("DB_POSTGRES_URL", "postgresql://user:password@localhost:5432/erp")

DATABASE_URL = (
    f"sqlite:///{DB_SQLITE_PATH}" if DB_TYPE == "sqlite" 
    else DB_POSTGRES_URL
)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

BCRYPT_ROUNDS = 12

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

APP_TITLE = "ERP System - Accounting & POS"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

CURRENCY = os.getenv("CURRENCY", "USD")
MIN_STOCK_WARNING = 10
MAX_DISCOUNT_PERCENT = 15
