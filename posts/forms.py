from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']
        labels = {
            'text': 'Напишите что нибудь',
            'group': 'Группа'
            }
        verbose = {
            'text': 'Текст',
            'group': 'Группа'
        }
