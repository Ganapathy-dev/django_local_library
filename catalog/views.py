from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre

# Create your views here.

def index(request):
    """ View funtion for home page of the site."""

    num_books=Book.objects.all().count()
    num_instance=Book.objects.all().count()
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()
    num_genre=Genre.objects.all().count()
    num_atom_books=Book.objects.filter(title__contains="Atom").count()
    context={
        'num_books':num_books,
        'num_instance':num_instance,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_genre':num_genre,
        "num_atom_books":num_atom_books
    }

    return render(request,'index.html',context=context)

class BookListView(generic.ListView):
    model=Book
    context_object_name='book_list'
    template_name='catalog/book_list.html'

    def get_queryset(self):
        return Book.objects.all()
    
    def get_context_data(self, **kwargs):
        context=super(BookListView,self).get_context_data(**kwargs)
        context['some_additonal_data']='this is just some data'
        return context

class BookDetailView(generic.DetailView):
    model=Book

class AuthorListView(generic.ListView):
    model=Author
    context_object_name='author_list'
    template_name='catalog/author_list.html'

    def get_queryset(self):
        return Author.objects.all()
    
class AuthorDetailView(generic.DetailView):
    model=Author
