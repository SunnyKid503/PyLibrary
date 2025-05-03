from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from ..models import Book, User, BorrowRecord
from django.utils.timezone import make_aware
from datetime import datetime

def addBorrow_record(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    error_message=None

    if request.method == 'POST':
        cin = request.POST.get('cin')
        estimated_return_raw = request.POST.get('estimated_return_at')
        estimated_return_at = parse_datetime(estimated_return_raw)


        if not cin.isdigit() or len(cin) != 8:
            error_message = "CIN must be exactly 8 digits."
            return render(request, 'borrow/Addborrow_record.html', {
            'book': book,
            'error_message': error_message
    })
        
        if estimated_return_at:
            estimated_return_at = make_aware(estimated_return_at)

        try:
            user = User.objects.get(cin=cin)
            BorrowRecord.objects.create(
                book=book,
                user=user,
                estimated_return_at=estimated_return_at
            )
            messages.success(request, f"{book.title} borrowed by {user.name}.")
            return redirect('available_books')
        except User.DoesNotExist:
            return redirect(f'/register_user/?cin={cin}&book_id={book.id}')

    return render(request, 'borrow/Addborrow_record.html', {
        'book': book,
        'error_message': error_message
    })


def endBorrowRecord(request, record_id):
    record = get_object_or_404(BorrowRecord, id=record_id)

    if request.method == 'POST':
        returned_at_raw = request.POST.get('returned_at')
        returned_at = parse_datetime(returned_at_raw)

        if returned_at:
            returned_at = make_aware(returned_at)

        record.returned_at = returned_at
        record.save()
        messages.success(request, "Book return recorded successfully.")
        return redirect('available_books')

    return render(request, 'borrow/Endborrow_record.html', {'record': record})


def update_borrow_record(request, record_id):
    record = get_object_or_404(BorrowRecord, id=record_id)

    if request.method == 'POST':
        borrowed_at_raw = request.POST.get('borrowed_at')
        estimated_return_at_raw = request.POST.get('estimated_return_at')
        returned_at_raw = request.POST.get('returned_at')

        # Parse and make aware
        if borrowed_at_raw:
            record.borrowed_at = make_aware(datetime.fromisoformat(borrowed_at_raw))
        if estimated_return_at_raw:
            record.estimated_return_at = make_aware(datetime.fromisoformat(estimated_return_at_raw))
        if returned_at_raw and record.returned_at:
            record.returned_at = make_aware(datetime.fromisoformat(returned_at_raw))

        record.save()
        messages.success(request, "Borrow record updated successfully.")
        return redirect('borrow_list')

    return render(request, 'borrow/update_borrow_record.html', {'record': record})


def delete_borrow_record(request, record_id):
    record = get_object_or_404(BorrowRecord, id=record_id)

    if request.method == 'POST':
        record.delete()
        messages.success(request, "Borrow record deleted successfully.")
        return redirect('borrow_list')

    return render(request, 'borrow/delete_borrow_record.html', {'record': record})


def borrow_list (request) :
    borrow_records = BorrowRecord.objects.select_related('book','user').all()
    return render (request,'borrow/borrow_list.html' , {'borrow_records' : borrow_records})




