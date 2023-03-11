from django.urls import path
from .views import index, BookListView, BookDetailView
# from django.conf.urls import url
from django.urls import re_path


urlpatterns = [
    path('', index, name='index'),
    path('books/', BookListView.as_view(), name='books' ),
    path('book/<slug>', BookDetailView.as_view(), name='book-detail'),
    # re_path(r'^book/(?P<slug>+)$', BookDetailView.as_view(), name='book-detail'),
]