from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Photo

class UserRegisterForm(UserCreationForm):
  username = forms.CharField(min_length=6, max_length=50)
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')



class PhotoUploadForm(forms.ModelForm):
  class Meta:
    model = Photo
    fields = ['title', 'image']
