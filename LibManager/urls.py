from django.urls import path
from . import views

urlpatterns = [
    path('addBook/', views.addBook, name='addBook'),
    path('update/<int:book_id>/', views.updateBook, name='updateBook'),
    path('update/', views.searchUpdateBook, name='searchUpdateBook'),
    path('view/', views.viewBookList, name='viewBookList'),
    path('view/<int:book_id>/', views.bookView, name='bookView'),
    path('search/', views.searchBook, name='searchBook'),
    path('delete/', views.deleteBook, name='deleteBook'),
    path('addMember/', views.addMember, name='addMember'),
    path('borrow/<int:book_id>/', views.borrowBook, name='borrow'),
    path('viewMember/<int:member_id>/', views.memberView, name='viewMember'),
    path('viewMember/', views.memberList, name='viewMemberList'),
]
