#!/usr/bin/env python3
# written by So Okada so.okada@gmail.com
# a part of toXiv for posting to mstdn and stdout
# https://github.com/so-okada/toXiv/

import re
import os
import time
import traceback
from mastodon import Mastodon as mstdn
import pandas as pd
from threading import Thread
from datetime import datetime, date, timedelta
from ratelimit import limits, sleep_and_retry, rate_limited

from variables import *
import toXiv_format as tXf
import toXiv_daily_feed as tXd
import extended_date_match as edm
import Semantic_Scholar_url as schurl


def main(switches, logfiles, captions, aliases, pt_mode):
    starting_time = datetime.utcnow().replace(microsecond=0)
    print('**process started at ' + str(starting_time) + ' (UTC)')

    api_dict = {}
    update_dict = {}
    entries_dict = {}
    webreplacements_dict = {}
    caption_dict = {}

    newsubmission_mode = {}
    abstract_mode = {}
    crosslisting_mode = {}
    toot_replacement_mode = {}
    boost_replacement_mode = {}

    for cat in switches:
        api_dict[cat] = mstdn_api(switches[cat])
        update_dict[cat] = sleep_and_retry(
            rate_limited(post_updates, mstdn_time_period)(update))
        newsubmission_mode[cat] = int(switches[cat]['newsubmissions'])
        abstract_mode[cat] = int(switches[cat]['abstracts'])
        crosslisting_mode[cat] = int(switches[cat]['crosslistings'])
        toot_replacement_mode[cat] = int(switches[cat]['toot_replacements'])
        boost_replacement_mode[cat] = int(switches[cat]['boost_replacements'])
        if cat in captions:
            caption_dict[cat] = captions[cat]
        else:
            caption_dict[cat] = ''

    # retrieval/new submissions/abstracts
    threads = []
    for i, cat in enumerate(switches):
        th = Thread(name=cat,
                    target=newentries,
                    args=(logfiles, aliases, cat, caption_dict[cat],
                          api_dict[cat], update_dict[cat], entries_dict,
                          newsubmission_mode[cat], abstract_mode[cat],
                          pt_mode))
        threads.append(th)
        ptext = \
            'starting a thread of ' +\
            'retrieval/new submissions/abstracts for ' +\
            th.name
        print(ptext)
        th.start()
        if i != len(switches) - 1:
            ptext = 'waiting for a next thread of ' + \
                'retrieval/new submissions/abstracts'
            print(ptext)
            time.sleep(main_thread_wait)

    print('joining threads of retrieval/new submissions/abstracts')
    [th.join() for th in threads]

    if not logfiles:
        ending_time = datetime.utcnow().replace(microsecond=0)
        if crosslisting_mode[cat] or toot_replacement_mode[
                cat] or boost_replacement_mode[cat]:
            ptext = \
                'No logfiles found. ' + \
                'toXiv needs logfiles for crosslistings and replacements '
            print(ptext)
            ptext = '\n**process ended at ' + str(ending_time) + ' (UTC)' +\
                '\n**elapsed time from the start: ' + \
                str(ending_time - starting_time)
            print(ptext)
            return None

    # cross lists
    crosslisting_time = \
        datetime.utcnow().replace(microsecond=0)
    ptext = \
        '\n**crosslisting process started at ' \
        + str(crosslisting_time) + \
        ' (UTC)' + ' \n**elapsed time from the start: ' +\
        str(crosslisting_time - starting_time)
    print(ptext)

    threads = []
    for i, cat in enumerate(switches):
        if entries_dict[cat] and crosslisting_mode[cat]:
            crosslisting_entries = entries_dict[cat].crosslistings
            th = Thread(name=cat,
                        target=crosslistings,
                        args=(logfiles, cat, api_dict[cat], update_dict[cat],
                              crosslisting_entries, pt_mode))
            threads.append(th)
            print('start a crosslisting thread of ' + th.name)
            th.start()
            if i != len(switches) - 1:
                print('waiting for a next crosslisting thread')
                time.sleep(main_thread_wait)

    if threads:
        print('joining crosslisting threads')
        [th.join() for th in threads]

    # replacements
    replacement_time = datetime.utcnow().replace(microsecond=0)
    ptext = \
        '\n**toot-replacement process started at ' + \
        str(replacement_time) + ' (UTC)' + \
        '\n**elapsed time from the start: ' + \
        str(replacement_time - starting_time) + \
        '\n**elapsed time from the crosslisting start: ' + \
        str(replacement_time - crosslisting_time)
    print(ptext)

    print("\n**toot-replacement starts")
    for i, cat in enumerate(switches):
        if entries_dict[cat]:
            replacement_entries = entries_dict[cat].replacements
            # version check: new sub web pages exclude versions > 5.
            webreplacements_dict[cat] = []
            for each in replacement_entries:
                if not each['version'] == '' and int(each['version']) > 5:
                    print('version unknown or >5 for ' + each['id'])
                    # exclude old arXiv identifiers
                elif not re.match('[a-z|A-Z]', each['id']):
                    webreplacements_dict[cat].append(each)

    threads = []
    for i, cat in enumerate(switches):
        if webreplacements_dict[cat] and toot_replacement_mode[cat]:
            th = Thread(name=cat,
                        target=toot_replacement,
                        args=(logfiles, cat, api_dict[cat], update_dict[cat],
                              webreplacements_dict[cat], pt_mode))
            threads.append(th)
            print('start a toot-replacement thread of ' + th.name)
            th.start()
            if i != len(switches) - 1:
                print('waiting for a next toot-replacement thread')
                time.sleep(main_thread_wait)

    if threads:
        print('joining toot-replacement threads')
        [th.join() for th in threads]

    print("\n**boost-replacement starts")
    threads = []
    for i, cat in enumerate(switches):
        if webreplacements_dict[cat] and boost_replacement_mode[cat]:
            th = Thread(name=cat,
                        target=boost_replacement,
                        args=(logfiles, cat, api_dict[cat], update_dict[cat],
                              webreplacements_dict[cat], pt_mode))
            threads.append(th)
            print('start a boost-replacement thread of ' + th.name)
            th.start()
            if i != len(switches) - 1:
                print('waiting for a next boost-replacement thread')
                time.sleep(main_thread_wait)

    if threads:
        print('joining boost-replacement threads')
        [th.join() for th in threads]

    ending_time = datetime.utcnow().replace(microsecond=0)
    ptext = '\n**process ended at ' + str(ending_time) + ' (UTC)' +\
        '\n**elapsed time from the start: ' + \
        str(ending_time - starting_time) + \
        '\n**elapsed time from the crosslisting start: ' + \
        str(ending_time - crosslisting_time) + \
        '\n**elapsed time from the replacement start: ' + \
        str(ending_time - replacement_time)
    print(ptext)


