from pomegranate import DiscreteDistribution
from pomegranate import BayesianNetwork
from pomegranate import Node
from pomegranate import ConditionalProbabilityTable
import json
import copy
import pandas as pd
import sn_service.service_spec.bayesian_pb2
from sn_service.service_spec.bayesian_pb2 import Query
import itertools
import typing
import numpy as np
from dateutil.parser import parse

T = typing.TypeVar("T")

class OrderedSet(typing.MutableSet[T]):
    """A set that preserves insertion order by internally using a dict."""

    def __init__(self, iterable: typing.Iterator[T]):
        self._d = dict.fromkeys(iterable)

    def add(self, x: T) -> None:
        self._d[x] = None

    def discard(self, x: T) -> None:
        self._d.pop(x, None)

    def __contains__(self, x: object) -> bool:
        return self._d.__contains__(x)

    def __len__(self) -> int:
        return self._d.__len__()

    def __iter__(self) -> typing.Iterator[T]:
        return self._d.__iter__()

    def __str__(self):
        return f"{{{', '.join(str(i) for i in self)}}}"

    def __repr__(self):
        return f"<OrderedSet {self}>"

def var_deps(bayesianNetwork):
    var_deps = {}
    for dist in bayesianNetwork.discreteDistributions:
        var_deps[dist.name] = []
    for table in bayesianNetwork.conditionalProbabilityTables:
        #print ("table: {}".format(table.name))
        var_deps[table.name]= []
        for var in table.randomVariables:
            #print(var.name)
            var_deps[table.name].append(var.name)
    return var_deps


def fillcols(var_dict):
    var_deps =copy.deepcopy(var_dict)
    #go through the dict and create a lists of lists , 
    #where a var goes in the list only if all of the variable upon which 
    #it depends are in the previous lists.
    tree_list = []
    initial_len = len(var_deps)
    final_len=0
    while len(var_deps)>  0 and final_len < initial_len:
        next_level = []
        deletes =[]
        for var,deplist in var_deps.items():
            all_found = True
            for d in deplist:
                found = False
                for l in tree_list:
                    if d in l:
                        found = True
                if not found:
                    all_found = False
            if all_found:
                deletes.append(var)
                next_level.append(var)
        for delete in deletes:
            var_deps.pop(delete)
        final_len = len(var_deps)
        tree_list.append(next_level)
    return(tree_list)    

def make_tree(bayesianNetwork):
    variable_dependencies = var_deps(bayesianNetwork)
    #print(variable_dependencies)
    tree = fillcols(variable_dependencies)
    #print(tree)
    newtree = []
    for ply in tree:
        newl=[]
        for v in ply: 
            newstr = v + "("
            #print(v)
            deps = variable_dependencies[v]
            for d in deps:
                newstr += d
                newstr += ","
            newstr = newstr[:-1]+ ")"
            newl.append(newstr)
        newtree.append(newl)
    df_dict ={}
    for i,l in enumerate(newtree):
        key = "level"+ str(i)
        df_dict[key] = l  
    df = pd.DataFrame.from_dict(df_dict, orient='index').T
    return df

def complexity_check(bayesianNetwork,
#todo: check obscenity                
        max_size_in_bytes = 256000000,             
        allowed_number_nodes = 5000,
        allowed_number_variables=9, allowed_number_variable_values= 15):

        passes = True
        messages = []
        size = bayesianNetwork.ByteSize()
        if size > max_size_in_bytes:
                passes = False
                messages.append("This net's size is {0} bytes while max size is {1} bytes".format(size,max_size_in_bytes))
        else:
                var_val_positions = get_var_val_positions(bayesianNetwork)
                num_nodes = len(var_val_positions)
                if num_nodes > allowed_number_nodes:
                        passes = False
                        messages.append("This net's number of nodes is {0} while allowed number is {1}".format(num_nodes,allowed_number_nodes))

                lenlist = [len(l) for l in list(var_val_positions.values())]
                maxvarval=  max(lenlist) if len(lenlist) > 0  else 0
                if maxvarval > allowed_number_variable_values:
                        passes = False
                        messages.append("This net's max number of variable values is {0} while allowed number is {1}".format(maxvarval,allowed_number_variable_values))
                row_test = True        
                for table in bayesianNetwork.conditionalProbabilityTables:
                        numvars = len(table.conditionalProbabilityRows[0].randomVariableValues)-1
                        if numvars > allowed_number_variables:
                                passes = False
                                messages.append("Variable {0} has {1} dependancies while the allowed number is {2}".format(table.name, numvars,allowed_number_variables))
        errors = '\n'.join(messages)
        return (passes,errors)

        

def get_var_positions(bayesianNetwork):
        var_positions = {}
        check_for_repeats= set()
        for i,dist in enumerate(bayesianNetwork.discreteDistributions):
                var_positions[dist.name]=i
                #print ("dist.name") 
                #print (dist.name)
                #print ("i")
                #print (i)
                if dist.name in check_for_repeats:
                    print(f"double instance of {dist.name}") 
                else:
                    check_for_repeats.add(dist.name)
        start = len(var_positions)
        #print ("start")
        #print(start)
        for j,table in enumerate(bayesianNetwork.conditionalProbabilityTables):
                var_positions[table.name] = j+ start
                #print("table.name")
                #print(table.name)
                #print("j")
                #print(j)
                if table.name in check_for_repeats:
                    print(f"double instance of {table.name}") 
                else:
                    check_for_repeats.add(table.name)

        return var_positions



def get_var_val_positions(bayesianNetwork):
        var_val_positions = {}
        for dist in bayesianNetwork.discreteDistributions:
                var_val_positions[dist.name] = {}
                for pos,var in enumerate(dist.variables):
                        var_val_positions[dist.name][var.name] = pos
        for j,table in enumerate(bayesianNetwork.conditionalProbabilityTables):
                var_val_positions[table.name] ={}
                for pos,var in enumerate(table.outvars):
                        var_val_positions[table.name][var.name] = pos
        return var_val_positions



def get_internal_var_val_positions(bayesianNetwork):
        var_val_positions = {}
        for j,table in enumerate(bayesianNetwork.conditionalProbabilityTables):
                var_val_positions[table.name] ={}
                for pos,var in enumerate(table.outvars):
                        var_val_positions[table.name][var.name] = pos
        return var_val_positions


def get_var_names(bayesianNetwork):
        var_names = {}
        for i,dist in enumerate(bayesianNetwork.discreteDistributions):
                var_names[i]=dist.name
        start = len(var_names)
        for j,table in enumerate(bayesianNetwork.conditionalProbabilityTables):
                var_names[j+ start] = table.name
        return var_names

def get_var_val_names(bayesianNetwork):
        var_val_names = {}
        for dist in bayesianNetwork.discreteDistributions:
                var_val_names[dist.name]={}
                for pos,var in enumerate(dist.variables):
                        var_val_names[dist.name][pos] = var.name
        for j,table in enumerate(bayesianNetwork.conditionalProbabilityTables):
                var_val_names[table.name] ={}
                for pos,var in enumerate(table.outvars):
                        var_val_names[table.name][pos] = var.name
        return var_val_names

def parse_net(query, bayesianNetwork):
        var_val_names = get_var_val_names(bayesianNetwork)
        var_names = get_var_names(bayesianNetwork)
        evidence_dict = {}
        anomaly_tuples = {}
        for e in query.evidence:
            if e.var_num in var_names and var_names[e.var_num] in var_val_names and e.response in var_val_names[ var_names[e.var_num]]:
                var_name = var_names[e.var_num]
                var_val_name = var_val_names[var_name][e.response]
                evidence_dict[var_name] = var_val_name 
        outvar_list =[var_names[o.var_num] for o in query.outvars if o.var_num in var_names]
        explainvars =[var_names[o.var_num] for o in query.explainvars if o.var_num in var_names]
        reverse_explain_list =[var_names[o.var_num] for o in query.reverse_explainvars if o.var_num in var_names]
        reverse_evidence =[var_names[o.var_num] for o in query.reverse_evidence if o.var_num in var_names]
        for s in query.timeseries:
            anomaly_tuples[var_names[s.var_num]] = [(t.val,t.interval)for t in s.timevals]
        anomaly_params_dict = {}
        for o in bayesianNetwork.anomalies:
            anomaly_params_dict[o.varName]= {}
            anomaly_params_dict[o.varName]['low'] = o.low
            anomaly_params_dict[o.varName]['high'] = o.high
            anomaly_params_dict[o.varName]['low_percent'] = o.low_percent
            anomaly_params_dict[o.varName]['high_percent'] = o.high_percent
            anomaly_params_dict[o.varName]['is_all']= o.is_all
            anomaly_params_dict[o.varName]['n_steps']= o.n_steps
            anomaly_params_dict[o.varName]['step_size'] = o.step_size
            anomaly_params_dict[o.varName]['c'] = o.c
            anomaly_params_dict[o.varName]['n'] = o.n
            anomaly_params_dict[o.varName]['side'] = o.side
            anomaly_params_dict[o.varName]['window'] = o.window
            anomaly_params_dict[o.varName]['detectors'] = []
            for d in o.detectors:
                anomaly_params_dict[o.varName]['detectors'].append(d.name)
        switch=query.switch
        baseline= readable(bayesianNetwork,query.baseline) if query.baseline else None
        include_list = [var_names[o.var_num] for o in query.include_list if o.var_num in var_names]
        return(evidence_dict, outvar_list, explainvars, reverse_explain_list, reverse_evidence,anomaly_tuples,anomaly_params_dict,include_list,baseline,switch)

