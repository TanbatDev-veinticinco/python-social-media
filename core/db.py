import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

users_db = {}
posts_db = {}
likes_db = set()