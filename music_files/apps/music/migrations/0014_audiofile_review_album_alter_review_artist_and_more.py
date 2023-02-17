# Generated by Django 4.1.5 on 2023-02-16 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0013_alter_comment_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='audio_files/')),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='album',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='music.album'),
        ),
        migrations.AlterField(
            model_name='review',
            name='artist',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='music.artist'),
        ),
        migrations.RemoveField(
            model_name='review',
            name='audio',
        ),
        migrations.AlterField(
            model_name='review',
            name='genre',
            field=models.ManyToManyField(blank=True, to='music.genre'),
        ),
        migrations.AddField(
            model_name='artist',
            name='file',
            field=models.ManyToManyField(blank=True, to='music.audiofile'),
        ),
        migrations.AddField(
            model_name='genre',
            name='file',
            field=models.ManyToManyField(blank=True, to='music.audiofile'),
        ),
        migrations.AddField(
            model_name='review',
            name='audio',
            field=models.ManyToManyField(blank=True, to='music.audiofile'),
        ),
    ]
