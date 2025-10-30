from database import engine

try:
    with engine.connect() as connection:
        print("✅ Connection successful!")
except Exception as e:
    print("❌ Connection failed:", e)