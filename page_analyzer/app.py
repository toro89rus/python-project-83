import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for

from page_analyzer.repository import UrlsRepository
from page_analyzer.url_validator import (
    has_valid_len,
    is_valid_url,
    normalize_url,
)

app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)


@app.route("/")
def index():
    message = session.get("message")
    session["message"] = None
    return render_template("main.html.j2", message=message), 200


@app.route("/urls")
def index_urls():
    urls = UrlsRepository(conn)
    urls_list = urls.get_all()
    return render_template("urls/urls.html.j2", urls=urls_list)


@app.post("/urls")
def url_new():
    urls = UrlsRepository(conn)
    url = request.form.to_dict()["url"]
    url = normalize_url(url)
    if is_valid_url(url) and has_valid_len(url):
        id = urls.save(url)
        session["message"] = "Страница успешно добавлена"
        return redirect(url_for("show_url", id=id), code=302)
    if not is_valid_url(url):
        session["message"] = "Некорректный URL"
    else:
        session["message"] = "Слишком длинный URL"
    return redirect(url_for("index"))


@app.route("/show/<id>")
def show_url(id):
    urls = UrlsRepository(conn)
    url = urls.find_by_id(id)
    message = session["message"]
    session["message"] = None
    return render_template("/urls/show.html.j2", url=url, message=message)
