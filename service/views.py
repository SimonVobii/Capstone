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

def volumeToValue(ticker, volume):
   return(priceLoader(ticker.tickerID)[ticker.tickerID][-1]*volume)

def pieCompressor(sizes, labels, threshold):
#used to make the pie chart display with reasonable # of buckets
    return_sizes = []
    return_labels = []
    othersize = 0.0

    for i in range(0,len(sizes)):
        if sizes[i]<threshold:
            othersize += sizes[i]
        else:
            return_sizes.append(sizes[i])
            return_labels.append(labels[i])

    return_sizes.append(othersize)
    return_labels.append('other')
    return(return_sizes, return_labels)

def portfolioCompressor(sizes, labels, threshold):
#removes assets that are less than threshold percent of the total portfolio value
    return_sizes = []
    return_labels = []
    removedSize = 0.0

    for i in range(0,len(sizes)):
        if sizes[i]<threshold:
            removedSize += sizes[i]
        else:
            return_sizes.append(sizes[i])
            return_labels.append(labels[i])

    for i in range(0, len(return_labels)):
        return_sizes[i] = return_sizes[i] * (1/(1-removedSize))

    #print(sum(return_sizes))
    return(return_sizes, return_labels)



@login_required
def better(request):
    if request.method == 'POST':
        form = betterPortForm(request.user, request.POST)   #just added the request.user
        if form.is_valid():
            inputPortfolio = form.cleaned_data['dropDown']

            portfolioAssets = list(PortfolioWeights.objects.filter(portfolioID = inputPortfolio))
            
            #storing input portfolio for comparison later
            port = {}
            for i in portfolioAssets:
                port[i.tickerID.tickerID] = i.volume

            inputSizes = []
            inputLabels = []
            for i in port:
                inputLabels.append(i)
                inputSizes.append(port[i] * 100)

            inputReturn, inputCvar, inputSharpe = currentCVAR(port)

            goalReturn, goalCvar, goalSharpe, goal_sizes, goal_labels = optimizeScript2(inputReturn)

            #saving metrics to session for passing
            request.session['inputSizes'] = inputSizes
            request.session['inputLabels'] = inputLabels
            request.session['inputReturn'] = str(round(inputReturn*100,2))+"%"
            request.session['inputCvar'] = str(round(inputCvar*100, 2))+"%"
            request.session['inputSharpe'] = str(round(inputSharpe, 2))

            request.session['outputSizes'] = goal_sizes
            request.session['outputLabels'] = goal_labels
            request.session['outputReturn'] = str(round(goalReturn*100, 2))+"%"
            request.session['outputCvar'] = str(round(goalCvar*100, 2))+"%"
            request.session['outputSharpe'] = str(round(goalSharpe, 2))

            messages.success(request, f'Optimization Completed Successfully')
            return redirect('betterRender')
        
    else:
        form = betterPortForm(request.user)
        html_graph = emptyPlot()
    return render(request, 'recommend_better_paul.html', {'graph':html_graph, 'form': form})

@login_required
def betterRender(request):
    #this seperate function handles the plotting and saving of the improved portfolio after the optimization algorithms are complete
    insizes = request.session.get('inputSizes')
    inlabels = request.session.get('inputLabels')
    inReturn = request.session.get('inputReturn')
    inCvar = request.session.get('inputCvar')
    inSharpe = request.session.get('inputSharpe')

    outsizes = request.session.get('outputSizes')
    outlabels = request.session.get('outputLabels')
    outReturn = request.session.get('outputReturn')
    outCvar = request.session.get('outputCvar')
    outSharpe = request.session.get('outputSharpe')

    #print(insizes, inlabels, outsizes, outlabels)

    inPieSize, inPieLabel = pieCompressor(insizes, inlabels, 0.05)
    outPieSize, outPieLabel = pieCompressor(outsizes, outlabels, 0.05)

    html_graph = plotDualPie(inPieSize, inPieLabel, outPieSize, outPieLabel)

    if request.method == 'POST':
        form = portfolioSaveForm(request.POST)
        if form.is_valid():

            #portfolio creation code
            portName = form.cleaned_data['portfolioName']
            p = PortfolioID(portfolioName = portName, userID = request.user)
            p.save()

            for i in range(0,len(outlabels)):
                saveTicker = stockID.objects.get(pk=outlabels[i])
                asset = PortfolioWeights(portfolioID = p, tickerID = saveTicker, volume = outsizes[i])
                asset.save()

            #freeing session variables to prevent leakage into other functions
            request.session['sizes'] = []
            request.session['labels'] = []
            request.session['portfolioReturn'] = ''
            request.session['cvar'] = ''
            request.session['sharpe'] = ''

            #message and returning to select menu
            messages.success(request, f'Portfolio {portName} Saved Successfully')
            return redirect('select')
        
    else:  
        form = portfolioSaveForm()
    return render(request, 'betterRender_paul.html', {'form':form, 'graph':html_graph, 'inreturn':inReturn, 'incvar':inCvar, 'insharpe':inSharpe, 'outreturn':outReturn, 'outcvar':outCvar, 'outsharpe':outSharpe})

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
            goalReturn, goalCvar, goalSharpe, goal_sizes, goal_labels = optimizeScript2(monthlyGoal)
            compressed_sizes, compressed_labels = portfolioCompressor(goal_sizes, goal_labels, 0.01)

            #print(type(goalReturn))
            #print(type(goalCvar))
            #print(type(goalSharpe))
            #print(type(compressed_sizes))
            #print(type(compressed_labels))

            #saving metrics for passing to the saving screen
            request.session['sizes'] = compressed_sizes
            request.session['labels'] = compressed_labels
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
    return render(request, 'goal_paul.html', {'form': form})

