from rest_framework import serializers

from .models import Bookshelf
from .models import Book
from .models import Author


class BookshelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookshelf
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):

    author_name = serializers.CharField(required=False)
    bookshelf_name = serializers.CharField(required=False)

    class Meta:
        model = Book
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
