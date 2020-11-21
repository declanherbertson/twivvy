from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import os
import time

AZURE_VISION_KEY = os.environ.get("AZURE_VISION_API_KEY")
AZURE_VISION_ENDPOINT = os.environ.get("AZURE_VISION_ENDPOINT")


def ocr_image(image):
  result_text = ""
  client = ComputerVisionClient(AZURE_VISION_ENDPOINT, CognitiveServicesCredentials(AZURE_VISION_KEY))
  recognize_handw_results = client.read(image,  raw=True)
  # Get the operation location (URL with an ID at the end) from the response
  operation_location_remote = recognize_handw_results.headers["Operation-Location"]
  # Grab the ID from the URL
  operation_id = operation_location_remote.split("/")[-1]

  # Call the "GET" API and wait for it to retrieve the results 
  while True:
    get_handw_text_results = client.get_read_result(operation_id)
    if get_handw_text_results.status not in ['notStarted', 'running']:
      break

    time.sleep(1)

  # Print the detected text, line by line
  if get_handw_text_results.status == OperationStatusCodes.succeeded:
    for text_result in get_handw_text_results.analyze_result.read_results:
      for line in text_result.lines:
        result_text += line.text + " "

      return result_text

  return None

def describe_image(image, raw=True):
  client = ComputerVisionClient(AZURE_VISION_ENDPOINT, CognitiveServicesCredentials(AZURE_VISION_KEY))
  client_result = client.describe_image(image)
  tags = client_result.tags
  descriptions = client_result.captions

  if len(descriptions) == 0:
    return (None, None)

  top_description = descriptions[0]

  if ("text" in tags and "text" in top_description.text) or ("letter" in tags and "letter" in top_description.text):
    return (ocr_image(image), -1)

  return (top_description.text, top_description.confidence)

# test_photo = "https://pbs.twimg.com/media/EnRIB6fUwAAdkiK?format=jpg&name=large"
# test_doc = "https://pbs.twimg.com/media/EnRRG56XUAoWT6B?format=jpg&name=large"
# test_doc_2 = "https://pbs.twimg.com/media/EnMaA0-XUAU5ucS?format=jpg&name=medium"
# test_doc_3 = "https://pbs.twimg.com/media/EnMoxi6W4AAWY67?format=jpg&name=medium"
# print(describe_image(test_photo))
