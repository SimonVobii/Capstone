from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .backtest import *
from .forms import *
from .demo import *
import matplotlib.pyplot as plt, mpld3
from django.contrib import messages
# Create your views here.

@login_required
def select(request):
    return render(request, 'select.html')
    #if request.method == ""

@login_required
def better(request):
    return render(request, 'recommend-better.html')

@login_required
def goal(request):
    return render(request, 'recommendforgoal.html')

def demo(request):
#    if request.method == 'POST':
#        form = choiceSelect(request.POST)
#
#    else:
#        form = choiceSelect()
#        #html_graph = emptyPlot()
    return render(request, 'demo.html', {'form': form})

@login_required
def backtest(request):
    if request.method == 'POST':
        form = backtestSelection(request.user, request.POST)   #just added the request.user
        if form.is_valid():

            #loading user inputs from form
            portfolioChoice = form.cleaned_data['dropDown']
            holding_period  = form.cleaned_data['holding_period']
            histChoice  = form.cleaned_data['histChoice']

            portfolioAssets = list(PortfolioWeights.objects.filter(portfolioID = portfolioChoice))
            
            port = {}
            for i in portfolioAssets:
                port[i.tickerID.tickerID] = i.volume

            html_graph = backtestScript(port, holding_period, histChoice)
            #print(type(html_graph))
            #print("we valid boys")
            #html_graph = mpld3.fig_to_html(fig)
    else:

        form = backtestSelection(request.user)
        html_graph = emptyPlot()
        #print(type(html_graph))
    return render(request, 'backtest_paul.html', {'graph':html_graph, 'form': form})

@login_required
def portfolio(request):
#loads the portfolio creation page

    if request.method == 'POST':
        form = portfolioForm(request.POST)
        if form.is_valid():
            #if valid, the form passed basic validation checks. We also want to check if the
            #input weights sum to 1, which we do below because it's hard to do with Django's
            #built-in form validation

            #pulling ticker selections from the form
            t1 = form.cleaned_data['ticker1']
            t2 = form.cleaned_data['ticker2']
            t3 = form.cleaned_data['ticker3']

            #pulling wieghts from the form
            w1 = form.cleaned_data['weight1']
            w2 = form.cleaned_data['weight2']
            w3 = form.cleaned_data['weight3']

            #checking that weights sum to 1
            weight_sum = w1
            weight_sum += 0 if(t2 is None) else 0 if(w2 is None) else w2
            weight_sum += 0 if(t3 is None) else 0 if(w3 is None) else w3

            if(weight_sum == 1):
                #pulling data for portfolio creation from form
                p = PortfolioID(portfolioName = form.cleaned_data['portfolioName'], userID = request.user)
                p.save()

                #saving asset weights
                asset1 = PortfolioWeights(portfolioID = p, tickerID = t1, volume = w1)
                asset1.save()

                if ((t2 is not None) and (w2 is not None)):
                    asset2 = PortfolioWeights(portfolioID = p, tickerID = t2, volume = w2)
                    asset2.save()

                if ((t3 is not None) and (w3 is not None)):
                    asset3 = PortfolioWeights(portfolioID = p, tickerID = t3, volume = w3)
                    asset3.save()

                messages.success(request, f'Portfolio Successfully Created')
                return redirect('select')
            else:
                messages.error(request, f'Weights must sum to 1')
    else:
        form = portfolioForm()
    return render(request, 'portfolio_paul.html', {'form': form})

