# Page Analyzer

## Hexlet tests, CodeClimate, linter statuses:[![Actions Status](https://github.com/toro89rus/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/toro89rus/python-project-83/actions) [![Actions Status](https://github.com/toro89rus/python-project-83/actions/workflows/lint-and-test.yml/badge.svg)](https://github.com/toro89rus/python-project-83/actions) [![Maintainability](https://api.codeclimate.com/v1/badges/e93115cb3814cdf62520/maintainability)](https://codeclimate.com/github/toro89rus/python-project-83/maintainability)

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)
![Flask](https://img.shields.io/badge/Flask-000?logo=flask&logoColor=fff)
![Postgres](https://img.shields.io/badge/Postgres-%23316192.svg?logo=postgresql&logoColor=white)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?logo=bootstrap&logoColor=fff)]

### Description

Page Analyzer is a web app build using Python and Flask, designed to evaluate SEO-friendliness of web pages.

### Features

- Add valid HTTP/HTTPS URLs to the database.
- Check URL availability.
- Extract SEO-related tags from added URLs.
- Store URLS and history of checks in a PostgreSQL database.
- User-friendly web interface for easy interaction.

### Requirements

- Python 3.12
- `uv`
- `make`
- `psql`

### Installation

#### Step 1: Clone the Repository

```bash
git clone git@github.com:toro89rus/python-project-83.git
cd python-project-83
make install
```

#### Step 2: Set up a Database

You need to setup a database in PSQL before using Page Analyzer. User following script(specify database name)

```bash
psql -d <database_name> -f database.sql
```

#### Step 3: Configure the Application

Update the database connection settings in config.py:

```bash
DATABASE_URI = 'postgresql://username:password@localhost/page_analyzer'
```

#### Step 4: Run the Application

```bash
make start
```

The application should be accessible at <http://127.0.0.1:5000>.

Check project on [Render.com](https://python-project-83-dkf1.onrender.com/)
