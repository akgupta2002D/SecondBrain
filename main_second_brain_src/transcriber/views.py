from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Transcription
from .tasks import transcribe_video


@csrf_exempt
def transcribe(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        transcription = Transcription.objects.create(video_url=video_url)
        transcribe_video.delay(transcription.id)
        return JsonResponse({'id': transcription.id, 'status': 'pending'})
    return render(request, 'transcriber.html')


def get_status(request, transcription_id):
    try:
        transcription = Transcription.objects.get(id=transcription_id)
        return JsonResponse({
            'status': transcription.status,
            'transcript': transcription.transcript if transcription.status == 'completed' else None
        })
    except Transcription.DoesNotExist:
        return JsonResponse({'error': 'Transcription not found'}, status=404)
