from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from .models import *

class PortfolioModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return("{}".format(obj.portfolioName))

class AssetModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return("{}".format(obj.tickerID))

class backtestSelection(forms.Form):
	def __init__(self, user, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(backtestSelection, self).__init__(*args, **kwargs)
		self.fields['dropDown'].queryset = PortfolioID.objects.filter(userID = user.id)
	dropDown = PortfolioModelChoiceField(queryset=PortfolioID.objects.order_by('portfolioName'), label = 'Portfolio to Test') #queryset=PortfolioID.objects.filter(userID=user)
	holding_period = forms.IntegerField(min_value=22, max_value=1300, label = 'Holding Period', initial=22)
	histChoice = forms.ChoiceField(choices = [("Historical","Historical"),("Forecast","Forecast")], label = 'Historical or Forecast')

class optimizeGoalForm(forms.Form):
	returnGoal = forms.FloatField(min_value=0, max_value=100, label='Return Objective (Percent)')
	holdingPeriod = forms.IntegerField(min_value=22, max_value=1300, label = 'Investment Horizon (Days)', initial=252)

class portfolioSaveForm(forms.Form):
	portfolioName = forms.CharField(max_length = 35, label='Portfolio Name')

class betterPortForm(forms.Form):
	def __init__(self, user, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(betterPortForm, self).__init__(*args, **kwargs)
		self.fields['dropDown'].queryset = PortfolioID.objects.filter(userID = user.id)
	dropDown = PortfolioModelChoiceField(queryset=PortfolioID.objects.order_by('portfolioName'), label = 'Portfolio to Beat')
	#returnGoal = forms.FloatField(min_value=0, max_value=1.0, label='Return Objective')
	#holding_period = forms.IntegerField(min_value=22, max_value=1300, label = 'Time Horizon')

class portfolioForm(forms.Form):
	portfolioName = forms.CharField(max_length = 35, label='Portfolio Name')

	ticker1 = AssetModelChoiceField(queryset=stockID.objects.order_by('tickerID').all(), label='Asset 1')
	weight1 = forms.FloatField(max_value=1000, min_value=0, label='Volume of Asset 1')

	ticker2 = AssetModelChoiceField(queryset=stockID.objects.order_by('tickerID').all(), required=False, label='Asset 2')
	weight2 = forms.FloatField(max_value=1000, min_value=0, required=False, label='Volume of Asset 2')
	
	ticker3 = AssetModelChoiceField(queryset=stockID.objects.order_by('tickerID').all(), required=False, label='Asset 3')
	weight3 = forms.FloatField(max_value=1000, min_value=0, required=False, label='Volume of Asset 3')
