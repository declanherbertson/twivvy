from audioAi import caption_audio
import urllib.request
import subprocess
import os

def get_captions_from_video_url(video_url):
  try:
    # download video
    video_file_name = video_url.split("/")[-1].split("?")[0]
    urllib.request.urlretrieve(video_url, video_file_name)

    # convert video to audio
    audio_file_name = video_file_name.split(".")[0] + ".wav"
    command = f"ffmpeg -i {video_file_name} -ab 160k -ac 2 -ar 44100 -vn {audio_file_name}"
    subprocess.call(command, shell=True)

    # caption audio
    captions = caption_audio(audio_file_name)

    # delete audio and video
    os.remove(audio_file_name)
    os.remove(video_file_name)

    # return captions
    return captions
  except:
    return None