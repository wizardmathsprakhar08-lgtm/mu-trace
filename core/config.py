import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "mu-trace"
    VERSION: str = "1.0.0"
    DATA_DIR: Path = BASE_DIR / "data"
    DB_PATH: Path = BASE_DIR / "data" / "financials.db"
    REPORTS_DIR: Path = BASE_DIR / "data" / "reports"
    
    # Financial normalization defaults
    DEFAULT_CURRENCY: str = "INR"
    DEFAULT_UNIT: str = "₹ Crore"
    DEFAULT_FY_END: str = "31st March"
    
    # Verification & Quality thresholds
    TARGET_NUMERIC_ACCURACY: float = 1.00 # 100% required
    TARGET_FAITHFULNESS: float = 0.90 # 90%+ target
    MAX_UNSUPPORTED_CLAIMS_TOLERANCE: int = 0 # Prune or escalate to analyst if > 0
    RED_TEAM_SEVERITY_ALERT_THRESHOLD: str = "high"
    
    # LLM Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    DEFAULT_MODEL: str = os.getenv("EQUITY_MODEL", "smart-hybrid")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
