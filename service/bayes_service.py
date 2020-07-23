import sys
import logging

import grpc
import concurrent.futures as futures

import service.common
import bayes
from bayes.utils import bayesInitialize
from bayes.utils import query
from bayes.utils import get_evidence_and_outvars
from bayes.utils import get_var_positions
from bayes.utils import get_var_val_positions
import os
import pickle
import pomegranate
import service.service_spec.bayesian_pb2

# Importing the generated codes from buildproto.sh
import service.service_spec.bayesian_pb2_grpc as grpc_bt_grpc
from service.service_spec.bayesian_pb2 import Answer

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

  def __init__(self,path="./nets"):
    self.baked_path = path+"_baked.p"
    self.spec_path = path+"_spec.p"
    self.error = False
    
    
    if os.path.isfile(self.baked_path) and os.path.isfile(self.spec_path):
        with open(self.baked_path, "rb") as f:
            try:
                self.baked  =  pickle.load(f)
            except Exception as e:
                print(e)
                self.baked = {}
                self.error = True
        if not self.error:
          with open(self.spec_path, "rb") as f:
              try:
                  self.spec  =  pickle.load(f)
              except Exception as e:
                  print(e)
                  self.spec = {}
        else:
          self.spec ={}
    else:
      self.baked ={}
      self.spec ={}
      
    log.debug("BayesServicer created")
    
  def getUniqueID(self):
    i=0
    while i in self.baked or i in self.spec:
      i += 1
    return i
    

  def StartNet(self, request, context):
    uniqueID = self.getUniqueID()
    self.spec[uniqueID]= request
    self.baked[uniqueID] = bayesInitialize(request)
    self.baked[uniqueID].bake()
    #todo: asyncronous return id before saving
    with open(self.baked_path, 'wb') as f:
      pickle.dump(self.baked, f)
      f.close()
    with open(self.spec_path, 'wb') as f:
      pickle.dump(self.spec, f)
      f.close()
    id = Id()
    id.id = uniqueID
    return id
  

  def AskNet(self, request, context):
    evidence,outvars = get_evidence_and_outvars(request.query, self.spec[request.id])
    answer_dict = query(self.baked[request.id], self.spec[request.id], evidence,outvars)
    answer = Answer()
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
    return(answer)

  def StatelessNet(self, request, context):
  
    net= bayesInitialize(request.bayesianNetwork)
    net.bake()
    evidence,outvars = get_evidence_and_outvars(request.query, request.bayesianNetwork)
    answer_dict = query(net, request.bayesianNetwork, evidence,outvars)
    answer = Answer()
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
    return(answer)
        


# The gRPC serve function.
#
# Params:
# max_workers: pool of threads to execute calls asynchronously
# port: gRPC server port
#
# Add all your classes to the server here.
# (from generated .py files by protobuf compiler)
def serve(max_workers=10, port=7777):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    grpc_bt_grpc.add_BayesNetServicer_to_server(BayesNetServicer(), server)
    server.add_insecure_port("[::]:{}".format(port))
    return server


if __name__ == "__main__":
    """
    Runs the gRPC server to communicate with the Snet Daemon.
    """
    parser = service.common.common_parser(__file__)
    args = parser.parse_args(sys.argv[1:])
    service.common.main_loop(serve, args)
