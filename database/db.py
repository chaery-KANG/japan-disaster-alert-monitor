import sqlite3
from pathlib import Path
from typing import List, Dict

DB_PATH = Path(__file__).resolve().parents[1] / "database" / "alerts.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            title_ja TEXT,
            title_ko TEXT,
            summary_ja TEXT,
            summary_ko TEXT,
            published TEXT,
            link TEXT,
            disaster_type TEXT,
            severity TEXT,
            matched_keywords TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_alerts(alerts: List[Dict[str, str]]):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM alerts")

    for alert in alerts:
        cur.execute("""
            INSERT INTO alerts (
                source, title_ja, title_ko, summary_ja, summary_ko,
                published, link, disaster_type, severity, matched_keywords
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            alert.get("source", ""),
            alert.get("title_ja", ""),
            alert.get("title_ko", ""),
            alert.get("summary_ja", ""),
            alert.get("summary_ko", ""),
            alert.get("published", ""),
            alert.get("link", ""),
            alert.get("disaster_type", ""),
            alert.get("severity", ""),
            alert.get("matched_keywords", ""),
        ))

    conn.commit()
    conn.close()

def load_alerts() -> List[Dict[str, str]]:
    if not DB_PATH.exists():
        return []

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM alerts ORDER BY id DESC")
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows
