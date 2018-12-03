from gurobipy import *
import numpy as np
import pandas
from .backtest import *
from .QRLH import *
from scipy.optimize import minimize

class cvar_opt:
    def goalOptimizer(self,ret,ret_goal):
    #Takes a certain return objective, and arrives at a portfolio consisting of the investment universie that minimizes portfolio CVaR

        m = Model("model1")
        z, c, x,expected_ret, quant = {}, {}, {}, {}, {}
        # Create variables
        for i in range(5000):
            z[i] = m.addVar(lb = 0, vtype=GRB.CONTINUOUS, name="z[%s]"%i)
        for i in range(len(ret)):
            x[i] = m.addVar(lb = 0, ub = 0.15, vtype=GRB.CONTINUOUS, name="x[%s]"%i)
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
        
        weightconstraint =LinExpr()
 
        for i in range(len(ret)):
            weightconstraint+=x[i]
        m.addConstr(weightconstraint == 1, "k1")
      
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
        portfolioReturn = 0
        for keys in expected_ret:
            if x[i].X !=0:
                #print ('allocate',x[i].X,'in',keys)
                portfolioReturn += x[i].X*expected_ret[keys]
                #CVaR += x[i].X*quant[keys]
            i = i+1 
        #print(ret_goal)
        
        labels = []
        sizes = []
        
        i =0 
        ret_port = np.zeros(5000)
        for keys in ret:
            if x[i].X !=0:
                ret_port +=(ret[keys]-1)*x[i].X
                labels.append(str(keys))
                sizes.append(x[i].X*100)
                
            i = i+1 

        riskfree = np.mean(ret['SHV'])-1
        std = np.std(ret_port)
        portfolioReturn = np.mean(ret_port)
        sharpe = (portfolioReturn - riskfree)/std
        var = np.percentile(ret_port,5)
        cvar = np.mean(ret_port[ret_port<var])

        #printing HTML output
        #fig = plt.figure()
        #print(sizes)
        #print(labels)
        #patches, texts = plt.pie(sizes, labels = labels, shadow=True, startangle=90)
        #plt.legend(patches, labels, loc="best")
        #plt.axis('equal')
        #plt.tight_layout()
        #returnGraph = mpld3.fig_to_html(fig)
        #returnGraph = emptyPlot()

        return (portfolioReturn, cvar, sharpe, sizes, labels)

    def goalOptimizer2(self,ret,goal, short=False):
        keys = list(ret.keys())
        keys.sort()

        # sort the returns and transform into np array
        sorted_ret = np.array([ret[key] for key in keys])

        print("in optimization function")
        # initially evenly distributed
        x0 = np.ones(len(keys)) / len(keys)

        #print("before optimization")
        port_ret = np.dot(sorted_ret.T, x0) - 1
        riskfree = np.mean(ret['SHV']) - 1
        #print("return is {0:.3f}".format(np.mean(port_ret)))
        #print("std is {0:.3f}".format(np.std(port_ret)))
        #print("var is {0:.3f}".format(np.percentile(port_ret, 1)))
        #print("cvar is {0:.3f}".format(np.mean(port_ret[port_ret < np.percentile(port_ret, 1)])))
        #print("sharpe is {0:.3f}".format((np.mean(port_ret) - riskfree) / np.std(port_ret)))
        #print()

        if short:
            con = ({"fun":constraint1, "type":"ineq", 'args':(sorted_ret, goal)}, {"fun":constraint2, "type":"eq"})
            sol = minimize(objective, x0, args=(sorted_ret), constraints=con)
        else:
            b = (0.0, 1.0)
            bnds = []
            for i in range(x0.size):
                bnds.append(b)
            bnds = tuple(bnds)
            con = ({"fun":constraint1, "type":"ineq", 'args':(sorted_ret, goal)}, {"fun":constraint2, "type":"eq"})
            sol = minimize(objective, x0, args=(sorted_ret), bounds=bnds, constraints=con)

        #print("after optimization")
        port_ret = np.dot(sorted_ret.T, sol.x) - 1
        #print("return is {0:.3f}".format(np.mean(port_ret)))
        #print("std is {0:.3f}".format(np.std(port_ret)))
        #print("var is {0:.3f}".format(np.percentile(port_ret, 1)))
        #print("cvar is {0:.3f}".format(np.mean(port_ret[port_ret < np.percentile(port_ret, 1)])))
        #print("sharpe is {0:.3f}".format((np.mean(port_ret) - riskfree) / np.std(port_ret)))

        optimizedReturn = np.std(port_ret)
        optimizedCvar = np.mean(port_ret[port_ret < np.percentile(port_ret, 1)])
        optimizedSharpe = (np.mean(port_ret) - riskfree) / np.std(port_ret)

        #sol.x is the list of weights
        security_names = np.array(keys)
        #names = security_names[index]
        weightList = sol.x.tolist()
        labelList = security_names.tolist()
        #print(sol.x)
        #print(security_names)
        #index = np.where(sol.x > 0.03)
        #big = sol.x[index]
        #big = np.concatenate((big, [1-np.sum(big)]))
        #return this for labels
        #names = security_names[index]
        print("leaving optimization function")
        return(optimizedReturn, optimizedCvar, optimizedSharpe, weightList, labelList)
        #print(sol.x)
        #print(sum(sol.x))
        #print(security_names)
        #names = np.concatenate((names, ['other']))
        #labels = ["{0}: {1:.3f}".format(x, y) for x, y in zip(names, big)]
        #plt.pie(big, labels=labels)
        #plt.show()
        #return big

