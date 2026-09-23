"""
BBMP Swachha Bengaluru - Command Line Administration Console
CLI tool for municipal officers to query waste reports, workers, and blockchain ledger.
"""

import sys
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'bbmp_waste.db')

def show_summary():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    total = c.execute("SELECT COUNT(*) FROM waste_reports").fetchone()[0]
    pending = c.execute("SELECT COUNT(*) FROM waste_reports WHERE status = 'pending'").fetchone()[0]
    verified = c.execute("SELECT COUNT(*) FROM waste_reports WHERE status = 'verified'").fetchone()[0]
    workers = c.execute("SELECT COUNT(*) FROM worker_progress WHERE duty_status = 'on_duty'").fetchone()[0]
    blocks = c.execute("SELECT COUNT(*) FROM blockchain_ledger").fetchone()[0]
    conn.close()

    print("="*65)
    print("🏛️  BBMP SWACHHA BENGALURU - MUNICIPAL COMMAND CONSOLE")
    print("="*65)
    print(f"📊 Total Waste Incidents:      {total}")
    print(f"🔴 Pending Red Alerts:          {pending}")
    print(f"🟢 Verified Cleanups:          {verified}")
    print(f"👷 Active On-Duty Workers:      {workers}")
    print(f"⛓️  Blockchain Blocks Mined:     {blocks}")
    print("="*65)

if __name__ == "__main__":
    show_summary()
