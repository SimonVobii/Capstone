from gurobipy import *
import numpy as np
import pandas
from .backtest import *
from .QRLH import *

class cvar_opt:
    def goalOptimizer(self,ret,ret_goal):
    #Takes a certain return objective, and arrives at a portfolio consisting of the investment universie that minimizes portfolio CVaR

        m = Model("model1")
        z, c, x, expected_ret, l, quant = {}, {}, {}, {}, {}, {}
        # Create variables
        for i in range(5000):
            z[i] = m.addVar(lb = 0, obj = 1/(0.05*5000), vtype=GRB.CONTINUOUS, name="z[%s]"%i)

        #for all assets in universe
        for i in range(len(ret)):
            x[i] = m.addVar(lb = -0.2, ub = 0.2, vtype=GRB.CONTINUOUS, name="x[%s]"%i)
        #for i in range(206):
            #l[i] = m.addVar(vtype=GRB.BINARY, name="l[%s]"%i)
        m.update()
        
        #calculates the mean & standard deviation of asset returns
        j = 0       
        total_ret = LinExpr()
        for keys in ret:
            expected_ret[keys] = np.mean(ret[keys]) - 1
            std = np.std(ret[keys])
            total_ret+= x[j]*(expected_ret[keys])
            j = j+1
          
        #setting up return constraint
        m.addConstr(total_ret >= ret_goal,"ret goal")
        m.update()
        
        #setting up optimization
        v = LinExpr()
        obj = LinExpr()
        obj += v
        m.setObjective(obj, GRB.MINIMIZE)  
        m.update()  
        sum = 0
        var = 0
        
        #Calculates the 5% CVaR of each asset
        p = 0
        for keys in ret:
            sum = 0
            var = np.percentile(ret[keys], 0.05)
            v += x[p]*var
            for i in range (5000):
                if ret[keys][i] <= var:
                    sum += (1/5000)*(ret[keys][i] - 1)
            quant[keys] = sum  
            p = p + 1
        m.update()
        
        #weight constraint
        weightconstraint =LinExpr()
        for i in range(len(ret)):
            weightconstraint+=x[i]
        m.addConstr(weightconstraint == 1, "k1")

        #cardinalityconstraint =LinExpr()    
        #for i in range(206):
         #   cardinalityconstraint+=l[i]
        #m.addConstr(cardinalityconstraint == 206, "k2")
        #m.update()
      
        #Set of constraints resulting from model formulation
        for i in range (5000):
            c[i] = LinExpr()
            k = 0 
            for keys in ret:          
                c[i]+=(ret[keys][i] - 1)*(-1)*x[k]
                k = k+1              
            m.addConstr(z[i] >= c[i] - v, "c[%s]"%i)
            m.update()
        
        #run optimization
        m.optimize()

        #printing out allocations and returns
        i =0 
        Return = 0
        CVaR = 0
        for keys in expected_ret:
            if x[i].X !=0:
                print ('allocate',x[i].X,'in',keys)
                Return += x[i].X*expected_ret[keys]
                CVaR += x[i].X*quant[keys]
            i = i+1 

        print (Return)
        print(CVaR)

def optimizeScript():

    ret = fullLoad()

    sg_op = ScenarioGenerator(ret, scenario_count=5000, period=22)
    scen_op = sg_op.generate_imc_scenario(beta=120) 

    p = cvar_opt()
    p.goalOptimizer(scen_op, 0.05)