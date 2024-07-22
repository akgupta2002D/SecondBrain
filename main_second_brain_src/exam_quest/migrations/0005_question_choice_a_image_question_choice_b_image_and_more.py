# Generated by Django 5.0.6 on 2024-07-20 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exam_quest", "0004_delete_answer"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="choice_a_image",
            field=models.ImageField(blank=True, null=True, upload_to="choice_images/"),
        ),
        migrations.AddField(
            model_name="question",
            name="choice_b_image",
            field=models.ImageField(blank=True, null=True, upload_to="choice_images/"),
        ),
        migrations.AddField(
            model_name="question",
            name="choice_c_image",
            field=models.ImageField(blank=True, null=True, upload_to="choice_images/"),
        ),
        migrations.AddField(
            model_name="question",
            name="choice_d_image",
            field=models.ImageField(blank=True, null=True, upload_to="choice_images/"),
        ),
        migrations.AlterField(
            model_name="question",
            name="question_type",
            field=models.CharField(
                choices=[
                    ("MCQ", "Multiple Choice"),
                    ("TF", "True/False"),
                    ("FIB", "Fill in the Blanks"),
                    ("SA", "Short Answer"),
                    ("LA", "Long Answer"),
                    ("MAT", "Matching"),
                    ("IMG", "Image Choice"),
                ],
                max_length=3,
            ),
        ),
    ]