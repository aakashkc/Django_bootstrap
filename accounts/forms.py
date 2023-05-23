from dataclasses import fields
from django import forms
from .models import Account
# missing-module-docstring


class RegistrationForm ( forms.ModelForm) :
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class' : 'form-control'

    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm_Password',
        'class' : 'form-control'
    }))


    class Meta:
        """ dummy docstring"""
        model= Account
        fields= ['first_name', 'last_name',  'phone_number',  'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__( *args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Confirm Password'


        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


#__init__ method
#It is called as a constructor in object oriented terminology.
# This method is called when an object is created from a class and it allows the class to initialize the attributes of the class

    def clean(self):
        cleaned_data=super(RegistrationForm, self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password didn't match")