# transcriber/tasks.py
from celery import shared_task
from .models import Transcription
from .transcriber import download_audio, transcribe_audio


@shared_task
def transcribe_video(transcription_id):
    transcription = Transcription.objects.get(id=transcription_id)
    transcription.status = 'in_progress'
    transcription.save()

    try:
        audio_file = download_audio(transcription.video_url)
        transcript = transcribe_audio(audio_file)
        transcription.transcript = transcript
        transcription.status = 'completed'
    except Exception as e:
        transcription.status = 'failed'
        print(f"Transcription failed: {str(e)}")

    transcription.save()
