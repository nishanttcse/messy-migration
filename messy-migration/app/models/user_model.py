# app/models/user_model.py

from app.db.database import get_db_connection
from app.utils.security import hash_password, check_password


def get_all_users():
    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email, password FROM users").fetchall()
    conn.close()
    return [dict(user) for user in users]

def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return dict(user) if user else None

def create_user(name, email, hashed_password):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (name, email, hashed_password)
    )
    conn.commit()
    conn.close()

def update_user(user_id, name, email):
    conn = get_db_connection()
    conn.execute(
        "UPDATE users SET name = ?, email = ? WHERE id = ?",
        (name, email, user_id)
    )
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )
    conn.commit()
    conn.close()

def search_users(name):
    conn = get_db_connection()
    users = conn.execute(
        "SELECT id, name, email FROM users WHERE name LIKE ?",
        (f"%{name}%",)
    ).fetchall()
    conn.close()
    return [dict(user) for user in users]

def get_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return dict(user) if user else None
def login_user(email, password):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    if user and check_password(password, user['password']):
        return dict(user)
    return None
