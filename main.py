import tweepy
import os
import time
from tweetUtils import get_alt_texts, get_medias, are_photos, is_video
from tweeter import tweet_descriptions

# 12s is min time to not exceed limit
SLEEP_TIME = 15

LAST_HANDLED_FILE_NAME = "last_handled.txt"

## Authenticate to Twitter
API_KEY = os.environ.get("TWITTER_API_KEY")
API_KEY_SECRET = os.environ.get("TWITTER_API_KEY_SECRET")
ACCESS_KEY = os.environ.get("TWITTER_ACCESS_KEY")
ACCESS_KEY_SECRET = os.environ.get("TWITTER_ACCESS_KEY_SECRET")
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_KEY_SECRET)

## Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Pre testing tweet Id 889145223221096448
last_handled_id = None
with open(LAST_HANDLED_FILE_NAME, 'r') as f:
  last_handled_id = f.read().strip()

# TODO use streams instead of event loop. for now, the sleep time will not exceed rate limit
while (True):
  time.sleep(SLEEP_TIME)
  print("iteration\n")

  # Would use a cursor, but I should be using a stream anyway
  mentions = api.mentions_timeline(since_id=last_handled_id)
  if len(mentions) == 0:
    continue

  last_handled_id = mentions[0].id
  with open(LAST_HANDLED_FILE_NAME, "w") as f:
    f.write(str(last_handled_id))

  reply_to_tweet_ids = [mention.in_reply_to_status_id_str for mention in mentions]
  reply_to_tweets = api.statuses_lookup(reply_to_tweet_ids, include_entities=True, tweet_mode='extended', include_ext_alt_text=True)
  for tweet in reply_to_tweets:
    medias = get_medias(tweet)
    if medias is None or len(medias) == 0:
      print("no media found for tweet {}".format(tweet.id))
      continue

    if are_photos(medias):
      alt_texts = get_alt_texts(medias)
      # Maybe filter low confidence responses here
      print(alt_texts)
      tweet_descriptions([alt_text[0] for alt_text in alt_texts])

    elif is_video(medias):
      print("TODO implement captioning")

    else:
      print("unsupported media type for tweet {}".format(tweet.id))




