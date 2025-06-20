import sqlite3
import hashlib
import binascii
import os
import streamlit as st
from config import HASH_NAME, ITERATIONS, SALT_SIZE
from db.database import execute_query, execute_update

def hash_password(password: str) -> str:
    salt = os.urandom(SALT_SIZE)
    pw_hash = hashlib.pbkdf2_hmac(HASH_NAME, password.encode('utf-8'), salt, ITERATIONS)
    salt_hex = binascii.hexlify(salt).decode('utf-8')
    hash_hex = binascii.hexlify(pw_hash).decode('utf-8')
    return f"{salt_hex}${hash_hex}"

def verify_password(password: str, stored: str) -> bool:
    try:
        salt_hex, hash_hex = stored.split('$')
        salt = binascii.unhexlify(salt_hex.encode('utf-8'))
        pw_hash = hashlib.pbkdf2_hmac(HASH_NAME, password.encode('utf-8'), salt, ITERATIONS)
        return binascii.hexlify(pw_hash).decode('utf-8') == hash_hex
    except Exception:
        return False

def register_user(username: str, password: str) -> bool:
    rows = execute_query("SELECT id FROM users WHERE username = ?", (username,))
    if rows:
        return False
    pw_hash = hash_password(password)
    execute_update(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, pw_hash)
    )
    return True

def authenticate_user(username: str, password: str) -> dict | None:
    rows = execute_query(
        "SELECT id, username, password_hash FROM users WHERE username = ?", (username,)
    )
    if not rows:
        return None
    user = rows[0]
    if verify_password(password, user['password_hash']):
        return {'id': user['id'], 'username': user['username']}
    return None

def login_user(user: dict):
    st.session_state['user_id'] = user['id']
    st.session_state['username'] = user['username']

def logout_user():
    for key in ['user_id', 'username']:
        if key in st.session_state:
            del st.session_state[key]

def get_current_user() -> dict | None:
    if 'user_id' in st.session_state and 'username' in st.session_state:
        return {'id': st.session_state['user_id'], 'username': st.session_state['username']}
    return None