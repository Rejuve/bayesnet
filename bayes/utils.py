from pomegranate import DiscreteDistribution
from pomegranate import BayesianNetwork
from pomegranate import Node

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
