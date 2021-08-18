from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('books', views.books),
    path('logout', views.logout),
    path('login', views.login),
    path('add', views.add),
    path('books/<int:book_id>', views.book_info),
    path('books/<int:book_id>/favorite_book', views.favorite_book),
    path('books/<int:book_id>/unfavorite_book', views.unfavorite_book),
    path('books/<int:book_id>/favorite_book_main', views.favorite_book_main),
    path('books/<int:book_id>/delete', views.delete),
    path('books/<int:book_id>/update', views.update),
]
