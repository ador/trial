import json
import codecs

infile = "data/streamed_book_tw_100.json"
outfilename = "data/streamed_book_tw_100.csv"
sep = "|"

out = open(outfilename, 'w')

def processSource(sourceStr):
    source = sourceStr.lower()
    listOfAppleDevices = ["iphone", "ipad", "for ios", "for mac"]
    listOfAutoTools = ["ifttt", "dlvr.it", "hootsuite", "twitterfeed", "tweetbot", "twittbot", "roundteam", "hubspot", "socialoomph", "smqueue", "linkis.com"]
    listOfSocialPlatforms = ["facebook", "linkedin", "tumblr", "wordpress"]
    listOfOtherMobile = ["windows phone", "mobile web", "for blackberry"]
    if "android" in source:
        return "android"
    for apple in listOfAppleDevices:
        if apple in source:
            return "appledevice"
    if "tweetdeck" in source:
        return "tweetdeck"
    if "twitter web client" in source:
        return "webclient"
    for soc in listOfSocialPlatforms:
        if soc in source:
            return "socialsite"
    for autoTool in listOfAutoTools:
        if autoTool in source:
            return "automated"
    for i in listOfOtherMobile:
        if i in source:
            return "othermobile"
    print(sourceStr)
    return "other"

def isRetweet(tweet):
    if 'retweeted_status' in tweet:
        if tweet['retweeted_status'] != None and len(tweet['retweeted_status']) > 0:
            return True
    return False

def getRetweetedTweetLikesNum(tweet):
    if isRetweet(tweet):
        return int(tweet['retweeted_status']['favorite_count'])
    else:
        return 0

def getRetweetedTweetRTNum(tweet):
    if isRetweet(tweet):
        return int(tweet['retweeted_status']['retweet_count'])
    else:
        return 0


def getLang(tweet):
    if 'lang' in tweet:
        return tweet['lang']
    return None

def getCountry(tweet):
    if 'place' in tweet and tweet['place'] != None:
        if 'country' in tweet['place']:
            return tweet['place']['country']
    return None

with open(infile, 'r') as f:
    for line in f:
        tweet = json.loads(unicode(line.encode('utf-8'), 'utf-8'))
        if "source" in tweet.keys():
            out.write(str(tweet['id']) + sep)
            out.write(str(tweet['timestamp_ms']) + sep)
            out.write(str(tweet['created_at']) + sep)
            out.write(str(processSource(tweet['source'])) + sep)
            out.write(str(isRetweet(tweet)) + sep)
            out.write(str(getRetweetedTweetLikesNum(tweet)) + sep)
            out.write(str(getRetweetedTweetRTNum(tweet)) + sep)
            out.write(str(getLang(tweet)) + sep)
            # out.write(str(getCountry(tweet)) + sep)
            out.write(repr(str(tweet['text'].encode('utf-8'))))
            out.write("\n")

        
        