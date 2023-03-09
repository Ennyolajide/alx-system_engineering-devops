#!/usr/bin/python3
""" Module for a function that queries the Reddit API recursively."""


import requests


def count_words(subreddit, word_list, after='', word_dict={}):
    """ A function that queries the Reddit API parses the title of
    all hot articles, and prints a sorted count of given keywords
    (case-insensitive, delimited by spaces.
    Javascript should count as javascript, but java should not).
    If no posts match or the subreddit is invalid, it prints nothing.
    """

    if word_dict is None:
        word_dict = {}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=100"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"after": after} if after else {}
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    if response.status_code != 200:
        return
    data = response.json()
    for post in data["data"]["children"]:
        title = post["data"]["title"].lower()
        for word in word_list:
            if (f" {word.lower()} " in f" {title} " 
                or title.startswith(f"{word.lower()} ") 
                or title.endswith(f" {word.lower()}")
                or title == f"{word.lower()}"):
                word_dict[word.lower()] = word_dict.get(word.lower(), 0) + 1
    if data["data"]["after"] is not None:
        word_dict = count_words(subreddit, word_list, data["data"]["after"], word_dict)
    else:
        sorted_counts = sorted(word_dict.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            print(f"{word}: {count}")