@login_required
def goalRender(request):
    #this seperate function handles the plotting and saving of portfolios after the optimization algorithms are complete
    sizes = request.session.get('sizes')
    labels = request.session.get('labels')
    portReturn = request.session.get('portfolioReturn')
    portCvar = request.session.get('cvar')
    portSharpe = request.session.get('sharpe')

    print(sizes)
    print(sum(sizes))
    
    piesize, pielabel = pieCompressor(sizes, labels, 0.03)
    html_graph = plotPie(piesize, pielabel)

    if request.method == 'POST':
        form = portfolioSaveForm(request.POST)
        if form.is_valid():

            #portfolio creation code
            portName = form.cleaned_data['portfolioName']
            p = PortfolioID(portfolioName = portName, userID = request.user)
            p.save()

            for i in range(0,len(labels)):
                saveTicker = stockID.objects.get(pk=labels[i])
                asset = PortfolioWeights(portfolioID = p, tickerID = saveTicker, volume = sizes[i])
                asset.save()

            #freeing session variables to prevent leakage into other functions
            request.session['sizes'] = []
            request.session['labels'] = []
            request.session['portfolioReturn'] = ''
            request.session['cvar'] = ''
            request.session['sharpe'] = ''

            #message and returning to select menu
            messages.success(request, f'Portfolio {portName} Saved Successfully')
            return redirect('select')
        
    else:  
        form = portfolioSaveForm()
    return render(request, 'goalRender_paul.html', {'form':form, 'graph':html_graph, 'return':portReturn, 'cvar':portCvar, 'sharpe':portSharpe})

def demo(request):
    sizes1 = [0.5,0.3,0.1, 0.05, 0.02, 0.02, 0.01]
    labels1 = ['a','b','c', 'd', 'e','f','g']

    #sizes2 = [0.7,0.1,0.2]
    #labels2 = ['testing','tesing','testing']

    #volumeToValue(stockID.objects.filter(tickerID='AAPL')[0], 0)
    #html_graph = emptyPlot()
    #optimizeTester()
    testsize, testlabel = portfolioCompressor(sizes1, labels1, 0.1)
    print(testsize)
    print(testlabel)
    form = optimizeGoalForm()
    return render(request, 'demo.html', {'form': form, 'demoVar':6})

@login_required
def backtest(request):
#preforms backtesting (or forward projection) using a given portfolio

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

            """
            #checking that weights sum to 1
            weight_sum = w1
            weight_sum += 0 if(t2 is None) else 0 if(w2 is None) else w2
            weight_sum += 0 if(t3 is None) else 0 if(w3 is None) else w3
            """

           # if(weight_sum == 1):
                #pulling data for portfolio creation from form
            inputPortfolioName =form.cleaned_data['portfolioName'] 
            p = PortfolioID(portfolioName = inputPortfolioName, userID = request.user)
            p.save()

            #converting volumes to weights
            val1 = volumeToValue(t1, w1)
            if ((t2 is not None) and (w2 is not None)):
                val2 = volumeToValue(t2, w2)
            else:
                val2 = 0
            if ((t3 is not None) and (w3 is not None)):
                val3 = volumeToValue(t3, w3)
            else:
                val3 = 0
            tot_val = val1 + val2 + val3

            #saving asset weights
            asset1 = PortfolioWeights(portfolioID = p, tickerID = t1, volume = val1/tot_val)
            print(volumeToValue(t1,1))
            asset1.save()

            if ((t2 is not None) and (w2 is not None)):
                asset2 = PortfolioWeights(portfolioID = p, tickerID = t2, volume = val2/tot_val)
                print(volumeToValue(t2,1))
                asset2.save()

            if ((t3 is not None) and (w3 is not None)):
                asset3 = PortfolioWeights(portfolioID = p, tickerID = t3, volume = val3/tot_val)
                print(volumeToValue(t3,1))
                asset3.save()

            messages.success(request, f'Portfolio "{inputPortfolioName}" Successfully Created')
            return redirect('select')
            #else:
            #    messages.error(request, f'Weights must sum to 1')
    else:
        form = portfolioForm()
    return render(request, 'portfolio_paul.html', {'form': form})

