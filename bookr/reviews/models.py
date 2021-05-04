from django.db import models
from django.contrib import auth
from django import forms
class Publisher(models.Model):
    """A company that publishes books."""
    name=models.CharField(max_length=50,
                          help_text='The name of the Publisher.')
    website=models.URLField(help_text="The Publisher's website.")
    email=models.EmailField(help_text="The Publisher's email address.")
    def __str__(self):
        return self.name

class Book(models.Model):
    """A published book."""
    title=models.CharField(max_length=70,
                           help_text="The title of the book.")
    publication_date=models.DateField(verbose_name="Date the book was published.")
    isbn=models.CharField(max_length=20,
                          verbose_name="ISBN number of the book.")
    publisher=models.ForeignKey(Publisher,on_delete=models.CASCADE)
    contributors=models.ManyToManyField('Contributor',through="BookContributor")

    cover=models.ImageField(upload_to='book_covers/',null=True,blank=True)
    sample=models.FileField(upload_to='book_samples/',null=True,blank=True)


    def __str__(self):
        return f"{self.title} ({self.isbn})"
    def isbn13(self):
        """
        '123333...' => '123-3-33-333333-3'
        """
        return f"{self.isbn[0:3]}-{self.isbn[3:4]}-{self.isbn[4:6]}-{self.isbn[6:12]}-{self.isbn[12:13]}"


class Contributor(models.Model):
    """
    A contributor to a Book, e.g. author, editor, co-author.
    """
    first_names=models.CharField(
        max_length=50,
        help_text="The contributor's first name or names."
    )
    last_names=models.CharField(
        max_length=50,
        help_text="The contributor's last name or names."
    )
    email=models.EmailField(help_text="The contact email for the contributor.")

    def initialled_name(self):
        initials = ''.join(name[0] for name in self.first_names.split(" "))
        return f"{self.last_names}, {initials}"

    def __str__(self):
        return self.initialled_name()

    def number_contributions(self):
        return self.bookcontributor_set.count()

class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR="AUTHOR","Author"
        CO_AUTHOR="CO_AUTHOR","Co-Author"
        EDITOR="EDITOR","Editor"
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    contributor=models.ForeignKey(Contributor,on_delete=models.CASCADE)
    role=models.CharField(verbose_name="The role this contributor had in the book.",
                          choices=ContributionRole.choices,
                          max_length=20)

class Review(models.Model):
    content=models.TextField(help_text="The Review text.")
    rating=models.IntegerField(help_text="The rating the reviewer has given.")
    date_created=models.DateTimeField(auto_now_add=True,
                                      help_text="The date and time the review was created.")
    date_edited=models.DateTimeField(null=True,
                                     help_text="The date and time the review was last edited.")
    creator=models.ForeignKey(auth.get_user_model(),
                              on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,
                           help_text="The Book that this review is for.")