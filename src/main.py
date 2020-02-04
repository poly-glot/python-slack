"""
A utility script to Query Stettix Quotes through Github and post them to provided web hook on slack.
"""

import os
from slack_webhook import Slack
from builtins import print

from slack import QuoteDownloadService, QuoteOfTheDayService

target_url = os.getenv('SLACK_QUOTE_URL',
                       "https://gist.githubusercontent.com/stettix/5bb2d99e50fdbbd15dd9622837d14e2b/raw/cab21e3627c1209e3000077abd7eade723bd5c6f/things-i-believe.md");

slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL', None);

def main():
    quote_service = QuoteDownloadService()
    quotes = quote_service.clean(quote_service.request(target_url))

    quote_of_the_day_service = QuoteOfTheDayService();
    quote = quote_of_the_day_service.pick(quotes)

    print("Quote of the day")
    print(quote)

    if slack_webhook_url is not None:
        slack = Slack(url=slack_webhook_url)
        slack.post(text=quote)


if __name__ == "__main__":
    main()
