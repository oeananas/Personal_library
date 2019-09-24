from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main'),
    path('authors/', views.AuthorViewSet.as_view({'get': 'list',
                                                  'post': 'create'}), name='authors'),
    path('authors/<str:slug>/', views.AuthorViewSet.as_view({'get': 'retrieve',
                                                             'post': 'update'}), name='author'),
    path('authors/<str:slug>/del/', views.AuthorViewSet.as_view({'post': 'destroy'}), name='del_author'),
    path('authors/<str:author_slug>/books/', views.BookViewSet.as_view({'get': 'author_list'}), name='author_books'),
    path('bookshelves/', views.BookshelfViewSet.as_view({'get': 'list',
                                                         'post': 'create'}), name='bookshelves'),
    path('bookshelves/<str:slug>/', views.BookshelfViewSet.as_view({'get': 'retrieve',
                                                                    'post': 'update'}), name='bookshelf'),
    path('bookshelves/<str:slug>/del/', views.BookshelfViewSet.as_view({'post': 'destroy'}), name='del_bookshelf'),
    path('bookshelves/<str:bookshelf_slug>/books/', views.BookViewSet.as_view({'get': 'bookshelf_list',
                                                                               'post': 'create'}), name='bookshelf_books'),
    path('books/', views.BookViewSet.as_view({'get': 'list',
                                              'post': 'create'}), name='books'),
    path('books/<str:slug>/', views.BookViewSet.as_view({'get': 'retrieve',
                                                         'post': 'update'}), name='book'),
    path('books/<str:slug>/del/', views.BookViewSet.as_view({'post': 'destroy'}), name='del_book'),
]