from adtk.data import validate_series

def quan(s,percentile):
    sr = s.quantile(percentile)
    return sr[0]

def std(s):
    sr = s.std()
    return sr

def iqr(s,c):
        sr = s.quantile(0.25)
        q1 = sr[0]
        sr = s.quantile(0.75)
        q3=sr[0]
        iqr = q3 - q1

        abs_low = (
            (
                q1
                - iqr
                * (c if (not isinstance(c, tuple)) else c[0])
            )
            if (
                (c if (not isinstance(c, tuple)) else c[0])
                is not None
            )
            else -float("inf")
        )
        abs_high = (
            q3
            + iqr * (c if (not isinstance(c, tuple)) else c[1])
            if (
                (c if (not isinstance(c, tuple)) else c[1])
                is not None
            )
            else float("inf")
        )
        #print("s.max()")
        #print (s.max())
        #print("s.min()")
        #print(s.min())
        if abs_high > s.max()[0] and abs_low < s.min()[0]:
            print ("no iqr anomalies")
        return(abs_low,abs_high)


def detect_anomalies(anomaly_tuples,bayesianNetwork,anomaly_params):
        evidence = {}
        anomaly_dict = {}
        signal_dict ={}
        combined_signals={}
        fitted={}
        s_dict = {}
        anomaly_out = {}
        anomaly_out['signal'] = {}
        anomaly_out['anomalies']= {}
        anomaly_out['fitted'] = {}
        anomaly_out['evidence'] = {}
        var_val_names = get_var_val_names(bayesianNetwork)
        var_names = get_var_names(bayesianNetwork)
        df = pd.DataFrame(columns=['time','value'])
        combined_df = pd.DataFrame(columns = ['time','value'])
        for var, time_tuples in anomaly_tuples.items():
            anomaly_dict[var]={}
            combined_signals[var] ={}
            fitted[var] = {}
            last_interval = 1
            dti = pd.to_datetime('1/1/2018')
            for tup in time_tuples:
                val = float(tup[0])
                interval = float(tup[1])
                if interval == 0.0:
                    interval = last_interval
                last_interval = interval
                if interval is not None and val is not None:
                    dti += pd.Timedelta(f'{interval} seconds')
                    if dti is not pd.NaT: 
                        df = df.append({'time': dti, 'value':val }, ignore_index=True)
            if not df.empty:
                df=df.set_index('time')
                s = validate_series(df)
                if pd.NaT in s.index:
                    s = s.drop(pd.NaT)
                signal_dict[var]=s
                #print("s")
                #print(s)
                s_dict[var]=[]
                last_dti = None
                interval = 0
                for index, row in signal_dict[var].iterrows():
                    if last_dti is not None:
                        this_dti = index
                        diff = this_dti - last_dti
                        interval = float(diff.total_seconds())
                        #print ("interval")
                        #print (interval)
                    last_dti = index
                    s_dict[var].append ((interval,row['value']))      
                detector_set = set(anomaly_params[var]["detectors"])
                for detector in detector_set:
                    if detector == "AutoregressionAD":
                        try:
                            from adtk.detector import AutoregressionAD
                            autoregression_ad = AutoregressionAD(n_steps=anomaly_params[var]["n_steps"], 
                                    step_size=anomaly_params[var]["step_size"], c=anomaly_params[var]["c"])
                            anomaly_dict[var][detector]  = autoregression_ad.fit_detect(s)
                            if  "low" not in fitted[var]:
                                fitted[var]["low"],fitted[var]["high"] = iqr(s,anomaly_params[var]["c"])                            
                        except RuntimeError as e:
                            print(f'AutoregressionAD-{var} RuntimeError')
                            print(e)
                        except ValueError as e:
                            print(f'AutoregressionAD-{var} ValueError')
                            print(e)
                    elif detector == "LevelShiftAD":
                        try:
                            from adtk.detector import LevelShiftAD
                            ls_ad = LevelShiftAD(c=anomaly_params[var]["c"],
                                    side=anomaly_params[var]["side"],window=anomaly_params[var]["window"])
                            anomaly_dict[var][detector] = ls_ad.fit_detect(s)
                            if "low" not in fitted[var]:
                                fitted[var]["low"],fitted[var]["high"] = iqr(s,anomaly_params[var]["c"])                            
                        except RuntimeError as e:
                            print(f'LevelShiftAD-{var} RuntimeError')
                            print(e)
                        except ValueError as e:
                            print(f'LevelShiftAD-{var} ValueError')
                            print(e)

                    elif detector == "InterQuartileRangeAD":
                        try:
                            from adtk.detector import InterQuartileRangeAD
                            iqr_ad = InterQuartileRangeAD(c=anomaly_params[var]["c"])
                            anomaly_dict[var][detector] = iqr_ad.fit_detect(s)
                            if "low" not in fitted[var]:
                                fitted[var]["low"],fitted[var]["high"] = iqr(s,anomaly_params[var]["c"])                            
                        except RuntimeError as e:
                            print(f'InterQuartileRangeAD-{var} RuntimeError')
                            print(e)
                        except ValueError as e:
                            print(f'InterQuartileRangeAD-{var} ValueError')
                            print(e)


                    elif detector == "QuantileAD":
                        try:
                            from adtk.detector import QuantileAD
                            quantile_ad = QuantileAD(high=anomaly_params[var]['high_percent'], low=anomaly_params[var]['low_percent'])
                            anomaly_dict[var][detector] = quantile_ad.fit_detect(s)
                            fitted[var]['low_percent'] = quan(s,anomaly_params[var]['low_percent'])
                            fitted[var]['high_percent'] = quan(s,anomaly_params[var]['high_percent'])

                        except RuntimeError as e:
                            print(f'QuantileAD-{var}')
                            print(e)
                        except ValueError as e:
                            print(f'QuantileAD-{var}')
                            print(e)

                    elif detector == "ThresholdAD":          
                        try:
                            from adtk.detector import ThresholdAD
                            threshold_ad = ThresholdAD(high=anomaly_params[var]['high'], low=anomaly_params[var]['low'])
                            anomaly_dict[var][detector] = threshold_ad.detect(s)

                        except RuntimeError as e:
                            print(f'ThresholdAD-{var}')
                            print(e)
                        except ValueError as e:
                            print(f'ThresholdAD-{var}')
                            print(e)

                    elif detector == "VolatilityShiftAD":
                        try:
                            from adtk.detector import VolatilityShiftAD
                            volatility_shift_ad = VolatilityShiftAD(c=anomaly_params[var]['c'], side=anomaly_params[var]['side'],window=anomaly_params[var]['window'])
                            anomaly_dict[var][detector] = volatility_shift_ad.detect(s)
                            fitted[var]['std'] = std(s)

               
                        except RuntimeError as e:
                            print(f'VolatilityShiftAD-{var}')
                            print(e)
                        except ValueError as e:
                            print(f'VolatilityShiftAD-{var}')
                            print(e)



                firsttime = True
                for detector,df in anomaly_dict[var].items():
                    if firsttime:
                        combined_df = df
                        combined_df = combined_df.rename(columns={'value': detector})
                        firsttime = False
                    else:
                        combined_df[detector] = df['value']
                combined_df['value']=combined_df.all(1) if anomaly_params[var]['is_all'] else combined_df.any(1)

                is_anomalous = combined_df[['value']].tail(anomaly_params[var]["n"])['value'].any()
                evidence[var] = var_val_names[var][0] if is_anomalous else var_val_names[var][1]
                #print("combined_df")
                #print(combined_df)
                temp = combined_df[['value']].to_records()
                #print("temp")
                #print(temp)
                anomaly_out['anomalies'][var]= [tup[1] for tup  in temp]
                #anomaly_out['signal'][var] = list(signal_dict[var].to_records())
                anomaly_out['signal'][var]=s_dict[var]
                #print (f"anomaly_out['anomalies'][{var}][0]:")
                #print (anomaly_out['anomalies'][var][0])
                anomaly_out['fitted'][var] = fitted[var]
                anomaly_out['evidence'][var] = evidence[var]
        return (anomaly_out)


def readable(bayesianNetwork,response):

        var_val_names = get_var_val_names(bayesianNetwork)
        var_names = get_var_names(bayesianNetwork)
        readable = {}
        for answer in response.varAnswers:
            var = var_names[answer.var_num]
            readable[var]={}
            #print("answer")
            #print(answer)
            for state in answer.varStates:
                readable[var][var_val_names[var][state.state_num]]= state.probability
        
        #print ("readable")
        #print(readable)
        return readable
                 
