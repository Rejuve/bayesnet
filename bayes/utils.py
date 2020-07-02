from pomegranate import DiscreteDistribution
from pomegranate import BayesianNetwork
from pomegranate import Node
from pomegranate import ConditionalProbabilityTable

class Bayesnet():
    
    varsAndValues = {}
    nmap ={}
    
    def __init__(bayesianNetwork): 
        for dist in bayesianNetwork.discreteDistributions:
            varsAndValues [dist.name]= []
            for var in dist.variables:
                varsAndValues[dist.name].append(var.name)
        cutoffs = {}
        for a in range(2,10):
            if not a in cutoffs:
                cutoffs[a] ={}
            val = 1/a
            for j in range (0,a):
                cutoff[a][j] = j*val
        for a in range(2,10):
            if not a in nmap:
                nmap[a]={}
            for b in range(2,10):
                if not b in nmap[a]:
                    nmap[a][b] = {}
                for i in range (0,a):
                
         
        
    
    def dictVarsAndValues(bayesianNetwork,cpt):
        if len(varsandValues) ==0:
            for dist in bayesianNetwork.discreteDistributions:
                varsAndValues [dist.name]= []
                for var in dist.variables:
                    varsAndValues[dist.name].append(var.name)
        for name,cpt_tuple in cpt.items():
            print('name')
            print(name)
            print('cpt_tuple')
            print(cpt_tuple)
            varsAndValues[name]= cpt_tuple[2]
        return varsAndValues

    def any(bayesianNetwork, cpt, invars, outvars):
        import itertools

        vdict = dictVarsAndValues(bayesianNetwork, cpt)
        vlist = [vdict[v] for v in invars.keys()]
        cartesian = list(itertools.product(*vlist))
        klist = [a for a in invars.values()]
        keylist = invars.keys()
        cpt_rows = []
        for c in cartesian:
            qany=False
            i=0
            while (not qany) and i < len(klist):
                vset = klist[i]
                i += 1
                if c[i] in vset:
                    qany = True
            for i,o in enumerate(outvars):
                cpt_row = []
                cpt_row.extend(c)
                cpt_row.append(o)
                val = 1.0 if (i == 0 and qany) or (i == 1 and not qany) else 0.0
                cpt_row.append(val)
                cpt_rows.append(cpt_row)
        return (cpt_rows,keylist, outvars)



    def all(bayesianNetwork, cpt, invars, outvars):
        import itertools

        vdict = dictVarsAndValues(bayesianNetwork, cpt)
        vlist = [vdict[v] for v in invars.keys()]
        cartesian = list(itertools.product(*vlist))
        klist = [a for a in invars.values()]
        keylist = invars.keys()
        cpt_rows = []
        for c in cartesian:
            qall=True
            for i,vset in enumerate(klist):
                    if c[i] not in vset:
                        qall = False
            for i,o in enumerate(outvars):
                cpt_row = []
                cpt_row.extend(c)
                cpt_row.append(o)
                val = 1.0 if (i == 0 and qall) or (i == 1 and not qall) else 0.0
                cpt_row.append(val)
                cpt_rows.append(cpt_row)
        return (cpt_rows,keylist,outvars)


    def avg(bayesianNetwork, cpt, invars, outvars):
        import itertools

        vdict = dictVarsAndValues(bayesianNetwork, cpt)
        vlist = [vdict[v] for v in invars.keys()]
        cartesian = list(itertools.product(*vlist))
        klist = [a for a in invars.values()]
        keylist = invars.keys()
        cpt_rows = []
        bins = {}
        for c in cartesian:
            qany=False
            for i,vset in enumerate(klist):
                    if c[i] in vset:
                        qany = True
            for i,o in enumerate(outvars):
                cpt_row = []
                cpt_row.extend(c)
                cpt_row.append(o)
                val = 1.0 if (i == 0 and qany) or (i == 1 and not qany) else 0.0
                cpt_row.append(val)
                cpt_rows.append(cpt_row)
        return (cpt_rows,keylist,outvars)




    def if_then_else(bayesianNetwork, cpt, invars, outvars):
        import itertools

        vdict = dictVarsAndValues(bayesianNetwork, cpt)
        vlist = [vdict[v] for v in invars.keys()]
        cartesian = list(itertools.product(*vlist))
        klist = [a for a in invars.values()]
        print('cartesian')
        print(cartesian)
        print('klist')
        print(klist)
        keylist = invars.keys()
        cpt_rows = [] 
        for c in cartesian:
            result = ""
            i=0
            while (result == "") and i < len(klist):
                vset = klist[i]
                i += 1
                if c[i] in vset:
                    result = outvars[i]
            if result == "":
                result = outvars[-1]

            for i,o in enumerate(outvars):
                cpt_row = []
                cpt_row.extend(c)
                cpt_row.append(o)
                val = 1.0 if (o == result) else 0.0
                cpt_row.append(val)
                cpt_rows.append(cpt_row)
        return (cpt_rows,keylist,outvars)





    def addCpt(bayesianNetwork, cpt):

        for name, cpt_tuple in cpt.items():
            conditionalProbabilityTable = bayesianNetwork.conditionalProbabilityTables.add()
            conditionalProbabilityTable.name = name
            for rv in cpt_tuple[1]:
                randomVariable = conditionalProbabilityTable.randomVariables.add()
                randomVariable.name = rv
            for row in cpt_tuple[0]:  
                conditionalProbabilityRow = conditionalProbabilityTable.conditionalProbabilityRows.add()
                for i,var in enumerate(row):
                  nvars = len(row)-1
                  if i < nvars:
                    randomVariableValue = conditionalProbabilityRow.randomVariableValues.add()
                    randomVariableValue.name = var
                  else:
                    conditionalProbabilityRow.probability = var
                    
        


    def bayesInitialize(bayesianNetwork,name):
        model = BayesianNetwork(name)
        state = {}
        general_distribution = {}
        for dist in bayesianNetwork.discreteDistributions:
            distribution ={}
            for var in dist.variables:
                distribution[var.name]= var.probability
            discreteDistribution = DiscreteDistribution(distribution)
            general_distribution[dist.name] = discreteDistribution
            state[dist.name] = Node(discreteDistribution, dist.name)
            model.add_state(state[dist.name])
        for table in bayesianNetwork.conditionalProbabilityTables:
            tablelist = []
            for row in table.conditionalProbabilityRows:
                rowlist = []
                for var in row.randomVariableValues:
                    rowlist.append (var.name)
                rowlist.append(row.probability)
                tablelist.append(rowlist)
            varlist = []
            for var in table.randomVariables:
                varlist.append(general_distribution[var.name])
            print("table.name")
            print(table.name)
            print("tablelist")
            print(tablelist)
            print("varlist")
            print(varlist)
            conditionalProbabilityTable = ConditionalProbabilityTable(tablelist,varlist)
            general_distribution[table.name] = conditionalProbabilityTable
            state[table.name] = Node(conditionalProbabilityTable, table.name)
            model.add_state(state[table.name])
            print('state')
            print(state)
            for var in table.randomVariables:
                print("var.name")
                print(var.name)
                print ("table.name")
                print (table.name)
                model.add_edge(state[var.name],state[table.name])

        return model
