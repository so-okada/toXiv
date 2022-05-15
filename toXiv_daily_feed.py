#!/usr/bin/env python3
# written by So Okada so.okada@gmail.com
# a part of toXiv for retrival of arXiv rss feeds
# by arXiv_feed_parser.py
# https://github.com/so-okada/toXiv/

import time
from datetime import datetime, date, timedelta
from ratelimit import limits, sleep_and_retry, rate_limited

from variables import *
import arXiv_feed_parser as afpa
import extended_date_match as edm


# overall limit
@sleep_and_retry
@limits(calls=arxiv_call_limit, period=arxiv_call_period)
def daily_entries(cat, aliases):
    trial_num = 0
    time_now = datetime.utcnow()
    while trial_num < arxiv_max_trial:
        feed = afpa.retrieve(cat, aliases)
        if feed.bozo:
            print(
                str(trial_num + 1) + 'th feed parse error for ' + cat)
        else:
            announced_time = feed.updated_parsed
        if trial_num < arxiv_max_trial - 1:
            if edm.match(announced_time, time_now):
                if len(feed.entries) > 0:
                    return feed
                else:
                    print('empty feed entries for ' + cat)
            else:
                print('not of today in UTC time zone for ' + cat)
        else:
            if edm.match(announced_time, time_now):
                return feed
            else:
                print('not of today in UTC time zone for ' + cat)
        trial_num += 1
        if trial_num < arxiv_max_trial:
            print('sleep and retry for ' + cat)
            time.sleep(arxiv_call_sleep)
        else:
            raise Exception('fatal parse error for ' + cat)
