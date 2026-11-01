import psycopg
from complaintiq.config import settings

# Database URL se '+psycopg' ko temporary hata kar 'postgresql://' kar diya gaya hai
database_url = settings.database_url.replace(
    "postgresql+psycopg://",
    "postgresql://",
)

with psycopg.connect(database_url) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT current_database();")
        result = cur.fetchone()
        print("Connected to database:", result[0])