"""
Připojení k SQLite databázi CHRONO
"""

import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "app",
    "users.db"
)


def get_connection():
    """Vrátí připojení k databázi."""
    return sqlite3.connect(DB_PATH)