def create_query (bayesianNetwork,evidence_dict,outvar_list,explainvars=[],
        reverse_explainvars=[],reverse_evidence=[],timeseries = [], include_list = [], baseline = None, switch= None):
        #create a query for the test service

        #print("evidence_dict")
        #print(evidence_dict)
        #print("outvar_list")
        #print(outvar_list)
        query = Query()
        query.switch = switch
        if baseline:
                query.baseline.CopyFrom( baseline)


        var_val_positions = get_var_val_positions(bayesianNetwork)
        #print ("var_val_positions")
        #print (var_val_positions)
        var_positions = get_var_positions(bayesianNetwork)
        #print ("var_positions")
        #print (var_positions)
        for v in include_list:
                if v in var_positions:
                        outvar = query.include_list.add()
                        outvar.var_num = var_positions[v]

                        #print ("outvar")
        for k,v in evidence_dict.items():
                if k in var_positions and k in var_val_positions and v in var_val_positions[k]:
                        evidence= query.evidence.add()
                        evidence.var_num = var_positions[k]
                        evidence.response = var_val_positions[k][v]
                        #print("evidence")
                        #print(evidence)
        for v in outvar_list:
                if v in var_positions:
                        outvar = query.outvars.add()
                        outvar.var_num = var_positions[v]
                        #print ("outvar")
                        #print(outvar)
        for v in explainvars:
                if v in var_positions:
                        explainvar = query.explainvars.add()
                        explainvar.var_num = var_positions[v]
        for v in reverse_explainvars:
                if v in var_positions:
                        explainvar = query.reverse_explainvars.add()
                        explainvar.var_num = var_positions[v]
        for v in reverse_evidence:
                if v in var_positions:
                        evidencevar = query.reverse_evidence.add()
                        evidencevar.var_num = var_positions[v]
        for t in timeseries:
            if t["var"] in var_positions:
                    time = query.timeseries.add()
                    time.var_num = var_positions[t["var"]]
                    for q in t["timevals"]:
                        timeseries = time.timevals.add()
                        timeseries.val = q["val"]
                        timeseries.interval = q["interval"]

                    
        return query
                        


def batch_query(baked_net, netspec, evidence_list,out_var_list):
        answer_list = []
        var_positions = get_var_positions(netspec)
        #print ('evidence_list')
        #print (evidence_list)
        evidence_list = list(evidence_list)
        description = baked_net.predict_proba(evidence_list,max_iterations=1,check_input = False, n_jobs=1)
        #print ("description")
        #print (description)
        for i,evidence in enumerate(evidence_list):
                answer = {}
                for dist_name in out_var_list:
                        try:
                                answer[dist_name] = (json.loads(description[i][var_positions[dist_name]].to_json()))['parameters'][0]
                        except AttributeError as e:
                                #print(dist_name)
                                #print(e)
                                pass
                answer_list.append(answer)
        return answer_list



def query(baked_net, netspec, evidence,out_var_list):
        answer = {}
        var_positions = get_var_positions(netspec)
        description = baked_net.predict_proba(evidence)
        for dist_name in out_var_list:
                try:
                        answer[dist_name] = (json.loads(description[var_positions[dist_name]].to_json()))['parameters'][0]
                except AttributeError as e:
                        #print(dist_name)
                        #print(e)
                        pass
        return answer

       

def explain_why_bad(baked_net, netspec, evidence,explain_list,internal_query_result=None, include_list = []):
    #print (internal_query_result)
    return explain(baked_net, netspec,evidence,explain_list, internal_query_result=internal_query_result, include_list = include_list)

def explain_why_good(baked_net, netspec, evidence, explain_list, internal_query_result = None, include_list = []):
    adict = dictVarsAndValues(netspec,{})
    return explain(baked_net, netspec,evidence, explain_list, reverse_explain_list = explain_list, reverse_evidence = adict.keys(),
            internal_query_result=internal_query_result,include_list = include_list)

def internal_query(baked_net, netspec,evidence):
        internal_var_val_positions = get_internal_var_val_positions(netspec)
        exclusion_list = [var for var, val in internal_var_val_positions.items()]
        result = query(baked_net,netspec,evidence,exclusion_list)
        return result
    
def explain(baked_net, netspec, evidence,explain_list, reverse_explain_list = [], reverse_evidence = [] , internal_query_result=None, include_list = []):
        #explain_list lists output variables to tell what input variable would make them less likely (for example covid severity)
        #reverse_explain_list tells which of those out vars to explain more likely rather than less likely  (for example social distancing)
        #reverse_evidence_list tells which of the evidence to explain should perturb one val to the left rather than the right (the default)
     #   
        #first make a list of all the pertubations to make
        #print  ("in explain, evidence,explain_list, reverse_explain_list, reverse_evidence")
        #print  (evidence)
        #print  (explain_list)
        #print  (reverse_explain_list)
        #print  (reverse_evidence)
        #print ("In explain, internal_query_result")
        #print(internal_query_result)
        #print ("include_list")
        #print(include_list)
        evidence_perturbations = {}
        var_val_positions = get_var_val_positions(netspec)
        var_val_names = get_var_val_names(netspec)
        for var,val in evidence.items():
                new_pos = None
                old_pos = var_val_positions[var][val]
                if var in reverse_evidence and old_pos > 0:
                        new_pos = old_pos-1
                elif var not in reverse_evidence and old_pos < len(var_val_positions[var])-1: 
                        new_pos = old_pos+ 1
                if new_pos is not None and (len(include_list) == 0 or var in include_list):
                        new_evidence = copy.deepcopy(evidence)
                        new_val = var_val_names[var][new_pos]
                        new_evidence[var]=new_val
                        evidence_perturbations[var]= new_evidence
                        
        # add in the internal nodes that arent the input nodes
        result = internal_query(baked_net,netspec,evidence) if internal_query_result == None else internal_query_result
        #print ("result")
        #print (result)
        internal_winners = {}
        for key,val_dict in result.items():
                winner = max(val_dict,key=val_dict.get)
                winner_val = val_dict[winner]
                internal_winners[key] = (winner,winner_val)
        #print('internal_winners')
        #print(internal_winners)
        internal_evidence = {k:tup[0] for k,tup in internal_winners.items() }
        #print ('internal_evidence')
        #print(internal_evidence)
        
        more_evidence = {}
        for var, val in internal_evidence.items():
                
                new_pos = None
                old_pos = var_val_positions[var][val]
                if var in reverse_evidence and old_pos > 0:
                        new_pos = old_pos-1
                elif var not in reverse_evidence and old_pos < len(var_val_positions[var])-1: 
                        new_pos = old_pos+ 1

                if new_pos is not None and (len(include_list) == 0 or var in include_list):
                        new_val = var_val_names[var][new_pos]
                        more_evidence[var] = copy.deepcopy(evidence)        
                        more_evidence[var].update({var:new_val})
        #print('more_evidence')
        #print(more_evidence)
        evidence_perturbations.update(more_evidence)
        #print ("evidence_perturbations")
        #print (evidence_perturbations)
        #next run each, obtaining the values of vars to be explained.  
        #find the difference between these outputvalues and the output values from the original evidence input
        #result = query(baked_net,netspec,evidence,explain_list)
        #print ("result (without changes)")
        #print(result)
        before_change = {}
        explanation = {}
        for key,val_dict in result.items():
                if key in explain_list:
                    winner = max(val_dict,key=val_dict.get)
                    winner_val = val_dict[winner]
                    before_change[key] = (winner,winner_val)
                    explanation[key] = {}
        #print("reverse_explain_list")
        #print(reverse_explain_list)
        #for explaining_var, evidence in evidence_perturbations.items():
                #print("explaining_var")
                #print(explaining_var)
                #print("evidence")
                #print(evidence)
        evidence = evidence_perturbations.values()
        after_change_list = batch_query(baked_net,netspec,evidence,explain_list)
        for explaining_var,after_change in zip(evidence_perturbations.keys(),after_change_list):
                #print("result")
                #print(result)
                for key in explain_list:
                        if key in after_change:
                                diff = before_change[key][1] - after_change[key][before_change[key][0]]
                                explanation[key][explaining_var] = diff
        return explanation
        
                

def make_nmap(): 
        nmap = {}
        cutoff = {}
        for a in range(2,10):
                if not a in cutoff:
                        cutoff[a] ={}
                val = 1/a
                for j in range (0,a):
                        cutoff[a][j] = j*val
        #print("cutoff")
        #print(cutoff)
        for a in range(2,10):
                if not a in nmap:
                        nmap[a]={}
                for b in range(2,10):
                        if not b in nmap[a]:
                                nmap[a][b] = {}
                        for i in range (0,a):
                                lowercutoffi = cutoff[a][i]
                                uppercutoffi = cutoff[a][i+1] if i+1 < a else 1
                                k=0
                                #print("len(cutoff[b])")
                                #print(len(cutoff[b]))
                                
                                while k< len(cutoff[b]) and lowercutoffi >= cutoff [b][k]:
                                        #print("cutoff [b][k]")
                                        #print(cutoff [b][k])
                                        k += 1
                                bucketnumLower = k-1
                                k=0
                                #print("len(cutoff[b])")
                                #print(len(cutoff[b]))
                                while k< len(cutoff[b]) and uppercutoffi > cutoff [b][k]:
                                        #print("cutoff [b][k]")
                                        #print(cutoff [b][k])
                                        k += 1
                                bucketnumUpper = k
                                #print("lowercutoffi")
                                #print(lowercutoffi)
                                #print("uppercutoffi")
                                #print(uppercutoffi)
                                #print("bucketnumLower")
                                #print(bucketnumLower)
                                #print("bucketnumUpper")
                                #print(bucketnumUpper)
                                coveredBuckets = [s for s in range(bucketnumLower, bucketnumUpper)]
                                nmap[a][b][i] = set(coveredBuckets)
                                
        return(nmap)
         
        

