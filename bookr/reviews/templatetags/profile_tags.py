from django import template
from reviews.models import Review
register=template.Library()
@register.inclusion_tag('book_list.html')
def book_list(username):
    """
    Render the list books read by user
    :param: str username The username for whom the books should be fetched
    :return: dict of books read by user

    """
    reviews=Review.objects.filter(creator__username__contains=username)
    return {'books_read':[r.book.title for r in reviews]}

