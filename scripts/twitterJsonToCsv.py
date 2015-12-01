import json
import codecs

infile = "data/streamed_book_tw_100.json"
outfilename = "data/streamed_book_tw_100.csv"
sep = "|"

out = open(outfilename, 'w')

def processSource(sourceStr):
    source = sourceStr.lower()
    listOfAppleDevices = ["iphone", "ipad", "for ios", "for mac", "os x", "apple.com"]
    listOfAutoTools = ["ifttt", "dlvr.it", "hootsuite", "twitterfeed", "tweetbot",
                       "twittbot", "roundteam", "hubspot", "socialoomph", "smqueue",
                       "linkis.com", "tweet jukebox", "tweetsuite", "bufferapp",
                       "thousandtweets", "postplanner", "manageflitter", "crowdfire"]
    listOfSocialPlatforms = ["facebook", "linkedin", "tumblr", "wordpress",
                             "instagram", "pinterest"]
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

def isNiceRetweet(tweet):
    if 'retweeted_status' in tweet and tweet['retweeted_status'] != None:
        rts = tweet['retweeted_status']
        if ('favorite_count' in rts and rts['favorite_count'] != None and
                'retweet_count' in rts and rts['retweet_count'] != None and
                'created_at' in rts and rts['created_at'] != None and 
                'source' in rts and rts['source'] != None and
                'user' in rts and rts['user'] != None and 
                'followers_count' in rts['user'] and rts['user']['followers_count'] != None):
            return True
    return False

def getRetweetedTweetId(tweet, isRetweet):
    if isRetweet:
        return tweet['retweeted_status']['id']
    else:
        return None

def getRetweetedTweetLikesNum(tweet, isRetweet):
    if isRetweet:
        return int(tweet['retweeted_status']['favorite_count'])
    else:
        return 0

def getRetweetedTweetRTNum(tweet, isRetweet):
    if isRetweet:
        return int(tweet['retweeted_status']['retweet_count'])
    else:
        return 0

def getRetweetedTweetSource(tweet, isRetweet):
    if isRetweet:
        rtstr = tweet['retweeted_status']['source']
        return processSource(rtstr)
    else: 
        return None

def getRetweetedTweetAuthorFollowerCount(tweet, isRetweet):
    if isRetweet:
        rts = tweet['retweeted_status']
        return rts['user']['followers_count']
    else: 
        return 0

def getLang(tweet):
    if 'lang' in tweet:
        return tweet['lang']
    return None


with open(infile, 'r') as f:
    for line in f:
        tweet = json.loads(unicode(line.encode('utf-8'), 'utf-8'))
        if "source" in tweet.keys():
            out.write(str(tweet['id']) + sep)
            out.write(str(tweet['created_at']) + sep)
            out.write(str(processSource(tweet['source'])) + sep)
            out.write(str(getLang(tweet)) + sep)
            isRetweet = isNiceRetweet(tweet)
            out.write(str(isRetweet) + sep)
            out.write(str(getRetweetedTweetId(tweet, isRetweet)) + sep)
            out.write(str(getRetweetedTweetLikesNum(tweet, isRetweet)) + sep)
            out.write(str(getRetweetedTweetRTNum(tweet, isRetweet)) + sep)
            out.write(str(getRetweetedTweetSource(tweet, isRetweet)) + sep)
            out.write(str(getRetweetedTweetAuthorFollowerCount(tweet, isRetweet)) + sep)
            out.write(repr(str(tweet['text'].encode('utf-8'))))
            out.write("\n")

        
        