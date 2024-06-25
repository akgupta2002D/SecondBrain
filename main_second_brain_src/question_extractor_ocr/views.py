from django.shortcuts import render, HttpResponse
import pytesseract
# Adjust the path as needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Create your views here.


def uploadImageForOCR(request):
    return render(request, 'question_extractor_ocr/uploadImageForOCR.html', {'ocr': "ocr"})
