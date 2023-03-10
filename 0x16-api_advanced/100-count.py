#!/usr/bin/python3
""" Module for a function that queries the Reddit API recursively."""


import requests


def count_words(subreddit, word_list, counts=None):
    """
    a recursive function that queries the Reddit API,
    parses the title of all hot articles, and prints a
    sorted count of given keywords (case-insensitive,
    delimited by spaces. Javascript should count as javascript,
    but java should not).
    Parameters:
        subreddit - the subreddit to search
        word_list - contains the same word (case-insensitive),
            the final count should be the sum of each duplicate
    """
    if counts is None:
        counts = {}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return
    data = response.json()
    for post in data['data']['children']:
        title = post['data']['title']
        for word in word_list:
            if word.lower() in title.lower() and not any(c.isalpha() for c in title.lower().split(word.lower())[0][-1:]):
                if word.lower() not in counts:
                    counts[word.lower()] = 1
                else:
                    counts[word.lower()] += 1
    if data['data']['after'] is not None:
        count_words(subreddit, word_list, counts=counts)
    else:
        for word, count in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
            print(f"{word}: {count}")
