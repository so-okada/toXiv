#!/usr/bin/env python3
# written by So Okada so.okada@gmail.com
# a part of toXiv for formatting arXiv metadata
# https://github.com/so-okada/toXiv/

import re

# from twitter_text import parse_tweet
from nameparser import HumanName
from variables import *


# format all new submissions
def format(entries):
    return [format_each(one) for one in entries]


# format each new submission
def format_each(orig_entry):
    fixed_length = urls_len + newsub_spacer + margin
    entry = orig_entry.copy()
    orig_title = entry["title"]

    authors_title = entry["authors"] + entry["title"]
    current_len = len(authors_title) + fixed_length

    # first,  a title
    if current_len > max_len:
        difference = current_len - max_len
        current_len_title = len(entry["title"])
        lim = max(min_len_title, current_len_title - difference)
        entry["title"] = simple(entry["title"], lim)

    authors_title = entry["authors"] + entry["title"]
    current_len = len(authors_title) + fixed_length

    # second, authors
    if current_len > max_len:
        difference = current_len - max_len
        current_len_authors = len(entry["authors"])
        lim = max(min_len_authors, current_len_authors - difference)
        entry["authors"] = authors(entry["authors"], lim)

    # third,  a longer title if the length of authors' names becomes shorter
    entry["title"] = orig_title
    authors_title = entry["authors"] + entry["title"]
    current_len = len(authors_title) + fixed_length

    if current_len > max_len:
        difference = current_len - max_len
        current_len_title = len(entry["title"])
        lim = max(min_len_title, current_len_title - difference)
        entry["title"] = simple(entry["title"], lim)

    entry["separated_abstract"] = separate_abstract(
        entry["abstract"], entry["id"], max_len - abst_tag - margin
    )
    return entry


# a simple text cut
def simple(orig, lim):
    orig = orig.strip()
    wlen = len(orig)
    if wlen <= lim:
        return orig

    while wlen > lim:
        orig = orig[:-1]
        wlen = len(orig)

    return orig[:-3] + "..."


# formating authors' names
def authors(orig, lim):
    if lim < 1:
        return ""
    if len(orig) <= lim:
        return orig

    collab = collaboration(orig)
    if collab != orig:
        if len(collab) <= lim:
            return collab
        else:
            return ""

    no_paren = noparen(orig)
    if len(no_paren) <= lim:
        return no_paren

    sr_names = surnames(no_paren)
    if len(sr_names) <= lim:
        return sr_names

    et_al = etal(no_paren)
    if len(et_al) <= lim:
        return et_al

    return ""


def collaboration(orig):
    collab = re.match(r"^[^:]+collaboration:", orig, re.IGNORECASE)
    if collab:
        return re.sub(":$", "", collab.group())
    else:
        return orig


def noparen(test_str):
    ret = ""
    skip = 0
    for i in test_str:
        if i == "(":
            skip += 1
        elif i == ")":
            skip -= 1
        elif skip == 0:
            ret += i
    ret = re.sub("[ ]+,", ",", ret)
    ret = re.sub("[ ]+$", "", ret)
    return ret


# cf. https://stackoverflow.com/questions/14596884/remove-text-between-and-in-python/14598135#14598135


def surnames(orig):
    names = orig.split(",")
    sr_names = [HumanName(one).last for one in names]
    separator = ", "
    return separator.join(sr_names)


def etal(orig):
    first_author = re.search(r"[\w|.| ]+,", orig)
    return first_author.group() + " et al."


# separate an abstract with a counter and url tag
def separate_abstract(orig, id, lim):
    sep_abstract = separate(orig, lim)
    num = len(sep_abstract)
    result = []
    for i, each in enumerate(sep_abstract):
        abst_url = "https://arxiv.org/abs/" + id + "v1"
        if max_len < 2000:
            ptext = (
                each + " \n[" + str(i + 1) + "/" + str(num) + " of " + abst_url + "]"
            )
        else:
            ptext = each + " \n[" + abst_url + "]"
        result.append(ptext)
    return result


def weighted_toot_len(toot_text):
    url_regex = r"https?://[^\s]+"
    urls = re.findall(url_regex, toot_text)
    text_without_urls_len = len(re.sub(url_regex, "", toot_text))
    total_chars = text_without_urls_len + (len(urls) * url_len)
    return total_chars


# separate a text by weighted toot lengths <=lim
def separate(orig, lim):
    sep_text = []
    orig = orig.strip()

    # no inf loop
    if any(weighted_toot_len(t) > lim for t in orig.split(" ")):
        print(
            "\n**cannot separate** \
        \nmax weighted length:  "
            + str(lim)
            + " \ninput:  "
            + orig
        )
        return sep_text

    while orig:
        partial_text = orig
        wlen = weighted_toot_len(partial_text)
        while wlen > lim:
            partial_text = partial_text.rsplit(" ", 1)[0]
            wlen = weighted_toot_len(partial_text)
        sep_text.append(partial_text.strip())
        orig = orig[len(partial_text) :].strip()
    return sep_text


# add a opening text and a counter to each text chunk
def add_chunk_counter(chunks, opening_text=""):
    n = len(chunks)
    formatted_chunks = []
    base_prefix = opening_text + " " if opening_text else ""

    for i, chunk in enumerate(chunks):
        prefix = base_prefix + "\n"
        counter = f"[{i + 1}/{n}]:"
        formatted_chunks.append(prefix + counter + "\n" + chunk + "\n")
    return formatted_chunks


def create_grouped_list(list_A, length_limit, separator="\n"):
    if not list_A:
        return []

    list_B = []
    current_chunk = ""

    for element in list_A:
        if current_chunk:
            potential_chunk = current_chunk + separator + element
        else:
            potential_chunk = element

        if weighted_toot_len(potential_chunk) > length_limit:
            if current_chunk:
                list_B.append(current_chunk)
                current_chunk = element
            else:
                list_B.append(element)
                current_chunk = ""
        else:
            current_chunk = potential_chunk

    if current_chunk:
        list_B.append(current_chunk)

    return list_B
