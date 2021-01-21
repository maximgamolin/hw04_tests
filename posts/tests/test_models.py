from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Post, Group

class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        Post.objects.create(
            text='Test Text',
            id='61'
        )

        cls.post= Post.objects.get(id='61')

        super().setUpClass()
        Group.objects.create(
            title='Test Title Group',
            slug='test-group',
            description='test-description'
        )
        cls.group = Group.objects.get(slug='test-group')

    def test_verbose_and_help_PostText(self):
        """verbose_name и help_text 
        в полях совпадает с ожидаемым в Post.
        """
        post = PostModelTest.post
        verbose = post._meta.get_field('text').verbose_name
        help = post._meta.get_field('text').help_text
        help_verbose={
            verbose:'Текст',
            help:'Текст вашего поста'
        }
        for value, expected in help_verbose.items():
            with self.subTest(value=value):
                self.assertEqual(value, expected)

    def test_verbose_and_help_PostText(self):
        """verbose_name и help_text 
        в полях совпадает с ожидаемым в Group.
        """
        group = PostModelTest.group
        verbose = group._meta.get_field('title').verbose_name
        help = group._meta.get_field('title').help_text

        help_verbose={
            verbose:'Группа в которую будет опубликован ваш пост',
            help:'Группа'
        }
        for value, expected in help_verbose.items():
            with self.subTest(value=value):
                self.assertEqual(value, expected)

    def test_str_Post(self):
        """str in Post."""
        post = PostModelTest.post
        self.assertEqual(post.text, 'Test text')

    def test_str_Group(self):
        """str in Group"""
        group = PostModelTest.group
        self.assertEqual(group.title, 'Test Title Group')