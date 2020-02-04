import datetime
import requests
from builtins import str, len, list, filter, map
from typing import List

Vector = List[str]


def download_quotes(url: str):
    request = requests.get(url)
    return request.text


def remove_markdown_heading_spaces(lines: str) -> Vector:
    quotes = [strip(l) for l in lines.splitlines() if strip(l)]
    quotes = filter(lambda l: not l.startswith('#'), quotes)
    return list(quotes)


def pick_quote_for_today(quotes: Vector) -> str:
    day_number = datetime.datetime.utcnow().timetuple().tm_yday
    cycled_index = (day_number - 1) % len(quotes)
    return quotes[cycled_index]


def strip(l):
    return l.strip()
