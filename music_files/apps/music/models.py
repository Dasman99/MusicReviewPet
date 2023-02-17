from django.db import models
# Create your models here.
from apps.accounts.models import User


# class AudioFile(models.Model):
#     # name = models.CharField(max_length=100)
#     file = models.FileField(upload_to='audio_files/')
#
#     def __str__(self):
#         return self.file


class Genre(models.Model):
    name = models.CharField("Название", max_length=200, unique=True)
    description = models.TextField("Описание", null=True)
    icon = models.ImageField(upload_to="genre/icon", null=True)
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField("Название", max_length=50)
    description = models.TextField("Описание", null=True)
    image = models.ImageField("Фото")
    slug = models.SlugField(max_length=50)
    genre = models.ManyToManyField(Genre, related_name="genre_artists")

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField("Название", max_length=50)
    image = models.ImageField("Фото", upload_to='media/albums_icon')
    release = models.DateTimeField()
    is_draft = models.BooleanField("Черновик", default=True)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        null=True,
    )
    genre = models.ManyToManyField(Genre, related_name="genre_albums")

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"

    def __str__(self):
        return self.title


# class AudioFile(models.Model):
#     album = models.ForeignKey(Album, on_delete=models.CASCADE, default=None)
#     file = models.FileField()

# class Attachment(models.Model):
#     file = models.FileField(upload_to='media/audio_files')


class Review(models.Model):
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    image = models.ImageField("Фото")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    is_draft = models.BooleanField("Черновик", default=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, default=None)
    genre = models.ManyToManyField(Genre)
    file = models.FileField(upload_to='media/audio_files', default=None)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Рецензия"
        verbose_name_plural = "Рецензии"

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = "Автор")
    review = models.ForeignKey(Review,  on_delete=models.CASCADE, verbose_name ="Рецензии", related_name= "comments")
    text = models.TextField("Комментарий", null=True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return format(self.text)