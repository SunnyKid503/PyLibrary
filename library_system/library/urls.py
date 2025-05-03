from django.urls import path
from .views.books import available_books, add_book
from .views.borrow import addBorrow_record, update_borrow_record
from .views.borrow import endBorrowRecord
from .views.borrow import borrow_list,delete_borrow_record
from .views.users import register_user
from .views.users import user_list, add_user, update_user, delete_user
from .views.library import landing_page 




urlpatterns = [

    path('',landing_page, name='landing_page'),
    path('available-books/', available_books, name='available_books'),
    path('add-book/', add_book, name='add_book'),

    path('borrowRecords/',borrow_list, name='borrow_list'),
    path('addborrow/<int:book_id>/', addBorrow_record, name='AddBorrow_record'),
    path('endborrow/<int:record_id>/',endBorrowRecord, name='EndBorrow_record'),
    path('deleteBorrow/<int:record_id>/',delete_borrow_record, name='deleteBorrow'),
    path('updateBorrow/<int:record_id>/',update_borrow_record, name='updateBorrow'),


    path('register_user/', register_user, name='register_user'),
    path('users/', user_list, name='user_list'),
    path('users/add/', add_user, name='add_user'),
    path('users/update/<int:user_id>/', update_user, name='update_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
]
