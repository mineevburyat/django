from django.shortcuts import render

# Create your views here.
from .models import Author

def index(request):
    ...

    num_authors=Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={
            'num_books':333,
            'num_instances':3333,
            'num_instances_available':3333,
            'num_authors':num_authors,
            'num_visits':num_visits}, # num_visits appended
    )