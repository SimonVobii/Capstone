from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .backtest import *
from .forms import *
from .demo import *
import matplotlib.pyplot as plt, mpld3
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
            html_graph = demoPlot()
            print("we valid boys")
            #html_graph = mpld3.fig_to_html(fig)
    else:
        form = DropDownForm()
        html_graph = emptyPlot()
    return render(request, 'demo.html', {'graph': html_graph, 'form': form})

