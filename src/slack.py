import datetime
import requests
from builtins import int, str, len, list, filter, map
from time import struct_time
from typing import List

Vector = List[str]

class QuoteDownloadService:
    def request(self, url: str):
        f = requests.get(url)
        return f.text.splitlines()

    def clean(self, lines: Vector) -> Vector:
        quotes = [l for l in lines if l.strip()]
        quotes = map(lambda l: l.strip(), quotes)
        quotes = filter(lambda l: not l.startswith('#'), quotes)
        return list(quotes)

class QuoteOfTheDayService:
    def pick(self, quotes: Vector, date: struct_time = None) -> str:
        i = self.day_to_number(date)
        t = len(quotes)
        cycled_index = (i - 1) % t
        return quotes[cycled_index]

    def day_to_number(self, date: struct_time = None) -> int:
        if date is not None:
            return date.tm_yday
        return datetime.datetime.utcnow().timetuple().tm_yday


