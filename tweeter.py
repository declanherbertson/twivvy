from tweeterUtil import format_descriptions_tweets, format_captions_tweets

def tweet_descriptions(api, descriptions, status_id):
  try:
    for tweet_text in format_descriptions_tweets(descriptions):
      print(tweet_text)
      api.update_status(tweet_text, status_id, auto_populate_reply_metadata=True)
  except Exception as e:
    print(e)

def tweet_captions(api, captions, status_id):
  try:
    for tweet_text in format_captions_tweets(captions):
      print(tweet_text)
      api.update_status(tweet_text, status_id, auto_populate_reply_metadata=True)
  except Exception as e:
    print(e)

def tweet_unsupported(api, status_id):
  try:
    api.update_status("Sorry, this media type is in progress👷", status_id, auto_populate_reply_metadata=True)
  except Exception as e:
    print(e)