import tweepy
import os
import time
from tweetUtils import get_alt_text, get_media

# 12s is min time to not exceed limit
SLEEP_TIME = 15

## Authenticate to Twitter
API_KEY = os.environ.get("TWITTER_API_KEY")
API_KEY_SECRET = os.environ.get("TWITTER_API_KEY_SECRET")
ACCESS_KEY = os.environ.get("TWITTER_ACCESS_KEY")
ACCESS_KEY_SECRET = os.environ.get("TWITTER_ACCESS_KEY_SECRET")
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_KEY_SECRET)

## Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

last_handled_id = 889145223221096448 # TODO read from file, Pre testing tweet id
# TODO use streams instead of event loop. for now, the sleep time will not exceed rate limit
while (True):
  time.sleep(SLEEP_TIME)

  # Would use a cursor, but I should be using a stream anyway
  mentions = api.mentions_timeline(since_id=last_handled_id)
  print(len(mentions))
  if len(mentions) == 0:
    continue

  last_handled_id = mentions[0].id
  # TODO write last_handled_id to file

  
  reply_to_tweet_ids = [mention.in_reply_to_status_id_str for mention in mentions]
  reply_to_tweets = api.statuses_lookup(reply_to_tweet_ids, include_entities=True, tweet_mode='extended')
  for tweet in reply_to_tweets:
    if not tweet.extended_entities or 'media' not in tweet.extended_entities:
      print("no media found for tweet {}".format(tweet.id))
      continue

    media = get_media(tweet)
    if media is None or len(media) == 0:
      print("no media found for tweet {}".format(tweet.id))

    else:
      media = media[0] # TODO alt text for all photos, if does not fit, multi-tweet
      if media["type"] == "photo":
        alt_text = get_alt_text(media)

      elif media["type"] == "video":
        print("TODO implement captioning")

      else:
        print("unrecognized media type for tweet {}".format(tweet.id))




