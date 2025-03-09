import requests
from flask import Flask, flash, redirect, render_template, request, url_for
from requests.exceptions import ConnectionError, HTTPError, Timeout

from page_analyzer.config import SECRET_KEY
from page_analyzer.html_parser import get_seo_content
from page_analyzer.repository import Repository
from page_analyzer.url_validator import normalize_url, validate_url

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
repo = Repository()


@app.route("/")
def index():
    return render_template("main.html.jinja")


@app.route("/urls")
def index_urls():
    urls_list = repo.get_all_urls()
    for url in urls_list:
        print(url)
        url["last_check"], url["status"] = repo.get_last_check_date_and_status(
            url["id"]
        )
    return render_template("urls/urls.html.jinja", urls=urls_list)


@app.post("/urls")
def add_url():
    url = request.form.get("url")
    normalized_url = normalize_url(url)
    errors = validate_url(normalized_url)
    if errors:
        if "Incorrect URL" in errors:
            flash_message = "Некорректный URL"
        elif "Exceeds max length" in errors:
            flash_message = "Слишком длинный URL"
        flash(flash_message, "danger")
        return render_template("main.html.jinja", url=url), 422
    existing_url = repo.get_url_by_name(normalized_url)
    if existing_url:
        url_id = existing_url.get("id")
        flash("Страница уже существует", "info")
    else:
        url_id = repo.save_url(normalized_url)
        flash("Страница успешно добавлена", "success")
    return redirect(url_for("show_url", id=url_id), code=302)


@app.route("/urls/<id>")
def show_url(id):
    url = repo.get_url_by_id(id)
    url_checks = repo.get_urls_checks_by_id(id)
    return render_template("/urls/show.html.jinja", url=url, checks=url_checks)


@app.post("/urls/<id>/checks")
def add_check(id):
    url = repo.get_url_by_id(id)
    try:
        r = requests.get(url["name"])
        r.raise_for_status()
        check = {"url_id": id, "status_code": r.status_code}
        seo_content = get_seo_content(r.text)
        check.update(seo_content)
        repo.add_check(**check)
        flash("Страница успешно проверена", "success")
    except (HTTPError, Timeout, ConnectionError):
        flash("Произошла ошибка при проверке", "danger")
    url_checks = repo.get_urls_checks_by_id(id)
    return render_template("/urls/show.html.jinja", url=url, checks=url_checks)
