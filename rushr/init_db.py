# init_db.py
from app.db import create_tables

print("📦 Creating rushr.db and tables...")
create_tables()
print("✅ Database initialized.")
# This script initializes the database by creating the necessary tables.
# Run it once to set up the database schema.
# You can run this script using: python init_db.py