from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView
from .models import Book

# Create your views here.
class BookListView(LoginRequiredMixin, ListView):
    """
    書籍を一覧表示するビュー。
    検索機能を実装。タイトルと著者名で部分一致検索を行えるようにする。
    """
    model = Book
    template_name = 'reading/book_list.html'
    paginate_by = 10  # 1ページあたりの表示件数

    def get_queryset(self):
        """検索結果を絞る。"""
        q = self.request.GET.get('q')
        qs = Book.objects.all().order_by("-created_at")
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(author__icontains=q)
        return qs
    
class BookDetailView(LoginRequiredMixin, DetailView):
    """
    書籍の詳細画面用のビュー。
    自分のレビューを表示するとともに、他者のレビューも表示させたい。
    """
    model = Book
    template_name = 'reading/book_detail.html'