def dictVarsAndValues(bayesianNetwork,cpt):
        varsAndValues = {}
        for dist in bayesianNetwork.discreteDistributions:
                varsAndValues [dist.name]= []
                for var in dist.variables:
                        varsAndValues[dist.name].append(var.name)
        for dist in bayesianNetwork.conditionalProbabilityTables:
                varsAndValues [dist.name]= []
                for var in dist.outvars:
                        varsAndValues[dist.name].append(var.name)
        for name,cpt_tuple in cpt.items():
                #print('name')
                #print(name)
                #print('cpt_tuple')
                #print(cpt_tuple)
                varsAndValues[name]= cpt_tuple[2]
        return varsAndValues

def any_of(bayesianNetwork, cpt, invars, outvars):
        #print (outvars)
        import itertools

        
        description = "{0} has the value of " + outvars[0] + " if "
        firsttime = True
        for var,vals in invars.items():
                phrase = "" if firsttime else ", OR "
                firsttime = False
                description = description + phrase + var + " has the value of "
                firsttime2 = True
                for val in vals:
                        phrase = "" if firsttime2 else " or " 
                        firsttime2 = False
                        description = description + phrase + val
        description = description + "; otherwise {0} has the value of " + outvars[1]+"."

        vdict = dictVarsAndValues(bayesianNetwork, cpt)
        vlist = [vdict[v] for v in invars.keys()]
        cartesian = list(itertools.product(*vlist))
        klist = [a for a in invars.values()]
        keylist = invars.keys()
        cpt_rows = []
        for c in cartesian:
                qany=False
                i=0
                while (not qany) and i < len(klist):
                        vset = klist[i]
                        if c[i] in vset:
                                qany = True
                        i += 1
                for i,o in enumerate(outvars):
                        cpt_row = []
                        cpt_row.extend(c)
                        cpt_row.append(o)
                        val = 1.0 if (i == 0 and qany) or (i == 1 and not qany) else 0.0
                        cpt_row.append(val)
                        cpt_rows.append(cpt_row)
        return (cpt_rows,keylist, outvars,description)



def all_of(bayesianNetwork, cpt, invars, outvars):
        #print (outvars)
        import itertools

        
        description = "{0} has the value of " + outvars[0] + " if "
        firsttime = True
        for var,vals in invars.items():
                phrase = "" if firsttime else ", AND "
                firsttime = False
                description = description + phrase + var + " has the value of "
                firsttime2 = True
                for val in vals:
                        phrase = "" if firsttime2 else " or " 
                        firsttime2 = False
                        description = description + phrase + val
        description = description + "; otherwise {0} has the value of " + outvars[1]+"."

        vdict = dictVarsAndValues(bayesianNetwork, cpt)
        vlist = [vdict[v] for v in invars.keys()]
        cartesian = list(itertools.product(*vlist))
        klist = [a for a in invars.values()]
        keylist = invars.keys()
        cpt_rows = []
        for c in cartesian:
                qall=True
                for i,vset in enumerate(klist):
                                if c[i] not in vset:
                                        qall = False
                for i,o in enumerate(outvars):
                        cpt_row = []
                        cpt_row.extend(c)
                        cpt_row.append(o)
                        val = 1.0 if (i == 0 and qall) or (i == 1 and not qall) else 0.0
                        cpt_row.append(val)
                        cpt_rows.append(cpt_row)

        return (cpt_rows,keylist,outvars, description)


def avg(bayesianNetwork, cpt, invars, outvars):
        clause = ""        
        description = ""
        veryfirsttime = True
        for outvar in outvars:
                description = description + "{0} has the value of " + outvar + " if the values of "
                if veryfirsttime:
                        firsttime = True
                        for var in invars:
                                phrase = "" if firsttime else " and "
                                firsttime = False
                                clause = clause + phrase + var 
                level = "" if veryfirsttime else "next "
                veryfirsttime = False
                description = description + clause + " average to the " + level + "highest level of risk. "


    
    #print (outvars)
        import itertools
        nmap = make_nmap()
        #print(nmap)
        vdict = dictVarsAndValues(bayesianNetwork, cpt)
        vlist = [vdict[v] for v in invars]
        cartesian = list(itertools.product(*vlist))
        #klist = [a for a in invars.values()]
        keylist = invars
        cpt_rows = []
        num_outvars = len(outvars)
        for c in cartesian:
                bins = {}
                #for i,vset in enumerate(klist):
                for i,varlist in enumerate(vlist):
                        for j , slot in enumerate(varlist):
                                if slot == c[i]:
                                        var_number = j
                        num_invars = len(varlist)
                        addset = nmap[num_invars][num_outvars][var_number]
                        incr = 1./len(addset)
                        for p in addset:
                                if p not in bins:
                                        bins[p] = 0
                                bins[p]+= incr
                #print("c")
                #print(c)
                #print("bins")
                #print(bins)

                area = sum(bins.values())
                mean = area/2.
                cummu = 0. 
                for k,v in bins.items():
                        cummu +=v
                        if cummu > mean:
                                winner = k
                                break

                for i,o in enumerate(outvars):
                        cpt_row = []
                        cpt_row.extend(c)
                        cpt_row.append(o)
                        #val = 1.0 if (winner == i) else 0.0)
                        val = bins[i]/area if i in bins else 0.0 #not in winner take all version
                        cpt_row.append(val)
                        cpt_rows.append(cpt_row)

        return (cpt_rows,keylist,outvars,description)




def if_then_else(bayesianNetwork, cpt, invars, outvars):
        #print (outvars)
        import itertools
 
        description = "" 
        firsttime = True
        for i, (var,vals) in enumerate(invars.items()):
                phrase = "" if firsttime else "; otherwise "
                description = description + phrase +"{0} has the value of " + outvars[i] + " if " + var + " has the value "
                firsttime = False
                firsttime2 = True
                for val in vals:
                        phrase = "" if firsttime2 else " or " 
                        firsttime2 = False
                        description = description + phrase + val
        description = description + "; otherwise {0} has the value of " + outvars[-1]+"."


        vdict = dictVarsAndValues(bayesianNetwork, cpt)
        vlist = [vdict[v] for v in invars.keys()]
        cartesian = list(itertools.product(*vlist))
        klist = [a for a in invars.values()]
        #print('cartesian')
        #print(cartesian)
        #print('klist')
        #print(klist)
        keylist = invars.keys()
        cpt_rows = [] 
        for c in cartesian:
                result = ""
                i=0
                while (result == "") and i < len(klist):
                        vset = klist[i]
                        if c[i] in vset:
                                result = outvars[i]
                        i += 1
                if result == "":
                        result = outvars[-1]

                for i,o in enumerate(outvars):
                        cpt_row = []
                        cpt_row.extend(c)
                        cpt_row.append(o)
                        val = 1.0 if (o == result) else 0.0
                        cpt_row.append(val)
                        cpt_rows.append(cpt_row)
        return (cpt_rows,keylist,outvars,description)





def addCpt(bayesianNetwork, cpt):

        outstring= ""

        for name, cpt_tuple in cpt.items():
                #print (name)
                conditionalProbabilityTable = bayesianNetwork.conditionalProbabilityTables.add()
                conditionalProbabilityTable.name = name
                for rv in cpt_tuple[1]:
                        randomVariable = conditionalProbabilityTable.randomVariables.add()
                        randomVariable.name = rv
                for row in cpt_tuple[0]:  
                        conditionalProbabilityRow = conditionalProbabilityTable.conditionalProbabilityRows.add()
                        for i,var in enumerate(row):
                                nvars = len(row)-1
                                if i < nvars:
                                        randomVariableValue = conditionalProbabilityRow.randomVariableValues.add()
                                        randomVariableValue.name = var
                                else:
                                        conditionalProbabilityRow.probability = var
                for outvar in cpt_tuple[2]:
                        out = conditionalProbabilityTable.outvars.add()
                        out.name = outvar
                outstring = outstring +  cpt_tuple[3].format(name) + "\n\n"

        return outstring

                                
        


