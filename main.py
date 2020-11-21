import tweepy
import os
import time
from tweetUtils import get_alt_texts, get_medias, are_photos, is_video, is_gif, extract_video_url
from tweeter import tweet_descriptions, tweet_captions, tweet_unsupported
from videoUtil import get_captions_from_video_url

# 12s is min time to not exceed limit -- use 15s for long term
SLEEP_TIME = 5

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
# start at bts id 1329878347438907393
# post bts id: 1329955777038020608
# starts video id 1328710401043931138
# post dancing dog id 1329965439980429312
last_handled_id = None
with open(LAST_HANDLED_FILE_NAME, 'r') as f:
  last_handled_id = f.read().strip()

# TODO use streams instead of event loop (loop is easier to test). For now, the sleep time will not exceed rate limit.
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
      print(alt_texts)
      tweet_descriptions(api, alt_texts, tweet.id)

    elif is_video(medias):
      video_url = extract_video_url(medias[0])
      if video_url is None:
        print("Could not extract_video_url")
        continue
      captions = get_captions_from_video_url(video_url)
      if not captions:
        print("Could not extract captions")
        continue
      tweet_captions(api, captions, tweet.id)

    elif is_gif(medias):
      alt_texts = get_alt_texts(medias)
      tweet_descriptions(api, alt_texts, tweet.id)

    else:
      print("unsupported media type for tweet {}".format(tweet.id))
      print(tweet._json)
      tweet_unsupported(api, tweet.id)
