# note: usual max toot length is 500
# url length is 23
# https://docs.joinmastodon.org/user/posting/

# this max_len is for title, authors, URLs, and margins
# arXiv abstract length <= 1920
# current new submission length <= 2000+1920 (mastoxiv.page toot length limit=5000)
max_len = 2000
url_len = 23
url_margin = 2

urls_len = (url_len + url_margin) * 3
min_len_authors = 90
min_len_title = 300
newsub_spacer = 3
margin = 9

# abstract tag for a counter and url
abst_tag = 11 + (url_len + url_margin) + 1

# arXiv API rate limits  2020-06-16
# no more than 1 request every 3 seconds,
# a single connection at a time.
# https://arxiv.org/help/api/tou
arxiv_call_limit = 1
arxiv_call_period = 5

arxiv_feed_timeout = 60

arxiv_max_trial = 2
arxiv_call_sleep = 10 * 60

main_thread_wait = 5

# 300 for 5mins per account/ip
# https://docs.joinmastodon.org/api/rate-limits/
# toXiv uses ratelimit library, assuming that different arXiv
# categories use different user accounts.
mstdn_time_period = 5 * 60
post_updates = 300
mstdn_sleep = 1

# overall posting limit independent to specific categories
overall_mstdn_limit_call = 1
overall_mstdn_limit_period = 3
