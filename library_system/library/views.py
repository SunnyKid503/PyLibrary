from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, User, BorrowRecord
from django.contrib import messages
from django.utils.dateparse import parse_datetime

def available_books(request):
    borrowed_books = BorrowRecord.objects.filter(returned_at__isnull=True).values_list('book_id', flat=True)
    books = Book.objects.exclude(id__in=borrowed_books)
    return render(request, 'library/available_books.html', {'books': books})

def borrow_record(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        cin = request.POST.get('cin')
        returned_at_raw = request.POST.get('returned_at')
        returned_at = parse_datetime(returned_at_raw) if returned_at_raw else None

        try:
            user = User.objects.get(cin=cin)
            BorrowRecord.objects.create(book=book, user=user, returned_at=returned_at)
            messages.success(request, f"{book.title} borrowed by {user.name}.")
            return redirect('available_books')

        except User.DoesNotExist:
            # redirect to user creation page with CIN prefilled
            return redirect(f'/register_user/?cin={cin}&book_id={book.id}')

    return render(request, 'library/borrow_record.html', {'book': book})

def register_user(request):
    if request.method == 'POST':
        cin = request.POST.get('cin')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        age = request.POST.get('age')
        book_id = request.POST.get('book_id')

        user = User.objects.create(cin=cin, name=name, surname=surname, age=age)
        book = Book.objects.get(id=book_id)

        BorrowRecord.objects.create(book=book, user=user)
        messages.success(request, f"{book.title} borrowed by {user.name} (new user).")
        return redirect('available_books')

    # GET: render form with pre-filled cin and book     
    cin = request.GET.get('cin')
    book_id = request.GET.get('book_id')
    return render(request, 'library/register_user.html', {'cin': cin, 'book_id': book_id})

from django.shortcuts import render, redirect
from .models import Author, Book
from django.contrib import messages

def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        isbn = request.POST.get('isbn')
        publication_year = request.POST.get('publication_year')
        author_id = request.POST.get('author')

        author = Author.objects.get(pk=author_id)
        Book.objects.create(
            title=title,
            ISBN=isbn,
            publication_year=publication_year,
            author=author
        )

        messages.success(request, f'Book "{title}" added successfully.')
        return redirect('available_books')

    authors = Author.objects.all()
    return render(request, 'library/add_book.html', {'authors': authors})


