from django.shortcuts import render

import feedparser
# Create your views here.
def news(ticker):
    rss_reuter = 'http://feeds.reuters.com/reuters/businessNews'
    rss_yahoo = 'http://finance.yahoo.com/rss/headline?s=' + ticker.lower()

    newsfeed = feedparser.parse(rss_reuter)
    newsfeed = newsfeed.entries

    stockfeed = feedparser.parse(rss_yahoo)
    stockfeed = stockfeed.entries[:12]

    newsPosts = []
    stockPosts = []

    for post in stockfeed:
        title = post.title
        link = post.link
        stockPosts.append({'title': title, 'link': link})

    for post in newsfeed:
        title = post.title
        link = post.link
        newsPosts.append({'title' : title, 'link' : link})

    return newsPosts, stockPosts
