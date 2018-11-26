from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .backtest import *
from .forms import *
from .demo import *
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
    if request.method == 'POST':
        form = DropDownForm(request.POST)
        if form.is_valid():
            demoPlot()
    else:
        form = DropDownForm()
    return render(request, 'demo.html', {'form': form})

