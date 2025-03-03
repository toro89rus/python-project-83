import requests
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from requests.exceptions import ConnectionError, HTTPError, Timeout

from page_analyzer.config import SECRET_KEY
from page_analyzer.html_parser import get_seo_content
from page_analyzer.repository import Repository
from page_analyzer.url_validator import normalize_url, validate_url

app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/")
def index():
    return render_template("main.html.j2")


@app.route("/urls")
def index_urls():
    repo = Repository()
    urls_list = repo.get_all_urls()
    for url in urls_list:
        url["last_check"], url["status"] = (
            repo.get_last_check_date_and_status(url["id"])
        )
    return render_template("urls/urls.html.j2", urls=urls_list)


@app.post("/urls")
def url_new():
    url = request.form.to_dict()["url"]
    normalized_url = normalize_url(url)
    errors = validate_url(normalized_url)
    if not errors:
        repo = Repository()
        id = repo.find_url_by_name(normalized_url).get("id")
        if not id:
            id = repo.save_url(normalized_url)
            flash("Страница успешно добавлена", "success")
        else:
            flash("Страница уже существует", "info")
        return redirect(url_for("show_url", id=id), code=302)
    if "Incorrect URL" in errors:
        flash("Некорректный URL", "danger")
    else:
        flash("Слишком длинный URL", "danger")
    return render_template("main.html.j2", url=url), 422


@app.route("/urls/<id>")
def show_url(id):
    repo = Repository()
    url = repo.find_url_by_id(id)
    url_checks = repo.get_urls_checks_by_id(id)
    return render_template("/urls/show.html.j2", url=url, checks=url_checks)


@app.post("/urls/<id>/checks")
def add_check(id):
    repo = Repository()
    url = repo.find_url_by_id(id)
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
    return render_template("/urls/show.html.j2", url=url, checks=url_checks)
