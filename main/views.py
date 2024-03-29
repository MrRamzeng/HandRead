from django.shortcuts import render, redirect

from .forms import UpdatePosition
from .models import Book, Content, UserBooks, BookPage


def index(request):
    books = list(Book.objects.order_by('?').values_list('id', flat=True))
    queryset = Content.objects.filter(
        type__tag='p', text_len__gte=200  # , text_len__lte=500
    ).values(
        'text', 'type__book', 'type__book__name', 'type__book__price',
        'type__book__image'
    ).order_by('?')
    contents = []
    while books:
        id = books.pop()
        for content in queryset:
            if content['type__book'] == id:
                contents.append(content)
                break

    return render(
        request, 'book/index.html', {
            'contents': contents,
            'books': books
        }
    )


def books(request):
    books = Book.objects.values('id', 'image', 'name', 'price')
    return render(
        request,
        'book/books.html',
        {
            'books': books,
        }
    )


def book(request, id):
    book = Book.objects.get(id=id)
    return render(
        request,
        'book/book.html',
        {
            'book': book
        }
    )


def add_book(request, book_id):
    UserBooks.objects.get_or_create(
        user_id=request.user.id, book_id=book_id
    )
    return redirect('user_books')


def user_books(request):
    books = UserBooks.objects.filter(user_id=request.user.id)
    return render(
        request,
        'book/user_books.html',
        {
            'books': books
        }
    )


def reading(request, book_id):
    book = UserBooks.objects.get(book_id=book_id, user_id=request.user.id)
    if book.has_read:
        return redirect('user_books')

    if request.method == 'POST':
        form = UpdatePosition(request.POST)
        if form.is_valid():
            book.page_position = form.cleaned_data.get('position')
            if book.page_position >= book.get_pages_count():
                book.has_read = True
            book.save()

            return redirect('reading', book_id)
    else:
        form = UpdatePosition(
            initial={
                'position': book.page_position
            }
        )
    pages = BookPage.objects.filter(
        book_id=book_id
    )[book.page_position:book.page_position + 2]

    return render(
        request,
        'book/reading.html',
        {
            'pages': pages,
            'form': form,
            'pages_count': book.get_pages_count()
        }
    )


def set_part(contents):
    part = []
    symbols = 1997
    for content in contents:
        if symbols > len(content.text):
            slice_content(part, content)
            symbols -= len(content.text)
        else:
            slice_content(part, content, symbols)
            break
    return part


def slice_content(lst, content, position=0):
    lst.append(
        {
            'tag': content.type.tag,
            'css': content.type.css,
            'src': content.type.src,
            'text': content.text[:position] + '...' if position else
            content.text
        }
    )


def typing(request, book_id):
    book = UserBooks.objects.get(book_id=book_id, user_id=request.user.id)
    if book.has_print:
        return redirect('user_books')

    if request.method == 'POST':
        form = UpdatePosition(request.POST)
        if form.is_valid():
            book.typing_position = form.cleaned_data.get('position')
            if book.get_print_progress() == 100:
                book.has_print = True
            book.save()
            return redirect('typing', book_id)
    else:
        form = UpdatePosition(
            initial={
                'position': book.typing_position
            }
        )

    contents = Content.objects.filter(
        type__book_id=book_id
    )[book.typing_position:]
    part = set_part(contents)

    return render(
        request,
        'book/typing.html',
        {
            'form': form,
            'contents': part
        }
    )
