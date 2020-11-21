from visionAi import describe_image

def are_photos(medias):
  return medias[0]["type"] == "photo"

def is_video(medias):
  return medias[0]["type"] == "video"

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
    return media["video_info"]["variants"][0]["url"]
  except:
    return None
    