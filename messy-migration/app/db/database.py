#Centralized DB connection with row_factory for dict access
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # dict-like access
    return conn
