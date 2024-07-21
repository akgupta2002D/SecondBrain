"""
Views for handling file uploads and text extraction in the OCR application.

This module contains views for uploading files and extracting text using OCR.
It interacts with the UploadedFile model and FileUploadForm.
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import UploadedFile
from .forms import FileUploadForm
from django.contrib.auth.decorators import login_required

from .extract_text_util import extract_text


@login_required
def upload_view(request):
    """
    Handle file uploads and render the upload form.

    This view processes POST requests for file uploads and renders the upload form
    for GET requests. It uses AJAX to handle file uploads asynchronously.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered upload form for GET requests.
        JsonResponse: JSON response for POST requests, indicating success or failure.

    Raises:
        None
    """
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                instance = form.save()
                return JsonResponse({
                    'success': True,
                    'file_url': instance.file.url,
                    'file_id': instance.id
                })
            except Exception as e:
                # Log the error here if you have logging set up
                return JsonResponse({'success': False, 'errors': str(e)})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = FileUploadForm()

    return render(request, 'question_extractor_ocr/upload_and_view.html', {'form': form})


@login_required
def extract_text_view(request):
    """
    Extract text from an uploaded file.

    This view processes POST requests to extract text from a previously uploaded file.
    It updates the UploadedFile instance with the extracted text.

    Args:
        request (HttpRequest): The request object.

    Returns:
        JsonResponse: JSON response indicating success or failure, including extracted text if successful.

    Raises:
        None
    """
    if request.method == 'POST':
        file_id = request.POST.get('file_id')

        if not file_id:
            return JsonResponse({'success': False, 'message': 'File ID is required'})

        try:
            uploaded_file = UploadedFile.objects.get(id=file_id)
        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'message': 'File not found'})

        try:
            extracted_text = extract_text(uploaded_file.file.path)
            uploaded_file.extracted_text = extracted_text
            uploaded_file.is_processed = True
            uploaded_file.save()
            return JsonResponse({'success': True, 'extracted_text': extracted_text})
        except Exception as e:
            # Log the error here if you have logging set up
            return JsonResponse({'success': False, 'message': f'Error extracting text: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})
