from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre, Language
from django.views import generic 
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from catalog.forms import RenewBookForm
import datetime

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from catalog.models import Author

def index(request):
	""" View function for home page of site. """
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()
	# num_languages = Language.objects.all().count()
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()
	num_authors = Author.objects.count()

	num_visits = request.session.get('num_visits', 1)
	request.session['num_visits'] = num_visits + 1

	context = {
		'num_books': num_books,
		'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,
		'num_visits': num_visits,
	}

	return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
	model = Book
	paginate_by = 10
	def get_context_data(self, **kwargs):
		context = super(BookListView, self).get_context_data(**kwargs)
		context['some_data'] = 'This is just some data'
		return context 

class BookDetailView(generic.DetailView):
	model = Book
	
class AuthorListView(generic.ListView):
	model = Author
	paginate_by = 10

class AuthorDetailView(generic.DetailView):
	model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10 

	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class BorrowedBooksByUserListView(PermissionRequiredMixin, generic.ListView):
	model = BookInstance
	permission_required = 'catalog.can_mark_returned'
	template_name = 'catalog/bookinstance_list_all_borrowed.html'
	paginate_by = 10 

	def get_queryset(self):
		return BookInstance.objects.all().filter(status__exact='o').order_by('due_back')

def author_detail_view(request, primary_key):
	author = get_object_or_404(Author, pk=primary_key)
	return render(request, 'catalog/author_detail.html', context={'author': author})

def book_detail_view(request, primary_key):
	book = get_object_or_404(Book, pk=primary_key)
	return render(request, 'catalog/book_detail.html', context={'book': book})

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
	book_instance = get_object_or_404(BookInstance, pk=pk)
	if request.method == 'POST':
		form = RenewBookForm(request.POST)

		if form.is_valid():
			book_instance.due_back = form.cleaned_data['renewal_date']
			book_instance.save()

			return HttpResponseRedirect(reverse('all-borrowed'))
	else:
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
		form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

	context = {
		'form': form, 
		'book_instance': book_instance,
	}

	return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
	model = Author
	fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
	initial = {'date_of_death': '11/06/2020'}
	permission_required = 'catalog.can_mark_returned'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
	model = Author
	fields = '__all__'
	permission_required = 'catalog.can_mark_returned'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
	model = Author
	success_url = reverse_lazy('author')
	permission_required = 'catalog.can_mark_returned'


class BookCreate(PermissionRequiredMixin, CreateView):
	model = Book
	fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
	permission_required = 'catalog.can_mark_returned'

class BookUpdate(PermissionRequiredMixin, UpdateView):
	model = Book
	fields = '__all__'
	permission_required = 'catalog.can_mark_returned'

class BookDelete(PermissionRequiredMixin, DeleteView):
	model = Book
	success_url = reverse_lazy('books')
	permission_required = 'catalog.can_mark_returned'








