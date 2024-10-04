from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
# Create your views here.
@login_required
def index(request):
    """ View funtion for home page of the site."""

    num_books=Book.objects.all().count()
    num_instance=Book.objects.all().count()
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()
    num_genre=Genre.objects.all().count()
    num_atom_books=Book.objects.filter(title__contains="Atom").count()

    '''visit counter using session'''
    num_visit=request.session.get("num_visitor",0)
    num_visit+=1
    request.session['num_visitor']=num_visit

    context={
        'num_books':num_books,
        'num_instance':num_instance,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_genre':num_genre,
        "num_atom_books":num_atom_books,
        "num_visit":num_visit
    }

    return render(request,'index.html',context=context)

class BookListView(LoginRequiredMixin,generic.ListView):
    model=Book
    paginate_by=2
    context_object_name='book_list'
    template_name='catalog/book_list.html'

    def get_queryset(self):
        return Book.objects.all()
    
    def get_context_data(self, **kwargs):
        context=super(BookListView,self).get_context_data(**kwargs)
        context['some_additonal_data']='this is just some data'
        return context

class BookDetailView(LoginRequiredMixin,generic.DetailView):
    model=Book

class AuthorListView(LoginRequiredMixin,generic.ListView):
    model=Author
    context_object_name='author_list'
    template_name='catalog/author_list.html'

    def get_queryset(self):
        return Author.objects.all()
    
class AuthorDetailView(LoginRequiredMixin,generic.DetailView):
    model=Author


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model=BookInstance
    template_name='catalog/bookinstance_list_borrowed_user.html'

    def get_queryset(self):
        return(
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )


class BorrowedListView(LoginRequiredMixin,generic.ListView): 
    # permission_required=('catalog.can_view_borrowed','catalog.staff_level') permissionrequiredmixin
    model=BookInstance
    context_object_name="borrowed_list"
    template_name='catalog/borrowed_list.html'

    def get_queryset(self):
        return(
            BookInstance.objects.filter(status__exact='o').order_by('due_back')
        )