def bayesInitialize(bayesianNetwork):
        model = BayesianNetwork()
        state = {}
        general_distribution = {}
        for dist in bayesianNetwork.discreteDistributions:
                distribution ={}
                for var in dist.variables:
                        distribution[var.name]= var.probability
                discreteDistribution = DiscreteDistribution(distribution)
                general_distribution[dist.name] = discreteDistribution
                state[dist.name] = Node(discreteDistribution, dist.name)
                model.add_state(state[dist.name])
        for table in bayesianNetwork.conditionalProbabilityTables:
                tablelist = []
                for row in table.conditionalProbabilityRows:
                        rowlist = []
                        for var in row.randomVariableValues:
                                rowlist.append (var.name)
                        rowlist.append(row.probability)
                        tablelist.append(rowlist)
                varlist = []
                for var in table.randomVariables:
                        varlist.append(general_distribution[var.name])
                #print("table.name")
                #print(table.name)
                #print("tablelist")
                #print(tablelist)
                #print("varlist")
                #print(varlist)
                conditionalProbabilityTable = ConditionalProbabilityTable(tablelist,varlist)
                general_distribution[table.name] = conditionalProbabilityTable
                state[table.name] = Node(conditionalProbabilityTable, table.name)
                model.add_state(state[table.name])
                #print('state')
                #print(state)
                for var in table.randomVariables:
                        #print("var.name")
                        #print(var.name)
                        #print ("table.name")
                        #print (table.name)
                        model.add_edge(state[var.name],state[table.name])

        return model


def non_cpt_descriptions(bayesianNetwork):
        description = ""
        for dist in bayesianNetwork.discreteDistributions:
                description += "\nThe prevalence of  " + dist.name 
                firsttime = True
                for var in dist.variables:
                        phrase = "" if firsttime else ","
                        if var is dist.variables[-1]:
                            phrase += " and"
                        description = description + phrase +" of value " + var.name + " is " + str(var.probability)
                        firsttime = False
                description += ".\n"
        return description


def get_priors(bayesianNetwork,invars,prevalence,cpt):
        var_positions = get_var_positions(bayesianNetwork)
        pomegranate= bayesInitialize(bayesianNetwork)
        #print(bayesianNetwork)
        pomegranate.bake()
        probs = pomegranate.predict_proba({})
        priors = {}
        vdict = dictVarsAndValues(bayesianNetwork, cpt)
        for vardict,numval_dict in invars:
                numval = numval_dict["relative_risk"] if "relative_risk" in numval_dict else (
                                    (numval_dict["sensitivity"]/prevalence) if "sensitivity" in numval_dict else 1) 
                asum = 0
                for k, varlist in vardict.items():
                        if k not in priors:
                            priors[k] = {}
                        for v in vdict[k]:
                                try:
                                        #problem="hypertension"
                                        #if k is problem or v is problem:
                                            #print("k")
                                            #print(k)
                                            #print("v")
                                            #print(v)
                                            #print("var_positions")
                                            #print(var_positions)
                                            #print ("probs")
                                            #print (probs)
                                            #print("priors")
                                            #print(priors)
                                            #print("json.loads(probs[var_positions[k]].to_json())['parameters']")
                                            #print(json.loads(probs[var_positions[k]].to_json())['parameters'])
                                        priors[k][v]=(json.loads(probs[var_positions[k]].to_json()))['parameters'][0][v]
                                        asum += priors[k][v]
                                except AttributeError as e:
                                        pass
                        #print("asum")
                        #print(asum)
        return priors
                
def get_frequencies(bayesianNetwork,keylist,cpt):
        #print ("keylist")
        #print (keylist)
        pomegranate= bayesInitialize(bayesianNetwork)
        #print(bayesianNetwork)
        pomegranate.bake()
       
        frequencies = {}
        var_positions = get_var_positions(bayesianNetwork)
        vdict = dictVarsAndValues(bayesianNetwork, cpt)
        #print ("vdict")
        #print (vdict)
        conditionals={}
        for i in range (len(keylist)):
                #print ("i")
                #print(i)
                short_keylist = keylist[:i] 
                vlist = [vdict[v] for v in short_keylist]
                #print("vlist")
                #print(vlist)
                cartesian = [()] if i==0 else ([tuple([a]) for a in vlist[0] ] if i==1 else list(itertools.product(*vlist)))
                #print ("cartesian")
                #print(cartesian)
                for c in cartesian:
                        evidence = {} if i == 0 else {k:v for k,v in zip(short_keylist,c)} 
                        #print ("evidence")
                        #print (evidence)
                        probs = pomegranate.predict_proba(evidence)
                        conditionals[c]={}
                        for val in vdict[keylist[i]]:
                                try:
                                        conditionals[c][val] = (json.loads(probs[var_positions[keylist[i]]].to_json()))['parameters'][0][val]
                                except AttributeError as e:
                                        pass
        #print("conditionals")
        #print(conditionals)
        vlist = [vdict[v] for v in keylist]
        cartesian = list(itertools.product(*vlist))


        #prob (a,b,c) = prob a * prob b|a * prob c|ab  
        asum = 0
        for c in cartesian:
                product = 1
                for i in range(len(c)):
                        key = tuple(c [:i])
                        #print("key")
                        #print(key)
                        product *= conditionals[key][c[i]]
                frequencies[c]=product
                asum += product
        #print("asum")
        #print(asum)
        return frequencies
        
                
def prob_a_given_b_and_not_b (invars, priors, outvars):
    
        # This function will find prob_a_given_b and prob_a_given_not_b.
        # Applies to variables with "relative_risk" values and those with "sensitivity" values
        # For the relative_risk case,
        # We have the equation 1, prob_a = (prob_good_b)(prob_a_given_good_b) + (prob_b1)(prob_a_given_b1) 
        # + (prob_b2)(prob_a_given_b2) +.... + (prob_bi)(prob_a_given_bi) where i is the number of key,value pairs for a key b.
        # (in invars, the keys may be variables like "age" and the values what fills them in, like "elderly" and "young_adult"
        # For each key,value pair in the invars there is the equation RRi * prob_a_given_good_b = prob_a_given_bi
        # That makes b + 1 equations and b +1 unknowns, where unknowns are prob_a_given_good_b, prob_a_given_b1, prob_a_given_b2, 
        # ... prob_a_given_bi.  We already know the values prob_a, prob_good_b, prob RRi and prob_bi, etc.
        # To solve, we eliminate all prob_a_given_bi in equation 1 using the other equations, and get 
        # prob_a = (prob_good_b)(prob_a_given_good_b) + (prob_b1)(RR1 * prob_a_given_good_b) 
        # + (prob_b2)(RR2 * prob_a_given_good_b) +.... + (prob_bi)(RRi * prob_a_given_good_b)
        # So this function computes prob_a_given_good_b = prob_a/( prob_good_b + RR1*prob_b1 + RR2*prob_b2 + ... + RRi*prob_bi)
        # Which is used to find prob_a_given_b = rr * prob_a_given_good_b 
        # For the sensitivity case,  prob_a_given_b = sensitivity 
        # For both the sensitivity and relative_risk cases,  prob_a given_not_b is from
        # prob_b * prob_a_given_b + (1-prob_b)(prob_a_given_not_b = prob_a
        # sensitivity for a variable should only occur once, because it is binary, so the last sensitivity is used 
        
        prob_a_given_b = {}
        prob_a_given_not_b = {}
        prob_a_given_good_b = {}
        prob_good_b={}
        
        prob_a = list(outvars.items())[0][1]
        
        
        for vardict,numval_dict in invars:
            for k,varlist in vardict.items():
                
                if k not in prob_a_given_b:
                    prob_a_given_b[k] = {}
                if k not in prob_a_given_not_b:
                    prob_a_given_not_b[k] = {}
                if k not in prob_a_given_good_b:
                    prob_a_given_good_b[k]=0
                if k not in prob_good_b:
                    prob_good_b[k] = 0
                if "relative_risk" in numval_dict:
                    rr = numval_dict["relative_risk"] 
                    #print("rr")
                    #print(rr)
                    #print("k")
                    #print(k)
                    for v in priors[k]:
                        #print("v")
                        #print(v)
                    
                        #print("priors[k][v]")
                        #print(priors[k][v])
                        if v in varlist:
                            prob_a_given_good_b[k] += rr*priors[k][v] 
                        else:
                            prob_good_b[k] += priors[k][v]
                elif "sensitivity" in numval_dict:
                    for v in varlist:
                        prob_b = priors[k][v]
                        prob_a_given_b[k][v] = numval_dict["sensitivity"]
                        prob_a_given_not_b[k][v] = (prob_a - (prob_b*prob_a_given_b[k][v] ))/(1-prob_b)
                        if prob_a_given_not_b[k][v] <0:
                            prob_a_given_not_b[k][v] = 0.0001
                        

        for vardict,numval_dict in invars:
            for k,varlist in vardict.items():
                if "relative_risk" in numval_dict:  
                    rr = numval_dict["relative_risk"]
                    #print("k")
                    #print(k)
                    #print("prob_a_given_good_b[k]")
                    #print(prob_a_given_good_b[k])
                    prob_a_given_good_b[k] += prob_good_b[k]
                    #print("prob_a_given_good_b[k] after add prob_good_b[k]")
                    #print(prob_a_given_good_b[k])
                    prob_a_given_good_b [k]= prob_a/prob_a_given_good_b[k]
                    #print("prob_a_given_good_b[k] after div prob_a")
                    #print(prob_a_given_good_b[k])
                    for v in varlist:
                        prob_b = priors[k][v]
                        prob_a_given_b[k][v] = rr * prob_a_given_good_b[k]
                        prob_a_given_not_b [k][v] = (prob_a - (prob_b* prob_a_given_b[k][v]))/(1.-prob_b)
                        if prob_a_given_b[k][v] < 0:
                            prob_a_given_b[k][v] = 0.0001
                        if prob_a_given_not_b[k][v] <0:
                            prob_a_given_not_b[k][v] = 0.0001
        
        return prob_a_given_b, prob_a_given_not_b



