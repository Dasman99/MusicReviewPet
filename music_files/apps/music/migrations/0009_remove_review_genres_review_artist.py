# Generated by Django 4.1.5 on 2023-02-14 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_album_updated_alter_album_artist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='genres',
        ),
        migrations.AddField(
            model_name='review',
            name='artist',
            field=models.ManyToManyField(related_name='artist', to='music.artist'),
        ),
    ]
