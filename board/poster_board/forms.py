from django import forms
from django.core.exceptions import ValidationError

from .models import *


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'author',
            'cat',
            'title',
            'text',
            'media',
        ]

        labels = {
            'author': 'Автор',
            'cat': 'Категории',
            'title': 'Заголовок',
            'text': 'Содержание',
            'media': 'Файл',
        }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        title = cleaned_data.get("title")

        if title == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'author',
            'post',
            'text'
        ]

        labels = {
            'author': 'Автор',
            'post': 'Объявление',
            'text': 'Содержание',
        }


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")
