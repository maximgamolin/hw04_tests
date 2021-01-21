import os
import shutil
import tempfile
from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse
from django import forms


from posts.forms import PostForm
from posts.models import Post, Group

class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostForm()

        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

        Post.objects.create(
            text ='Тестовый текст',
        )

        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()

        form_data = {
            'text': 'Тестовый текст'
        }
        response = self.guest_client.post(
            reverse('posts:index'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, 'index')
        self.assertEqual(Post.objects.count(), posts_count+1)
        self.assertTrue(Post.objects.filter(text='Тестовый текст').exists())

    def test_post_exist_in_db(self):
        post = Post.objects.create(
            text='Ох уж эти кошечки',
            pub_date='11.10.2020',
        form_data = {
            'text': 'Кошечки пожирают тунца'
        }
        post_count = Post.objects.count()
        response = self.authorized_client.post(
            reverse('post_edit', args=[self.user.username, post.id]),
            data=form_data,
            follow=True,
        )
        post.refresh_from_db()
        self.assertEqual(Post.objects.count(), post_count)
        self.assertNotEqual(post.text, form_data['text'])
        self.assertEqual(post.group.title, form_data['group'])
        self.assertEqual(response.status_code, 200)