# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 19:35:05 2018

@author: cici
"""

import numpy as np
#from load import Loader

#generates 5000 scenarios from past return
class ScenarioGenerator:
    
    def __init__(self, historical_return, scenario_count=5000, period=20):
        self.period = period
        self.scenario_count = scenario_count
        self.historical_return = historical_return

    def generate_indices(self, beta):
        # exponential back-off date, more recent is preferred
        starting_date = (np.random.exponential(beta, (self.scenario_count, 1)) * -1 - self.period).astype(int)
        f = np.arange(self.period).astype(int)
        # the date index for each day in scenario
        indices = np.repeat(starting_date, int(self.period), axis=1) + f
        return indices

    def generate_imc_scenario(self, beta = 60):
        indices = self.generate_indices(beta)
        collected_securities = {}
        for security in self.historical_return:
            # get historical return given the date indices
            sampled_return = self.historical_return[security][indices]
            # use product to get last day return
            collected_securities[security] = np.prod(sampled_return, axis=1)
        return collected_securities

#not used here
if __name__ == '__main__':
    l = Loader()
    ret = l.read('C:/Users/cici/Desktop/data/stockret.csv')
    ret = l.filter(ret, 1300)
    sg = ScenarioGenerator(ret, scenario_count=5000)
    scen = sg.generate_imc_scenario(beta=100)
    print(scen)