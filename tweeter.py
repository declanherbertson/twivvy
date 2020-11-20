from tweeterUtil import format_descriptions_tweets

def tweet_descriptions(api, descriptions, status_id):
  for tweet_text in format_descriptions_tweets(descriptions):
    pass
    # api.update_status(tweet_text, in_reply_to_status_id_str=status_id)