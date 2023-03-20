# Generated by Django 3.2.16 on 2023-03-05 08:03

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0014_alter_question_correct_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='videolesson',
            name='description',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='videolesson',
            name='video',
            field=models.FileField(null=True, upload_to='video_uploaded/%Y/%m'),
        ),
    ]
