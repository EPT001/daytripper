from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Bookmark, Review
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class TextSearchForm(forms.Form):
    query = forms.CharField(label='Current location', max_length=100)
    radius = forms.IntegerField(label='Radius')
    place_type = forms.ChoiceField(choices=[
        ('restaurant', 'Restaurant'),
        ('cafe', 'Cafe'),
        ('bar', 'Bar'),
        ('museum', 'Museum'),
        ('art_gallery', 'Art gallery')

    ])


# jessie code about bookmark & Review
class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ['place_id']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['place_id', 'text']
