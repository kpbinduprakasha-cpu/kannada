"""
BCC Swachha Belagavi - Command Line Administration Console
CLI tool for Belagavi City Corporation (BCC) municipal officers.
"""

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

    worker_list = c.execute("SELECT worker_name, worker_emp_id, cleanups_today, performance_score FROM worker_progress").fetchall()
    conn.close()

    print("="*70)
    print("🏛️  SWACHHA BELAGAVI (ಸ್ವಚ್ಛ ಬೆಳಗಾವಿ) - BELAGAVI CITY CORPORATION")
    print("="*70)
    print(f"📍 City Location:              Belagavi (ಬೆಳಗಾವಿ), Karnataka")
    print(f"📊 Total Waste Incidents:      {total}")
    print(f"🔴 Pending Red Alerts:          {pending}")
    print(f"🟢 Verified Cleanups:          {verified}")
    print(f"👷 Active On-Duty Workers:      {workers}")
    print(f"⛓️  Blockchain Blocks Mined:     {blocks}")
    print("-"*70)
    print("👷 Individual Worker Active Progress:")
    for w in worker_list:
        print(f"   • {w[0]} ({w[1]}) | Cleanups Today: {w[2]} | Score: {w[3]}%")
    print("="*70)

if __name__ == "__main__":
    show_summary()
