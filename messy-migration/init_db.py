#Initializes DB schema and inserts a hashed default user
import sqlite3
from app.utils.security import hash_password

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Insert default user only if email doesn't exist
    default_email = 'admin@example.com'
    cursor.execute("SELECT * FROM users WHERE email = ?", (default_email,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            ('Admin User', default_email, hash_password('admin123'))
        )
        print("[+] Default user created.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("[+] Database initialized.")