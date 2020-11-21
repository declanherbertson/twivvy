import math

MAX_TWEET_LENGTH = 280 - 30 # for added metadata
SPLIT_SIZE = MAX_TWEET_LENGTH - 15 # for added split characters

def breakup_tweets(tweet_text, hashtag):
  tweet_text = tweet_text.split(hashtag)[1]
  num_tweets = math.ceil(len(tweet_text) / SPLIT_SIZE)
  print(num_tweets)
  tweets = []
  for i in range(1, num_tweets + 1):
    tweet_i = f"[{i}/{num_tweets}] {hashtag}"
    tweet_i += tweet_text[(i-1)*SPLIT_SIZE:i*SPLIT_SIZE]
    if i != num_tweets:
      tweet_i += "..."
    tweets.append(tweet_i)
  return tweets

def punctate_descriptions(unpunctated_descriptions):
  punctated_descriptions = []
  for description in unpunctated_descriptions:
    punctated_description = description
    if punctated_description[-1] != ".":
      punctated_description += "."
    punctated_descriptions.append(punctated_description.capitalize())
  return punctated_descriptions

def format_descriptions_tweets(descriptions):
  descriptions = [d if d[1] != -1 else ("extracted text - " + d[0], 1) for d in descriptions]
  descriptions = [d[0] if d[1] >= .35 else "Unsure of image description 😢." for d in descriptions]
  descriptions = punctate_descriptions(descriptions)
  if len(descriptions) == 0:
    return []
  tweet_text = "#alttext\n"
  for i, description in enumerate(descriptions, start=1):
    tweet_text += "pic" + str(i) + ": " + description + "\n"
  if len(tweet_text) > MAX_TWEET_LENGTH:
    return breakup_tweets(tweet_text, "#alttext\n")
  return [tweet_text]

def format_captions_tweets(captions):
  tweet_text = "#captions\n" + captions
  if len(tweet_text) > MAX_TWEET_LENGTH:
    return breakup_tweets(tweet_text, "#captions\n")
  return [tweet_text]

# test_caption = "Officially good morning everyone. I guess yesterday there was a bunch of drama with other people not involving me, but people still want to mention my name. First of all, I have no idea what happened. I don't give a **** what happened. I'm too busy worrying about myself, my family. I don't care. I don't entertain it. So if you were friends with me and you're not anymore, keep my ******* name out of your mouth. *****. Thank you."
# print(len(test_caption))
# print(format_captions_tweets(test_caption))

# test_description = [("this is a picture of a man on a white sand beach holding a large picturesque spoon", 1), ("this is a turtule of a man on a white sand beach holding a large picturesque spoon", 1), ("this is a turtule of a man on a white sand beach holding a large picturesque spoon", 1), ("this is a turtule of a man on a white sand beach holding a large picturesque spoon", 1)]
# for t in format_descriptions_tweets(test_description):
#   print(t)