from gurobipy import *
import numpy as np
import pandas


class cvar_opt:
    def optimization(self,ret,ret_goal):
        m = Model("model1")
        z, c, x, expected_ret = {}, {}, {}, {}
        # Create variables
        for i in range(5000):
            z[i] = m.addVar(lb = 0, obj = 1/(0.05*5000), vtype=GRB.CONTINUOUS, name="z[%s]"%i)
        for i in range(206):
            x[i] = m.addVar(lb = -0.2, ub = 0.2, vtype=GRB.CONTINUOUS, name="x[%s]"%i)
        m.update()
        
        j = 0 
        v = LinExpr()
        total_ret = LinExpr()
        for keys in ret:
            expected_ret[keys] = np.mean(ret[keys]) - 1
            std = np.std(ret[keys])
            total_ret+= x[j]*(expected_ret[keys])
            v += (x[j])*norm.ppf(0.05, expected_ret[keys], std)
            j = j+1
        
        print (total_ret)
        m.addConstr(total_ret >= ret_goal,"ret goal")
        m.update()
        
        obj = LinExpr()
        obj += v
        #for i in range(5000):
            #obj+=1/(0.01*5000)*z[i]
        #for i in range(5000):
         #   obj.add(z[i], 1/(0.05*5000))
        m.setObjective(obj, GRB.MINIMIZE)  
        m.update()
        #print(v)
        #v = abs(v)      
        weightconstraint =LinExpr()
        for i in range(206):
            weightconstraint+=x[i]
      #  print(weightconstraint)    
        #Add Constraints
        m.addConstr(weightconstraint == 1, "k1")
        m.update()
       # for i in range(206):
           # m.addConstr(x[i] >= -0.15)
          # m.addConstr(x[i] <= 0.15)
        #m.update()
            
        #for i in range(5000):
        #    m.addConstr(z[i] >=0 ,"c2")
        #m.update()
        #First Constraint
        for i in range (5000):
            c[i] = LinExpr()
            k = 0 
            for keys in ret:          
                c[i]+=(ret[keys][i] - 1)*(-1)*x[k]
                k = k+1              
            m.addConstr(z[i] >= c[i] - v, "c[%s]"%i)
            m.update()
        m.optimize()

        i =0 
        for keys in expected_ret:
            if x[i].X !=0:
                print ('allocate',x[i].X,'in',keys)
            i = i+1 
        print(ret_goal)
        m.write("refinery-output.sol")

        


    