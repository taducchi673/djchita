# Generated by Django 3.2.16 on 2023-03-05 09:00

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0015_auto_20230305_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='notebooklesson',
            name='content',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]