from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import User, Book, BorrowRecord

def register_user(request):
    cin = request.GET.get('cin')
    book_id = request.GET.get('book_id')


    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        age = request.POST.get('age')

        
        user = User.objects.create(cin=cin, name=name, surname=surname, age=age)
        book = get_object_or_404(Book, id=book_id)
        BorrowRecord.objects.create(book=book, user=user)
        messages.success(request, f"{book.title} borrowed by {user.name} (new user).")
        return redirect('available_books')
    
    return render(request, 'users/register_user.html', {
        'cin': cin,
        'book_id': book_id,
    })


def user_list (request):
    users = User.objects.all()
    return render (request,'users/user_list.html',{'users' : users})

def add_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        cin = request.POST.get('cin')
        age = request.POST.get('age')

        
        if not cin.isdigit() or len(cin) != 8:
            messages.error(request, "CIN must be exactly 8 digits.")
            return redirect('add_user')

       
        if User.objects.filter(cin=cin).exists():
            messages.error(request, "A user with this CIN already exists.")
        else:
            User.objects.create(name=name, surname=surname, cin=cin, age=age)
            messages.success(request, "User added successfully.")
            return redirect('user_list')

    return render(request, 'users/add_user.html')


def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        cin = request.POST.get('cin')
        age = request.POST.get('age')

        
        if not cin.isdigit() or len(cin) != 8:
            messages.error(request, "CIN must be exactly 8 digits.")
            return redirect('update_user', user_id=user.id)

        
        if User.objects.exclude(id=user.id).filter(cin=cin).exists():
            messages.error(request, "Another user with this CIN already exists.")
            return redirect('update_user', user_id=user.id)

        
        user.name = name
        user.surname = surname
        user.cin = cin
        user.age = age
        user.save()

        messages.success(request, "User updated successfully.")
        return redirect('user_list')

    return render(request, 'users/update_user.html', {'user': user})


def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('user_list')

    return render(request, 'users/delete_user.html', {'user': user})



