from django.db import models
from django.conf import settings


class UploadedFile(models.Model):
    """
    Represents a file uploaded for OCR processing.

    Stores information about uploaded files, including the file itself,
    upload timestamp, extracted text, and processing status.

    Fields:
        file: The uploaded file, stored in 'uploads/' directory.
        uploaded_at: Timestamp of file upload, auto-set on creation.
        extracted_text: Text extracted from the file (optional).
        is_processed: Boolean indicating if the file has been processed.

    Note:
        Consider adding user association if needed in the future.
    """

    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True, null=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        """Returns the name of the uploaded file."""
        return self.file.name
