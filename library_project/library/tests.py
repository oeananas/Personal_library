from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from library.models import Bookshelf
from library.models import Book
from library.models import Author


class TestLibrary(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="author", slug='default')
        self.bookshelf = Bookshelf.objects.create(name="bookshelf", slug='default')
        self.book = Book.objects.create(
            title='title',
            author=self.author,
            bookshelf=self.bookshelf,
            number_on_shelf=1,
            slug='default'
        )

    def tearDown(self):
        self.bookshelf.delete()
        self.book.delete()
        self.author.delete()

    def test_bookshelf_create(self):
        client = APIClient()
        url = reverse('bookshelves')
        data = {
            'name': 'new name',
            'slug': 'default'
        }

        resp = client.post(url, data)
        self.assertEqual(resp.status_code, 201)

    def test_author_create(self):
        client = APIClient()
        url = reverse('authors')
        data = {
            'name': 'new name',
            'slug': 'default'
        }

        resp = client.post(url, data)
        self.assertEqual(resp.status_code, 201)

    def test_book_create(self):
        client = APIClient()
        url = reverse('books')
        data = {
            'title': 'new title',
            'author': self.author.id,
            'bookshelf': self.bookshelf.id,
            'number_on_shelf': 1,
            'slug': 'default'
        }

        resp = client.post(url, data)
        self.assertEqual(resp.status_code, 201)

    def test_book_create_big_number(self):
        client = APIClient()
        url = reverse('books')
        data = {
            'title': 'new title',
            'author': self.author.id,
            'bookshelf': self.bookshelf.id,
            'number_on_shelf': 100,
            'slug': 'default'
        }

        resp = client.post(url, data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['title'], 'new title')
        self.assertEqual(resp.data['number_on_shelf'], 2)

    def test_update_book_number(self):
        client = APIClient()
        url = reverse('book', kwargs={'slug': self.book.slug})
        self.assertEqual(self.book.title, 'title')
        self.assertEqual(self.book.bookshelf, self.bookshelf)
        self.assertEqual(self.bookshelf.books.count(), 1)
        self.assertEqual(self.book.number_on_shelf, 1)
        data = {
            'title': 'update',
            'author': self.book.author.id,
            'bookshelf': self.book.bookshelf.id,
            'number_on_shelf': 2,
            'slug': self.book.slug
        }
        resp = client.post(url, data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['title'], 'update')
        self.assertEqual(resp.data['number_on_shelf'], 1)

    def test_update_book_big_number(self):
        client = APIClient()
        url = reverse('book', kwargs={'slug': self.book.slug})
        data = {
            'title': 'update',
            'author': self.book.author.id,
            'bookshelf': self.book.bookshelf.id,
            'number_on_shelf': 100,
            'slug': self.book.slug
        }

        resp = client.post(url, data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['title'], 'update')
        self.assertEqual(resp.data['number_on_shelf'], 1)
