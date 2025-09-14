from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from reading.models import Book, Review, Tag

User = get_user_model()

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username="alice", password="pw")
        self.user2 = User.objects.create_user(username="bob", password="pw")
        self.book1 = Book.objects.create(title="Django テスト", author="著者1")
        self.book2 = Book.objects.create(title="Python チュートリアル", author="著者2")
        # reviews
        self.review1 = Review.objects.create(user=self.user1, book=self.book1, rating=4, comment="良い")
        self.review2 = Review.objects.create(user=self.user2, book=self.book1, rating=5, comment="最高")
        # tags
        self.tag_u1 = Tag.objects.create(owner=self.user1, name="読了")
        self.tag_u2 = Tag.objects.create(owner=self.user2, name="積読")

    def test_book_list_search(self):
        self.client.force_login(self.user1)
        url = reverse("book_list")
        resp = self.client.get(url, {"q": "Django"})
        self.assertEqual(resp.status_code, 200)
        # context に object_list があり、book1 が含まれる
        self.assertIn(self.book1, resp.context["object_list"])
        self.assertNotIn(self.book2, resp.context["object_list"])

    def test_book_detail_context_reviews(self):
        self.client.force_login(self.user1)
        url = reverse("book_detail", args=[self.book1.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # 自分のレビューが my_reviews に含まれる
        self.assertIn(self.review1, resp.context["my_reviews"])
        # 他者レビューが other_reviews に含まれる
        other = list(resp.context["other_reviews"])
        self.assertIn(self.review2, other)
        # other_reviews は user を select_related しているため、user が読み込める
        self.assertTrue(all(hasattr(r, "user") for r in other))

    def test_review_create_redirects_if_exists(self):
        self.client.force_login(self.user1)
        url = reverse("review_create", args=[self.book1.pk])
        resp = self.client.get(url)
        # 既に自分のレビューがある場合、編集ページへリダイレクト
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("review_edit", args=[self.review1.pk]), resp["Location"])

    def test_review_update_forbidden_for_other_user(self):
        # 他ユーザーのレビュー編集ページは404になる（get_querysetでフィルタ）
        self.client.force_login(self.user1)
        url = reverse("review_edit", args=[self.review2.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_tag_list_create_view_shows_and_creates_user_tags(self):
        self.client.force_login(self.user1)
        url = reverse("tag_list_create")
        # GET: 自分のタグのみが context にある
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        tags = resp.context["tags"]
        self.assertIn(self.tag_u1, tags)
        self.assertNotIn(self.tag_u2, tags)

        # POST: 新しいタグを作成して owner が自分になる
        resp2 = self.client.post(url, {"name": "新しいタグ"})
        self.assertEqual(resp2.status_code, 302)  # success_url にリダイレクト
        created = Tag.objects.get(owner=self.user1, name="新しいタグ")
        self.assertIsNotNone(created)
