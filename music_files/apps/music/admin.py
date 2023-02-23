from django.contrib import admin

from django import forms
from .models import *


class ReviewAdminForm(forms.ModelForm):
    description = forms.Textarea()

    class Meta:
        model = Review
        fields = '__all__'


# admin.site.register(Genre)
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "slug", "id"]


class SongInline(admin.TabularInline):
    model = Song


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm
    # inlines = [SongInline]
    list_display = ["title", "created"]
    list_filter = ["genre", "created", ]
    filter_horizontal = ["genre", "song"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["text"]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    inlines = [SongInline]
    list_display = ["title"]
    filter_horizontal = ["genre"]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ["title"]
    filter_horizontal = ["genre"]


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ["name"]
    filter_horizontal = ["genre"]


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ["name"]
    filter_horizontal = ["song"]


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    # list_display = ["song"]
    filter_horizontal = ["song"]
