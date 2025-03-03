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
        id = cur.fetchone()[0]
        return id

    def get_url_by_name(self, name_to_find):
        """Gets URL from DB by name.
        Returns URL in form of a dict, empty dict if not found"""
        return self._get_url_by_fieldname("name", name_to_find)

    def get_url_by_id(self, id_to_find):
        """Gets URL in DB by id.
        Returns URL in form of a dict, empty dict if not found"""
        return self._get_url_by_fieldname("id", id_to_find)

    @use_connection
    def _get_url_by_fieldname(self, cur, field_name, value):
        query = f"""
            SELECT id, name, DATE(created_at)
            FROM urls
            WHERE {field_name} = %s"""
        cur.execute(query, (value,))
        url = cur.fetchone()
        return dict(url) if url else {}

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
        last_check = cur.fetchone()
        if last_check:
            last_check_date, last_check_status_code = last_check
            return last_check_date, last_check_status_code
        return "", ""
