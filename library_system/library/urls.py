from django.urls import path
from . import views

urlpatterns = [
    path('available-books/', views.available_books, name='available_books'),
    path('borrow/<int:book_id>/', views.borrow_record, name='borrow_record'),
    path('register_user/', views.register_user, name='register_user'),
    path('add-book/', views.add_book, name='add_book'),



]
