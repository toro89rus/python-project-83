import os

import requests
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from requests.exceptions import ConnectionError, HTTPError, Timeout

from page_analyzer.html_parser import get_seo_content
from page_analyzer.repository import ChecksRepository, UrlsRepository
from page_analyzer.url_validator import normalize_url, validate_url

app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template("main.html.j2")


@app.route("/urls")
def index_urls():
    urls = UrlsRepository()
    urls_list = urls.get_all()
    checks = ChecksRepository()
    for url in urls_list:
        (url["last_check"], url["status"]) = checks.get_last_check(url["id"])
    return render_template("urls/urls.html.j2", urls=urls_list)


@app.post("/urls")
def url_new():
    urls = UrlsRepository()
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
        flash("Некорректный URL", "danger")
    else:
        flash("Слишком длинный URL", "danger")
    return render_template("main.html.j2", url=url), 422


@app.route("/urls/<id>")
def show_url(id):
    urls = UrlsRepository()
    url = urls.find_by_id(id)
    checks = ChecksRepository()
    url_checks = checks.get_checks(id)
    return render_template("/urls/show.html.j2", url=url, checks=url_checks)


@app.post("/urls/<id>/checks")
def add_check(id):
    urls = UrlsRepository()
    url = urls.find_by_id(id)
    checks = ChecksRepository()
    try:
        r = requests.get(url["name"])
        r.raise_for_status()
        seo_content = get_seo_content(r.text)
        checks.add_check(id, r.status_code, *seo_content)
        flash("Страница успешно проверена", "success")
    except (HTTPError, Timeout, ConnectionError):
        flash("Произошла ошибка при проверке", "danger")
    url_checks = checks.get_checks(id)
    return render_template("/urls/show.html.j2", url=url, checks=url_checks)
