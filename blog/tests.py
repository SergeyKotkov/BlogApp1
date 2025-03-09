from django.test import TestCase
from django.utils import timezone
from datetime import date, timedelta
from blog.models import CustomUser, Post, Comment
from django.core.exceptions import ValidationError

class UserModelTests(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            birth_date=date(2000, 1, 1)  # Явный объект date
        )
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(user.email, 'test@example.com')

    def test_create_superuser(self):
        admin = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
        self.assertEqual(admin.birth_date, date(1990, 1, 1))  # Проверка даты

class PostModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='author',
            email='author@example.com',
            password='authorpass',
            birth_date=date(1990, 1, 1)  # Явный объект date
        )
        self.post = Post.objects.create(
            title='Test Post',
            text='This is a test post',
            author=self.user
        )

    def test_create_post(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.user)

    def test_validate_author_age(self):
        young_user = CustomUser.objects.create_user(
            username='young',
            email='young@example.com',
            password='youngpass',
            birth_date=date.today() - timedelta(days=365*17)  # 17 лет
        )
        with self.assertRaises(ValidationError):
            post = Post(title='Too Young', text='Test', author=young_user)
            post.full_clean()

    def test_validate_forbidden_words(self):
        with self.assertRaises(ValidationError):
            Post.objects.create(
                title='Post with ерунда',
                text='Content',
                author=self.user
            )

class CommentModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='commenter',
            email='commenter@example.com',
            password='commentpass',
            birth_date=date(1995, 5, 5)  # Явный объект date
        )
        self.post = Post.objects.create(
            title='Test Post',
            text='Post content',
            author=self.user
        )
        self.comment = Comment.objects.create(
            author=self.user,
            post=self.post,
            text='Test comment'
        )

    def test_create_comment(self):
        self.assertEqual(self.comment.text, 'Test comment')
        self.assertEqual(self.comment.post, self.post)