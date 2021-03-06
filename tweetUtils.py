from visionAi import describe_image

def are_photos(medias):
  return medias[0]["type"] == "photo"

def is_video(medias):
  return medias[0]["type"] == "video"

def is_gif(medias):
  return medias[0]["type"] == "animated_gif"

def has_alt_text(media):
  return ("ext_alt_text" in media
  and media["ext_alt_text"] is not None
  and media["ext_alt_text"] != "Image" and media["ext_alt_text"] != "")

def get_alt_text(media):
  if has_alt_text(media):
    return (media["ext_alt_text"], 1)
  return describe_image(media["media_url"])

def get_alt_texts(medias):
  return [get_alt_text(media) for media in medias]
  
def get_medias(tweet):
  if tweet.extended_entities and "media" in tweet.extended_entities:
    return tweet.extended_entities["media"]
  elif tweet.entities and "media" in tweet.entities:
    return tweet.entities["media"]
  else:
    return None

def extract_video_url(media):
  try:
    variants = media["video_info"]["variants"]
    mp4s = [v for v in variants if v["content_type"] == "video/mp4"]
    return mp4s[0]["url"]
  except:
    return None
    
def zip_mentions_to_reply_tweets(mentions, tweets):
  reply_to_id_dict = {}
  for mention in mentions:
    reply_to_id_dict[mention.in_reply_to_status_id_str] = mention
  results = []
  for tweet in tweets:
    results.append((reply_to_id_dict[str(tweet.id)], tweet))
  return results