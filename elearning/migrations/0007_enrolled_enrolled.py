# Generated by Django 3.2.16 on 2023-02-14 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0006_rename_topic_name_blog_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrolled',
            name='enrolled',
            field=models.BooleanField(default=False),
        ),
    ]
