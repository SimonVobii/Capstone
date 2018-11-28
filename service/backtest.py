# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 19:35:05 2018

# @author: cici
"""

import numpy as np
import matplotlib.pyplot as plt, mpld3
#from load import Loader
from .QRLH import ScenarioGenerator
from .optimization import cvar_opt
import gurobipy 
from .models import *

class backtester:
    
    def __init__(self, holding_period, historical_return, portfolio):
        self.period = holding_period
        self.max_length = float("inf")
        for ticker in portfolio:
            if len(historical_return[ticker]) < self.max_length:
                self.max_length = len(historical_return[ticker])
        self.portfolio = portfolio
        self.historical_return = historical_return

    def plot_rolling_return(self, path):
        xs = []
        rets = []
        # find return of port for period days given a starting date going back to max len
        for i in range(-self.max_length, -self.period + 1):
            xs.append(i)
            port_ret = 0
            for ticker in self.portfolio:
                port_ret += self.portfolio[ticker] * np.prod(self.historical_return[ticker][i:i+self.period])
            port_ret = port_ret -1
            rets.append(port_ret)
        line = plt.figure()
        plt.plot(np.divide(xs,252), rets)
        #plt.setp(line, color='r', linewidth=0.333)
        plt.title('portfolio return for given period')
        plt.xlabel('start year from today')
        plt.ylabel('cumulative return')
        return(mpld3.fig_to_html(line))
        #plt.savefig(path)
        #plt.clf()

    def forecast_randomwalk(self, scen_count = 5000):
        forecast = np.zeros((scen_count, self.period))
        standard_normal = np.random.randn(scen_count, self.period)
        for ticker in self.portfolio:
            drift = np.mean(self.historical_return[ticker])
            volatility = np.std(self.historical_return[ticker])
            print(volatility)
            sim_daily_ret = standard_normal * volatility + drift
            cum_prod = np.cumprod(sim_daily_ret, axis=1)
            forecast = forecast + cum_prod * self.portfolio[ticker]
        forecast = forecast - 1
        return np.concatenate((np.zeros((scen_count, 1)), forecast), axis=1)

    def plot_forecast(self, forecast, path, plot_count = 10):
        # plot plot_count number of forecasts
        xs = list(range(self.period + 1))
        for scenario in forecast[:plot_count]:
            color = 'g'
            if scenario[-1] < 0:
                color = 'r'
            fig = plt.figure()
            plt.plot(xs, scenario, color=color, linewidth=0.333)
        mean = np.mean(forecast, axis=0)
        fifth = np.percentile(forecast, 5, axis=0)
        nintyfifth = np.percentile(forecast, 95, axis=0)
        mean_plot, = plt.plot(xs, mean, color='xkcd:black', linewidth=3, label='Mean')
        fifth_plot, = plt.plot(xs, fifth, color='xkcd:dark red', linewidth=3, label='5th Perc')
        nintyfifth_plot, = plt.plot(xs, nintyfifth, color='xkcd:forest green', linewidth=3, label='95th Perc')
        # set random shit
        plt.text(self.period + 3, mean[-1], '{0:.2f}'.format(mean[-1]))
        plt.text(self.period + 3, fifth[-1], '{0:.2f}'.format(fifth[-1]))
        plt.text(self.period + 3, nintyfifth[-1], '{0:.2f}'.format(nintyfifth[-1]))
        plt.legend(handles = [mean_plot, fifth_plot, nintyfifth_plot])
        plt.xlim(-5, self.period)
        plt.title('portfolio simulation')
        plt.xlabel('start date from today')
        plt.ylabel('cumulative return')
        return(mpld3.fig_to_html(fig))
        #plt.savefig(path)
        #plt.clf()

def backtestScript():
#if __name__ == '__main__':
    #constants for simulation, tuned to balance portfolio performance with calculation complexity
    hist_min_len = 1300
    scen_count = 5000

    #USER_INPUT (this is in days)
    holding_period = 120
    #USER_INPUT (as a fraction of total value)
    port = {'EXPE': 0.5, 'MSFT': 0.5}

    #load from database
    ret = {}
    for i in port:
        x=returnLoader(i)
        if len(x[i])>hist_min_len:
            ret.update(x)

    #class initialization
    b = backtester(holding_period, ret, port)
    f = b.forecast_randomwalk(scen_count)

    #accumulated return on the last day (this is 5000x1)
    forecast_lastday = f[:, -1]
    mean = np.mean(forecast_lastday)
    std = np.std(forecast_lastday)
    cvar = np.percentile(forecast_lastday, 1)
    #print('mean is {0}, std is {1}, cvar is {2}'.format(mean, std, cvar))

    #same thing again, using the second method (bootstrap, exponential with beta = 90)

    """
    full = []
    for i in stockID.objects.all():
        full.append(i.tickerID)

    ret = {}
    for i in full:
        x=returnLoader(i)
        if len(x[i])>1300:
            ret.update(x)

    sg = ScenarioGenerator(ret, scenario_count=scen_count, period=holding_period)
    scen = sg.generate_imc_scenario(beta=90)
    forecast_lastday = np.zeros(scen_count)
    for ticker in port:
        forecast_lastday += port[ticker] * scen[ticker]
    mean = np.mean(forecast_lastday) - 1
    std = np.std(forecast_lastday)
    cvar = np.percentile(forecast_lastday, 1) - 1
    """
   # print(forecast_lastday)
   # print('mean is {0}, std is {1}, cvar is {2}'.format(mean, std, cvar))
   
    #return( b.plot_rolling_return('./ret1.png') )
    return(b.plot_forecast(f, './rw.png', plot_count=20))
    #b.plot_rolling_return('.rolling.png')

    #p = cvar_opt()
    #p.optimization(scen)

def returnLoader(ticker):
#loading data from database in format needed for business logic

    loaded = list(stockHistory.objects.filter(tickerID = ticker))
    
    #initializing the dictionary object
    finalDict = dict.fromkeys([ticker])
    finalDict[ticker] = np.zeros(0)

    #we know the database is stored oldest -> newest, can use this when appending returns
    for i in loaded:
        finalDict[ticker] = np.insert(finalDict[ticker], 0, i.assetReturn)

    return(finalDict)

def fullLoad():
    
    port = []
    for i in stockID.objects.all():
        port.append(i.tickerID)

    ret = {}
    for i in port:
        x=returnLoader(i)
        if len(x[i])>1300:
            ret.update(x)