import sqlite3
import json
from typing import Dict, List, Optional, Any
from pathlib import Path
from core.config import settings

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(settings.DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Companies
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        ticker TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        sector TEXT,
        industry TEXT,
        currency TEXT DEFAULT 'INR',
        unit TEXT DEFAULT '₹ Crore',
        fiscal_year_end TEXT DEFAULT '31st March',
        isin TEXT,
        bse_code TEXT,
        nse_symbol TEXT
    )
    """)
    
    # Financial statements (Income, Balance Sheet, Cash Flow)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS financials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        period_type TEXT NOT NULL, -- 'ANNUAL' or 'QUARTERLY'
        period_label TEXT NOT NULL, -- 'FY24', 'Q3FY25'
        line_item TEXT NOT NULL,
        value REAL NOT NULL,
        unit TEXT NOT NULL,
        source_doc TEXT,
        source_page INTEGER,
        as_of_date TEXT,
        UNIQUE(ticker, period_type, period_label, line_item)
    )
    """)
    
    # Evidence & Filing documents chunks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evidence_chunks (
        id TEXT PRIMARY KEY,
        ticker TEXT NOT NULL,
        source_title TEXT NOT NULL,
        doc_type TEXT NOT NULL,
        period TEXT NOT NULL,
        page_number INTEGER,
        table_cell TEXT,
        transcript_timestamp TEXT,
        content TEXT NOT NULL,
        created_at TEXT
    )
    """)

    # Generated Reports & Audit Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS report_records (
        report_id TEXT PRIMARY KEY,
        ticker TEXT NOT NULL,
        company_name TEXT NOT NULL,
        created_at TEXT NOT NULL,
        status TEXT NOT NULL,
        numeric_accuracy REAL,
        faithfulness REAL,
        unsupported_count INTEGER,
        report_json TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

init_db()
