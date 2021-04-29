from django import forms
CHOICES=(('title','title1'),('contributor','contributor1'))
class SearchForm(forms.Form):
    search=forms.CharField(min_length=3)
    search_in=forms.ChoiceField(choices=CHOICES,
                                required=False)

