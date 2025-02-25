import psycopg2


class UrlsRepository:
    def __init__(self, conn):
        self.conn = conn

    def save(self, url):
        query = "INSERT INTO urls (name) VALUES (%s) RETURNING ID"
        with self.conn.cursor() as cur:
            cur.execute(query, (url,))
            id = cur.fetchone()[0]
        return id
