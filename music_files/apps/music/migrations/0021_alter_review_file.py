# Generated by Django 4.1.5 on 2023-02-17 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0020_remove_review_audio_review_file_delete_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='file',
            field=models.FileField(default=None, upload_to='media/audio_files'),
        ),
    ]