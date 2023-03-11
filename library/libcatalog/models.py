from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date



# Create your models here.
class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        
    name = models.CharField(
        max_length=200, 
        help_text="жанр книги")

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ["title"]
        
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=30,
                            default = str(title),
                            verbose_name='отображение в пути url',
                            help_text='желательно латинские символы и цифры без пробелов, а так же смысловая нагрузка')
    author = models.ForeignKey(
        'Author', 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name='Автор',
        help_text='выберите автора книги')
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file.
    summary = models.TextField(
        max_length=1000, 
        help_text="описание содержания книги")
    isbn = models.CharField(
        'ISBN',
        max_length=13, 
        help_text='ISBN 13-ти значный индентификатор <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name='Жанр', 
        help_text="укажите жанр этой книги")
    lang = models.CharField('Язык',max_length=25,default='Русский')
    
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.slug)])
    
    def display_genre(self):
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    class Meta:
        verbose_name = 'Экземпляр книги'
        verbose_name_plural = 'Экземпляры книг'
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Отметить как возвращенный"),)
        
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        help_text="Уникальный ID физического экземляра книги")
    book = models.ForeignKey(
        'Book', 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name='книга в каталоге',
        help_text='книга описанная в каталоге')
    imprint = models.CharField(max_length=200,
                               verbose_name="издательство")
    due_back = models.DateField(null=True, 
                                blank=True,
                                verbose_name='дата возврата')

    LOAN_STATUS = (
        ('m', 'На обслуживании'),
        ('o', 'На руках'),
        ('a', 'Доступен'),
        ('r', 'Зарезервирован'),
    )

    status = models.CharField(
        'Статус',
        max_length=1, 
        choices=LOAN_STATUS, 
        blank=True, 
        default='m', 
        help_text='статус книги, доступность')
    
    borrower = models.ForeignKey(User, 
                                 on_delete=models.SET_NULL, 
                                 null=True, blank=True)

    def __str__(self):
        return '%s (%s)' % (self.id,self.book.title)
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

class Author(models.Model):
    """
    Model representing an author.
    """
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        
    first_name = models.CharField(
        'Первое имя',
        max_length=100)
    last_name = models.CharField(
        'Второе имя',
        max_length=100)
    slug = models.CharField(
        'url представление имени ',
        default = str(first_name),
        help_text='латинские символы и цифры одной строкой без пробелов',
        max_length=100)
    date_of_birth = models.DateField(
        'дата рождения',
        null=True, blank=True)
    date_of_death = models.DateField(
        'дата смерти', 
        null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.slug)])

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)

