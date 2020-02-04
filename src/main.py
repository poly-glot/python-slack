"""
A utility script to Query Stettix Quotes through Github and post them to provided web hook on slack.
"""

import os
from builtins import print
from slack_webhook import Slack
from slack import download_quotes, remove_markdown_heading_spaces, pick_quote_for_today

target_url = os.getenv('SLACK_QUOTE_URL',
                       "https://gist.githubusercontent.com/stettix/5bb2d99e50fdbbd15dd9622837d14e2b/raw"
                       "/cab21e3627c1209e3000077abd7eade723bd5c6f/things-i-believe.md")

slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL', None);

def main():
    quotes = download_quotes(target_url)
    quotes = remove_markdown_heading_spaces(quotes)
    quote = pick_quote_for_today(quotes)

    print("Quote of the day")
    print(quote)

    if slack_webhook_url is not None:
        slack = Slack(url=slack_webhook_url)
        slack.post(text=quote)


if __name__ == "__main__":
    main()
