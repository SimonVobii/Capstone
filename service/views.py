from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from .backtest import *
# Create your views here.

@login_required
def select(request):
    return render(request, 'select.html')
    #if request.method == ""

@login_required
def backtest(request):
    return render(request, 'backtest.html')
    #if request.method == ""

@login_required
def better(request):
    return render(request, 'recommend-better.html')
    #if request.method == ""

@login_required
def goal(request):
    return render(request, 'recommendforgoal.html')
    #if request.method == ""


def demo(request):
	for i in range(1,5):
		print(i)
	return render(request, 'select.html')

