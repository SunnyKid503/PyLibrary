from django.contrib import admin
from .models import Author, Book, BorrowRecord, User

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BorrowRecord)
admin.site.register(User)
