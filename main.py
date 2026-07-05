import sys
from config.database import init_db
from config.settings import BASE_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

def main():
    try:
        init_db()
        logger.info("ERP System - Backend initialized successfully!")
        print("✅ ERP System - Backend initialized successfully!")
        print(f"📁 Database location: {BASE_DIR / 'data' / 'erp.db'}")
        print(f"📦 All services loaded and ready")
    except Exception as e:
        logger.error(f"Failed to initialize: {str(e)}")
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
