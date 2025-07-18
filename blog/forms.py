from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image', 'my_choice_rating', 'category']

class DateInput(forms.DateInput):
    input_type = 'date'


class BlogDateFilterForm(forms.Form):
    date = forms.DateField(
        required=False,
        widget=DateInput(attrs={'placeholder' : 'Válassz dátumot!'})
    )
