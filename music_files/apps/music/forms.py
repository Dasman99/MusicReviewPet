from django import forms
from  django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from .models import *
from django.forms.widgets import ClearableFileInput
from multiupload.fields import MultiFileField, MultiMediaField


class GenreForm(forms.Form):
    title = forms.CharField(max_length=50)
    slug = forms.SlugField()
    image = forms.ImageField()
    description = forms.Textarea()

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug уже занят')
        return new_slug

    def save(self):
        new_add = Genre.object.create(
            title=self.cleaned_data['title'],
            desc=self.cleaned_data['description'],
            slug=self.cleaned_data['slug']
        )

        return new_add


class ArtistForm(forms.Form):
    title = forms.CharField(max_length=50)
    slug = forms.SlugField()
    img = forms.ImageField()
    description = forms.Textarea()

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug уже занят')
        return new_slug

    def save(self):
        new_add = Artist.object.create(
            title=self.cleaned_data['title'],
            desc=self.cleaned_data['description'],
            img=self.cleaned_data['img'],
            slug=self.cleaned_data['slug'],
        )

        return new_add


# class ReviewCreateForm(forms.ModelForm):
#     description = forms.Textarea()
class UploadForm(forms.ModelForm):
    files = MultiMediaField(
        min_num=1,
        max_num=15,
        # max_file_size=1024*1024*5,
        media_type='audio'  # 'audio', 'video' or 'image'
    )

    class Meta:
        model = Review
        fields = (
            'title',
            'description',
            'image',
            'artist',
            'genre',
            'file',
            'is_draft',
        )

    widgets = {
        "title":forms.TextInput(attrs={"class":"form-group"}),
        "image":forms.FileInput(attrs={"class":"form-group"}),
        "file":forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True})),
        "artist":forms.Select(attrs={"class":"form-group"}),
        "genre": forms.Select(attrs={"class":"form-group"}),
    }


class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["text",]
        widgets = {
            "text":forms.Textarea(attrs={"class":"cmnt_field"})
        }


# class UploadForm(forms.Form):
#     attachments = MultiMediaField(
#         min_num=1,
#         max_num=15,
#         # max_file_size=1024*1024*5,
#         media_type='audio'  # 'audio', 'video' or 'image'
#     )

