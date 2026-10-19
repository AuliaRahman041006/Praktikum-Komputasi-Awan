import os
import time
import mysql.connector
from flask import Flask

app = Flask(__name__)

def get_conn():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "rootpass"),
        database=os.getenv("DB_NAME", "praktikum"),
    )

def wait_for_db():
    for _ in range(30):
        try:
            get_conn().close()
            return
        except Exception as e:
            print("Menunggu database...", e)
            time.sleep(2)
    raise RuntimeError("Database tidak tersedia")

@app.route("/")
def hello():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS kunjungan (id INT AUTO_INCREMENT PRIMARY KEY, waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cur.execute("INSERT INTO kunjungan () VALUES ()")
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM kunjungan")
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return f"Halo dari Flask + Docker + Jenkins! Terhubung ke MySQL. Total kunjungan tersimpan di database: {total}"

if __name__ == "__main__":
    wait_for_db()
    app.run(host="0.0.0.0", port=5000)
