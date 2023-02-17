from django.contrib import admin

from django import forms
from .models import *


class ReviewAdminForm(forms.ModelForm):
    description = forms.Textarea()

    class Meta:
        model = Review
        fields = '__all__'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "slug", "id"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm
    list_display = ["title", "created", "is_draft"]
    list_filter = ["genre", "is_draft", "created", ]
    filter_horizontal = ["genre"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["text", ]


admin.site.register(Album)
admin.site.register(Artist)
# admin.site.register(Attachment)


# Register your models here.
