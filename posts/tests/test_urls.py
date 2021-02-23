from django.contrib import auth
from django.http import response
from django.test import TestCase, Client
from posts.models import Post, Group
from django.contrib.auth import get_user_model

User = get_user_model()


class StaticURLTests(TestCase):

    def setUp(self):
        super().setUp()

        self.guest_client = Client()
        self.user = User.objects.create(username='TestUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.group = Group.objects.create(
            title='TestTitle',
            slug='test-slug',
            description='TestDescription'
        )
        Post.objects.create(
            author=self.user,
            text='Тестовый текст',
            pub_date = '01.01.2000',
            group = self.group
        )

        self.templates={
            'index.html': '/',
            'group.html': '/group/test-slug',
            'templates/new.html': '/new'
        }

        
    def test_correct_template_used_guest(self):
        """URL-Adress uses correct template with guest"""
        for template, reverse_name in self.templates.items():
            with self.subTest():
                response = self.guest_client.get(reverse_name, follow = True)
                self.assertTemplateUsed(response, template)

    
    def test_correct_template_used_with_auth(self):
        """URL-Adress uses correct template with auth client"""
        for template, reverse_name in self.templates.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name, follow = True)
                self.assertTemplateUsed(response, template)