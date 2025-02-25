import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request

from page_analyzer.repository import UrlsRepository

app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)


@app.route("/")
def index():
    return render_template("main.html"), 200


@app.post("/urls")
def url_new():
    urls = UrlsRepository(conn)
    url = request.form.to_dict()["url"]
    id = urls.save(url)
    return render_template("main.html", messages=id)
