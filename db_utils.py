# db_utils.py

import sqlite3

DB_FILE = "subdomain_scans.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS scan_results (
            domain TEXT,
            subdomain TEXT,
            ip TEXT,
            reverse_dns TEXT,
            scheme TEXT,
            url TEXT,
            status INTEGER,
            length INTEGER,
            title TEXT,
            content_hash TEXT,
            server_header TEXT,
            ssl_sans TEXT,
            open_ports TEXT,
            banners TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_result(row):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO scan_results VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        row["domain"],
        row["subdomain"],
        row["ip"],
        row["reverse_dns"],
        row["scheme"],
        row["url"],
        row["status"],
        row["length"],
        row["title"],
        row["content_hash"],
        row["server_header"],
        row["ssl_sans"],
        row["open_ports"],
        row["banners"]
    ))
    conn.commit()
    conn.close()

def fetch_all():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM scan_results")
    rows = c.fetchall()
    conn.close()
    return rows
