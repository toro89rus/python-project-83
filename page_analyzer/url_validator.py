from urllib.parse import urlparse

import validators

from page_analyzer.config import URL_MAX_LEN


def normalize_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.hostname}"


def validate_url(url):
    errors = {}
    if not validators.url(url):
        errors["Incorrect URL"] = True
    if len(url) > URL_MAX_LEN:
        errors["Exceeds max length"] = True
    return errors