# mstdn api
def mstdn_api(keys):
    atoken = keys['access_token']
    return mstdn(access_token=atoken, api_base_url=mstdn_instance)


# update with overall limit
@sleep_and_retry
@limits(calls=overall_mstdn_limit_call, period=overall_mstdn_limit_period)
def update(logfiles, cat, api, total, arxiv_id, text, tot_id_str,\
           pt_method, pt_mode):
    result = 0

    if not pt_mode:
        update_print(cat, arxiv_id, text, tot_id_str, '',\
                     pt_method, pt_mode)
        return result

    error_text = '\nthread arXiv category: ' + cat + \
        '\narXiv id: ' + arxiv_id + \
        '\ntext: ' + text + \
        '\ntot_id_str: ' + tot_id_str + '\n'

    if pt_method == 'toot':
        try:
            result = api.toot(text)
            update_print(cat, arxiv_id, text, tot_id_str, str(result.id),
                         pt_method, pt_mode)
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = '\n**error to toot**' + '\nutc: ' + str(time_now) + \
                error_text
            print(error_text)
            traceback.print_exc()
    elif pt_method == 'boost':
        try:
            result = api.status_reblog(tot_id_str)
            update_print(cat, arxiv_id, text, tot_id_str, str(result.id),
                         pt_method, pt_mode)
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = '\n**error to boost**' + '\nutc: ' + str(time_now) + \
                error_text
            print(error_text)
            traceback.print_exc()
    elif pt_method == 'unboost':
        try:
            result = api.unreblog(tot_id_str)
            update_print(cat, arxiv_id, text, tot_id_str, str(result.id),
                         pt_method, pt_mode)
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = '\n**error to unboost**' + \
                '\nutc: ' + str(time_now) + error_text
            print(error_text)
            traceback.print_exc()
    elif pt_method == 'reply':
        try:
            result = api.status_post(text, in_reply_to_id=tot_id_str)
            update_print(cat, arxiv_id, text, tot_id_str, str(result.id),
                         pt_method, pt_mode)
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = '\n**error to reply**' + '\nutc: ' + str(time_now) + \
                error_text
            print(error_text)
            traceback.print_exc()
    # fix this 2022-05-10
    elif pt_method == 'quote':
        try:
            result = api.toot(text)
            update_print(cat, arxiv_id, text, tot_id_str, str(result.id),
                         pt_method, pt_mode)
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = '\n**error to quote**' + '\nutc: ' + str(time_now) + \
                error_text
            print(error_text)
            traceback.print_exc()

    update_log(logfiles, cat, total, arxiv_id, result, pt_method, pt_mode)
    time.sleep(mstdn_sleep)
    return result


