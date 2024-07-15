# Generated by Django 5.0.6 on 2024-07-15 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("question_extractor_ocr", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UploadedFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="uploads/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("extracted_text", models.TextField(blank=True, null=True)),
                ("is_processed", models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name="ExtractedText",
        ),
    ]
