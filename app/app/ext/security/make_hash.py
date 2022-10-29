from datetime import datetime
from app.ext.utils.commons import Commons
from app.config.settings import CSRF_SESSION_KEY, SECRET_KEY

from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

import hashlib
import base64

hash_method = 'pbkdf2:sha512'
hash_salt = 10
hash_key = '-please-change-this-key-secret-for-backend-base-3.x-code-name-'

def generate_password(password):
    secret_key = cipher_password(password)
    password_hash = generate_password_hash(secret_key, method=hash_method, salt_length=hash_salt)
    return password_hash

def generate_password_bcrypt(password):
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed

def check_password_bcrypt(password, hashed):
    is_valid = bcrypt.checkpw(password, hashed)
    return is_valid


def cipher_password(str_key):
    sanitized_str = Commons.sanity_check(str_key, False)
    cipher_key = generate_key_hash(sanitized_str)
    return cipher_key

def generate_key_hash(user_key):
    user_digest = generate_digest(user_key)
    hash_digest = generate_digest(hash_key)
    hash_csrf = generate_digest(CSRF_SESSION_KEY)
    new_hash_key = "{0}{1}{2}{3}".format(SECRET_KEY, user_digest, hash_digest, hash_csrf)
    hashed = base64encode(new_hash_key)
    return hashed

def generate_digest(key_digest=None):
    if key_digest is None: return None
    return hashlib.sha512(key_digest.encode()).hexdigest()

def base64encode(text):
    return base64.b64encode(bytes(text, encoding='utf-8'))

def check_password(password_hash, password):
    secret_key = cipher_password(password)
    is_valid = check_password_hash(password_hash, secret_key)
    return is_valid