import youtube_dl
import speech_recognition as sr
from pydub import AudioSegment
import os


def download_audio(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return 'audio.wav'


def transcribe_audio(audio_file):
    audio = AudioSegment.from_wav(audio_file)
    chunk_length_ms = 60000  # 1 minute
    chunks = [audio[i:i+chunk_length_ms]
              for i in range(0, len(audio), chunk_length_ms)]

    recognizer = sr.Recognizer()
    transcript = ""
    for i, chunk in enumerate(chunks):
        chunk_file = f"chunk{i}.wav"
        chunk.export(chunk_file, format="wav")
        with sr.AudioFile(chunk_file) as source:
            audio = recognizer.record(source)
        try:
            transcript += recognizer.recognize_google(audio) + " "
        except sr.UnknownValueError:
            transcript += "[inaudible] "
        os.remove(chunk_file)

    os.remove(audio_file)
    return transcript
