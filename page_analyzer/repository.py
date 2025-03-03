import datetime

import psycopg2
from psycopg2.extras import DictCursor

from page_analyzer.config import DATABASE_URL


def use_connection(method):
    """Automatically manages connection to DB and cursor"""
    conn = psycopg2.connect(DATABASE_URL)

    def wrapper(self, *args, **kwargs):
        with conn, conn.cursor(cursor_factory=DictCursor) as cur:
            return method(self, cur, *args, **kwargs)

    return wrapper


class Repository:

    @use_connection
    def get_all_urls(self, cur):
        query = "SELECT * FROM urls ORDER BY id DESC"
        cur.execute(query)
        return [dict(url) for url in cur]

    @use_connection
    def save_url(self, cur, url):
        """Saves new url to DB, returns ID"""
        query = (
            "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING ID"
        )
        values = (url, datetime.datetime.now())
        cur.execute(query, values)
        id = cur.fetchone()
        return id

    @use_connection
    def find_url_by_name(self, cur, name_to_find):
        """Searches URL in DB by name.
        Returns URL in form of a dict, empty dict if not found"""
        query = "SELECT * FROM urls WHERE name = %s"
        cur.execute(query, (name_to_find,))
        url = cur.fetchone()
        return dict(url) if url else {}

    @use_connection
    def find_url_by_id(self, cur, id_to_find):
        """Searches URL in DB by id.
        Returns URL in form of a dict, empty dict if not found"""
        query = "SELECT id, name, DATE(created_at) FROM urls WHERE id = %s"
        cur.execute(query, (id_to_find,))
        row = cur.fetchone()
        return dict(row) if row else {}

    @use_connection
    def get_urls_checks_by_id(self, cur, url_id):
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
        cur.execute(query, (url_id,))
        return [dict(check) for check in cur]

    @use_connection
    def add_check(self, cur, **check):
        query = """INSERT INTO url_checks
        (url_id, status_code, h1, title, description, created_at)
        VALUES (%s, %s, %s,%s, %s, %s) RETURNING ID"""
        values = (
            check["url_id"],
            check["status_code"],
            check["h1"],
            check["title"],
            check["content"],
            datetime.datetime.now(),
        )
        cur.execute(query, values)
        id = cur.fetchone()
        return id

    @use_connection
    def get_last_check_date_and_status(self, cur, url_id):
        query = """SELECT DATE(MAX(created_at)), status_code
                FROM url_checks
                WHERE url_id = %s
                GROUP BY status_code"""

        cur.execute(query, (url_id,))
        result = cur.fetchone()
        if result:
            last_check_date, status_code = result
            return last_check_date, status_code
        return "", ""
