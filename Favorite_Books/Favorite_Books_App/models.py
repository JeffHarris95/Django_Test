from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters."
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 3 characters."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):        
            errors['email'] = ("Invalid email address!")
        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Passwords do not matach."
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 3 characters."
        email = User.objects.filter(email_address=postData['email'])
        if email:
            errors["unique"] = "Email is Taken."
        
        return errors
    
    def login_validator(self, postData):
        errors = {}
        email = User.objects.filter(email_address=postData['email'])
        if not email:
            errors["creds"] = "Invalid Credentails."

        else:
            logged_user = email[0]
            if not bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                errors["creds"] = "Invalid Credentails."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors["title"] = "Title is required."
        if len(postData['description']) < 5:
            errors["description"] = "Description is must be at least 5 characters."
        
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()