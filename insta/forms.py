from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Image, Comment

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

class commentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['related_post', 'name' , 'created_on']
