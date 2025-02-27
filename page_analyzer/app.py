import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from page_analyzer.repository import ChecksRepository, UrlsRepository
from page_analyzer.url_validator import normalize_url, validate_url

app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)


@app.route("/")
def index():
    return render_template("main.html.j2")


@app.route("/urls")
def index_urls():
    urls = UrlsRepository(conn)
    urls_list = urls.get_all()
    checks = ChecksRepository(conn)
    for url in urls_list:
        url["last_check"] = checks.get_last_check(url["id"])
    return render_template("urls/urls.html.j2", urls=urls_list)


@app.post("/urls")
def url_new():
    urls = UrlsRepository(conn)
    url = request.form.to_dict()["url"]
    normalized_url = normalize_url(url)
    errors = validate_url(normalized_url)
    if not errors:
        id = urls.find_by_name(normalized_url).get("id")
        if not id:
            id = urls.save(normalized_url)
            flash("Страница успешно добавлена", "success")
        else:
            id = urls.find_by_name(normalized_url)["id"]
            flash("Страница уже существует", "info")
        return redirect(url_for("show_url", id=id), code=302)
    if "Incorrect URL" in errors:
        flash("Неккоректный URL", "danger")
    else:
        flash("Слишком длинный URL", "danger")
    return render_template("main.html.j2")


@app.route("/show/<id>")
def show_url(id):
    urls = UrlsRepository(conn)
    url = urls.find_by_id(id)
    checks = ChecksRepository(conn)
    url_checks = checks.get_checks(id)
    return render_template("/urls/show.html.j2", url=url, checks=url_checks)


@app.post("/urls/<id>/checks")
def add_check(id):
    urls = UrlsRepository(conn)
    url = urls.find_by_id(id)
    checks = ChecksRepository(conn)
    checks.add_check(id)
    url_checks = checks.get_checks(id)
    return render_template("/urls/show.html.j2", url=url, checks=url_checks)
