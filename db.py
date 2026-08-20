import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="library",
    user="postgres",
    password="13alogug"
)

try:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM readers ORDER BY id;")
        rows = cur.fetchall()
        for row in rows:
            print(row)
finally:
    conn.close()