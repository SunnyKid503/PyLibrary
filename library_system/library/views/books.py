from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Author, Book

def available_books(request):
    from ..models import BorrowRecord  # only here to avoid circular import
    borrowed_books = BorrowRecord.objects.filter(returned_at__isnull=True).values_list('book_id', flat=True)
    books = Book.objects.exclude(id__in=borrowed_books)
    return render(request, 'books/available_books.html', {'books': books})

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
    return render(request, 'books/add_book.html', {'authors': authors})



