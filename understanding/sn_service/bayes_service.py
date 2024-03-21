import sys
#print("sys.path")
#print(sys.path)
import logging

import grpc
import uuid
import distutils.util
import concurrent.futures as futures
from google.protobuf import json_format


from sn_bayes.utils import bayesInitialize
from sn_bayes.utils import query
from sn_bayes.utils import internal_query
from sn_bayes.utils import parse_net 
from sn_bayes.utils import get_var_positions
from sn_bayes.utils import get_var_val_positions
from sn_bayes.utils import complexity_check
from sn_bayes.utils import explain
from sn_bayes.utils import explain_why_good
from sn_bayes.utils import explain_why_bad
from sn_bayes.utils import detect_anomalies
from sn_bayes.utils import readable

import os
import pickle
import pomegranate
import sn_service
from sn_service import service_spec
import sn_service.service_spec.bayesian_pb2
import copy
# Importing the generated codes from buildproto.sh

import sn_service.service_spec.bayesian_pb2_grpc as grpc_bt_grpc
from sn_service.service_spec.bayesian_pb2 import Answer
from sn_service.service_spec.bayesian_pb2 import BayesianNetwork
from sn_service.service_spec.bayesian_pb2 import Id

logging.basicConfig(level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
log = logging.getLogger("example_service")

"""
Bayesian net service, where you can either send a Bayesian net, and a query, and
have an answer without saving your net saved, or you can send a net to be saved,
and then query it with its unique id. 

"""


# Create a class to be added to the gRPC server
# derived from the protobuf codes.


class BayesNetServicer(grpc_bt_grpc.BayesNetServicer):

  def __init__(self,path="./nets",reset=False):
    self.baked = {}
    self.spec = {}
    self.spec_path = path+"_spec.p"
    

    if os.path.isfile(self.spec_path):
          with open(self.spec_path, "rb") as f:
              try:
                  self.spec_json  =  pickle.load(f)
              except Exception as e:
                  print(e)
                  self.spec_json = {}
    else:
      self.spec_json ={}
      
    for i,json_string in self.spec_json.items():
       self.spec[i] = json_format.Parse(json_string, BayesianNetwork())
       self.baked[i] = bayesInitialize(self.spec[i])
       self.baked[i].bake() 
      
    log.debug("BayesServicer created")
    
  def getUniqueID(self):
    #i=1
    #while i in self.baked or i in self.spec:
      #i += 1
    uniq = str(uuid.uuid4())
    #print ("uniq")
    #print (uniq)
    return uniq
    

  
  def EndNet(self, request, context):
    #print (request)
    #print (self.spec)
    answer = Answer()
    if request.id in self.spec:
      self.spec.pop(request.id)
      self.baked.pop(request.id)
      self.spec_json = {}
      #todo: return id asynchronously without waiting to save, or save if guaranteed upon error
      for i, message in self.spec.items():
        self.spec_json[i] = json_format.MessageToJson(message)
      with open(self.spec_path, 'wb') as f:
        pickle.dump(self.spec_json, f)
        f.close()
    else:
      answer.error_msg = "Net {} does not exist".format(request.id)
    return(answer)
	
	
  def StartNet(self, request, context):
    id = Id()
    not_too_complex,error_msg = complexity_check(request)
    if not_too_complex:
      uniqueID = self.getUniqueID()
      self.spec[uniqueID]= request
      self.baked[uniqueID] = bayesInitialize(request)
      self.baked[uniqueID].bake()
      self.spec_json = {}
      #todo: return id asynchronously without waiting to save, or save if guaranteed upon error
      for i, message in self.spec.items():
        self.spec_json[i] = json_format.MessageToJson(message)
      with open(self.spec_path, 'wb') as f:
        pickle.dump(self.spec_json, f)
        f.close()
      id.id = uniqueID
    else:
      id.error_msg = error_msg
    return id
  
  


  def AskNet(self, request, context):
    answer = Answer()
    if request.id in self.spec:
      bayesianNetwork = self.spec[request.id]
      evidence,outvars,explainvars, reverse_explain_list, reverse_evidence,anomaly_tuples, anomaly_params_dict,include_list,baseline,switch = parse_net(
              request.query, bayesianNetwork)
      #print  ("evidence,outvars,explainvars, reverse_explain_list, reverse_evidence,anomaly_tuples, anomaly_params_dict,include_list,baseline,switch")
      #print  (evidence)
      #print  (outvars)
      #print  (explainvars)
      #print  (reverse_explain_list)
      #print  (reverse_evidence)
      #print  (anomaly_tuples)
      #print  (anomaly_params_dict)
      #print  (include_list)
      #print  (baseline)
      #print  (switch)
      anomaly_out = {}
      answer_dict = {}
      if not switch or switch == "query" or switch == "internal_query":  
        anomaly_out = detect_anomalies(anomaly_tuples,bayesianNetwork,anomaly_params_dict)
        #print ("anomaly_out")
        #print (anomaly_out)
        evidence.update(anomaly_out['evidence'])   
        answer_dict =  internal_query(self.baked[request.id], self.spec[request.id], evidence
                        ) if switch is "internal_query" else query(self.baked[request.id], self.spec[request.id], evidence,outvars)
        #answer.error_msg = answer.error_msg + f",anomaly_out:{anomaly_out},answer_dict:{answer_dict}"
      explain_dict= explain(self.baked[request.id],self.spec[request.id],evidence,explainvars,reverse_explain_list, reverse_evidence,
              internal_query_result = baseline,include_list = include_list)if not switch or switch == "explain" else (  
              explain_why_bad(self.baked[request.id],self.spec[request.id],evidence,explainvars,
              internal_query_result = baseline,include_list = include_list)if switch == "explain_why_bad" else (  
              explain_why_good(self.baked[request.id],self.spec[request.id],evidence,explainvars,
              internal_query_result = baseline,include_list = include_list)if switch =="explain_why_good" else {}))  
      
      #print("readable(baseline)")
      #print(readable(bayesianNetwork,baseline))
      #print("explain_dict")
      #print(explain_dict)
      #answer.error_msg = answer.error_msg + f",explain_dict:{explain_dict}"
      var_positions = get_var_positions(self.spec[request.id])
      var_val_positions = get_var_val_positions(self.spec[request.id])

      for var, val_dict in answer_dict.items():
        var_answer = answer.varAnswers.add()
        if var in var_positions:
          var_num = var_positions[var]
          var_answer.var_num = var_num
          for val, prob in val_dict.items():
            val_num = var_val_positions[var][val]
            var_state = var_answer.varStates.add()
            var_state.state_num = val_num
            var_state.probability =prob
      for var, val_dict in explain_dict.items():
        var_answer = answer.explanations.add()
        if var in var_positions:
          var_num = var_positions[var]
          var_answer.var_num = var_num
          for var, val in val_dict.items():
            val_num = var_positions[var]
            var_state = var_answer.varStates.add()
            var_state.state_num = val_num
            var_state.probability =val
      if 'fitted' in anomaly_out:      
          for var, val_dict in anomaly_out['fitted'].items():
            if var in var_positions:
              var_answer = answer.anomalies.add()
              var_num = var_positions[var]
              var_answer.var_num = var_num
              for var, val in val_dict.items():
                var_state = var_answer.fitStates.add()
                var_state.fitted = var
                var_state.val =val
      if 'signal' in anomaly_out and 'anomalies' in anomaly_out:
          for var,val_dict in anomaly_out['anomalies'].items():
            if var in anomaly_out['signal'] and var in var_positions:
              var_answer1 = answer.signal_anomalies.add()
              var_num = var_positions[var]
              var_answer1.var_num = var_num
              #for tup in anomaly_out['signal'][var]:
                #var_state1 = var_answer1.signals.add()
                #var_state1.interval = tup[0]
                #var_state1.val = tup[1]
              for is_anomaly in anomaly_out['anomalies'][var]:
                var_state2 = var_answer1.anomalies.add()
                #var_state2.is_anomaly = bool(distutils.util.strtobool(is_anomaly))
                var_state2.is_anomaly = is_anomaly
    else:
      answer.error_msg = "Net {} does not exist".format(request.id)
    return(answer)

  def StatelessNet1(self, request, context):
    answer = Answer()
    not_too_complex,error_msg = complexity_check(request.bayesianNetwork)
    if not_too_complex:
      net= bayesInitialize(request.bayesianNetwork)
      net.bake()
      evidence,outvars,explainvars, reverse_explain_list, reverse_evidence,anomaly_tuples, anomaly_params_dict = parse_net(request.query, request.bayesianNetwork)
      #print("anomaly_params_dict")
      #print(anomaly_params_dict)
      #for var,params in anomaly_params_dict.items():
       # new_dict = {copy.deepcopy(var):copy.deepcopy(params)}
       # anomaly_out = detect_anomalies(anomaly_tuples,bayesianNetwork,new_dict)
        #print ("anomaly_out")
        #print (anomaly_out)
      anomaly_out = detect_anomalies(anomaly_tuples,request.bayesianNetwork,anomaly_params_dict)
      evidence.update(anomaly_out['evidence'])    
      answer_dict = query(net, request.bayesianNetwork, evidence,outvars)
      explain_dict= explain(net,request.bayesianNetwork,evidence,explainvars,reverse_explain_list, reverse_evidence)
      var_positions = get_var_positions(request.bayesianNetwork)
      var_val_positions = get_var_val_positions(request.bayesianNetwork)


      for var, val_dict in answer_dict.items():
        var_answer = answer.varAnswers.add()
        if var in var_positions:
          var_num = var_positions[var]
          var_answer.var_num = var_num
          for val, prob in val_dict.items():
            val_num = var_val_positions[var][val]
            var_state = var_answer.varStates.add()
            var_state.state_num = val_num
            var_state.probability =prob
      for var, val_dict in explain_dict.items():
        var_answer = answer.explanations.add()
        if var in var_positions:
          var_num = var_positions[var]
          var_answer.var_num = var_num
          for var, val in val_dict.items():
            val_num = var_positions[var]
            var_state = var_answer.varStates.add()
            var_state.state_num = val_num
            var_state.probability =val
      for var, val_dict in anomaly_out['fitted'].items():
        var_answer = answer.anomalies.add()
        if var in var_positions:
          var_num = var_positions[var]
          var_answer.var_num = var_num
          for var, val in val_dict.items():
            var_state = var_answer.fitStates.add()
            var_state.fitted = var
            var_state.val =val


    else:
      answer.error_msg = error_msg
        
    return(answer)
 	
  

  def StatelessNet(self, request, context):
    #print ("entered Statelessnet")
    answer = Answer()
    not_too_complex,error_msg = complexity_check(request.bayesianNetwork)
    #print(not_too_complex)
    if not_too_complex:
      bayesianNetwork= bayesInitialize(request.bayesianNetwork)
      bayesianNetwork.bake()
 
      evidence,outvars,explainvars, reverse_explain_list, reverse_evidence,anomaly_tuples, anomaly_params_dict,include_list,baseline,switch = parse_net(
              request.query, request.bayesianNetwork)
      #print  ("evidence,outvars,explainvars, reverse_explain_list, reverse_evidence,anomaly_tuples, anomaly_params_dict,include_list,baseline,switch")
      #print  (evidence)
      #print  (outvars)
      #print  (explainvars)
      #print  (reverse_explain_list)
      #print  (reverse_evidence)
      #print  (anomaly_tuples)
      #print  (anomaly_params_dict)
      #print  (include_list)
      #print  (baseline)
      #print  (switch)
      anomaly_out = {}
      answer_dict = {}
      if not switch or switch == "query" or switch == "internal_query":  
        anomaly_out = detect_anomalies(anomaly_tuples,request.bayesianNetwork,anomaly_params_dict)
        #print ("anomaly_out")
        #print (anomaly_out)
        evidence.update(anomaly_out['evidence'])   
        answer_dict =  internal_query(bayesianNetwork, request.bayesianNetwork, evidence
                        ) if switch is "internal_query" else query(bayesianNetwork, request.bayesianNetwork, evidence,outvars)
        #answer.error_msg = answer.error_msg + f",anomaly_out:{anomaly_out},answer_dict:{answer_dict}"
      explain_dict= explain(bayesianNetwork,request.bayesianNetwork,evidence,explainvars,reverse_explain_list, reverse_evidence,
              internal_query_result = baseline,include_list = include_list)if not switch or switch == "explain" else (  
              explain_why_bad(bayesianNetwork,request.bayesianNetwork,evidence,explainvars,
              internal_query_result = baseline,include_list = include_list)if switch == "explain_why_bad" else (  
              explain_why_good(bayesianNetwork,request.bayesianNetwork,evidence,explainvars,
              internal_query_result = baseline,include_list = include_list)if switch =="explain_why_good" else {}))  
      
      #print("explain_dict")
      #print(explain_dict)
      #answer.error_msg = answer.error_msg + f",explain_dict:{explain_dict}"
      var_positions = get_var_positions(request.bayesianNetwork)
      var_val_positions = get_var_val_positions(request.bayesianNetwork)

      for var, val_dict in answer_dict.items():
        var_answer = answer.varAnswers.add()
        if var in var_positions:
          var_num = var_positions[var]
          var_answer.var_num = var_num
          for val, prob in val_dict.items():
            val_num = var_val_positions[var][val]
            var_state = var_answer.varStates.add()
            var_state.state_num = val_num
            var_state.probability =prob
      for var, val_dict in explain_dict.items():
        var_answer = answer.explanations.add()
        if var in var_positions:
          var_num = var_positions[var]
          var_answer.var_num = var_num
          for var, val in val_dict.items():
            val_num = var_positions[var]
            var_state = var_answer.varStates.add()
            var_state.state_num = val_num
            var_state.probability =val
      if 'fitted' in anomaly_out:      
          for var, val_dict in anomaly_out['fitted'].items():
            if var in var_positions:
              var_answer = answer.anomalies.add()
              var_num = var_positions[var]
              var_answer.var_num = var_num
              for var, val in val_dict.items():
                var_state = var_answer.fitStates.add()
                var_state.fitted = var
                var_state.val =val
      if 'signal' in anomaly_out and 'anomalies' in anomaly_out:
          for var,val_dict in anomaly_out['anomalies'].items():
            if var in anomaly_out['signal'] and var in var_positions:
              var_answer1 = answer.signal_anomalies.add()
              var_num = var_positions[var]
              var_answer1.var_num = var_num
              #for tup in anomaly_out['signal'][var]:
                #var_state1 = var_answer1.signals.add()
                #var_state1.interval = tup[0]
                #var_state1.val = tup[1]
              for is_anomaly in anomaly_out['anomalies'][var]:
                var_state2 = var_answer1.anomalies.add()
                #var_state2.is_anomaly = bool(distutils.util.strtobool(is_anomaly))
                var_state2.is_anomaly = is_anomaly

    else:
      answer.error_msg = error_msg
        
    return(answer)
          


# The gRPC serve function.
#
# Params:
# max_workers: pool of threads to execute calls asynchronously
# port: gRPC server port
#
# Add all your classes to the server here.
# (from generated .py files by protobuf compiler)
# The gRPC serve function.
#
# Params:
# max_workers: pool of threads to execute calls asynchronously
# port: gRPC server port
#
# Add all your classes to the server here.
# (from generated .py files by protobuf compiler)
def serve(max_workers=10, port=7777):
    choptions = [('grpc.max_send_message_length', 1000000000),
                ('grpc.max_receive_message_length', 1000000000)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers), options=choptions)
    #server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    grpc_bt_grpc.add_BayesNetServicer_to_server(BayesNetServicer(), server)
    server.add_insecure_port("[::]:{}".format(port))
    return server


if __name__ == "__main__":
    """
    Runs the gRPC server to communicate with the Snet Daemon.
    """
    parser = sn_service.common.common_parser(__file__)
    args = parser.parse_args(sys.argv[1:])
    sn_service.common.main_loop(serve, args)
