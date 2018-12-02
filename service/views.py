from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .backtest import *
from .optimization import *
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
    if request.method == 'POST':
        form = betterPortForm(request.user, request.POST)   #just added the request.user
        if form.is_valid():
            optimizeScript()

            html_graph = optimizeGoalForm()
    else:

        form = betterPortForm(request.user)
        html_graph = emptyPlot()
    return render(request, 'recommend_better_paul.html', {'graph':html_graph, 'form': form})

@login_required
def goal(request):
    if request.method == 'POST':
        form = optimizeGoalForm(request.POST)   #just added the request.user
        if form.is_valid():
            inputGoal = form.cleaned_data['returnGoal']/100
            inputHorizon = form.cleaned_data['holdingPeriod']

            #converting input goal to monthly goal (for rebalancing)
            monthlyGoal = (1+inputGoal)**(22/inputHorizon) - 1
            
            #optimize portfolio based on input parameters
            goalReturn, goalCvar, goalSharpe, goal_sizes, goal_labels = optimizeScript(monthlyGoal)

            #saving metrics for passing to the saving screen
            request.session['sizes'] = goal_sizes
            request.session['labels'] = goal_labels
            request.session['portfolioReturn'] = str(round(goalReturn*100, 2))+"%"
            request.session['cvar'] = str(round(goalCvar*100, 2))+"%"
            request.session['sharpe'] = str(round(goalSharpe, 2))

            messages.success(request, f'Optimization Completed Successfully')

            return redirect('goalRender')
        
    else:
        form = optimizeGoalForm()
        html_graph = emptyPlot()
        goalReturn, goalCvar, goalSharpe = '','',''
        #print(type(html_graph))
    return render(request, 'goal_paul.html', {'graph':html_graph, 'form': form, 'return':goalReturn, 'cvar':goalCvar, 'sharpe':goalSharpe})

@login_required
def goalRender(request):
    #this seperate function handles the plotting and saving of portfolios after the optimization algorithms are complete
    sizes = request.session.get('sizes')
    labels = request.session.get('labels')
    portReturn = request.session.get('portfolioReturn')
    portCvar = request.session.get('cvar')
    portSharpe = request.session.get('sharpe')
    html_graph = plotPie(sizes, labels)

    if request.method == 'POST':
        form = portfolioSaveForm(request.POST)
        if form.is_valid():

            #portfolio creation code
            portName = form.cleaned_data['portfolioName']
            p = PortfolioID(portfolioName = portName, userID = request.user)
            p.save()

            for i in range(0,len(labels)):
                saveTicker = stockID.objects.get(pk=labels[i])
                asset = PortfolioWeights(portfolioID = p, tickerID = saveTicker, volume = sizes[i]/100)
                asset.save()

            messages.success(request, f'Portfolio {portName} Saved Successfully')
            return redirect('select')
        
    else:
        
        form = portfolioSaveForm()
        #html_graph = emptyPlot()
        #goalReturn, goalCvar, goalSharpe = '','',''
        #print(type(html_graph))
    return render(request, 'goalRender_paul.html', {'form':form, 'graph':html_graph, 'return':portReturn, 'cvar':portCvar, 'sharpe':portSharpe})

def demo(request):
    global_label.append("happy")
    return redirect('goalRender')
    #html_graph = demoPie()
    #form = optimizeGoalForm()
    #return render(request, 'demo.html', {'form': form, 'demoVar':6, 'graph':html_graph})

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

            #return Key Performance Indicators for the Portfolio
            mean_backtest, cvar_backtest, sharpe_backtest = currentCVAR(port)

            #format KPIs to prepare for printing
            mean_backtest = str(round(mean_backtest*100, 2))+"%"
            cvar_backtest = str(round(cvar_backtest*100, 2))+"%"
            sharpe_backtest = str(round(sharpe_backtest, 2))

            html_graph = backtestScript(port, holding_period, histChoice)

    else:

        form = backtestSelection(request.user)
        html_graph = emptyPlot()
        mean_backtest, cvar_backtest, sharpe_backtest = '','',''

    return render(request, 'backtest_paul.html', {'graph':html_graph, 'form': form, 'return': mean_backtest, 'cvar':cvar_backtest, 'sharpe':sharpe_backtest})

"""
@login_required
def optimizeGoal(request):
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

    else:

        form = backtestSelection(request.user)
        html_graph = emptyPlot()
        #print(type(html_graph))
    return render(request, 'goal_paul.html', {'graph':html_graph, 'form': form})

"""

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

