from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from .models import *

"""
class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()

    error_messages = {
        'invalid_login': "Please Insert correct username and password",
    }

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("Please activate your account in your email")
"""

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()	#left default required = True

	class Meta:		#gives us a nested namespace for configurations
		model = User 	#this is the model that will be saved to
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class SurveySubmissionForm(ModelForm):
    class Meta:
        model = SurveyID
        fields = ['age','gender','status','investment','combination']