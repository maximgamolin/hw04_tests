from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Post, Group


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get('/')  
        self.assertEqual(response.status_code, 200)
    
    def test_author(self):
        response = self.guest_client.get('/author')
        self.assertEqual(response.status_code, 200)
    
    def test_tech(self):
        response = self.guest_client.get('/tech')
        self.assertEqual(response.status_code, 200)

class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Post.objects.create(
            text = "test text",
            id = '60'
        )

        super().setUpClass()
        Group.objects.create(
            title="Test Title",
            slug="Test-slug",
            description="Test description"
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = get_user_model().objects.create_user(username='SergeiM')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_correct_url_auth_user(self):
        """URL-адрес использует соответствующий шаблон."""

        templates_url_names = {
            'templates/index.html': '/',
            'templates/group.html':'group/test-slug/',
            'templates/posts/new.html': 'new/',
            'posts/templates/post.html': 'SergeiM/60',
            'posts/templates/profile.html': 'SergeiM/',
            'templates/posts/new.html': 'SergeiM/60/edit/'
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template) 

            with self.subTest():
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template) 
    
    def test_correct_template_edit(self):
        """Проверка страницы /new при вызовые /edit"""
        template = ['templates/posts/new.html', 'SergeiM/60/edit/']
        self.assertTemplateUsed(template[1], template[0])

    def test_correct_redirect_unauth_users_from_edit(self):
        """Проверка редиректа с /edit если 
        юзер не авторизован
        """
        response = self.guest_client.get('templates/posts/new.html', follow=True)
        self.assertRedirects(
            response, ('/new')
        )

