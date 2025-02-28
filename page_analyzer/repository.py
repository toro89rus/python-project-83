import datetime

from psycopg2.extras import DictCursor


class UrlsRepository:
    def __init__(self, conn):
        self.conn = conn

    def save(self, url):
        query = (
            "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING ID"
        )
        with self.conn.cursor() as cur:
            cur.execute(query, (url, datetime.datetime.now()))
            id = cur.fetchone()[0]
        self.conn.commit()
        return id

    def get_all(self):
        query = "SELECT * FROM urls ORDER BY id DESC"
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query)
            return [dict(row) for row in cur]

    def find_by_name(self, name_to_find):
        query = "SELECT * FROM urls WHERE name = %s"
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query, (name_to_find,))
            row = cur.fetchone()
            return dict(row) if row else {}

    def find_by_id(self, id_to_find):
        query = "SELECT id, name, DATE(created_at) FROM urls WHERE id = %s"
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query, (id_to_find,))
            row = cur.fetchone()
            return dict(row) if row else {}

    def find_by_fieldname(self, fieldname, value):
        if fieldname not in ("name", "created_at", "id"):
            raise ValueError(f"Invalid fieldname:{fieldname}")
        query = f"SELECT * FROM urls WHERE {fieldname} = %s"
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query, (value,))
            row = cur.fetchone()
            return dict(row) if row else None


class ChecksRepository:
    def __init__(self, conn):
        self.conn = conn

    def add_check(self, url_id, status_code, h1, title, description):
        query = """INSERT INTO url_checks
        (url_id, status_code, h1, title, description, created_at)
        VALUES (%s, %s, %s,%s, %s, %s) RETURNING ID"""
        with self.conn.cursor() as cur:
            cur.execute(
                query,
                (
                    url_id,
                    status_code,
                    h1,
                    title,
                    description,
                    datetime.datetime.now(),
                ),
            )
            id = cur.fetchone()[0]
        self.conn.commit()
        return id

    def get_checks(self, url_id):
        query = """SELECT
                id,
                url_id,
                status_code,
                h1,
                title,
                description,
                DATE(created_at)
                FROM url_checks
                WHERE url_id = %s
                ORDER BY created_at DESC;
        """
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query, (url_id,))
            return [dict(row) for row in cur]

    def get_last_check(self, url_id):
        query = """SELECT DATE(created_at)
                FROM url_checks
                WHERE url_id = %s
                ORDER BY created_at DESC;"""
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query, (url_id,))
            last_check = cur.fetchone()
            return last_check[0] if last_check else ""
