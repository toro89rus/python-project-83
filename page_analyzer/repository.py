import datetime
import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)


def get_conn():
    return psycopg2.connect(DATABASE_URL)


class UrlsRepository:

    def save(self, url):
        conn = get_conn()
        query = (
            "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING ID"
        )
        with conn.cursor() as cur:
            cur.execute(query, (url, datetime.datetime.now()))
            id = cur.fetchone()[0]
        conn.commit()
        conn.close()
        return id

    def get_all(self):
        conn = get_conn()
        query = "SELECT * FROM urls ORDER BY id DESC"
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query)
            urls = [dict(row) for row in cur]
            conn.close()
            return urls

    def find_by_name(self, name_to_find):
        conn = get_conn()
        query = "SELECT * FROM urls WHERE name = %s"
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query, (name_to_find,))
            row = cur.fetchone()
            conn.close()
            return dict(row) if row else {}

    def find_by_id(self, id_to_find):
        conn = get_conn()
        query = "SELECT id, name, DATE(created_at) FROM urls WHERE id = %s"
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query, (id_to_find,))
            row = cur.fetchone()
            conn.close()
            return dict(row) if row else {}

    def find_by_fieldname(self, fieldname, value):
        conn = get_conn()
        if fieldname not in ("name", "created_at", "id"):
            raise ValueError(f"Invalid fieldname:{fieldname}")
        query = f"SELECT * FROM urls WHERE {fieldname} = %s"
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query, (value,))
            row = cur.fetchone()
            conn.close()
            return dict(row) if row else None


class ChecksRepository:

    def add_check(self, url_id, status_code, h1, title, description):
        conn = get_conn()
        query = """INSERT INTO url_checks
        (url_id, status_code, h1, title, description, created_at)
        VALUES (%s, %s, %s,%s, %s, %s) RETURNING ID"""
        with conn.cursor() as cur:
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
        conn.commit()
        conn.close()
        return id

    def get_checks(self, url_id):
        conn = get_conn()
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
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query, (url_id,))
            checks = [dict(row) for row in cur]
            conn.close()
            return checks

    def get_last_check(self, url_id):
        conn = get_conn()
        query = """SELECT DATE(MAX(created_at)), status_code
                FROM url_checks
                WHERE url_id = %s
                GROUP BY status_code"""

        with conn.cursor() as cur:
            cur.execute(query, (url_id,))
            result = cur.fetchall()
            conn.close()
            if result:
                last_check, status_code = result[0]
                return (last_check, status_code)
            return ("", "")
