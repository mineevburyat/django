from django.urls import path
from .views import index, BookListView, \
                    BookDetailView, \
                    AuthorListView, \
                    AuthorDetailView, \
                    LoanedBooksByUserListView, \
                    LoanedBooksLibrarerListView, \
                    renew_book_librarian
# from django.conf.urls import url
from django.urls import re_path


urlpatterns = [
    path('', index, name='index'),
    
    path('books/', BookListView.as_view(), name='books' ),
    path('book/<slug>', BookDetailView.as_view(), name='book-detail'),
    path('authors/', AuthorListView.as_view(), name='authors' ),
    path('borrowed/', LoanedBooksLibrarerListView.as_view(), name='borrowed' ),
    path('author/<slug>', AuthorDetailView.as_view(), name='author-detail'),
    # re_path(r'^book/(?P<slug>+)$', BookDetailView.as_view(), name='book-detail'),
]

urlpatterns += [
    re_path(r'^mybooks/$', LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [
    re_path(r'^book/(?P<pk>[-\w]+)/renew/$', renew_book_librarian, name='renew-book-librarian'),
]