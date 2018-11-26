from gurobipy import *

import numpy as np

import pandas


class cvar_opt:
    def optimization(self,ret):

        

        m = Model("model1")

        

        z, c, x = {}, {}, {}

        # Create variables

        for i in range(5000):

            z[i] = m.addVar(obj=1, vtype='C', name="z[%s]"%i)

        for i in range(206):

            x[i] = m.addVar(obj=1, vtype='C', name="x[%s]"%i)
        m.update()
            

        # Set objective

        


        obj = LinExpr()
        obj+=-0.05
        for i in range(5000):
            obj+=1/(0.05*5000)*z[i]
        

        #for i in range(5000):

         #   obj.add(z[i], 1/(0.05*5000))

    

        m.setObjective(obj, GRB.MINIMIZE)

        

        weightconstraint =LinExpr()

        

        for i in range(206):

            weightconstraint+=x[i]

      #  print(weightconstraint)    

        #Add Constraints

        m.addConstr(weightconstraint == 1, "c1")

        

        #for i in range(206):

           ## m.addConstr(x[i] >= 0.01)

            #m.addConstr(x[i] <= 0.20)

            

        for i in range(5000):

            m.addConstr(z[i] >=0 ,"c2")

        

        

        

        #First Constraint

        for i in range (5000):

            c[i] = LinExpr()
            k = 0 

            for keys in ret:
                
                c[i]+=(ret[keys][i]-1)*(1)*x[k]
                k = k+1
               

            m.addConstr(z[i] >= c[i] - 0.05, "c[%s]"%i)

        
        m.update()
        m.optimize()
        print (m.getVars())
        m.write("refinery-output.sol")

        


    