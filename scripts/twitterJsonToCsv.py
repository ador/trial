import json
import codecs

infile = "data/streamed_book_tw_100.json"
outfilename = "data/streamed_book_tw_100.csv"
sep = "|"

out = open(outfilename, 'w')

def processSource(sourceStr):
    source = sourceStr.lower()
    apple = ["for mac", "iphone", "ios", "ipad"]
    for s in apple:
        if s in source:
            return "apple-device"
    automated = ["hootsuite", "ifttt", "roundteam"]
    for s in automated:
        if s in source:
            return "automated"
    if "android" in source:
        return "android"
    if "windows" in source:
        return "windows"
    if "facebook" in source or "linkedin" in source:
        return "socialsite"
    if "mobile" in source or "blackberry" in source:
        return "mobile"
    if "web client" in source:
        return "webclient"
    if "tweetdeck" in source:
        return "tweetdeck"
    else:
        return "other"

def isRetweet(tweet):
    if 'retweeted_status' in tweet:
        if tweet['retweeted_status'] != None and len(tweet['retweeted_status']) > 0:
            return True
    return False

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
            out.write(str(getLang(tweet)) + sep)
            # out.write(str(getCountry(tweet)) + sep)
            out.write(str(tweet['text'].encode('utf-8')))
            out.write("\n")

        
        