from pomegranate import DiscreteDistribution
from pomegranate import BayesianNetwork
from pomegranate import Node
from pomegranate import ConditionalProbabilityTable

def dictVarsAndValues(bayesianNetwork,cpt):
    varsAndValues ={}
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
    klist = [list(a)[0] for a in invars.values()]
    cpt_rows = []
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
    return (cpt_rows,klist, outvars)



def all(bayesianNetwork, cpt, invars, outvars):
    import itertools

    vdict = dictVarsAndValues(bayesianNetwork, cpt)
    vlist = [vdict[v] for v in invars.keys()]
    cartesian = list(itertools.product(*vlist))
    klist = [list(a)[0] for a in invars.values()]
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
    return (cpt_rows,klist,outvars)


def avg(bayesianNetwork, cpt, invars, outvars):
    import itertools

    vdict = dictVarsAndValues(bayesianNetwork, cpt)
    vlist = [vdict[v] for v in invars.keys()]
    cartesian = list(itertools.product(*vlist))
    klist = [list(a)[0] for a in invars.values()]
    cpt_rows = []
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
    return (cpt_rows,klist,outvars)




def if_then_else(bayesianNetwork, cpt, invars, outvars):
    import itertools

    vdict = dictVarsAndValues(bayesianNetwork, cpt)
    vlist = [vdict[v] for v in invars.keys()]
    cartesian = list(itertools.product(*vlist))
    klist = [list(a)[0] for a in invars.values()]
    cpt_rows = []
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
    return (cpt_rows,klist,outvars)





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
    for dist in bayesianNetwork.discreteDistributions:
        distribution ={}
        for var in dist.variables:
            distribution[var.name]= var.probability
        discreteDistribution = DiscreteDistribution(distribution)
        state[dist.name] = Node(discreteDistribution, dist.name)
        model.add_state(state[dist.name])
    for table in bayesianNetwork.conditionalProbabilityTables:
        tablelist = []
        for row in table.conditionalProbabilityRows:
            rowlist = []
            for var in row.randomVariableValues:
                rowlist.append (var)
            rowlist.append(row.probability)
            tablelist.append(rowlist)
        varlist = []
        for var in table.randomVariables:
            varlist.append(state[var.name])
        conditionalProbabilityTable = ConditionalProbabilityTable(tablelist,varlist)
        state[table.name] = Node(conditionalProbabilityTable, table.name)
        model.add_state(state[table.name])
                
    return model
