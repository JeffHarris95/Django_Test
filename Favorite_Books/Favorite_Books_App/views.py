from django.shortcuts import redirect, render, HttpResponse
from .models import User, Book
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.user_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='reg')
        return redirect('/')
    
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email_address=request.POST['email'],
            password= pw_hash
            )
        request.session['user_id'] = new_user.id
    return redirect('/books')

def books(request):
    context = {
        "user" : User.objects.get(id=request.session['user_id']),
        "all_books" : Book.objects.all()
    }
    return render(request, 'books.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    else:
        logged_user = User.objects.get(email_address=request.POST['email'])
        request.session['user_id'] = logged_user.id
        return redirect('/books')

def add(request):
    errors = Book.objects.book_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books')
    
    else:
        logged_user = User.objects.get(id=request.session['user_id'])
        new_book = Book.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            uploaded_by=logged_user,
            )

        logged_user = User.objects.get(id=request.session['user_id'])
        logged_user.liked_books.add(new_book)

    return redirect('/books')

def book_info(request, book_id):
    logged_user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=book_id)
    context = {
        "user" : User.objects.get(id=request.session['user_id']),
        "book" : Book.objects.get(id=book_id),
        "all_users" : User.objects.all()
    }
    if logged_user == book.uploaded_by:
        return render(request, 'book_info_edit.html', context)
    if logged_user != book.uploaded_by:
        return render(request, 'book_info.html', context)

def favorite_book(request, book_id):
    book = Book.objects.get(id=book_id)
    logged_user = User.objects.get(id=request.session['user_id'])
    logged_user.liked_books.add(book)
    return redirect('/books/'+ str(book_id))

def unfavorite_book(request, book_id):
    book = Book.objects.get(id=book_id)
    logged_user = User.objects.get(id=request.session['user_id'])
    logged_user.liked_books.remove(book)
    return redirect('/books/'+ str(book_id))

def delete(request, book_id):
    delete_book = Book.objects.get(id=book_id)
    delete_book.delete()
    return redirect('/books')

def update(request, book_id):
    errors = Book.objects.book_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books/'+ str(book_id))
    
    else:

        book_update = Book.objects.get(id=book_id)

        book_update.title=request.POST['title']
        book_update.network=request.POST['description']

        book_update.save()

        return redirect('/books')

def favorite_book_main(request, book_id):
    book = Book.objects.get(id=book_id)
    logged_user = User.objects.get(id=request.session['user_id'])
    logged_user.liked_books.add(book)
    return redirect('/books')