# delete_db.py
import os

DB_PATH = "./rushr.db"

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("🔥 rushr.db deleted.")
else:
    print("⚠️ rushr.db does not exist.")