# update stdout text format
def update_print(cat, arxiv_id, text, tot_id_str, result_id_str, pt_method,
                 pt_mode):
    time_now = datetime.utcnow().replace(microsecond=0)
    status_url = mstdn_instance + 'web/statuses/'
    ptext = '\nutc: ' + str(time_now) + \
        '\nthread arXiv category: ' + cat +\
        '\narXiv id: ' + arxiv_id + \
        '\nurl: '+status_url + tot_id_str +\
        '\npost method: ' + pt_method +\
        '\npost mode: ' + str(pt_mode) +\
        '\nurl: '+status_url + result_id_str + \
        '\ntext: ' + text + '\n'
    print(ptext)


# logging for update
def update_log(logfiles, cat, total, arxiv_id, \
               posting, pt_method, pt_mode):
    if not posting or not pt_mode or not logfiles:
        return None

    time_now = datetime.utcnow().replace(microsecond=0)

    if not arxiv_id and pt_method == 'toot':
        filename = logfiles[cat]['newsubmission_summary_log']
        log_text = [[
            time_now, total, logfiles[cat]['username'],
            str(posting.id)
        ]]
        df = pd.DataFrame(log_text,
                          columns=['utc', 'total', 'username', 'toot_id'])
    else:
        log_text = [[
            time_now, arxiv_id, logfiles[cat]['username'],
            str(posting.id)
        ]]
        df = pd.DataFrame(log_text,
                          columns=['utc', 'arxiv_id', 'username', 'toot_id'])
        # fix this 2022-05-10
        filename = logfiles[cat][pt_method + '_log']

    if not filename:
        return None
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=None, index=None)
    else:
        df.to_csv(filename, mode='w', index=None)

# retrieval of daily entries, and
# calling a sub process for new submissions and abstracts
def newentries(logfiles, aliases, cat, caption, api,\
               update_limited,  entries_dict, \
               newsubmission_mode, abstract_mode, pt_mode):
    print("getting daily entries for " + cat)
    try:
        entries_dict[cat] = tXd.daily_entries(cat, aliases)
    except Exception:
        entries_dict[cat] = {}
        print("\n**error for retrieval**\nthread arXiv category:" + cat)
        traceback.print_exc()
        if not check_log_dates(cat, 'newsubmission_log', logfiles) and \
           not check_log_dates(cat, 'newsubmission_summary_log', logfiles):
            # daily entries retrieval failed and
            # no toots for today have been made.
            print("check_log_dates returns False for " + cat)
            time_now = datetime.utcnow().replace(microsecond=0)
            ptext = intro(time_now, 0, cat, caption)
            update_limited(logfiles, cat, api, '0', '', ptext, '', 'toot',
                           pt_mode)

    # new submissions and abstracts
    if newsubmission_mode:
        print("new submissions for " + cat)
        if entries_dict[cat]:
            newsub_entries = tXf.format(entries_dict[cat].newsubmissions)
            if not check_log_dates(cat, 'newsubmission_log', logfiles) and \
               not check_log_dates(cat, 'newsubmission_summary_log', logfiles):
                newsubmissions(logfiles, cat, caption, api, update_limited,
                               newsub_entries, abstract_mode, pt_mode)
            else:
                print(cat + ' already tooted for today')


# an introductory text of each category
# an example: [2020-08-01 (UTC),  4 new articles found for mathCV]
def intro(given_time, num, cat, caption):
    ptext = '[' + \
        given_time.strftime('%Y-%m-%d %a') + ' (UTC), '
    # On the variable num, arXiv_feed_parser gives new
    # submissions whose primary subjects are the given category.
    if num == 0:
        ptext = ptext + \
            "no new articles found for "
    elif num == 1:
        ptext = ptext + str(num) + \
            " new article found for "
    else:
        ptext = ptext + str(num) + \
            " new articles found for "
    if caption:
        ptext = ptext + re.sub(r'\.', '', cat) + " " + caption + "]"
    else:
        ptext = ptext + re.sub(r'\.', '', cat) + "]"
    return ptext


