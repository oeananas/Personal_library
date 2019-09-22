from django.db import models
from django.utils.text import slugify


class Author(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(allow_unicode=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save()

    def __str__(self):
        return self.name


class Bookshelf(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(allow_unicode=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    bookshelf = models.ForeignKey(Bookshelf, related_name='books', on_delete=models.CASCADE)
    number_on_shelf = models.IntegerField()
    slug = models.SlugField(allow_unicode=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save()

    def __str__(self):
        return self.title
