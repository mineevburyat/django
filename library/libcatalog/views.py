from django.shortcuts import render

# Create your views here.
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RenewBookForm
from django.http import HttpResponseRedirect
import datetime
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required

def help(request):
    return render(
        request,
        'help.html',
        context={} )

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # Метод 'all()' применён по умолчанию.
     # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_books':num_books,
                 'num_instances':num_instances,
                 'num_instances_available':num_instances_available,
                 'num_authors':num_authors,
                 'num_visits': num_visits},
    )
    
class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    
class BookDetailView(generic.DetailView):
    model = Book
    
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='libcatalog/bookinstance_list_borrowed_user.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksLibrarerListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='libcatalog/bookinstance_list_loaned_librarer.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

# @login_required
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2
    
class AuthorDetailView(generic.DetailView):
    model = Author

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = RenewBookForm(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            #(здесь мы просто присваиваем их полю due_back)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # Переход по адресу 'all-borrowed':
            return HttpResponseRedirect(reverse('borrowed') )

    # Если это GET (или какой-либо ещё), создать форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'book_renew_librarian.html', {'form': form, 'bookinst':book_inst})