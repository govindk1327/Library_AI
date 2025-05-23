import time
import psycopg2
from psycopg2 import OperationalError
import os

while True:
    try:
        conn = psycopg2.connect(
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            host="db",
            port="5432",
        )
        conn.close()
        print("✅ Database ready")
        break
    except OperationalError:
        print("⏳ Waiting for DB...")
        time.sleep(1)
