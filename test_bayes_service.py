import sys
import grpc
import sn_bayes
from sn_bayes.utils import create_query


	

# import the generated classes
import sn_service.service_spec.bayesian_pb2_grpc as grpc_bayes_grpc
import sn_service.service_spec.bayesian_pb2
from sn_service.service_spec.bayesian_pb2 import BayesianNetworkQuery
from sn_service.service_spec.bayesian_pb2 import QueryId

from sn_service import registry

from sn_bayes import covid_bayes

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
	evidence["body_temperature"]= "body_temperature_above_102F"
	evidence["age"]= "elderly"
	evidence["diabetes"]= "diabetes"
        outvars= ["social_distancing", "social_distancing_binary","emergency_treatment","covid_risk","covid_risk_binary","covid_severity","covid_severity_binary"]
	explainvars= ["social_distancing", "social_distancing_binary","emergency_treatment","covid_risk","covid_risk_binary","covid_severity","covid_severity_binary"]
	reverse_explainvars = ["social_distancing", "social_distancing_binary"]
        query = create_query(bayesianNetwork,evidence,outvars,explainvars,reverse_explainvars)
        
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
            print("response.explanations")
            print(response.explanations)
            print("response.error_msg")
            print(response.error_msg)
        elif grpc_method == "statefull":
            response = stub.StartNet(bayesianNetwork)
            print("response.id")
            print(response.id)
            print("response.error_msg")
            print(response.error_msg)
            queryId = QueryId()
            queryId.id = response.id
            queryId.query.CopyFrom(query)
            response = stub.AskNet(queryId)
            print("response.varAnswers")
            print(response.varAnswers)
            print("response.explanations")
            print(response.explanations)
            print("response.error_msg")
            print(response.error_msg)
        else:
            print("Invalid method!")
            exit(1)

    except Exception as e:
        print("Exception")
        print(e)
        exit(1)
