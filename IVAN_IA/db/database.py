import sqlite3
from sqlite3 import Connection
import os

from config import DB_PATH, SCHEMA_PATH


def get_connection() -> Connection:
    """
    Returns a SQLite connection with foreign key support enabled.
    """
    # Ensure the database directory exists
    db_dir = os.path.dirname(DB_PATH)
    os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # Enable foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """
    Initializes the database by creating it (if necessary) and applying the schema.
    """
    # Ensure the database directory exists
    db_dir = os.path.dirname(DB_PATH)
    os.makedirs(db_dir, exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    # Execute schema SQL
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)

    conn.commit()
    conn.close()


def execute_query(query: str, params: tuple = ()) -> list[sqlite3.Row]:
    """
    Executes a SELECT query and returns all fetched rows.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows


def execute_update(query: str, params: tuple = ()) -> int:
    """
    Executes an INSERT/UPDATE/DELETE query and returns the last row id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id
