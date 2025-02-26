from urllib.parse import urlparse

import validators

MAX_LENGTH = 255


def normalize_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.hostname}"


def is_valid_url(url):
    if not validators.url(url):
        return False
    return True

def has_valid_len(url):
    return len(url) <= MAX_LENGTH


class UrlValidator:
    def __init__(self, url):
        self.url = url

    def validate_url(self):
        if not validators.url(self.url):
            return False
        return True

    def validate_url_len(self):
        pass


is_valid_url(normalize_url("https://vk.com/asdasd"))