def objective(x, ret):
    port_ret = -1 * (np.dot(ret.T, x) - 1)
    var = np.percentile(port_ret, 95)
    objective = var + 1 / 0.05 * np.mean(np.max(port_ret - var, 0))
    return objective

def constraint1(x, ret, target):
    return np.mean(np.dot(ret.T, x) - 1) - target
            
def constraint2(x):
    return np.sum(x)-1

def optimizeScript(goal):

    ret = fullLoad()

    sg_op = ScenarioGenerator(ret, scenario_count=5000, period=22)
    scen_op = sg_op.generate_imc_scenario(beta=120) 

    p = cvar_opt()
    mean_port, cvar_port, sharpe_port, sizes, labels = p.goalOptimizer(scen_op, goal)
    print("leaving optimization script")
    return(mean_port, cvar_port, sharpe_port, sizes, labels)

def plotPie(sizes, labels):
    fig = plt.figure()
    #sizes = [0.5,0.3,0.2]
    #labels = ['tesing','testing','testing']

    patches, texts = plt.pie(sizes,shadow=True, startangle=90) #labels = labels, shadow=True, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    return(mpld3.fig_to_html(fig))

def plotDualPie(sizes1, labels1, sizes2, labels2):

    fig = plt.figure()

    plt.subplot2grid((3,7),(0,0), colspan=3,rowspan=3)
    patches1, texts1 = plt.pie(sizes1,shadow=True, startangle=90) #labels = labels, shadow=True, startangle=90)
    plt.legend(patches1, labels1, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.title('Input Portfolio')

    plt.subplot2grid((3,7),(0,4), colspan=3,rowspan=3)
    patches2, texts2 = plt.pie(sizes2,shadow=True, startangle=90) #labels = labels, shadow=True, startangle=90)
    plt.legend(patches2, labels2, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.title('Output Portfolio')

    return(mpld3.fig_to_html(fig))

def optimizeScript2(goal):
    ret = fullLoad()

    sg_op = ScenarioGenerator(ret, scenario_count=5000, period=22)
    scen_op = sg_op.generate_imc_scenario(beta=120) 

    p = cvar_opt()
    mean_port, cvar_port, sharpe_port, sizes, labels = p.goalOptimizer2(scen_op, goal)

    return(mean_port, cvar_port, sharpe_port, sizes, labels)