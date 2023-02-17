# Generated by Django 4.1.5 on 2023-02-16 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0016_alter_review_artist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='created',
            new_name='release',
        ),
        migrations.RemoveField(
            model_name='album',
            name='audio',
        ),
        migrations.RemoveField(
            model_name='album',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='country',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='file',
        ),
        migrations.RemoveField(
            model_name='genre',
            name='file',
        ),
        migrations.AddField(
            model_name='audiofile',
            name='album',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='music.album'),
        ),
        migrations.AddField(
            model_name='genre',
            name='description',
            field=models.TextField(null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='music.artist'),
        ),
        migrations.AlterField(
            model_name='audiofile',
            name='file',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='genre',
            name='icon',
            field=models.ImageField(null=True, upload_to='genre/icon'),
        ),
    ]
