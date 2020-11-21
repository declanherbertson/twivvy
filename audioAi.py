import azure.cognitiveservices.speech as speechsdk
import os, time

AZURE_SPEECH_KEY = os.environ.get("AZURE_SPEECH_API_KEY")
AZURE_REGION = os.environ.get("AZURE_REGION")

captions = ""

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

def caption_audio_long(filename):
  speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
  audio_config = speechsdk.audio.AudioConfig(filename=filename)
  speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

  done = False
  global captions
  captions = ""

  def stop_cb(evt):
    print('CLOSING on {}'.format(evt))
    speech_recognizer.stop_continuous_recognition()
    nonlocal done
    done = True
  def recognize_cb(evt):
    global captions
    # print(captions)
    captions += " " + evt.result.text
    print(evt.result.text)


  speech_recognizer.recognizing.connect(lambda evt: None)
  speech_recognizer.recognized.connect(recognize_cb)
  speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
  speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
  speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

  speech_recognizer.session_stopped.connect(stop_cb)
  speech_recognizer.canceled.connect(stop_cb)

  speech_recognizer.start_continuous_recognition()
  while not done:
      time.sleep(.5)
  return captions


# test_audio = "male_FDUwvzDY.wav"
# test_audio_long = "male.wav"
# print(caption_audio_long(test_audio))
