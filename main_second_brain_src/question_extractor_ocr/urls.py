"""
URL Configuration for the OCR application.

This module defines the URL patterns for the OCR application, mapping URLs to their corresponding views.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_view, name='upload_and_view'),
    path('extract/', views.extract_text_view, name='extract_text'),
]

"""
URL Patterns:

1. upload/
   - View: views.upload_view
   - Name: 'upload_and_view'
   - Description: Handles file uploads and renders the upload form.

2. extract/
   - View: views.extract_text_view
   - Name: 'extract_text'
   - Description: Processes text extraction from uploaded files.

Usage:
    These URL patterns should be included in the main urls.py file of the project.
    Example:
        from django.urls import include, path
        
        urlpatterns = [
            path('ocr/', include('ocr_app.urls')),
        ]

Note:
    Ensure that the view functions (upload_view and extract_text_view) are properly imported
    and defined in the views.py file of this application.
"""
