from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import random


from .models import Order

# class OrderForm(ModelForm):
#     class Meta:
#         model = Order
#         fields = '__all__'
        
        
        
class CreateUserForm(UserCreationForm):
    class Meta:
        model =  User
        fields =['username','email','password1','password2']
        
    # def save(self, commit=True):
    #     user.email = self.cleaned_data['email']
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #         return user
            