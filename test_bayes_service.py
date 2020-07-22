import sys
import grpc
import bayes
from bayes.utils import create_query


	

# import the generated classes
import service.service_spec.bayesian_pb2_grpc as grpc_bayes_grpc
import service.service_spec.bayesian_pb2
from service.service_spec.bayesian_pb2 import BayesianNetworkQuery

from service import registry

from bayes import covid_bayes

if __name__ == "__main__":

    try:
        test_flag = False
        if len(sys.argv) == 2:
            if sys.argv[1] == "auto":
                test_flag = True

        # Example Service - Arithmetic
        endpoint = input("Endpoint (localhost:{}): ".format(registry["bayes_service"]["grpc"])) if not test_flag else ""
        if endpoint == "":
            endpoint = "localhost:{}".format(registry["bayes_service"]["grpc"])
        #print ("endpoint")
        #print (endpoint)
        bayesianNetwork = covid_bayes.covid_bayes()
        #print("bayesianNetwork")
        #print(bayesianNetwork)
        evidence = {}
        outvars= ["emergency_treatment","covid_risk","covid_severity"]
        query = create_query(evidence,outvars,bayesianNetwork)
        #print ("query")
        #print (query)
        bayesianNetworkQuery = BayesianNetworkQuery()
        bayesianNetworkQuery.bayesianNetwork.CopyFrom( bayesianNetwork)
        bayesianNetworkQuery.query.CopyFrom(query)
        #print("bayesianNetworkQuery")
        #print(bayesianNetworkQuery)
        
        grpc_method = input("Method (net|query|both): ") if not test_flag else "both"
        #print("grpc_method")
        #print(grpc_method)

        # Open a gRPC channel
        channel = grpc.insecure_channel("{}".format(endpoint))
        #print("channel")
        #print(channel)
        stub = grpc_bayes_grpc.BayesNetStub(channel)
        #print("stub")
        #print(stub)

        if grpc_method == "both":
            response = stub.StatelessNet(bayesianNetworkQuery)
            print("response")
            print(response)
	
            print("response.varAnswers")
            print(response.varAnswers)
        elif grpc_method == "net":
            pass
        elif grpc_method == "query":
           pass
        else:
            print("Invalid method!")
            exit(1)

    except Exception as e:
        print("Exception")
        print(e)
        exit(1)
