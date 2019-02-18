from django import forms
from .models import Classroom, Students
from django.contrib.auth.models import User

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        #fields = '__all__'
        exclude = ['teacher']

class UserRegister(forms.ModelForm):
        class Meta:
            model = User
            fields = ['username', 'first_name', 'last_name', 'email' ,'password']

            widgets={
            'password': forms.PasswordInput(),
            }

class UserLogin(forms.Form):
        username = forms.CharField(required=True)
        password = forms.CharField(required=True, widget=forms.PasswordInput())


class AddStudent(forms.ModelForm):
        class Meta:
            model = Students
            exclude = ['classroom']
            
            
            widgets={
                    'date_of_birth': forms.DateInput(attrs={'type':'date'})
                    }