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

    # def clean_slug(self):
    #     new_slug = self.cleaned_data['slug'].lower()
    #
    #     if new_slug == 'create':
    #         raise ValidationError('Slug уже занят')
    #     return new_slug

    class Meta:
        model = Genre
        fields = [
            "text",
            "slug",
            "image",
                  ]
        widgets = {
            "text":forms.Textarea(attrs={"class":"form-control"}),
            "slug":forms.SlugField(),
            "image":forms.ImageField(),
        }


class ArtistForm(forms.Form):
    title = forms.CharField(max_length=50)
    slug = forms.SlugField()
    img = forms.ImageField()
    description = forms.Textarea()

    # def clean_slug(self):
    #     new_slug = self.cleaned_data['slug'].lower()
    #
    #     if new_slug == 'create':
    #         raise ValidationError('Slug уже занят')
    #     return new_slug

    def save(self):
        new_add = Artist.object.create(
            title=self.cleaned_data['title'],
            desc=self.cleaned_data['description'],
            img=self.cleaned_data['img'],
            slug=self.cleaned_data['slug'],
        )
        return new_add


from django_select2 import forms as s2forms

class ArtistWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]


class ReviewForm(forms.ModelForm):
    files = MultiMediaField(
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
            # 'file',
            'is_draft',
        )

        widgets = {
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "image":forms.FileInput(attrs={"class":"form-control"}),
            # "file":forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True})),
            "artist":ArtistWidget(attrs={"class":"form-control"}),
            "genre": forms.Select(attrs={"class":"form-control"}),
        }


class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["text",]
        widgets = {
            "text":forms.Textarea(attrs={"class":"cmnt_field"})
        }

