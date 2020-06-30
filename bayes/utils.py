from pomegranate import DiscreteDistribution
from pomegranate import BayesianNetwork
from pomegranate import Node

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
    klist = list(invars.values())
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



def all(bayesianNetwork, cpt, invars, outvars):
    import itertools

    vdict = dictVarsAndValues(bayesianNetwork, cpt)
    vlist = [vdict[v] for v in invars.keys()]
    cartesian = list(itertools.product(*vlist))
    klist = list(invars.values())
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


def avg(bayesianNetwork, cpt, invars, outvars):
    import itertools

    vdict = dictVarsAndValues(bayesianNetwork, cpt)
    vlist = [vdict[v] for v in invars.keys()]
    cartesian = list(itertools.product(*vlist))
    klist = list(invars.values())
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
    klist = list(invars.values())
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
    #print("bayesianNetwork")
    #print(bayesianNetwork)
    #print("cpt")
    #print(cpt)
    pass


def bayesInitialize(bayesianNetwork,name):
    model = BayesianNetwork(name)
    for dist in bayesianNetwork.discreteDistributions:
        distribution ={}
        for var in dist.variables:
            distribution[var.name]= var.probability
        discreteDistribution = DiscreteDistribution(distribution)
        state = Node(discreteDistribution, dist.name)
        model.add_state(state)
    return model
