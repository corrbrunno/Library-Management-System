from datetime import datetime
from django.shortcuts import render,redirect
from .models import Book, Member, BookLoan
from django.db.models import Q


def viewBookList(request):
    book_list = Book.objects.all()
    context = {'book_list': book_list}
    return render(request, 'bookList.html', context)

def addBook(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        genre = request.POST.get('genre')
        copies = request.POST.get('copies')
        book = Book(title=title, author=author, genre=genre, copies=copies)
        book.save()
        return redirect('bookView', book_id=book.id)
    
    return render(request, 'addBook.html')

def bookView(request, book_id):
    book = Book.objects.get(pk=book_id)
    context = {'book': book}
    return render(request, 'viewBook.html', context)

def deleteBook(request):
    if request.method == 'POST':
        query = request.POST['query']
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
        if len(books) == 1:
                books.delete()
                return redirect('viewBookList')
        elif len(books) > 1:
            for book in books:
                book.delete()
            return redirect('viewBookList')
        else:
            context = {
            'title': 'Book not found',
            'message': 'Please enter a valid book title or author name.'
            }
            return render(request, 'ErrorHandler.html', context)
    else:
        return render(request, 'deleteBook.html')

def searchUpdateBook(request):
    if request.method != 'POST':
        return render(request, 'searchUpdateBook.html')
    
    query = request.POST['query']
    books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query) | Q(id=query))

    if len(books) == 1:
        return redirect('updateBook', book_id=books[0].id)
    
    if len(books) > 1:
        context = {
        'title': 'Multiple Books found',
        'message': 'Please be more specific in your search.'
        }
        return render(request, 'ErrorHandler.html', context)

    context = {
    'title': 'Book not found',
    'message': 'Please enter a valid book title or author name.'
    }
    return render(request, 'ErrorHandler.html', context)
        
    

def updateBook(request, book_id):
    book = Book.objects.get(pk=book_id)
    if request.method != 'POST':
        context = {'book': book}
    
        return render(request, 'updateBook.html', context)
    
    book.title = request.POST.get('title')
    book.author = request.POST.get('author')
    book.genre = request.POST.get('genre')
    book.copies = request.POST.get('copies')
    
    book.save(force_update=True)
    
    return redirect('bookView', book_id=book_id)

def searchBook(request):
    if request.method == 'POST':
        query = request.POST['query']
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))

        if len(books) == 1:
            # Redirect to the first book found (assuming you want to display the first result)
            return redirect('bookView', book_id=books[0].id)
        elif len(books) > 1:
            # Display a list of books
            context = {'book_list': books}
            return render(request, 'bookList.html', context)
        else:
            context = {
                'title': 'Book not found',
                'message': 'Please enter a valid book title or author name.'
            }
            return render(request, 'ErrorHandler.html', context)
    else:
        return render(request, 'search.html')

def addMember(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        identifier = request.POST.get('identifier')
        member = Member(name=name, identifier=identifier)
        member.save()

        return render(request, "viewMember.html", member_id=member.id)
    return render(request, "addMember.html")


def borrowBook(request, book_id):
    book = Book.objects.get(pk=book_id)

    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        borrowed = request.POST.get('borrowed')
        member = Member.objects.filter(Q(identifier__icontains=identifier)).first()

        if member == None:
            context = {
            'title': 'Member not found',
            'message': 'Please enter a valid member identifier.'
            }
            return render(request, 'ErrorHandler.html', context)

        book.copies = book.copies - int(borrowed)
        book.save()
        bookLoan = BookLoan(member=member, book=book, books_borrowed=borrowed)
        bookLoan.save()
        return render(request, "home.html")
    
    context = {'book_list': [book]}
    return render(request, "borrowBook.html", context=context)

def memberView(request, member_id):
    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')
        book_loan = BookLoan.objects.get(pk=loan_id)
        
        if book_loan.is_active:
            book_loan.book.copies = book_loan.book.copies + book_loan.books_borrowed
            book_loan.returned_date = datetime.now()
            book_loan.save()
            book_loan.book.save()

    member = Member.objects.get(pk=member_id)
    borrowed_books = BookLoan.objects.filter(Q(member=member))
    context = context = {
        'member': member, 
        'member_loans': borrowed_books
    }
    return render(request, "viewMember.html", context)
    
def memberList(request):
    context = {'member_list': Member.objects.all()}
    return render(request, "memberList.html", context)