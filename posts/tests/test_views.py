from django.contrib.auth import get_user_model
from django.http import response
from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from django.db import models

from posts.models import Post, Group

class PostTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Post.objects.create(
            text="test text",
            id='62'
        )

        super().setUpClass()
        Group.objects.create(
            title="Test Title",
            slug="Test-slug",
            description="Test description"
        )

    def setUp(self):
        User = get_user_model()
        self.guest_client = Client()
        self.user = get_user_model().objects.create_user(username='SergeiM')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
       
        templates_pages_names = {
            'templates/index.html': reverse('posts:index'),
            'templates/group.html': (
                reverse('posts: group_posts', kwargs={'slug': 'Test-slug'})
                ),
            'templates/posts/new.html': reverse('posts:new_post')
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template) 

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""

        response = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)

    def test_group_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('post:group'))
        model_fields = {
            'title': models.CharField,
            'slug': models.SlugField,
            'description': models.TextField
        }

        for value, expected in model_fields.items():
            with self.subTest(value=value):
                model_field = response.context.get('model').fields.get(value)
                self.assertIsInstance(model_field, expected)

    def test_new_shows_correct_context(self):
        """Шаблон new сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:new'))
        forms_fields={
            'text': forms.fields.CharField,
            'group': models.ForeignKey,
        }
        for value, expected in forms_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_new_post_is_correct_index_and_group(self):
        """Пост на главной странице и группу"""
        
        templates_pages_names = {
            'templates/index.html': reverse('posts:index'),
            'templates/group.html': (
                reverse('posts: group_posts', kwargs={'slug': 'Test-slug'})
                ),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse('posts:index'))
                self.assertTemplateUsed(response, template) 

    def test_edit_has_correct_context(self):
        """Проверка контекста изменения поста"""
        response = self.authorized_client.get(reverse('posts: post_edit'))
        
        form_fields = {
            'text': forms.fields.CharField,
        }

        for value, expected in form_fields.items():
             with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
    
    def test_username_correct_context(self):
        """Проверка контекста username"""
        response = self.guest_client.get(reverse('posts: profile'))
        profile_author = response.context.get("SergeiM").user
        self.assertIsInstance(response, profile_author)
        self.assertEqual(profile_author.posts, 15)

    def test_post_id_correct_context(self):
        """Проверка контекста post_id"""
        response = self.guest_client.get(reverse('posts: post'))
        profile_author = response.context.get("SergeiM").user
        self.assertIsInstance(response, profile_author)

    def test_about_author_tech_correct_template(self):
        templates = {
            'templates/about/author': reverse('about:author'),
            'templates/about/tech': reverse('about:tech')
        }
        for template, reverse_name in templates.items():
            with self.subTest(template=template):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template) 