# new submissions by toots and abstracts by replies
def newsubmissions(logfiles, cat, caption, api, \
                   update_limited, entries, abstract_mode, pt_mode):
    time_now = datetime.utcnow().replace(microsecond=0)
    ptext = intro(time_now, len(entries), cat, caption)
    update_limited(logfiles, cat, api, str(len(entries)), '', ptext, '',
                   'toot', pt_mode)

    for each in entries:
        arxiv_id = each['id']
        article_text = \
            each['authors'] + ": " + \
            each['title'] + " " + \
            each['abs_url'] + " " + \
            each['pdf_url']
        posting = update_limited(logfiles, cat, api, '', arxiv_id,
                                 article_text, '', 'toot', pt_mode)

        if abstract_mode and posting:
            sep_abst = each['separated_abstract']
            for i, partial_abst in enumerate(sep_abst):
                if i == 0:
                    abst_posting = update_limited(logfiles, cat, api, '',
                                                  arxiv_id, partial_abst,
                                                  str(posting.id), 'reply',
                                                  pt_mode)
                else:
                    abst_posting = update_limited(logfiles, cat, api, '',
                                                  arxiv_id, partial_abst,
                                                  str(abst_posting.id),
                                                  'reply', pt_mode)
                if abst_posting == 0:
                    break


# crosslistings by boosts
def crosslistings(logfiles, cat, api, update_limited, entries, pt_mode):
    # if-clause to avoid duplication errors
    # when toXiv runs twice with crosslistings in a day.

    boost_filename = logfiles[cat]['crosslisting_log']
    time_now = datetime.utcnow().replace(microsecond=0)
    error_text = '\nutc: ' + str(
        time_now) + '\nboost_filename: ' + boost_filename
    if os.path.exists(boost_filename):
        try:
            dboost_f = pd.read_csv(boost_filename, dtype=object)
        except Exception:
            error_text = '\n**error for pd.read_csv**' + error_text
            print(error_text)
            traceback.print_exc()
            return False
        for boost_index, boost_row in dboost_f.iterrows():
            try:
                log_time = boost_row['utc']
            except Exception:
                error_text = "\n**error for row['utc']**" + error_text
                print(error_text)
                traceback.print_exc()
            log_time = datetime.fromisoformat(log_time)
            if edm.match(time_now, log_time):
                ptext = 'already boosted today for crosslistings: ' + cat
                print(ptext)
                return None

    for each in entries:
        arxiv_id = each['id']
        subject = each['primary_subject']
        print(cat, ' ', arxiv_id, ' ', subject)

        if subject == cat:
            # This case is not listed in new submission web pages,
            # but was in rss feeds (2020-06-14).
            ptext = 'skip: crosslisting of an article in its own category \n'
            print(ptext)
            continue
        if subject not in logfiles.keys():
            print('not in logfiles: ' + subject)
            continue

        toot_filename = logfiles[subject]['newsubmission_log']
        # skip without newsubmission_log
        if not os.path.exists(toot_filename):
            print('no toot log file for ' + subject)
            continue

        # open newsubmission_log file
        try:
            toot_df = pd.read_csv(toot_filename, dtype=object)
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = '\nutc: ' + str(
                time_now) + '\ntoot_filename: ' + toot_filename
            error_text = '\n**error for pd.read_csv**' + error_text
            print(error_text)
            traceback.print_exc()
            return False

        time_now = datetime.utcnow().replace(microsecond=0)
        for toot_index, toot_row in toot_df.iterrows():
            if arxiv_id == toot_row['arxiv_id']:
                toot_id = toot_row['toot_id']
                toot_time = datetime.fromisoformat(toot_row['utc'])
                # if-clause to avoid double boosts
                if not edm.match(time_now, toot_time):
                    update_limited(logfiles, cat, api, '', arxiv_id, '',
                                   toot_id, 'unboost', pt_mode)
                update_limited(logfiles, cat, api, '', arxiv_id, '', toot_id,
                               'boost', pt_mode)


