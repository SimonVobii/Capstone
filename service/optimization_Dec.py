#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 10:40:04 2018

@author: Daniel
"""

from gurobipy import *
import numpy as np
from scipy.stats import norm


class cvar_opt:
    def optimization(self,ret,ret_goal):
        m = Model("model1")
        z, c, x,expected_ret, quant = {}, {}, {}, {}, {}
        # Create variables
        for i in range(5000):
            z[i] = m.addVar(lb = 0, vtype=GRB.CONTINUOUS, name="z[%s]"%i)
        for i in range(len(ret)):
            x[i] = m.addVar(lb = 0, ub = 0.2, vtype=GRB.CONTINUOUS, name="x[%s]"%i)
        #for i in range(206):
            #l[i] = m.addVar(vtype=GRB.BINARY, name="l[%s]"%i)
        m.update()
        
        j = 0       
        total_ret = LinExpr()
        for keys in ret:
            expected_ret[keys] = np.mean(ret[keys]) - 1
            std = np.std(ret[keys])
            total_ret+= x[j]*expected_ret[keys]
            j = j+1
          
        #print (total_ret)
        m.addConstr(total_ret >= ret_goal,"ret goal")
        m.update()

        v = LinExpr()
 
        var = {}
        p = 0
        for keys in ret:
            var[keys] = np.percentile((ret[keys]-1)*-1,95)
            v+= x[p]*var[keys]
            p = p+1
     
   

        obj = LinExpr()
        obj += v
        for i in range(5000):
            obj+=1/(0.05*5000)*z[i]
        #obj +=y
        m.setObjective(obj, GRB.MINIMIZE)  
        m.update()
        
   

        #for i in range(5000):
            #for keys in ret:
             #   sum += 1/206*(ret[keys] - 1)
            #k[i] = sum

       

            #sum = 0
            #var = np.percentile(ret[keys], 5)
            #v += x[p]*var
            #for i in range (5000):
             #   if ret[keys][i] <= var:
             #       sum += (1/5000)*(ret[keys][i] - 1)
            #quant[keys] = sum  
            #p = p + 1
        
     
        
        weightconstraint =LinExpr()
 
        for i in range(len(ret)):
            weightconstraint+=x[i]
        m.addConstr(weightconstraint == 1, "k1")
        
        #for i in range(206):
         #   cardinalityconstraint+=l[i]
        #m.addConstr(cardinalityconstraint == 206, "k2")
        #m.update()
      
        for i in range (5000):
            c[i] = LinExpr()
            k = 0 
            for keys in ret:          
                c[i]+=(-1)*(ret[keys][i] - 1)*x[k]
                k = k+1              
            m.addConstr(z[i] >= c[i] - v, "c[%s]"%i)
            m.update()
        m.optimize()


        i =0 
        Return = 0
        CVaR = 0
        for keys in expected_ret:
            if x[i].X !=0:
                print ('allocate',x[i].X,'in',keys)
                Return += x[i].X*expected_ret[keys]
                
                #CVaR += x[i].X*quant[keys]
            i = i+1 
        #print(ret_goal)
        
        i =0 
        ret_port = np.zeros(5000)
        for keys in ret:
            if x[i].X !=0:
                ret_port +=(ret[keys]-1)*x[i].X
            
            i = i+1 
        #print(ret_port)

        riskfree = np.mean(ret['SHV'])-1
        std = np.std(ret_port)
        Return = np.mean(ret_port)
       # print(min(ret_port))
        sharpe = (Return - riskfree)/std
        var = np.percentile(ret_port,5)
        print('var',var)
        cvar = np.mean(ret_port[ret_port<var])

        return(Return,cvar,sharpe)
     
        
        
    

        


    