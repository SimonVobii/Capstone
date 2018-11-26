from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from .models import *

class DropDownForm(forms.Form):
	ticker1 = forms.ModelChoiceField(queryset=stockID.objects.all())
	weight1 = forms.FloatField(max_value=1, min_value=0)
	ticker2 = forms.ModelChoiceField(queryset=stockID.objects.all(), required=False)
	weight2 = forms.FloatField(max_value=1, min_value=0, required=False)
	
	#ticker3 = forms.ModelChoiceField(queryset=stockID.objects.all(), required=False)
	#weight3 = forms.FloatField(max_value=1, min_value=0, required=False)
	#ticker4 = forms.ModelChoiceField(queryset=stockID.objects.all(), required=False)
	#weight4 = forms.FloatField(max_value=1, min_value=0, required=False)
	#ticker5 = forms.ModelChoiceField(queryset=stockID.objects.all(), required=False)
	#weight5 = forms.FloatField(max_value=1, min_value=0, required=False)