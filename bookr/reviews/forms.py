from django import forms
from .models import Publisher,Review,Book
CHOICES=(('title','title'),('contributor','contributor'))
class SearchForm(forms.Form):
    search=forms.CharField(min_length=3)
    search_in=forms.ChoiceField(choices=CHOICES,
                                required=False)
class NewsletterSignupForm(forms.Form):
    signup=forms.BooleanField(label='sign up to newsletter?',required=False)
    email=forms.EmailField(help_text="Enter your email address to subscribe",required=False)
    def clean(self):
        cleaned_data=super().clean()
        if cleaned_data["signup"] and not cleaned_data.get("email"):
            self.add_error("email","email address is required if signing up for newsletters")
class OrderForm(forms.Form):
    item_a = forms.IntegerField(min_value=0, max_value=100)
    item_b=forms.IntegerField(min_value=0,max_value=100)
    def clean(self):
        cleaned_data=super().clean()
        if cleaned_data.get("item_a",0)+cleaned_data.get("item_b",0)>100:
            self.add_error(None,"The total must not exceed 100")

class PublisherForm(forms.ModelForm):
    email_on_save = forms.BooleanField(required=False, help_text="send notification on save to email")

    class Meta:
        model=Publisher
        fields="__all__"
        widgets={
            "name":forms.TextInput(attrs={
                "placeholder":'the publicher name'
            })
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        exclude=('date_edited',)
        rating=forms.IntegerField(min_value=0,max_value=5)


class BookMediaForm(forms.ModelForm):
    class Meta:
        model=Book
        fields=('cover','sample',)