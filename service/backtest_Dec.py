# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 19:35:05 2018

# @author: cici
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from load import Loader
from QRLH import ScenarioGenerator
from optimization import cvar_opt
#from cvar_opt import opt
import gurobipy 

class backtester:
    
    def __init__(self, holding_period, historical_return, portfolio):
        self.period = holding_period
        self.max_length = float("inf")
        for ticker in portfolio:
            if len(historical_return[ticker]) < self.max_length:
                self.max_length = len(historical_return[ticker])
        self.portfolio = portfolio
        self.historical_return = historical_return

    def profile_monthly_parameter(self,port,scen,scen_count):
        monthly_ret = np.zeros(scen_count)
        for ticker in port:
            monthly_ret += port[ticker] * scen[ticker]
        
        monthly_ret = monthly_ret - 1
        mean = np.mean(monthly_ret) 
        std = np.std(monthly_ret)
        var = np.percentile(monthly_ret, 5) 

        cvar =np.mean(monthly_ret[monthly_ret<var])
        riskfree = np.mean(scen['SHV'])-1
        sharpe = (mean - riskfree)/std
        return (mean,cvar,sharpe)
        

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
            #print(port_ret)
            rets.append(port_ret)
        line = plt.plot(np.divide(xs,252), rets)
        plt.setp(line, color='r', linewidth=0.333)
        plt.title('portfolio return for given period')
        plt.xlabel('start year from today')
        plt.ylabel('cumulative return')
        plt.savefig(path)
        plt.clf()

    def forecast_randomwalk(self, scen_count = 5000):
        forecast = np.zeros((scen_count, self.period))
  
        standard_normal = np.random.randn(scen_count, self.period)
        for ticker in self.portfolio:
            drift = np.mean(self.historical_return[ticker])
            volatility = np.std(self.historical_return[ticker])
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
        plt.savefig(path)
        plt.clf()

if __name__ == '__main__':
    hist_min_len = 2600
    scen_count = 5000
    holding_period =120

    l = Loader()
    ret = l.read('stockret.csv')
    ret = l.filter(ret, hist_min_len)
    port = {'EXPE': 0.5, 'MSFT': 0.5}
    b = backtester(holding_period, ret, port)
    f = b.forecast_randomwalk(scen_count)

    forecast_lastday_gbm = f[:, -1]
    mean = np.mean(forecast_lastday_gbm)
    std = np.std(forecast_lastday_gbm)
    cvar = np.percentile(forecast_lastday_gbm, 5)
    #print('mean is {0}, std is {1}, cvar is {2}'.format(mean, std, cvar))
    
  
    ret = l.filter(ret, hist_min_len)
    sg = ScenarioGenerator(ret, scenario_count=scen_count, period=holding_period)
    scen = sg.generate_imc_scenario(beta=63)

    sg_monthly = ScenarioGenerator(ret,scenario_count = scen_count, period = 21)
    scen_monthly = sg_monthly.generate_imc_scenario(beta = 120)
   # sg_op = ScenarioGenerator(ret, scenario_count=scen_count, period=22)
    #scen_op = sg_op.generate_imc_scenario(beta = 90)

    #sg_gbm = ScenarioGenerator(ret,scenario_count=scen_count,period = 22)
    #scen_gbm = sg_gbm.forecast_randomwalk()
    

    forecast_lastday = np.zeros(scen_count)
    for ticker in port:
        forecast_lastday += port[ticker] * scen[ticker]
    
    forecast_lastday = forecast_lastday - 1
    mean = np.mean(forecast_lastday) 
    std = np.std(forecast_lastday)
    cvar = np.percentile(forecast_lastday, 5) 
    plt.hist(forecast_lastday,bins= np.linspace(-0.1, 0.26, num = 30))
    plt.savefig('histogran for last day')
    b.plot_forecast(f, './rw.png', plot_count=20)
    b.plot_rolling_return('.rolling.png')

    mean_port, cvar_port, sharpe_port = b.profile_monthly_parameter(port,scen_monthly,scen_count)
    print(mean_port,cvar_port,sharpe_port)


    p = cvar_opt()
    #mean_opt, cvar_opt, sharpe_opt = 
    p.optimization(scen_monthly,0.0256)
    
    #print(mean_opt,cvar_opt,sharpe_opt)




 
