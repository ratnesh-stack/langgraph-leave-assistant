import os
import sqlite3

DB_NAME = "leave_management.db"

def init_db(reset: bool = False):
    """Initializes the database schema and seed data.
    Sets reset=False by default so updates persist across multiple script runs.
    """
    if reset and os.path.exists(DB_NAME):
        os.remove(DB_NAME)

    # Check if DB already exists before running script
    db_exists = os.path.exists(DB_NAME)

    conn = sqlite3.connect(DB_NAME)
    if not db_exists:
        with open("init_db.sql", "r") as f:
            conn.executescript(f.read())
    conn.close()
