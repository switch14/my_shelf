from django.urls import path
from . import views

urlpatterns = [
    path("", views.BookListView.as_view(), name="book_list"),
    path("books/<uuid:pk>/", views.BookDetailView.as_view(), name="book_detail"),
    path("books/<uuid:book_id>/review/new/", views.ReviewCreateView.as_view(), name="review_create"),
    path("reviews/<uuid:pk>/edit/", views.ReviewUpdateView.as_view(), name="review_edit"),
    path("tags/", views.TagListCreateView.as_view(), name="tag_list_create"),
]
