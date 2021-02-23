from django.test import TestCase
from posts.models import Post, Group
from django.contrib.auth import get_user_model


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = get_user_model()

        

        cls.post = Post.objects.create(
            text='Тестовый текст',
            author = User.objects.create(username='testUser'),
            pub_date = '01.01.2000'
        )

    def test_verbose(self):
        """verbose_name в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verbose = {
            'text': 'Текст поста',
            'group': 'Группа'
        }
        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, 
                    expected
                )

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Напишите что-нибудь',
            'group': 'Укажите группу'
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, 
                    expected
                )

    def test_str_is_title(self):
        """__str__ совпадает с ожидаемым"""
        post = PostModelTest.post
        expected_object_name = post.text[:15]
        self.assertEquals(expected_object_name, str(post))