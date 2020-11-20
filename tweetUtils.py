from visionAi import describe_image

def has_alt_text(media):
  return ("ext_alt_text" in media
  and media["ext_alt_text"] is not None
  and media["ext_alt_text"] != "Image" and media["ext_alt_text"] != "")

def get_alt_text(media):
  if has_alt_text(media):
    return (media["ext_alt_text"], 1)
  return describe_image(media)
  
def get_media(tweet):
  if tweet.extended_entities and "media" in tweet.extended_entities:
    return tweet.extended_entities["media"]
  elif tweet.entities and "media" in tweet.entities:
    return tweet.entities["media"]
  else:
    return None