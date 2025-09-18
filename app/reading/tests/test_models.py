from django.test import TestCase
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from reading.models import Book, Tag, Review

User = get_user_model()

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass")
        self.book = Book.objects.create(title="Django入門", author="著者A", year=2020)
        self.tag = Tag.objects.create(owner=self.user, name="お気に入り")

    def test_book_str(self):
        """
        Book.bookが書籍タイトルを正しく返すことを検証するテスト
        """
        self.assertEqual(str(self.book), "Django入門")

    def test_tag_str(self):
        """
        Tag.tagがタグ名を正しく返すことを検証するテスト
        """
        self.assertEqual(str(self.tag), "お気に入り")

    def test_review_str_and_unique_together(self):
        """
        Review.reviewが「書籍タイトル - 評価」を正しく返すこと。
        同一ユーザーが同一書籍のレビューを作成できないことを確認するためのテスト。
        """
        r = Review.objects.create(user=self.user, book=self.book, rating=5, comment="良かった")
        self.assertEqual(str(r), f"{self.book.title} - {r.rating}")

        # 同一ユーザー・同一書籍のレビューは2件目の作成でIntegrityError
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Review.objects.create(user=self.user, book=self.book, rating=4)