# replacements by toots
def toot_replacement(logfiles, cat, api, update_limited, entries, pt_mode):

    toot_filename = logfiles[cat]['newsubmission_log']
    # skip without newsubmission_log
    if not os.path.exists(toot_filename):
        print('no toot log file for ' + cat)
        return None

    # open newsubmission_log file
    try:
        toot_df = pd.read_csv(toot_filename, dtype=object)
    except Exception:
        time_now = datetime.utcnow().replace(microsecond=0)
        error_text = '\nutc: ' + str(
            time_now) + '\ntoot_filename: ' + toot_filename
        error_text = '\n**error for pd.read_csv**' + error_text
        print(error_text)
        traceback.print_exc()
        return False

    quote_filename = logfiles[cat]['toot_replacement_log']
    # skip without toot_replacement_log with posting mode
    if not os.path.exists(toot_filename) and pt_mode:
        print('posting mode without quote log file for ' + cat)
        return None

    # open toot_replacement_log file
    try:
        quote_df = pd.read_csv(quote_filename, dtype=object)
    except Exception:
        time_now = datetime.utcnow().replace(microsecond=0)
        error_text = '\nutc: ' + str(
            time_now) + '\nquote_filename: ' + quote_filename
        error_text = '\n**error for pd.read_csv**' + error_text
        print(error_text)
        traceback.print_exc()
        return False

    # if-clause to avoid duplication errors
    time_now = datetime.utcnow().replace(microsecond=0)
    if pt_mode and \
       any(edm.match(time_now, datetime.fromisoformat(t))
           for t in quote_df.utc.values):
        print('already made toot-replacements today for ' + cat)
        return None

    entries_to_quote = []
    for each in entries:
        arxiv_id = each['id']
        if each['primary_subject'] == cat and \
           not any(arxiv_id == toot_row['arxiv_id']
                for toot_index, toot_row in quote_df.iterrows()):
            entries_to_quote.append(each)

    for each in entries_to_quote:
        arxiv_id = each['id']
        username = logfiles[cat]['username']
        ptext = 'This https://arxiv.org/abs/' + arxiv_id + \
            ' has been replaced. ' + \
            tools(arxiv_id)

        for toot_index, toot_row in toot_df.iterrows():
            if arxiv_id == toot_row['arxiv_id']:
                toot_id = toot_row['toot_id']
                status_url = mstdn_instance + 'web/statuses/'
                ptext = ptext + ' ' + status_url + toot_id
                update_limited(logfiles, cat, api, '', arxiv_id, ptext,
                               toot_id, 'quote', pt_mode)


# replacement by boosts
def boost_replacement(logfiles, cat, api, update_limited, entries, pt_mode):
    for each in entries:
        arxiv_id = each['id']
        subject = each['primary_subject']

        if subject not in logfiles.keys():
            print('No quote log for ' + subject)
            continue
        quote_filename = logfiles[subject]['toot_replacement_log']

        # skip without toot_replacement_log
        if not os.path.exists(quote_filename):
            print('no quote log file for ' + subject)
            continue

        # open toot_replacement_log
        try:
            quote_df = pd.read_csv(quote_filename, dtype=object)
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = '\nutc: ' + str(
                time_now) + '\nquote_filename: ' + quote_filename
            error_text = '\n**error for pd.read_csv**' + error_text
            print(error_text)
            traceback.print_exc()
            return False

        # unboost and boost
        for toot_index, toot_row in quote_df.iterrows():
            # check if arxiv_id is in toot_replacement_log.
            if arxiv_id == toot_row['arxiv_id']:
                log_time = toot_row['utc']
                log_time = datetime.fromisoformat(log_time)
                time_now = datetime.utcnow().replace(microsecond=0)
                if cat != subject or not edm.match(time_now, log_time):
                    toot_id = toot_row['toot_id']
                    update_limited(logfiles, cat, api, '', arxiv_id, '',
                                   toot_id, 'unboost', pt_mode)
                    update_limited(logfiles, cat, api, '', arxiv_id, '',
                                   toot_id, 'boost', pt_mode)


# true if this finds a today's toot.
def check_log_dates(cat, logname, logfiles):
    if not logfiles:
        print('no log files')
        return False

    filename = logfiles[cat][logname]
    if not os.path.exists(filename):
        print('log file does not exists: ' + filename)
        return False

    time_now = datetime.utcnow().replace(microsecond=0)
    try:
        df = pd.read_csv(filename, dtype=object)
    except Exception:
        error_text = '\nutc: ' + str(time_now) + '\nfilename: ' + filename
        error_text = '\n**error for pd.read_csv**' + error_text
        print(error_text)
        traceback.print_exc()
        return False
    for index, row in df.iterrows():
        log_time = datetime.fromisoformat(row['utc'])
        if edm.match(log_time, time_now) and \
           row['username'] == logfiles[cat]['username']:
            return True
    return False


def tools(arxiv_id):
    google_url = 'https://scholar.google.com/scholar?q=arXiv%3A' +\
        arxiv_id
    sch_url = 'https://api.semanticscholar.org/'
    ctdp_url = 'https://www.connectedpapers.com/main/'

    paperid = ''
    try:
        paperid = schurl.paperid('arXiv:' + arxiv_id)
    except Exception:
        error_text = '\narXiv_id: ' + arxiv_id
        error_text = '\n**error for sch_paperid**' + error_text
        print(error_text)

    if paperid:
        urls = google_url + ' ' + \
            sch_url + paperid + ' ' + \
            ctdp_url + paperid
        return 'Links: ' + urls
    else:
        return 'Link: ' + google_url
