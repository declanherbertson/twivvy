from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os

AZURE_VISION_KEY = os.environ.get("AZURE_VISION_API_KEY")
AZURE_VISION_ENDPOINT = os.environ.get("AZURE_VISION_ENDPOINT")

def describe_image(image):
  client = ComputerVisionClient(AZURE_VISION_ENDPOINT, CognitiveServicesCredentials(AZURE_VISION_KEY))
  descriptions = client.describe_image(image).captions
  if len(descriptions) == 0:
    return (None, None)
  top_description = descriptions[0]
  return (top_description.text, top_description.confidence)

# test_photo = "https://images.unsplash.com/photo-1605812830455-2fadc55bc4ba?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80"
# print(describe_image(test_photo))