from pomegranate import DiscreteDistribution

def any(bayesianNetwork, cpt, invars, outvars):
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


def bayesInitialize(bayesianNetwork):
    print("bayesianNetwork")
    for dist in bayesianNetwork.discreteDistributions:
        print ("dist.name")
        print (dist.name)
        for var in dist.variables:
            print ("var.name")
            print (var.name)
            print ("var.probability")
            print (var.probability)

    return None
