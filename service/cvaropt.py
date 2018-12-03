'''
Created on Dec 1st

Author:Cici
'''


from scipy.optimize import minimize
import matplotlib.pyplot as plt
import numpy as np

def objective(x, ret):
    port_ret = -1 * (np.dot(ret.T, x) - 1)
    var = np.percentile(port_ret, 95)
    objective = var + 1 / 0.05 * np.mean(np.max(port_ret - var, 0))
    return objective

def constraint1(x, ret, target):
    return np.mean(np.dot(ret.T, x) - 1) - target
            
def constraint2(x):
    return np.sum(x)-1
        
def optimize(ret, goal, short=False):
    keys = list(ret.keys())
    keys.sort()

    # sort the returns and transform into np array
    sorted_ret = np.array([ret[key] for key in keys])

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

    print("after optimization")
    port_ret = np.dot(sorted_ret.T, sol.x) - 1
    print("return is {0:.3f}".format(np.mean(port_ret)))
    print("std is {0:.3f}".format(np.std(port_ret)))
    print("var is {0:.3f}".format(np.percentile(port_ret, 1)))
    print("cvar is {0:.3f}".format(np.mean(port_ret[port_ret < np.percentile(port_ret, 1)])))
    print("sharpe is {0:.3f}".format((np.mean(port_ret) - riskfree) / np.std(port_ret)))

    #sol.x is the list of weights
    security_names = np.array(keys)
    index = np.where(sol.x > 0.03)
    big = sol.x[index]
    big = np.concatenate((big, [1-np.sum(big)]))
    #return this for labels
    names = security_names[index]
    names = np.concatenate((names, ['other']))
    labels = ["{0}: {1:.3f}".format(x, y) for x, y in zip(names, big)]
    plt.pie(big, labels=labels)
    plt.show()
    return big