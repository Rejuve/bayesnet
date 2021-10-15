import sys
import grpc
import sn_bayes
from sn_bayes.utils import create_query
import pandas as pd
import pickle
from os.path import exists
from sn_bayes.utils import readable

	

# import the generated classes
import sn_service.service_spec.bayesian_pb2_grpc as grpc_bayes_grpc
import sn_service.service_spec.bayesian_pb2
from sn_service.service_spec.bayesian_pb2 import BayesianNetworkQuery
from sn_service.service_spec.bayesian_pb2 import QueryId
from sn_service.service_spec.bayesian_pb2 import Id

from sn_service import registry
from sn_bayes import longevity_bayes
from sn_bayes import covid_bayes



if __name__ == "__main__":

    try:
        test_flag = False
        if len(sys.argv) == 2:
            if sys.argv[1] == "auto":
                test_flag = True

        endpoint = input("Endpoint (localhost:{}): ".format(registry["bayes_service"]["grpc"])) if not test_flag else ""
        if endpoint == "":
            endpoint = "localhost:{}".format(registry["bayes_service"]["grpc"])
        #bayesianNetwork,outstr = covid_bayes.covid_bayes()a
        if exists("bayesianNetwork.pkl"):
            infile = open("bayesianNetwork.pkl",'rb')
            bayesianNetwork = pickle.load(infile)
            infile.close()
        else:
            bayesianNetwork,outstr = longevity_bayes.longevity_bayes()
        evidence = {}
        evidence["age"]= "elderly"
        evidence["diabetes"]= "diabetes"
        #outvars= ["social_distancing", "social_distancing_binary","emergency_treatment","covid_risk","covid_risk_binary","covid_severity","covid_severity_binary"]
        #explainvars= ["social_distancing", "social_distancing_binary","emergency_treatment","covid_risk","covid_risk_binary","covid_severity","covid_severity_binary"]
        #reverse_explainvars = ["social_distancing", "social_distancing_binary"]
        reverse_explainvars = []
        outvars = ["hallmark_1_genomic_instability","hallmark_2_telomere_attrition","hallmark_3_epigenetic_alterations","hallmark_4_loss_of_proteostasis",
                "hallmark_5_deregulated_nutrient_sensing","hallmark_6_mitochondrial_dysfunction","hallmark_7_cellular_senescence","hallmark_8_stem_cell_exhaustion",
                "hallmark_9_altered_intercellular_communication","hallmark_10_extracellular_matrix_dysfunction","poor_diet",
                "poor_diet_flag","poor_sleep","psychological_disorders","obesity","lack_of_exercise","poor_diet_quantity","smoking"]
        explainvars=outvars
        include_list = ["heart_rate_variability_anomaly","oxygen_anomaly","lack_of_exercise","uv_exposure","blood_age_indicators",
                "poor_sleep","inflammation_from_behavior","poor_diet","smoking","frailty_signals","cancer","frailty","liver_disorders",
                "cardiovascular_disease","inactivated_sirtuins","inflammation","sarcopenia","comorbidities","general_aging_signs",
                "blood_metabolism_disorder_indicators","obesity","hypertension","diabetes","metabolic_disease","gender"]
        timeseries = []
        oxygen = {}
        timeseries.append(oxygen)
        oxygen["var"] = "steps_anomaly"
        timevals = []
        oxygen["timevals"] = timevals

        heart_rate_df = pd.read_csv(f'./data/sleep-accel/heart_rate/1066528_heartrate.txt')
        firstrow = None
        lastrow = None
        for index, row in heart_rate_df.iterrows():
            if firstrow is None:
                firstrow= row[0]
            thisrow = row[0]-lastrow if lastrow is not None else row[0]-firstrow
            lastrow = row[0]
            reading = {}
            reading["val"] = row[1]
            reading["interval"] = thisrow
            timevals.append(reading)

        print("Creating query")    
        query1 = create_query(bayesianNetwork,evidence,outvars,explainvars,reverse_explainvars,[],timeseries,include_list=include_list,switch="internal_query")


        #grpc_method = input("Method (stateless|statefull): ") if not test_flag else "statefull"
        grpc_method = "statefull"
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
            #print("response.anomalies")
            #print(response.anomalies)
            print("response.error_msg")
            print(response.error_msg)
            id_num = Id()
            id_num.id = queryId.id
            response = stub.EndNet(id_num)
        elif grpc_method == "statefull":
            print ("Calling StartNet")
            response = stub.StartNet(bayesianNetwork)
            print("response.id")
            print(response.id)
            print("response.error_msg")
            print(response.error_msg)
            queryId = QueryId()
            queryId.id = response.id
            queryId.query.CopyFrom(query1)
            response = stub.AskNet(queryId)
            print("response.varAnswers")
            print(response.varAnswers)
            print("response.explanations")
            print(response.explanations)
            #print("response.anomalies")
            #print(response.anomalies)
            print("response.error_msg")
            print(response.error_msg)
            baseline = response
            query2= create_query(bayesianNetwork,evidence,outvars,explainvars,reverse_explainvars,[],
                timeseries,include_list=include_list,baseline=baseline,switch="explain_why_bad")
            #print("query2")
            #print(query2)
            queryId.query.CopyFrom(query2)
            response = stub.AskNet(queryId)
            print("response.varAnswers")
            print(response.varAnswers)
            print("response.explanations")
            print(response.explanations)
            #print("response.anomalies")
            #print(response.anomalies)
            print("response.error_msg")
            print(response.error_msg)
            query3= create_query(bayesianNetwork,evidence,outvars,explainvars,reverse_explainvars,[],
                timeseries,include_list=include_list,baseline=baseline,switch="explain_why_good")
            #print("query3")
            #print(query3)
            queryId.query.CopyFrom(query3)
            response = stub.AskNet(queryId)
            print("response.varAnswers")
            print(response.varAnswers)
            print("response.explanations")
            print(response.explanations)
            #print("response.anomalies")
            #print(response.anomalies)
            print("response.error_msg")
            print(response.error_msg)



            id_num = Id()
            id_num.id = queryId.id
            response = stub.EndNet(id_num)
        else:
            print("Invalid method!")
            exit(1)

    except Exception as e:
        print("Exception")
        print(e)
        exit(1)
