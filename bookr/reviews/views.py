from django.shortcuts import render, get_object_or_404
from .models import Book, Contributor #,Review
from .utils import average_rating
from .forms import SearchForm

def book_list(request):
    books = Book.objects.all()
    book_list = []
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating(
                [review.rating for review in reviews]
            )
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        book_list.append({
            'book': book,
            'book_rating': book_rating,
            'number_of_reviews': number_of_reviews
        })
    context = {
        'book_list': book_list,
    }
    return render(request, 'reviews/books_list.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)

    reviews = book.review_set.all()
    if reviews:
        book_rating = average_rating(
            [review.rating for review in reviews]
        )
        number_of_reviews = len(reviews)
    else:
        book_rating = None
        number_of_reviews = 0

    context = {'book': book, 'book_rating': book_rating, 'number_of_reviews': number_of_reviews, 'reviews': reviews}
    return render(request, 'reviews/book_detail.html', context)


def index(request):
    return render(request, 'base.html')

def book_search(request):
    search_text=request.GET.get("search","")
    form=SearchForm(request.GET)
    books=set()
    if form.is_valid() and form.cleaned_data["search"]:
        search=form.cleaned_data["search"]
        if form.cleaned_data.get('search_in')=='title':
            bookobjs=Book.objects.filter(title__icontains=search)
            for b in bookobjs:
                books.add(b)
        if form.cleaned_data.get('search_in')=='contributor':
            contributors1 = Contributor.objects.filter(first_names__icontains = search)
            contributors2 = Contributor.objects.filter(last_names__icontains = search)
            for contributors in [contributors1,contributors2]:
                for contributor in contributors:
                    bookobjs=Book.objects.filter(contributors=contributor)
                    for b in bookobjs:
                        books.add(b)


    return render(request,'reviews/search-results.html',{'search_text':search_text,'books':books,'form':form})
