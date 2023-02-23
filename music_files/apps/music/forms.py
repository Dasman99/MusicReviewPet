from django import forms
from  django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from .models import *
from django.forms.widgets import ClearableFileInput
from multiupload.fields import MultiFileField, MultiMediaField


class GenreForm(forms.ModelForm):

    class Meta:
        model = Genre
        fields = [
            "name",
            "slug",
            "icon",
        ]
        widgets = {
            "text": forms.TextInput(),
            "slug": forms.TextInput(),
            "icon": forms.FileInput(),
        }


class ArtistForm(forms.Form):
    title = forms.CharField(max_length=50)
    img = forms.ImageField()
    description = forms.Textarea()

    # def clean_slug(self):
    #     new_slug = self.cleaned_data['slug'].lower()
    #
    #     if new_slug == 'create':
    #         raise ValidationError('Slug уже занят')
    #     return new_slug

    class Meta:
        model = Artist
        fields = (
            'title',
            'image',
            'description',
        )

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }


from django_select2 import forms as s2forms


class ArtistWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]


class GenreWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains",
    ]


class ReviewForm(forms.ModelForm):
    song = MultiMediaField(
        min_num=1,
        max_num=15,
        # max_file_size=1024*1024*5,
        media_type='audio',  # 'audio', 'video' or 'image',
        attrs={"class":"form-control"}
    )

    class Meta:
        model = Review
        fields = (
            'title',
            'description',
            'image',
            'artist',
            'genre',
            'song',
            'is_draft',
        )

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "song": forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True})),
            "artist": ArtistWidget(attrs={"class": "form-control"}),
            "genre": GenreWidget(attrs={"class": "form-control"}),
            "is_draft": forms.CheckboxInput(attrs={"class":"form-control"})
        }


class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["text",]
        widgets = {
            "text":forms.Textarea(attrs={"class":"cmnt_field"})
        }


class PlaylistCreateForm(forms.ModelForm):
    name = forms.TextInput()

    class Meta:
        model = Playlist
        fields = (
            'name',
        )

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }