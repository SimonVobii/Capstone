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

class portfolioSelection(forms.Form):
	def __init__(self, user, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(portfolioSelection, self).__init__(*args, **kwargs)
		self.fields['dropDown'].queryset = PortfolioID.objects.filter(userID = user.id)
	dropDown = forms.ModelChoiceField(queryset=PortfolioID.objects) #queryset=PortfolioID.objects.filter(userID=user)

class backtestSelection(forms.Form):
	def __init__(self, user, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(backtestSelection, self).__init__(*args, **kwargs)
		self.fields['dropDown'].queryset = PortfolioID.objects.filter(userID = user.id)
	dropDown = forms.ModelChoiceField(queryset=PortfolioID.objects, label = 'Portfolio to Test') #queryset=PortfolioID.objects.filter(userID=user)
	holding_period = forms.IntegerField(min_value=22, max_value=1300, label = 'Holding Period')
	histChoice = forms.ChoiceField(choices = [("Historical","Historical"),("Forecast","Forecast")], label = 'Historical or Forecast')

class portfolioForm(forms.Form):
	portfolioName = forms.CharField(max_length = 15)
	#totalValue = forms.FloatField(min_value=0, max_value=10000000)

	ticker1 = forms.ModelChoiceField(queryset=stockID.objects.all())
	weight1 = forms.FloatField(max_value=1, min_value=0)

	ticker2 = forms.ModelChoiceField(queryset=stockID.objects.all(), required=False)
	weight2 = forms.FloatField(max_value=1, min_value=0, required=False)
	
	ticker3 = forms.ModelChoiceField(queryset=stockID.objects.all(), required=False)
	weight3 = forms.FloatField(max_value=1, min_value=0, required=False)
	#ticker4 = forms.ModelChoiceField(queryset=stockID.objects.all(), required=False)
	#weight4 = forms.FloatField(max_value=1, min_value=0, required=False)
	#ticker5 = forms.ModelChoiceField(queryset=stockID.objects.all(), required=False)
	#weight5 = forms.FloatField(max_value=1, min_value=0, required=False)