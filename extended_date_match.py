#!/usr/bin/env python3
# written by So Okada so.okada@gmail.com
# a part of toXiv
# https://github.com/so-okada/toXiv/

from datetime import timedelta

# true if dates of input times are the same during weekdays
# extended match during weekends
def match(time1, time2):
    time1w = time1.weekday()
    time2w = time2.weekday()
    if time1w >= 5:
        time1 = time1 - timedelta(time1w - 4)
    if time2w >= 5:
        time2 = time2 - timedelta(time2w - 4)
    if time1.date() == time2.date():
        return True
    else:
        return False

