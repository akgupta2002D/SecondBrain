# Generated by Django 5.0.6 on 2024-07-06 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("progress_portal", "0002_alter_todoitem_todo_list_delete_todolist"),
    ]

    operations = [
        migrations.AddField(
            model_name="lifegoal",
            name="icon",
            field=models.ImageField(
                blank=True, default="icons/default_icon.png", upload_to="icons/"
            ),
        ),
    ]
