import azure.cognitiveservices.speech as speechsdk
import os

AZURE_SPEECH_KEY = os.environ.get("AZURE_SPEECH_API_KEY")
AZURE_REGION = os.environ.get("AZURE_REGION")

def caption_audio(filename):
  speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
  audio_input = speechsdk.AudioConfig(filename=filename)
  speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
  # NOTE: this only captions the first 15-30s, use continuous recognition for longer captions, twit max len = 2min 20sec
  result = speech_recognizer.recognize_once()

  # Error Checking
  if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))
  elif result.reason == speechsdk.ResultReason.NoMatch:
      print("No speech could be recognized: {}".format(result.no_match_details))
      return ""
  elif result.reason == speechsdk.ResultReason.Canceled:
      cancellation_details = result.cancellation_details
      print("Speech Recognition canceled: {}".format(cancellation_details.reason))
      if cancellation_details.reason == speechsdk.CancellationReason.Error:
          print("Error details: {}".format(cancellation_details.error_details))
      return ""

  return result.text

# test_audio = "male_FDUwvzDY.wav"
# test_audio_long = "male.wav"
# print(caption_audio(test_audio))
