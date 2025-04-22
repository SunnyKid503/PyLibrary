from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    ISBN = models.CharField(max_length=13)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    cin = models.CharField(max_length=8, unique=True)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} {self.surname} (CIN: {self.cin})"
    
class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.name} borrowed {self.book}"


