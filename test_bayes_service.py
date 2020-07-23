import sys
import grpc
import bayes
from bayes.utils import create_query


	

# import the generated classes
import service.service_spec.bayesian_pb2_grpc as grpc_bayes_grpc
import service.service_spec.bayesian_pb2
from service.service_spec.bayesian_pb2 import BayesianNetworkQuery
from service.service_spec.bayesian_pb2 import QueryId

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
        bayesianNetwork = covid_bayes.covid_bayes()
        evidence = {}
        outvars= ["emergency_treatment","covid_risk","covid_severity"]
        query = create_query(evidence,outvars,bayesianNetwork)
        
        grpc_method = input("Method (stateless|statefull): ") if not test_flag else "statefull"

        # Open a gRPC channel
        channel = grpc.insecure_channel("{}".format(endpoint))
        stub = grpc_bayes_grpc.BayesNetStub(channel)

        if grpc_method == "stateless":
            bayesianNetworkQuery = BayesianNetworkQuery()
            bayesianNetworkQuery.bayesianNetwork.CopyFrom( bayesianNetwork)
            bayesianNetworkQuery.query.CopyFrom(query)
            response = stub.StatelessNet(bayesianNetworkQuery)
            print("response.varAnswers")
            print(response.varAnswers)
        elif grpc_method == "statefull":
            response = stub.StartNet(bayesianNetwork)
            print("response.id")
            print(response.id)
            queryId = QueryId()
            queryId.id = response.id
            queryId.query.CopyFrom(query)
            response = stub.AskNet(queryId)
            print("response.varAnswers")
            print(response.varAnswers)
        else:
            print("Invalid method!")
            exit(1)

    except Exception as e:
        print("Exception")
        print(e)
        exit(1)
