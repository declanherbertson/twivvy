from tweeterUtil import format_descriptions_tweets

def tweet_descriptions(api, descriptions, status_id):
  for tweet_text in format_descriptions_tweets(descriptions):
    print(tweet_text)
    # api.update_status(tweet_text)
    api.update_status(tweet_text, status_id, auto_populate_reply_metadata=True)