from tweeterUtil import format_descriptions_tweets, format_captions_tweets

def tweet_descriptions(api, descriptions, status_id):
  try:
    reply_to_id = status_id
    for tweet_text in format_descriptions_tweets(descriptions):
      print(tweet_text)
      last_tweet = api.update_status(tweet_text, reply_to_id, auto_populate_reply_metadata=True)
      reply_to_id = last_tweet.id
  except Exception as e:
    print(repr(e))

def tweet_captions(api, captions, status_id):
  try:
    reply_to_id = status_id
    for tweet_text in format_captions_tweets(captions):
      print(tweet_text)
      last_tweet = api.update_status(tweet_text, reply_to_id, auto_populate_reply_metadata=True)
      reply_to_id = last_tweet.id
  except Exception as e:
    print(repr(e))

def tweet_unsupported(api, status_id):
  try:
    api.update_status("Sorry, this media type is in progress👷", status_id, auto_populate_reply_metadata=True)
  except Exception as e:
    print(repr(e))