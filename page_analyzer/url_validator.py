from urllib.parse import urlparse

import validators

MAX_LENGTH = 255


def normalize_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.hostname}"


def validate_url(url):
    errors = {}
    if not validators.url(url):
        errors["Incorrect URL"] = True
    if len(url) > MAX_LENGTH:
        errors["Exceeds max length"] = True
    return errors
