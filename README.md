# App Info

toXiv gives arXiv daily new submissions by toots, abstracts
by replies, cross-lists by boosts, and replacements by
toots and boosts.  We use python3 scripts. toXiv is not
affiliated with arXiv.


## Setup

* Install Mastodon.py, pandas, ratelimit, semanticscholar, mastodon, nameparser, and beautifulsoup4. 

	```
	% pip3 install  Mastodon.py pandas ratelimit semanticscholar nameparser beautifulsoup4
	```

* Let toXiv.py be executable.
 
	 ```
	 % chmod +x toXiv.py
	 ```

*  Put the following python scripts in the same directory.

	- toXiv.py
	- toXiv_post.py 	
	- toXiv_format.py
	- toXiv_daily_feed.py 	
	- extended_date_match.py
	- Semantic_Scholar_url.py
	- arXiv_feed_parser.py
	- variables.py


* Configure switches.json, logfiles.json, and aliases.json in the
  tests directory for your settings.

	- accesses.json specifies mastodon access tokens
	and whether to use
	new submissions/abstracts/cross-lists/replacements by toXiv.

    - logfiles.json indicates logfile locations.  You can check their
	formats by samples in the tests/logfiles directory.  toXiv
	needs a toot log file for cross-lists and replacements. 
		
	- aliases.json tells toXiv aliases of arXiv category
    names.  For example, math.IT is an alias of
    cs.IT. Without this file, toXiv of rss feeds returns no
    new submissions, when you take the category name
    math.IT.  If provided, toXiv replaces category names by
    their aliases for new submissions, cross-lists, and
    replacements.
	
* Configure variables.py for your settings. 

   - variables.py assigns format parameters for toXiv toots 
   and access frequencies for arXiv and mastodon.

## Notes

* Outputs of toXiv can differ from arXiv new submission web
  pages.  First, items of arXiv rss feeds are not
  necessarily the same as those of arXiv new submission web
  pages.  Second, arXiv_feed_parser for an arXiv category C
  gives new submissions whose primary subjects are the
  category C.  Then, toXiv for the category C counts and
  toots a new paper whose principal subject matches the
  category C.  This avoids duplicate toots and clarifies
  what toXiv toots, boosts, and unboosts for each paper, as
  toXiv runs on multiple categories.

	- For example, let us assume that there is no new paper whose
	principal subject matches the category C, but there is a
	new paper P whose non-principal subject matches the
	category C. Then, the arXiv new submission web page of
	the category C lists the paper P as a new submission of
	the category C, not as a cross-list.  However, toXiv
	keeps considering the paper P as a cross-list for the
	category C.  Then, the output of toXiv for the category
	C differs from the arXiv new submission web page of the
	category C.

* 	On the use of metadata of arXiv articles, there is the
   web page of [Terms of Use for arXiv
   APIs](https://arxiv.org/help/api/tou). As of the revision
   0.9.5, this says that " You are free to use descriptive
   metadata about arXiv e-prints under the terms of the
   Creative Commons Universal (CC0 1.0) Public Domain
   Declaration." and "Descriptive metadata includes
   information for discovery and identification purposes,
   and includes fields such as title, abstract, authors,
   identifiers, and classification terms."



## Usage

```
% ./toXiv.py -h
usage: toXiv.py [-h] --switches_keys SWITCHES_KEYS
                [--logfiles LOGFILES] [--aliases ALIASES]
                [--captions CAPTIONS] [--mode {0,1}]

arXiv daily new submissions by toots, abstracts by
replies, cross-lists by boosts, and replacements by
toots and boosts.

optional arguments:
  -h, --help            show this help message and exit
  --switches_keys SWITCHES_KEYS, -s SWITCHES_KEYS
                        output switches and api keys in
                        json
  --logfiles LOGFILES, -l LOGFILES
                        log file names in json
  --aliases ALIASES, -a ALIASES
                        aliases of arXiv categories in
                        json
  --captions CAPTIONS, -c CAPTIONS
                        captions of arXiv categories in
                        json
  --mode {0,1}, -m {0,1}
                        1 for mastodon and 0 for stdout
                        only
```

## Sample stdouts


* New submissions for math.CA:

```
%toXiv ./toXiv.py -s var/test_switches.json  -l var/logfiles.json -a var/aliases.json -c var/captions.json -m 1
**process started at 2022-xx-xx xx:xx:xx (UTC)
starting a thread of retrieval/new submissions/abstracts for math.CA
getting daily entries for math.CA
joining threads of retrieval/new submissions/abstracts
new submissions for math.CA

utc: 2022-xx-xx xx:xx:xx
thread arXiv category: math.CA
arXiv id: 
username: @xxxx@xxxx
url: https://xxxx/web/statuses/
aim: newsubmission_summary
post method: toot
post mode: 1
url: https://xxxx/web/statuses/xxxxxx
text: [2022-xx-xx Sun (UTC), 1 new article found for math.CA Classical Analysis and ODEs]


utc: 2022-xx-xx xx:xx:xx
thread arXiv category: math.CA
arXiv id: xxxx.xxxxx
username: @xxxx@xxxx
url: https://xxxx/web/statuses/
aim: newsubmission
post method: toot
post mode: 1
url: https://xxxx/web/statuses/xxxxxx
text: xxxxxxxxxxxxxxxxxxxxxx


utc: 2022-xx-xx xx:xx:xx
thread arXiv category: math.CA
arXiv id: xxxx.xxxxx
username: @xxxx@xxxx
url: https://xxxx/web/statuses/xxxxxx
aim: abstract
post method: reply
post mode: 1
url: https://xxxx/web/statuses/xxxxxx
text:


utc: 2022-xx-xx xx:xx:xx
thread arXiv category: math.CA
arXiv id: xxxx.xxxxx
username: @xxxx@xxxx
url: https://xxxx/web/statuses/xxxxxx
aim: abstract
post method: reply
post mode: 1
url: https://xxxx/web/statuses/xxxxxx
text:


**crosslisting process started at 2022-xx-xx xx:xx:xx (UTC) 
**elapsed time from the start: xx:xx:xx

**replacement process started at 2022-xx-xx xx:xx:xx (UTC)
**elapsed time from the start: xx:xx:xx
**elapsed time from the crosslisting start: xx:xx:xx

**checking replacement entries

**toot-replacement starts

**boost-replacement starts

**process ended at 2022-xx-xx xx:xx:xx (UTC)
**elapsed time from the start: xx:xx:xx
**elapsed time from the crosslisting start: xx:xx:xx
**elapsed time from the replacement start: xx:xx:xx
```

* Without the option ```-c tests/captions.json```above, you get

```
text: [2022-xx-xx Sun (UTC), 1 new article found for math.CA]
```

 instead of

```
text: [2022-xx-xx Sun (UTC), 1 new articles found for math.CA Classical Analysis and ODEs]
```

## Versions

* 0.0.1

  * 2022-05, initial release.

## List of Bots

## Author
So Okada, so.okada@gmail.com, https://so-okada.github.io/

## Motivation

Since 2013-04, the author has been running twitter bots for
all arXiv math categories (see
https://github.com/so-okada/twXiv#motivation).
Since 2022-05, the author has been developing mastodon
bots by toXiv.


## Contributing
Pull requests are welcome. For major changes, please open an 
issue first to discuss what you would like to change.

## License
[AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html)


