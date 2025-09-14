from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView,UpdateView,CreateView
from django.db import transaction
from django.contrib import messages
from .models import Book, Review, Tag
from .forms import ReviewForm,BookForm

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_reviews = Review.objects.filter(user=self.request.user, book=self.object)
        other_reviews = Review.objects.filter(book=self.object).exclude(user=self.request.user).select_related('user').order_by('-created_at')[:5]#最新5件
        context['my_reviews'] = my_reviews
        context['other_reviews'] = other_reviews
        return context
    
class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "reading/review_form.html"


    def get_form_kwargs(self):
        """
        ユーザー情報をフォームに渡す。
        レビュー時に選択できるタグをログインユーザーのものに限定するため。
        """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        """すでにレビューが存在する場合は編集画面へリダイレクト"""
        self.book = get_object_or_404(Book, pk=kwargs["book_id"])
        exists = Review.objects.filter(user=request.user, book=self.book).first()
        if exists:
            return redirect("review_edit", pk=exists.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """保存に際し、フォームに存在しないユーザーと書籍の情報をセット"""
        form.instance.user = self.request.user
        form.instance.book = self.book
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("book_detail", args=[self.book.pk])
    
    
class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "reading/review_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("book_detail", args=[self.object.book_id])
    

class TagListCreateView(LoginRequiredMixin, CreateView):
    """tag登録用ビュー"""
    model = Tag
    fields = ["name"]
    template_name = "reading/tag_list_create.html"
    success_url = reverse_lazy("tag_list_create")

    def form_valid(self, form):
        """フォームにないユーザー情報を追加"""
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # ★自分のタグだけ一覧表示
        ctx["tags"] = Tag.objects.filter(owner=self.request.user).order_by("name")
        return ctx
    
class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "reading/book_form.html"
    
    def get_success_url(self):
        return reverse_lazy("book_detail", args=[self.object.pk])