def dependency(bayesianNetwork, cpt, invars, outvars):
        
        import itertools
        from scipy.optimize import linprog

        import time

        print("start timing...")
        tic = time.perf_counter()
        keyset = OrderedSet([])
        prevalence_condition_regardless = list(outvars.items())[0][1]
        priors = get_priors(bayesianNetwork,invars,prevalence_condition_regardless,cpt)
        #print("priors")
        #print(priors)
        val_prevalence, better_than_val_prevalence =  prob_a_given_b_and_not_b (invars, priors, outvars)

        description = "Against the baseline risks, "
        firsttime = True
        for k,v in outvars.items():                        
                phrase = "" if firsttime else " and "
                description + phrase + k + " of " + str(v) + " , "
                firsttime = False
        firsttime = True
        for vardict,numval_dict in invars:
                    numval = numval_dict["relative_risk"] if "relative_risk" in numval_dict else (
                            numval_dict["sensitivity"] if "sensitivity" in numval_dict else 1) 
                    for val, varlist in vardict.items():
                            keyset.add(val)
                            phrase = "" if firsttime else (" , and " if varlist [-1] is val else " , " )

                            description= description + phrase + "the relative risk of {0} for those in the " + val + " category of " 
                            firsttime1 = True
                            sum_priors = 0
                            for var in varlist:                                
                                    phrase = "" if firsttime1 else " or "
                                    description = description + phrase + var
                                    firsttime1 = False
                                    sum_priors += priors[val][var]
                            if "sensitivity" in numval_dict:
                                numval = (1-sum_priors)*numval_dict["sensitivity"]/(prevalence_condition_regardless-(numval_dict["sensitivity"]* sum_priors))
                            description = description + " is " + str(numval)
                            if "sensitivity" in numval_dict:
                                description = description + ", calculated from a sensitivity of " + str(numval_dict["sensitivity"])

                            firsttime = False
                                    
        description = description + "."
       
        #print("better_than_val_prevalence")
        #print (better_than_val_prevalence)
        #print("val_prevalence")
        #print(val_prevalence)

        keylist = list(keyset)
        pos = {k:n for n,k in enumerate(keylist)}
        vdict = dictVarsAndValues(bayesianNetwork, cpt)

        #print("vdict")
        #print(vdict)
        val_prev = {}
        for k in keylist:
                val_prev[k]={}
                previous = None
                for v in vdict[k]:
                        #natural order is worse to better, and we want to fill in worse first because better is more accurate
                        if k in val_prevalence and v in val_prevalence[k]:
                                val_prev[k][v] = val_prevalence[k][v] 
                                previous = better_than_val_prevalence[k][v]
                        elif previous is not None:
                                val_prev [k][v] = previous
                        else:
                                val_prev [k][v] = prevalence_condition_regardless
        #print("val_prev")                        
        #print(val_prev)                            


        vlist = [vdict[v] for v in keylist]
        cartesian = list(itertools.product(*vlist))
       #in cartesian, worst is first and best comes later
        cpt_rows = []
        lhs_equality_equation1 = {}
        lhs_equality_equation2 = {}
        rhs_equality_equation1 = {}
        rhs_equality_equation2 = {}
        obj = np.zeros(len(cartesian))
        frequencies = get_frequencies(bayesianNetwork,keylist,cpt)
        #print ("frequencies")
        #print(frequencies)
        #bnd = [(1.0,1.0)] * len(cartesian)
        bnd = []
        for i,c in enumerate(cartesian):
                #print ("c")
                #print (c)
        
        
                #equation1  (doesnt have every one in it )
                #(non elderly hbp prevalence from 1.) = 
                #(prevalence of hbp among adult obese psych) * prevalence of adult obese psych 
                #+ (prevalence of hbp among youngadult obese psych) * prevalence of youngadult obese psych
                #+ (prevalence of hbp among teen obese psych) * prevalence of teen obese psych
                #+ (prevalence of hbp among child obese psych) * prevalence of child obese psych
                #+ (prevalence of hbp among adult overweight psych) * prevalence of adult overweight psych
                #+ (prevalence of hbp among youngadult overweight psych) * prevalence of youngadult overweight psych
                #+ (prevalence of hbp among teen overweight psych) * prevalence of teen overweight psych
                #+ (prevalence of hbp among child overweight psych) * prevalence of child overweight psych
                #+ (prevalence of hbp among adult healthy psych) * prevalence of adult healthy psych
                #+ (prevalence of hbp among youngadult healthy psych) * prevalence of youngadult healthy psych
                #+ (prevalence of hbp among teen healthy psych) * prevalence of teen healthy psych
                #+ (prevalence of hbp among child healthy psych) * prevalence of child healthy psych
                #+ (prevalence of hbp among adult obese psych) * prevalence of adult obese psych 
                #+ (prevalence of hbp among youngadult obese psych) * prevalence of youngadult obese psych
                #+ (prevalence of hbp among teen obese psych) * prevalence of teen obese psych
                #+ (prevalence of hbp among child obese psych) * prevalence of child obese psych
                #+ (prevalence of hbp among adult overweight psych) * prevalence of adult overweight psych
                #+ (prevalence of hbp among youngadult overweight psych) * prevalence of youngadult overweight psych
                #+ (prevalence of hbp among teen overweight psych) * prevalence of teen overweight psych
                #+ (prevalence of hbp among child overweight psych) * prevalence of child overweight psych
                #+ (prevalence of hbp among adult healthy psych) * prevalence of adult healthy psych
                #+ (prevalence of hbp among youngadult healthy psych) * prevalence of youngadult healthy psych
                #+ (prevalence of hbp among teen healthy psych) * prevalence of teen healthy psych
                #+ (prevalence of hbp among child healthy psych) * prevalence of child healthy psych
                         
                         
                #equation2 (has the balance)         
                # elderly with hbp relative risk X (non elderly hbp prevalence from 1.) = 
                #(prevalence of hbp among elderly obese psych) * prevalence of elderly obese psych 
                #+ (prevalence of hbp among elderly overweight psych) * prevalence of elderly overweight psych
                #+ (prevalence of hbp among elderly healthy psych) * prevalence of elderly healthy psych
                #+ (prevalence of hbp among elderly obese psych) * prevalence of elderly obese psych 
                #+ (prevalence of hbp among elderly overweight psych) * prevalence of elderly overweight psych
                #+ (prevalence of hbp among elderly healthy psych) * prevalence of elderly healthy psych
                
                for vardict,numval_dict in invars:
                        #relative_risk = numval_dict["relative_risk"] if "relative_risk" in numval_dict else (
                        #    (prevalence_condition_regardless-numval_dict["sensitivity"])/numval_dict["sensitivity"] if "sensitivity" in numval_dict else 1) 
                        for k, varlist in vardict.items():
                        
                                if k not in lhs_equality_equation1:
                                        lhs_equality_equation1[k] = {}
                                if k not in lhs_equality_equation2:
                                        lhs_equality_equation2[k] = {}
                                if k not in rhs_equality_equation1:
                                        rhs_equality_equation1[k] = {}
                                if k not in rhs_equality_equation2:
                                        rhs_equality_equation2[k] = {}
                
                                for v in varlist:
                                        if v not in lhs_equality_equation1[k]:
                                                lhs_equality_equation1[k][v] = np.zeros(len(cartesian)) #lhs will be list of lists
                                        if v not in lhs_equality_equation2[k]:
                                                lhs_equality_equation2[k][v] = np.zeros(len(cartesian))
                                        if v not in rhs_equality_equation1[k]:
                                                rhs_equality_equation1[k][v] = 0 #rhs will be list of floats
                                        if v not in rhs_equality_equation2[k]:
                                                rhs_equality_equation2[k][v] = 0
                                        #print ("c[pos[k]]")
                                        #print (c[pos[k]])
                                        if c[pos[k]]  == v:
                                                # rhs_equality_equation2[k][v] = priors[k][v]*relative_risk* val_prev[k][v]
                                                rhs_equality_equation2[k][v] = val_prevalence[k][v]
                                                lhs_equality_equation2[k][v][i] = frequencies [c]
                                        else:
                                                # rhs_equality_equation1[k][v] = val_prev[k][v]
                                                rhs_equality_equation1[k][v] = better_than_val_prevalence[k][v]
                                                lhs_equality_equation1[k][v][i] = frequencies [c]
                                                
                obj[i]=frequencies[c]

                #make independence the lower bound
                #product = 1
                #for j,k in enumerate(keylist):
                        #product *= 1.-val_prev [k][c[j]] 
                #bnd.append(( 1-product, 1.0))

                minimum = 1.0
                for j,k in enumerate(keylist):
                        if val_prev [k][c[j]] < minimum:
                            minimum = val_prev [k][c[j]] 
                bnd.append(( minimum, 1.0))

        window = 1.0
        cut = 1.0
        lastTrue = None
        #At first test window at 1.0 to ensure that there is a solution at all , then narrow down on it with binary search to get the smallest feasable window
        while cut > 0.05:
                                        
                lhs_eq = []
                rhs_eq = []
                                
                for vardict,numval_dict in invars:
                        #relative_risk= numval_dict["relative_risk"] if "relative_risk" in numval_dict else (
                         #           (prevalence_condition_regardless-numval_dict["sensitivity"])/numval_dict["sensitivity"] if "sensitivity" in numval_dict else 1) 
                        for k, varlist in vardict.items():
                                for v in varlist:

                                        #equality doesnt work
                                        #lhs_eq.append(lhs_equality_equation1[k][v])
                                        #rhs_eq.append(rhs_equality_equation1[k][v])
                                        #lhs_eq.append(lhs_equality_equation2[k][v])
                                        #rhs_eq.append(rhs_equality_equation2[k][v])

                                        #UB    
                                        lhs_eq.append(np.multiply(lhs_equality_equation1[k][v],1))
                                        rhs_eq.append(rhs_equality_equation1[k][v]*(1+window))
                                        lhs_eq.append(np.multiply(lhs_equality_equation2[k][v],1))
                                        rhs_eq.append(rhs_equality_equation2[k][v]*(1+window))

                                        #LB
                                        lhs_eq.append(np.multiply(lhs_equality_equation1[k][v],-1))
                                        rhs_eq.append(rhs_equality_equation1[k][v]*(-1+window))
                                        lhs_eq.append(np.multiply(lhs_equality_equation2[k][v],-1))
                                        rhs_eq.append(rhs_equality_equation2[k][v]*(-1+window))


                               
                
                #opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,method="revised simplex")
                #print ("obj")
                #print (obj)
                #print ("lhs_eq")
                #print(lhs_eq)
                #print("rhs_eq")
                #print (rhs_eq)
                #print ("bnd")
                #print(bnd)

                #opt = linprog(c=obj, A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,method="revised simplex")
         
                opt = linprog(c=obj, A_ub=lhs_eq, b_ub=rhs_eq, bounds=bnd,method="revised simplex")
                #print("opt")
                #print (opt)
                if window == 1.0 and not opt.success:
                    break
                cut /= 2
                window = window - cut if opt.success else window + cut
                if opt.success:
                    lastTrue = opt
                #print("window")
                #print (window)


        if lastTrue is not None:
            opt = lastTrue
        for i,c in enumerate(cartesian):
                #there are only two values of outvars for relative risk
                cpt_row = []
                cpt_row.extend(c)
                cpt_row.append(list(outvars.items())[0][0])
                val = opt.x[i] 
                cpt_row.append(val)
                cpt_rows.append(cpt_row)
                
                cpt_row = []
                cpt_row.extend(c)
                cpt_row.append(list(outvars.items())[1][0])
                val =  1.0-opt.x[i]
                cpt_row.append(val)
                cpt_rows.append(cpt_row)
        #print ("cpt_rows")
        #print(cpt_rows)
        toc = time.perf_counter()
        diff = toc - tic

        print (f"{outvars} took {diff} seconds")
        return (cpt_rows,keylist,outvars,description)





