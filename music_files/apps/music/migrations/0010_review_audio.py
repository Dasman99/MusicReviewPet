# Generated by Django 4.1.5 on 2023-02-14 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0009_remove_review_genres_review_artist'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='audio',
            field=models.FileField(null=True, upload_to='media/albums'),
        ),
    ]
