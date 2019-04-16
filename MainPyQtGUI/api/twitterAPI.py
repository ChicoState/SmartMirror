from twitter import *


from . import config

def getTrending():
    twitter = Twitter(auth = OAuth(config.access_key,
                      config.access_secret,
                      config.consumer_key,
                      config.consumer_secret))
    results = twitter.trends.place(_id = 23424977)
    trendList = ''
    num = 0
    for location in results:
        for trend in location["trends"]:
            if num < 5:
                trendList += str(trend["name"]) + '\n'
            num += 1
    return trendList
