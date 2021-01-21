from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200, 
        help_text='Группа в которую будет опубликован ваш пост',
        verbose_name='Группа',)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        help_text='Текст вашего поста', 
        verbose_name='Текст'
        )
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, 
             related_name="posts")
    group = models.ForeignKey(Group, blank=True, null=True, 
            on_delete=models.SET_NULL, related_name="posts")

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]