def dependency_old(bayesianNetwork, cpt, invars, outvars):
        
        import itertools
        from scipy.optimize import linprog

        import time

        print("start timing...")
        tic = time.perf_counter()
 
        var_positions = get_var_positions(bayesianNetwork)
        vdict = dictVarsAndValues(bayesianNetwork, cpt)
 
        # non elderly hbp prevalence = (prevalence of hbp regardless)/ ((prevalence of elderly X elderly with hbp relative risk) + (1-prevalence of elderly))
        
        prevalence_condition_regardless = list(outvars.items())[0][1]
  
        priors = get_priors(bayesianNetwork,invars,prevalence_condition_regardless,cpt)
        print("priors")
        print(priors)
        better_than_val_prevalence={}
        val_prevalence = {}
        keyset = OrderedSet([])
        keys_vals_risks = {}

        better_than_val_prevalence1 = {}
 

        #window = 1.0
        #cut = 1.0
        #lastTrue = None
        #while cut > 0.05:
                #windows of 1.0 goes from zero to 2*risk, .5 goes from .5 risk to 1.5 rish, from LB to UB
                #print("bayesianNetwork")
                #print(bayesianNetwork)

        description = "Against the baseline risks, "
        firsttime = True
        for k,v in outvars.items():                        
                phrase = "" if firsttime else " and "
                description + phrase + k + " of " + str(v) + " , "
                firsttime = False
        firsttime = True
        for vardict,numval_dict in invars:
                    numval = numval_dict["relative_risk"] if "relative_risk" in numval_dict else (
                            numval_dict["sensitivity"] if "sensitivity" in numval_dict else 1) 
                    for val, varlist in vardict.items():
                            phrase = "" if firsttime else (" , and " if varlist [-1] is val else " , " )

                            description= description + phrase + "the relative risk of {0} for those in the " + val + " category of " 
                            firsttime1 = True
                            sum_priors = 0
                            for var in varlist:                                
                                    phrase = "" if firsttime1 else " or "
                                    description = description + phrase + var
                                    firsttime1 = False
                                    sum_priors += priors[val][var]
                            if "sensitivity" in numval_dict:
                                numval = (1-sum_priors)*numval_dict["sensitivity"]/(prevalence_condition_regardless-(numval_dict["sensitivity"]* sum_priors))
                            description = description + " is " + str(numval)
                            if "sensitivity" in numval_dict:
                                description = description + ", calculated from a sensitivity of " + str(numval_dict["sensitivity"])

                            firsttime = False
                                    
        description = description + "."
       
        for vardict,numval_dict in invars:                            
                numval = numval_dict["relative_risk"] if "relative_risk" in numval_dict else (
                            numval_dict["sensitivity"] if "sensitivity" in numval_dict else 1) 

                for k, varlist in vardict.items():
                        keyset.add(k)
                        if k not in keys_vals_risks:
                                keys_vals_risks[k] = {}
                        for v in varlist:
                                keys_vals_risks[k][v]=numval
                                sum_priors += priors[k][v]
                        if "sensitivity" in numval_dict:
                                numval = (1-sum_priors)*numval_dict["sensitivity"]/(prevalence_condition_regardless-(numval_dict["sensitivity"]* sum_priors))
        keylist = list(keyset) 
        
        for k in keylist:
                asum = 0
                for val in vdict[k]:
                    asum += (keys_vals_risks[k][val] * priors[k][val])  if val in keys_vals_risks[k] else priors[k][val]
                            
                better_than_val_prevalence1 [k] = prevalence_condition_regardless/asum
               
        for vardict,numval_dict in invars:
                numval = numval_dict["relative_risk"] if "relative_risk" in numval_dict else (
                            numval_dict["sensitivity"] if "sensitivity" in numval_dict else 1) 
                for k, varlist in vardict.items():
                        keyset.add(k)
                        group_sum = 0
                        for v in varlist:
                                group_sum += priors[k][v]
                        if k not in better_than_val_prevalence:        
                                better_than_val_prevalence[k] = {}
                                val_prevalence[k] = {}
                        for v in varlist:
                                print ("k")
                                print (k)
                                print ("v")
                                print (v)
                                print ("prevalence_condition_regardless")
                                print (prevalence_condition_regardless)
                                print ("priors[k][v]")
                                print (priors[k][v])
                                sum_priors += priors[k][v]
                                if "sensitivity" in numval_dict:
                                        numval = (1-sum_priors)*numval_dict["sensitivity"]/(prevalence_condition_regardless-(numval_dict["sensitivity"]* sum_priors))
                                print ("numval")
                                print (numval)
                                # better_than_val_prevalence[k][v]= prevalence_condition_regardless/((group_sum*numval)+(1.-group_sum))
                                # better_than_val_prevalence[k][v]= prevalence_condition_regardless/((priors[k][v]*numval)+(1.-priors[k][v]))
                                better_than_val_prevalence[k][v]= (prevalence_condition_regardless- (better_than_val_prevalence1[k]
                                        *numval*priors[k][v]))/(1-priors[k][v])
                                #val_prevalence[k][v] = better_than_val_prevalence1[k][v] * numval
                                val_prevalence[k][v] = better_than_val_prevalence1[k] * numval


                                print("better_than_val_prevalence1")
                                print (better_than_val_prevalence1)
                                print("better_than_val_prevalence")
                                print (better_than_val_prevalence[k][v])
                                print("val_prevalence")
                                print(val_prevalence[k][v])

       
        pos = {k:n for n,k in enumerate(keylist)}

        print("vdict")
        print(vdict)
        val_prev = {}
        for k in keylist:
                val_prev[k]={}
                previous = None
                for v in vdict[k]:
                        #natural order is worse to better, and we want to fill in worse first because better is more accurate
                        if k in val_prevalence and v in val_prevalence[k]:
                                val_prev[k][v] = val_prevalence[k][v] 
                                previous = better_than_val_prevalence1[k]
                        elif previous is not None:
                                val_prev [k][v] = previous
                        else:
                                val_prev [k][v] = prevalence_condition_regardless
        print("val_prev")                        
        print(val_prev)                            


        vlist = [vdict[v] for v in keylist]
        cartesian = list(itertools.product(*vlist))
       #in cartesian, worst is first and best comes later
        cpt_rows = []
        lhs_equality_equation1 = {}
        lhs_equality_equation2 = {}
        rhs_equality_equation1 = {}
        rhs_equality_equation2 = {}
        obj = np.zeros(len(cartesian))
        frequencies = get_frequencies(bayesianNetwork,keylist,cpt)
        print ("frequencies")
        print(frequencies)
        #bnd = [(1.0,1.0)] * len(cartesian)
        bnd = []
        for i,c in enumerate(cartesian):
                print ("c")
                print (c)
        
        
                #equation1  (doesnt have every one in it )
                #(non elderly hbp prevalence from 1.) = 
                #(prevalence of hbp among adult obese psych) * prevalence of adult obese psych 
                #+ (prevalence of hbp among youngadult obese psych) * prevalence of youngadult obese psych
                #+ (prevalence of hbp among teen obese psych) * prevalence of teen obese psych
                #+ (prevalence of hbp among child obese psych) * prevalence of child obese psych
                #+ (prevalence of hbp among adult overweight psych) * prevalence of adult overweight psych
                #+ (prevalence of hbp among youngadult overweight psych) * prevalence of youngadult overweight psych
                #+ (prevalence of hbp among teen overweight psych) * prevalence of teen overweight psych
                #+ (prevalence of hbp among child overweight psych) * prevalence of child overweight psych
                #+ (prevalence of hbp among adult healthy psych) * prevalence of adult healthy psych
                #+ (prevalence of hbp among youngadult healthy psych) * prevalence of youngadult healthy psych
                #+ (prevalence of hbp among teen healthy psych) * prevalence of teen healthy psych
                #+ (prevalence of hbp among child healthy psych) * prevalence of child healthy psych
                #+ (prevalence of hbp among adult obese psych) * prevalence of adult obese psych 
                #+ (prevalence of hbp among youngadult obese psych) * prevalence of youngadult obese psych
                #+ (prevalence of hbp among teen obese psych) * prevalence of teen obese psych
                #+ (prevalence of hbp among child obese psych) * prevalence of child obese psych
                #+ (prevalence of hbp among adult overweight psych) * prevalence of adult overweight psych
                #+ (prevalence of hbp among youngadult overweight psych) * prevalence of youngadult overweight psych
                #+ (prevalence of hbp among teen overweight psych) * prevalence of teen overweight psych
                #+ (prevalence of hbp among child overweight psych) * prevalence of child overweight psych
                #+ (prevalence of hbp among adult healthy psych) * prevalence of adult healthy psych
                #+ (prevalence of hbp among youngadult healthy psych) * prevalence of youngadult healthy psych
                #+ (prevalence of hbp among teen healthy psych) * prevalence of teen healthy psych
                #+ (prevalence of hbp among child healthy psych) * prevalence of child healthy psych
                         
                         
                #equation2 (has the balance)         
                # elderly with hbp relative risk X (non elderly hbp prevalence from 1.) = 
                #(prevalence of hbp among elderly obese psych) * prevalence of elderly obese psych 
                #+ (prevalence of hbp among elderly overweight psych) * prevalence of elderly overweight psych
                #+ (prevalence of hbp among elderly healthy psych) * prevalence of elderly healthy psych
                #+ (prevalence of hbp among elderly obese psych) * prevalence of elderly obese psych 
                #+ (prevalence of hbp among elderly overweight psych) * prevalence of elderly overweight psych
                #+ (prevalence of hbp among elderly healthy psych) * prevalence of elderly healthy psych
                
                for vardict,numval_dict in invars:
                        #relative_risk = numval_dict["relative_risk"] if "relative_risk" in numval_dict else (
                        #    (prevalence_condition_regardless-numval_dict["sensitivity"])/numval_dict["sensitivity"] if "sensitivity" in numval_dict else 1) 
                        for k, varlist in vardict.items():
                        
                                if k not in lhs_equality_equation1:
                                        lhs_equality_equation1[k] = {}
                                if k not in lhs_equality_equation2:
                                        lhs_equality_equation2[k] = {}
                                if k not in rhs_equality_equation1:
                                        rhs_equality_equation1[k] = {}
                                if k not in rhs_equality_equation2:
                                        rhs_equality_equation2[k] = {}
                
                                for v in varlist:
                                        if v not in lhs_equality_equation1[k]:
                                                lhs_equality_equation1[k][v] = np.zeros(len(cartesian)) #lhs will be list of lists
                                        if v not in lhs_equality_equation2[k]:
                                                lhs_equality_equation2[k][v] = np.zeros(len(cartesian))
                                        if v not in rhs_equality_equation1[k]:
                                                rhs_equality_equation1[k][v] = 0 #rhs will be list of floats
                                        if v not in rhs_equality_equation2[k]:
                                                rhs_equality_equation2[k][v] = 0
                                        print ("c[pos[k]]")
                                        print (c[pos[k]])
                                        if c[pos[k]]  == v:
                                                # rhs_equality_equation2[k][v] = priors[k][v]*relative_risk* val_prev[k][v]
                                                rhs_equality_equation2[k][v] = val_prevalence[k][v]
                                                lhs_equality_equation2[k][v][i] = frequencies [c]
                                        else:
                                                # rhs_equality_equation1[k][v] = val_prev[k][v]
                                                rhs_equality_equation1[k][v] = better_than_val_prevalence[k][v]
                                                lhs_equality_equation1[k][v][i] = frequencies [c]
                                                
                obj[i]=frequencies[c]

                #make independence the lower bound
                #product = 1
                #for j,k in enumerate(keylist):
                        #product *= 1.-val_prev [k][c[j]] 
                #bnd.append(( 1-product, 1.0))

                minimum = 1.0
                for j,k in enumerate(keylist):
                        if val_prev [k][c[j]] < minimum:
                            minimum = val_prev [k][c[j]] 
                bnd.append(( minimum, 1.0))

        window = 1.0
        cut = 1.0
        lastTrue = None
        while cut > 0.05:
                                        
                lhs_eq = []
                rhs_eq = []
                                
                for vardict,numval_dict in invars:
                        #relative_risk= numval_dict["relative_risk"] if "relative_risk" in numval_dict else (
                         #           (prevalence_condition_regardless-numval_dict["sensitivity"])/numval_dict["sensitivity"] if "sensitivity" in numval_dict else 1) 
                        for k, varlist in vardict.items():
                                for v in varlist:

                                        #equality doesnt work
                                        #lhs_eq.append(lhs_equality_equation1[k][v])
                                        #rhs_eq.append(rhs_equality_equation1[k][v])
                                        #lhs_eq.append(lhs_equality_equation2[k][v])
                                        #rhs_eq.append(rhs_equality_equation2[k][v])

                                        #UB    
                                        lhs_eq.append(np.multiply(lhs_equality_equation1[k][v],1))
                                        rhs_eq.append(rhs_equality_equation1[k][v]*(1+window))
                                        lhs_eq.append(np.multiply(lhs_equality_equation2[k][v],1))
                                        rhs_eq.append(rhs_equality_equation2[k][v]*(1+window))

                                        #LB
                                        lhs_eq.append(np.multiply(lhs_equality_equation1[k][v],-1))
                                        rhs_eq.append(rhs_equality_equation1[k][v]*(-1+window))
                                        lhs_eq.append(np.multiply(lhs_equality_equation2[k][v],-1))
                                        rhs_eq.append(rhs_equality_equation2[k][v]*(-1+window))


                               
                
                #opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,method="revised simplex")
                print ("obj")
                print (obj)
                print ("lhs_eq")
                print(lhs_eq)
                print("rhs_eq")
                print (rhs_eq)
                print ("bnd")
                print(bnd)

                #opt = linprog(c=obj, A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,method="revised simplex")
         
                opt = linprog(c=obj, A_ub=lhs_eq, b_ub=rhs_eq, bounds=bnd,method="revised simplex")
                print("opt")
                print (opt)
                if window == 1.0 and not opt.success:
                    break
                cut /= 2
                window = window - cut if opt.success else window + cut
                if opt.success:
                    lastTrue = opt
                print("window")
                print (window)


        if lastTrue is not None:
            opt = lastTrue
        for i,c in enumerate(cartesian):
                #there are only two values of outvars for relative risk
                cpt_row = []
                cpt_row.extend(c)
                cpt_row.append(list(outvars.items())[0][0])
                val = opt.x[i] 
                cpt_row.append(val)
                cpt_rows.append(cpt_row)
                
                cpt_row = []
                cpt_row.extend(c)
                cpt_row.append(list(outvars.items())[1][0])
                val =  1.0-opt.x[i]
                cpt_row.append(val)
                cpt_rows.append(cpt_row)
        print ("cpt_rows")
        print(cpt_rows)
        toc = time.perf_counter()
        diff = toc - tic

        print (f"{outvars} took {diff} seconds")
        return (cpt_rows,keylist,outvars,description)





