from django.shortcuts import render, get_object_or_404,redirect
from .models import Book, Contributor,Publisher,Review
from .utils import average_rating
from .forms import SearchForm,PublisherForm,ReviewForm,BookMediaForm
from django.contrib import messages
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.images import ImageFile
from django.contrib.auth import PermissionDenied
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test
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

    if request.user.is_authenticated:
        max_viewed_books_length=10
        viewed_books=request.session.get('viewed_books',[])
        viewed_book=[book.id,book.title]
        if viewed_book in viewed_books:
            viewed_books.pop(viewed_books.index(viewed_book))
        viewed_books.insert(0,viewed_book)
        viewed_books=viewed_books[:max_viewed_books_length]
        request.session['viewed_books']=viewed_books
    return render(request, 'reviews/book_detail.html', context)


def index(request):
    return render(request, 'base.html')

def book_search(request):
    search_text=request.GET.get("search","")
    form=SearchForm(request.GET)
    books=set()
    if form.is_valid() and form.cleaned_data["search"]:
        search=form.cleaned_data["search"]
        search_in=form.cleaned_data.get("search_in") or "title"
        if search_in=='title':
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

def is_staff_user(user):
    return user.is_staff
# @permission_required('edit_publisher')
@user_passes_test(is_staff_user)
def publisher_edit(request,pk=None):
    if pk is not None:
        publisher=get_object_or_404(Publisher,pk=pk)
    else:
        publisher=None
    if request.method=="POST":
        form=PublisherForm(request.POST,instance=publisher)
        if form.is_valid():
            updated_publisher=form.save()
            if publisher is None:
                messages.success(request,f"Publisher {updated_publisher} was created.")
            else:
                messages.success(request,f"Publisher {updated_publisher} was updated.")
            return redirect("publisher_edit",updated_publisher.pk)
        return render(request,'reviews/instance-form.html',{"method":request.method,"form":form})

    else:
        form = PublisherForm(instance=publisher)
        return render(request,'reviews/instance-form.html',{
            "form":form,
            "instance":publisher,
            "model_type":request.method
        })
@login_required
def review_edit(request,book_pk,review_pk=None):
    book = get_object_or_404(Book, pk=book_pk)
    if review_pk is None:
        instance=None
    else:
        instance=get_object_or_404(Review,pk=review_pk)
        user=request.user
        if not user.is_staff and review.creator.id!=user.id:
            raise PermissionDenied
    if request.method=="POST":
        form=ReviewForm(request.POST,instance=instance)
        if form.is_valid():
            review_=form.save(commit=False)
            review_.book=book
            if instance is not None:
                review_.date_edited=timezone.now()
            review_.save()
            if instance is not None:
                messages.success(request,f'Review for "{book.title}" was updated.')
            else:
                messages.success(request,f'Review for "{book.title}" was created.')
            redirect("review_edit",book.pk,review_.pk)
    form = ReviewForm(instance=instance)
    context={

        "form":form,
        "instance":instance,
        "model_type(Review)":Review,
        "related_model_type":'Book',
        'related_instance':book
    }
    return render(request,'reviews/instance-form.html',context)

@login_required
def book_media(request,pk):
    book=get_object_or_404(Book,pk=pk)
    if request.method=="POST":
        form=BookMediaForm(request.POST,request.FILES,instance=book)

        if form.is_valid():
            book=form.save(commit=False)
            cover=form.cleaned_data.get('cover')
            if cover:
                image=Image.open(cover)
                image.thumbnail((300,300))
                image_data=BytesIO()
                image.save(fp=image_data,format=cover.image.format)
                image_file=ImageFile(image_data)
                book.cover.save(cover.name,image_file)
            book.save()
            messages.success(request,f'Book {book} was successfully updated.')
            return redirect('book_detail',book.pk)
    else:
        form=BookMediaForm(instance=book)
    return render(request,'reviews/instance-form.html',{
        "form": form,
        "instance": book,
        "model_type": "Book",
        'is_file_upload':True
    })

