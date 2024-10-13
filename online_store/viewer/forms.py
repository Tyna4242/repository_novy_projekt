from django.forms import ModelForm
from viewer.models import Category, Product, Comment, CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'city', 'address', 'avatar', 'role', 'preferred_communication']



class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise forms.ValidationError('Název produktu musí mít alespoň 3 znaky.')
        return title
    


class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = ['text']







