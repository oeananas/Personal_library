from django.db.models import F
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.http import QueryDict
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .models import Bookshelf
from .models import Book
from .models import Author
from .serializers import BookshelfSerializer
from .serializers import BookSerializer
from .serializers import AuthorSerializer


def set_correct_number_of_shelf(bookshelf, number, is_create=False, new_bookshelf=False, set_last=False):
    """
    Function set correct number on bookshelf, depends of books count on current bookshelf
    :param bookshelf:
    :param number:
    :param is_create:
    :param new_bookshelf:
    :param set_last:
    :return: number
    """
    count = Book.objects.filter(bookshelf=bookshelf).count()
    correct_number = number
    if is_create:
        if number > count + 1:
            correct_number = count + 1
    elif set_last or new_bookshelf:
        correct_number = count + 1
    else:
        if number > count:
            correct_number = count
    return correct_number


class MainPageView(TemplateView):
    template_name = 'library/index.html'


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer
    lookup_field = 'slug'
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "library/author.html"

    def create(self, request, *args, **kwargs):
        if settings.TEST_MODE:
            return super().create(request, *args, **kwargs)
        else:
            return redirect(to='/authors')

    def update(self, request, *args, **kwargs):
        if settings.TEST_MODE:
            return super().create(request, *args, **kwargs)
        else:
            return redirect(to='/authors')

    def destroy(self, request, *args, **kwargs):
        if settings.TEST_MODE:
            return super().create(request, *args, **kwargs)
        else:
            return redirect(to='/authors')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})


class BookshelfViewSet(viewsets.ModelViewSet):
    queryset = Bookshelf.objects.all()
    serializer_class = BookshelfSerializer
    lookup_field = 'slug'
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "library/bookshelf.html"

    def create(self, request, *args, **kwargs):
        if settings.TEST_MODE:
            return super().create(request, *args, **kwargs)
        else:
            return redirect(to='/bookshelves')

    def update(self, request, *args, **kwargs):
        if settings.TEST_MODE:
            return super().create(request, *args, **kwargs)
        else:
            return redirect(to='/bookshelves')

    def destroy(self, request, *args, **kwargs):
        if settings.TEST_MODE:
            return super().create(request, *args, **kwargs)
        else:
            return redirect(to='/bookshelves')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all() \
        .select_related('author', 'bookshelf') \
        .annotate(author_name=F('author__name'), bookshelf_name=F('bookshelf__name')) \
        .order_by('bookshelf', 'number_on_shelf')

    serializer_class = BookSerializer
    lookup_field = 'slug'
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "library/book.html"

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        context = {
            'authors': Author.objects.all().values('name', 'id'),
            'bookshelves': Bookshelf.objects.all().values('name', 'id')
        }
        response_data = self.get_list_response(queryset, context=context)
        return response_data

    def get_list_response(self, queryset, context=None):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response({'data': serializer.data, 'context': context})

    def author_list(self, request, *args, **kwargs):
        author_list_queryset = Author.objects.get(slug=kwargs['author_slug']).books \
            .select_related('bookshelf') \
            .annotate(author_name=F('author__name'), bookshelf_name=F('bookshelf__name')) \
            .order_by('number_on_shelf')
        context = {
            'author_slug': kwargs['author_slug'],
            'authors': Author.objects.all().values('name', 'id', 'slug'),
            'bookshelves': Bookshelf.objects.all().values('name', 'id', 'slug')
        }
        response_data = self.get_list_response(author_list_queryset, context=context)
        return response_data

    def bookshelf_list(self, request, *args, **kwargs):
        bookshelf_list_queryset = Bookshelf.objects.get(slug=kwargs['bookshelf_slug']).books \
            .select_related('author') \
            .annotate(author_name=F('author__name'), bookshelf_name=F('bookshelf__name')) \
            .order_by('number_on_shelf')
        context = {
            'bookshelf_slug': kwargs['bookshelf_slug'],
            'authors': Author.objects.all().values('name', 'id', 'slug'),
            'bookshelves': Bookshelf.objects.all().values('name', 'id', 'slug')
        }
        response_data = self.get_list_response(bookshelf_list_queryset, context=context)
        return response_data

    def create(self, request, *args, **kwargs):
        number_on_shelf = None
        if request.data.get('number_on_shelf'):
            number_on_shelf = int(request.data.get('number_on_shelf'))
        bookshelf = int(request.data.get('bookshelf'))
        number_on_shelf = set_correct_number_of_shelf(bookshelf, number_on_shelf, is_create=True)
        instance_qs = Book.objects.filter(bookshelf=bookshelf, number_on_shelf=number_on_shelf)
        if instance_qs.exists():
            new_number = Book.objects.filter(bookshelf=bookshelf).count()
            instance_qs.update(number_on_shelf=new_number + 1)
        request_data = request.data.dict()
        request_data['number_on_shelf'] = number_on_shelf
        query_dict_data = QueryDict('', mutable=True)
        query_dict_data.update(request_data)
        serializer = self.get_serializer(data=query_dict_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if settings.TEST_MODE:
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return redirect(to=request.META.get('HTTP_REFERER'))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        old_bookshelf = instance.bookshelf
        new_bookshelf = int(request.data.get('bookshelf'))
        old_number_on_shelf = instance.number_on_shelf
        new_number_on_shelf = int(request.data.get('number_on_shelf'))

        is_new_bookshelf = old_bookshelf.id != new_bookshelf
        is_new_number = old_number_on_shelf != new_number_on_shelf

        if is_new_bookshelf:
            Book.objects.filter(bookshelf=old_bookshelf, number_on_shelf__gt=old_number_on_shelf) \
                .update(number_on_shelf=F('number_on_shelf') - 1)

        new_number_on_shelf = set_correct_number_of_shelf(
            new_bookshelf,
            new_number_on_shelf,
            is_create=False,
            new_bookshelf=is_new_bookshelf,
        )
        if is_new_number and not is_new_bookshelf:
            Book.objects.filter(bookshelf=instance.bookshelf, number_on_shelf=new_number_on_shelf) \
                .update(number_on_shelf=old_number_on_shelf)
        elif is_new_number and is_new_bookshelf:
            last_number = set_correct_number_of_shelf(new_bookshelf, new_number_on_shelf, set_last=True)
            Book.objects.filter(bookshelf=new_bookshelf, number_on_shelf=new_number_on_shelf) \
                .update(number_on_shelf=last_number)

        request_data = request.data.dict()
        request_data['number_on_shelf'] = new_number_on_shelf
        query_dict_data = QueryDict('', mutable=True)
        query_dict_data.update(request_data)
        serializer = self.get_serializer(instance, data=query_dict_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        if settings.TEST_MODE:
            return Response(serializer.data)
        return redirect(to=request.META.get('HTTP_REFERER'))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        instance_number_on_shelf = instance.number_on_shelf
        Book.objects.filter(bookshelf=instance.bookshelf, number_on_shelf__gt=instance_number_on_shelf) \
            .update(number_on_shelf=F('number_on_shelf') - 1)
        if settings.TEST_MODE:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return redirect(to=request.META.get('HTTP_REFERER'))
