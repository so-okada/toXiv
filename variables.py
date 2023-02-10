# common max toot length is 500 
# mastodon url length is 23
# https://docs.joinmastodon.org/user/posting/

max_len = 500
url_len = 23
url_margin = 2

urls_len = (url_len + url_margin) * 2
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

arxiv_max_trial = 4
arxiv_call_sleep = 20 * 60

main_thread_wait = 60

# 300 for 5mins per account/ip
# https://docs.joinmastodon.org/api/rate-limits/
# toXiv uses ratelimit library, assuming that different arXiv
# categories use different user accounts.
mstdn_time_period = 5 * 60
post_updates = 200
mstdn_sleep = 9

# overall posting limit independent to specific categories
overall_mstdn_limit_call = 1
overall_mstdn_limit_period = 10

# semanticscholar API rate limits  2020-12-30
# The API is freely available, but enforces a rate limit and will respond
# with HTTP status 429 'Too Many Requests' if the limit is exceeded
# (100 requests per 5 minute window per IP address).
# https://api.semanticscholar.org/
sch_call_limit = 90
sch_call_period = 5 * 60

sch_max_trial = 2
sch_call_sleep = 5
