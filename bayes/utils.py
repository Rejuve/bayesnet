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
        print('cpt_tuple;)
        print(cpt_tuple)
        varsAndValues[name]= cpt_tuple[2]
    return varsAndValues

def any(bayesianNetwork, cpt, invars, outvars):
    import itertools

    vdict = dictVarsAndValues(bayesianNetwork, cpt)
    vlist = [vdict[v] for v in invars.keys()]
    cartesian = list(itertools.product(*vlist))
    klist = invars.values()
    cpt_rows = []
    for c in cartesian:
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






    cpt["emergency_treatment"] = any(bayesianNetwork, cpt,
                                     {
                                         "possible_dehydration": {"possible_dehydration"},
                                         "possible_meningitis": {"possible_meningitis"},
                                         "acute_medical_condition": {"acute_medical_condition"}
                                     },
                                     ["no_emergency_treatment", "emergency_treatment"]
                                     )

    #print("bayesianNetwork")
    #print(bayesianNetwork)
    #print("cpt")
    #print(cpt)
    #print ("invars")
    #print (invars)
    #print ("outvars")
    #print (outvars)
    return None

def all(bayesianNetwork, cpt, invars, outvars):
    #print("bayesianNetwork")
    #print(bayesianNetwork)
    #print("cpt")
    #print(cpt)
    #print("invars")
    #print(invars)
    #print("outvars")
    #print(outvars)
    return None

def avg(bayesianNetwork, cpt, invars, outvars):
    #print("bayesianNetwork")
    #print(bayesianNetwork)
    #print("cpt")
    #print(cpt)
    #print ("invars")
    #print (invars)
    #print ("outvars")
    #print (outvars)
    return None

def if_then_else(bayesianNetwork, cpt, invars, outvars):
    #print("bayesianNetwork")
    #print(bayesianNetwork)
    #print("cpt")
    #print(cpt)
    #print ("invars")
    #print (invars)
    #print ("outvars")
    #print (outvars)
    return None

def addCpt(bayesianNetwork, cpt):
    #print("bayesianNetwork")
    #print(bayesianNetwork)
    #print("cpt")
    #print(cpt)
    pass


def bayesInitialize(bayesianNetwork,name):
    model = BayesianNetwork(name)
    print("bayesianNetwork")
    for dist in bayesianNetwork.discreteDistributions:
        print ("dist.name")
        print (dist.name)
        distribution ={}
        for var in dist.variables:
            print ("var.name")
            print (var.name)
            print ("var.probability")
            print (var.probability)
            distribution[var.name]= var.probability
        discreteDistribution = DiscreteDistribution(distribution)
        state = Node(discreteDistribution, dist.name)
        model.add_state(state)
    print("model")
    print(model)
    return model
