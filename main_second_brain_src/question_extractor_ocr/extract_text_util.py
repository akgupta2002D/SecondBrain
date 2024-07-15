"""
Utility for extracting text from image and PDF files using OCR.

This module provides functions to extract text from various file types,
primarily focusing on images and PDFs. It uses Tesseract OCR for text
extraction and supports both Nepali and English languages.
"""

import logging
import os
import sys
from PIL import Image
import pytesseract
import PyPDF2
import pdf2image
import html

# Set the path to Tesseract executable

from django.conf import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# To use it in a seperate module outside of django environment, uncomment the below.

# tesseract_dir = os.path.abspath(os.path.join('..', '..', 'tesseract_exe'))
# pytesseract.pytesseract.tesseract_cmd = os.path.join(
#     tesseract_dir, 'tesseract.exe')

pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD


def extract_text_from_image(file_path, language='nep+eng'):
    """
    Extract text from an image file.

    Args:
        file_path (str): Path to the image file.
        language (str): Language(s) for OCR. Defaults to 'nep+eng'.

    Returns:
        str: Extracted text or None if extraction fails.
    """
    try:
        image = Image.open(file_path)
        # Add custom configuration here
        custom_config = r'--oem 3 --psm 6 -c preserve_interword_spaces=1'
        text = pytesseract.image_to_string(
            image, lang=language, config=custom_config)
        return text
    except Exception as e:
        print(f"Error extracting text from image: {str(e)}")
        return None


def extract_text_from_pdf(file_path, language='nep+eng'):
    """
    Extract text from a PDF file.

    Attempts direct text extraction first, falls back to OCR if no text is found.

    Args:
        file_path (str): Path to the PDF file.
        language (str): Language(s) for OCR. Defaults to 'nep+eng'.

    Returns:
        str: Extracted text or None if extraction fails.
    """
    try:
        # Try direct text extraction first
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""

        # If direct extraction yields no text, use OCR
        if not text.strip():
            print("No text found through direct extraction. Attempting OCR...")
            images = pdf2image.convert_from_path(file_path)
            text = ""
            # Add custom configuration here
            custom_config = r'--oem 3 --psm 6 -c preserve_interword_spaces=1'
            for image in images:
                text += pytesseract.image_to_string(
                    image, lang=language, config=custom_config) + "\n\n"

        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return None


def extract_text(file_path, language='nep+eng'):
    """
    Extract text from a file based on its extension.

    Supports image files (.png, .jpg, .jpeg, .tiff, .bmp) and PDFs.

    Args:
        file_path (str): Path to the file.
        language (str): Language(s) for OCR. Defaults to 'nep+eng'.

    Returns:
        str: Extracted text or None if extraction fails or file type is unsupported.
    """
    logger.debug(f"Attempting to extract text from: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return None

    file_extension = os.path.splitext(file_path.lower())[1]

    try:
        if file_extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            logger.debug(f"Extracting text from image: {file_path}")
            return extract_text_from_image(file_path, language)
        elif file_extension == '.pdf':
            logger.debug(f"Extracting text from PDF: {file_path}")
            return extract_text_from_pdf(file_path, language)
        else:
            logger.error(f"Unsupported file type: {file_extension}")
            return None
    except Exception as e:
        logger.exception(f"Error in extract_text: {str(e)}")
        return None


def create_html_output(extracted_text, file_path):
    """
    Create an HTML file with the extracted text.

    Args:
        extracted_text (str): The text extracted from the file.
        file_path (str): Original file path, used for naming the output.

    Returns:
        str: Path to the created HTML file.
    """
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Extracted Text from {os.path.basename(file_path)}</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }}
            h1 {{ color: #333; }}
            pre {{ background-color: #f4f4f4; padding: 15px; border-radius: 5px; white-space: pre-wrap; word-wrap: break-word; }}
        </style>
    </head>
    <body>
        <h1>Extracted Text from {os.path.basename(file_path)}</h1>
        <pre>{html.escape(extracted_text)}</pre>
    </body>
    </html>
    """

    output_file = f"extracted_text_{os.path.splitext(os.path.basename(file_path))[0]}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_file


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_text_util.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    print(f"Processing file: {file_path}")
    print(f"Using Tesseract from: {pytesseract.pytesseract.tesseract_cmd}")

    extracted_text = extract_text(file_path)

    if extracted_text:
        print("Extracted text:")
        print(extracted_text)

        # Create HTML output
        # html_file = create_html_output(extracted_text, file_path)
        # print(f"\nHTML output created: {html_file}")
    else:
        print("Text extraction failed.")


if __name__ == "__main__":
    main()
