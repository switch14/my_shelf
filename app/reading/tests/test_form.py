from django.test import TestCase, RequestFactory #ビュー単体でテストするため
from django.contrib.auth import get_user_model
from reading.forms import ReviewForm
from reading.models import Tag, Book

User = get_user_model()

class ReviewFormTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(username="u1", password="p")
        self.user2 = User.objects.create_user(username="u2", password="p")
        self.tag1 = Tag.objects.create(owner=self.user1, name="t1")
        self.tag2 = Tag.objects.create(owner=self.user2, name="t2")
        self.book = Book.objects.create(title="本1", author="A")

    def test_tags_queryset_limited_to_request_user(self):
        """
        フォーム内のタグ選択肢がリクエストユーザーのタグに限定されていることを検証するテスト
        """
        request = self.factory.get("/")
        request.user = self.user1
        form = ReviewForm(request=request)
        qs = form.fields["tags"].queryset
        self.assertIn(self.tag1, qs)
        self.assertNotIn(self.tag2, qs)

    def test_read_date_widget_type(self):
        """
        フォーム内のread_dateフィールドのwidgetがDate型であることを検証するテスト
        """
        form = ReviewForm()
        widget = form.fields["read_date"].widget
        # DateInput の input_type は 'date' であること
        self.assertEqual(getattr(widget, "input_type", None), "date")
