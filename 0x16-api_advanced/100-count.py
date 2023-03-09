#!/usr/bin/python3
""" Module for a function that queries the Reddit API recursively."""


import requests


def count_words(subreddit, word_list, after=None, counts={}):
    # Base case: no more articles to fetch
    if after == "":
        # Sort the counts by count (descending) and then by word (ascending)
        sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            print(f"{word}: {count}")
        return
    
    # Query the Reddit API for hot articles in the subreddit
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"after": after}
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    
    # Base case: invalid subreddit or no more articles to fetch
    if response.status_code != 200:
        return
    
    # Recursively call count_words with the next "after" parameter
    data = response.json()
    children = data["data"]["children"]
    for child in children:
        title = child["data"]["title"].lower()
        for word in word_list:
            # Ignore words with special characters (e.g. java. or java!)
            if f"{word.lower()} " in title:
                counts[word.lower()] = counts.get(word.lower(), 0) + title.count(f"{word.lower()} ")
    count_words(subreddit, word_list, data["data"]["after"], counts)