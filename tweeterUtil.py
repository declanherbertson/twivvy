MAX_TWEET_LENGTH = 280

def breakup_description(description):
  return [description] # TODO breakup tweet

def punctate_descriptions(unpunctated_descriptions):
  punctated_descriptions = []
  for description in unpunctated_descriptions:
    punctated_description = description
    if punctated_description[-1] != ".":
      punctated_description += "."
    punctated_descriptions.append(punctated_description.capitalize())
  return punctated_descriptions

def format_descriptions_tweets(descriptions):
  descriptions = punctate_descriptions(descriptions)
  if len(descriptions) == 0:
    return []
  tweet_text = "#alttext\n"
  for i, description in enumerate(descriptions, start=1):
    tweet_text += "pic" + str(i) + ": " + description + "\n"
  if len(tweet_text) > MAX_TWEET_LENGTH:
    return breakup_description(tweet_text)
  return [tweet_text]