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
import time

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

def make_tree(bayesianNetwork, connections = True):
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
    if not connections:
        df=df.replace(to_replace=r"([0-9a-zA-Z\-_\.]+)(.*)", value=r"\1", regex=True) 
    #df.str.replace(r'[^0-9a-zA-Z\-_]+', '', regex=True)  
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
        #print("get_var_positions")
        #print(get_var_positions)
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
        #print("parse_net query")
        #print(query)
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
        #print ("anomaly_tuples")
        #print(anomaly_tuples)
        #print ("anomaly_params")
        #print (anomaly_params)
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
                            low= None if anomaly_params[var]['side'] == "positive" else anomaly_params[var]['low_percent']
                            high=None if anomaly_params[var]['side'] == 'negative' else anomaly_params[var]['high_percent']
                            quantile_ad = QuantileAD(high=high, low=low)
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
                            low= None if anomaly_params[var]['side'] == "positive" else anomaly_params[var]['low']
                            high=None if anomaly_params[var]['side'] == 'negative' else anomaly_params[var]['high']
                            threshold_ad = ThresholdAD(high=high, low=low)
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
                            anomaly_dict[var][detector] = volatility_shift_ad.fit_detect(s)
                            fitted[var]['std'] = std(s)
                            #print (f"fitted[{var}]['std']")
                            #print (fitted[var]['std'])
               
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
                #print("anomaly_dict")
                #print(anomaly_dict)
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

def get_template_priors(bayesianNetwork):
        template_priors = {}
        for dist in bayesianNetwork.discreteDistributions:
                template_priors[dist.name]={}
                for var in dist.variables:
                        template_priors[dist.name][var.name] = var.probability
        return template_priors


def predict_proba_adjusted ( baked_net,netspec,evidence_list = {},adjust=False):
    var_val_names = get_var_val_names(netspec)
    var_positions = get_var_positions(netspec)
    template_priors = get_template_priors(netspec)
    prior_var = list(template_priors.keys())[0]
    #print ("template_priors")
    #print (template_priors)
    dist = {}
    answer = {}
    if len (evidence_list) < 1 and adjust:
        for prior_val,prior_prob in template_priors[prior_var].items():
            evidence = {prior_var:prior_val}
            description = baked_net.predict_proba(evidence)
            for dist_name,val_dict in var_val_names.items():
                if dist_name not in dist:
                    dist[dist_name]={}
               
                try:
                        answer[dist_name] = (json.loads(description[var_positions[dist_name]].to_json()))['parameters'][0]
                except AttributeError as e:
                        #print("AttributeError")
                        #print(dist_name)
                        #print(e)
                        pass
                for k,v in evidence.items(): 
                    var_vals = {}
                    for num,val in var_val_names[k].items():
                        prob = 0.99999 if v == val else 0.00001
                        var_vals[val]= prob
                    answer[k]=var_vals

                for dummy,val in val_dict.items():
                    if val not in dist[dist_name]:
                        dist[dist_name][val] = answer[dist_name][val]*prior_prob
                    else:
                        dist[dist_name][val] += answer[dist_name][val]*prior_prob

    else:
            description = baked_net.predict_proba(evidence_list)
            for dist_name,val_dict in var_val_names.items():
                if dist_name not in dist:
                    dist[dist_name]={}
               
                try:
                        answer[dist_name] = (json.loads(description[var_positions[dist_name]].to_json()))['parameters'][0]
                except AttributeError as e:
                        #print("AttributeError")
                        #print(dist_name)
                        #print(e)
                        pass
                for k,v in evidence_list.items(): 
                    var_vals = {}
                    for num,val in var_val_names[k].items():
                        prob = 0.99999 if v == val else 0.00001
                        var_vals[val]= prob
                    answer[k]=var_vals
                for dummy,val in val_dict.items():
                    if val not in dist[dist_name]:
                        try:
                            dist[dist_name][val] = answer[dist_name][val]
                        except KeyError as e:
                            print("KeyError e") 
                            print(e)
                            print("answer")
                            print(answer)
                            print("description")
                            print(description)

    return dist




def batch_query(baked_net, netspec, evidence_list,out_var_list):
        answer_list = []
        var_positions = get_var_positions(netspec)
        #print ('evidence_list')
        #print (evidence_list)
        evidence_list = list(evidence_list)
        if "always_true" in var_positions:
                evidence_list["always_true"]="always_true"
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



def query(baked_net, netspec, evidence,out_var_list,adjust=False):
        answer={}
        probs = predict_proba_adjusted(baked_net,netspec,evidence,adjust)

        for dist_name in out_var_list:
                answer[dist_name] = probs[dist_name]
        return answer

       

def explain_why_bad(baked_net, netspec, evidence,explain_list,internal_query_result=None, include_list = []):
    #print (internal_query_result)
    return explain(baked_net, netspec,evidence,explain_list, internal_query_result=internal_query_result, include_list = include_list)

def explain_why_good(baked_net, netspec, evidence, explain_list, internal_query_result = None, include_list = []):
    adict = dictVarsAndValues(netspec,{})
    return explain(baked_net, netspec,evidence, explain_list, reverse_explain_list = explain_list, reverse_evidence = adict.keys(),
            internal_query_result=internal_query_result,include_list = include_list)

def internal_query(baked_net, netspec,evidence,adjust=False):
        internal_var_val_positions = get_internal_var_val_positions(netspec)
        exclusion_list = [var for var, val in internal_var_val_positions.items()]
        result = query(baked_net,netspec,evidence,exclusion_list,adjust)
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
                best_pos = len(var_val_positions[var])-1
                new_pos = None
                old_pos = var_val_positions[var][val]
                if var in reverse_evidence and old_pos > 0:
                        #new_pos = old_pos-1
                        new_pos = 0
                elif var not in reverse_evidence and old_pos < best_pos: 
                        #new_pos = old_pos+ 1
                        new_pos = best_pos
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
                best_pos = len(var_val_positions[var])-1
                new_pos = None
                old_pos = var_val_positions[var][val]
                if var in reverse_evidence and old_pos > 0:
                        #new_pos = old_pos-1
                        new_pos = 0
                elif var not in reverse_evidence and old_pos < best_pos: 
                        #new_pos = old_pos+ 1
                        new_pos = best_pos
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
        #print("before_change")
        #print(before_change)
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
        keylist = list(invars.keys())
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
        keylist = list(invars.keys())
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
        keylist = list(invars.keys())
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



def get_priors(bayesianNetwork,invars,prevalence,cpt,adjust=False):
        var_positions = get_var_positions(bayesianNetwork)
        var_val_names = get_var_val_names(bayesianNetwork)
        pomegranate= bayesInitialize(bayesianNetwork)
        #print(bayesianNetwork)
        pomegranate.bake()
        evidence = {}
        if "always_true" in var_positions:
                evidence["always_true"]="always_true"
        priors = {}
        for k,v in evidence.items(): 
                var_vals = {}
                for num,val in var_val_names[k].items():
                        prob = 0.99999 if v == val else 0.00001
                        var_vals[val]= prob
                priors[k]=var_vals
        probs = predict_proba_adjusted(pomegranate,bayesianNetwork,evidence,adjust)#pomegranate.predict_proba(evidence)
        #print("probs")
        #print (probs)
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
                                        priors[k][v]=probs[k][v]#(json.loads(probs[var_positions[k]].to_json()))['parameters'][0][v]
                                        asum += priors[k][v]
                                except AttributeError as e:
                                        pass
                        #print("asum")
                        #print(asum)
        return priors
                
def get_frequencies(bayesianNetwork,keylist,cpt,adjust=False,preconditionals = {}):
        #print ("keylist")
        #print (keylist)
        #print ("preconditionals")
        #print(preconditionals)

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
                        if "always_true" in keylist:
                            evidence["always_true"]="always_true"
                        evidence.update(preconditionals)
                        #print ("evidence")
                        #print (evidence)
                        #probs = pomegranate.predict_proba(evidence)
                        probs=predict_proba_adjusted(pomegranate,bayesianNetwork,evidence,adjust)
                        #print ("probs")
                        #print(probs)
                        conditionals[c]={}
                        for val in vdict[keylist[i]]:
                                if keylist[i] in evidence:
                                    conditionals[c][val] = 0.99999 if val in evidence[keylist[i]] else 0.00001
                                try:
                                        conditionals[c][val] = probs[keylist[i]][val]#(json.loads(probs[var_positions[keylist[i]]].to_json()))['parameters'][0][val]
                                except AttributeError as e:
                                        print (e)
                                        pass
        #print("conditionals")
        #print(conditionals)
        vlist = [vdict[v] for v in keylist]
        cartesian = list(itertools.product(*vlist))


        #prob (a,b,c) = prob a * prob b|a * prob c|ab  
        asum = 0
        for c in cartesian:
                #print ("cartesian")
                #print(cartesian)
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
        
 

def rr_prob_a_and_not_a_given_b_and_not_b (rr_dict,prior_a,prior_b_dict):

#Solution to these equations:
#rri=probagivenbi / probagivengood
#probagivengood= sum(probagivengoodbi*priorgoodbi)/sum(priorgoodbi)
#probagivenbi*priorbi +probagivennotbi * (1-prior bi) = priora
#sumi(probagivenbi*priorbi)=priora
#probagivenbi + probnotagivenbi = 1.0
#probagivennotbi + probnotagivennotbi = 1.0

#rr_dict: {v:rr}  (if no rr it is good) prior_b_dict: {v:prior}
#returns {b:{prob_a_given_b, prob_a_given_not_b, prob_not_a_given_b, prob_not_a_given_not_b}}

        b = {}
        sum_prior_b_rr = 0
        for v,prior in prior_b_dict.items():
                rr = rr_dict[v] if v in rr_dict else 1.
                sum_prior_b_rr += prior * rr
        prob_a_given_good = prior_a/sum_prior_b_rr
        
        for v,prior in prior_b_dict.items():
                b[v] = {}
                rr = rr_dict[v] if v in rr_dict else 1.
                b[v]["prob_a_given_b"] = prob_a_given_good * rr
                b[v]["prob_not_a_given_b"] = 1. - b[v]["prob_a_given_b"]
                b[v]["prob_a_given_not_b"] = -1*prior_a * (sum_prior_b_rr-prior*rr)/((prior-1.)*sum_prior_b_rr)
                b[v]["prob_not_a_given_not_b"]= 1. - b[v]["prob_a_given_not_b"] 
                
        return b

def ss_prob_a_and_not_a_given_b_and_not_b (sensitivity,specificity,prior_a,prior_b):
    #Strategy:  break down into TP, TN, FP, FN
    # 4 equations with 4 unknowns:
    #1.  sensitivity = TP/(TP+FN)
    #2.  specificity = TN/(TN+FP)
    #3.  prior_b = TP+FP
    #4.  prior_a = FN+TP
    #
    #Therefore:
    TP = sensitivity * prior_a
    TN = specificity * (1.-prior_a)
    FN = prior_a - TP
    FP = (1.-prior_a) - TN 

    #print ("tp tn fn fp")
    #print (f"{TP} {TN} {FN} {FP}")
    
    #Solution:
    prob_a_given_b = TP/(TP+FP)
    prob_a_given_not_b = FN/(TN+FN)
    prob_not_a_given_b = FP/(TP+FP)
    prob_not_a_given_not_b = TN/(TN+FN)

 
    return prob_a_given_b, prob_a_given_not_b, prob_not_a_given_b, prob_not_a_given_not_b
 

def prob_a_and_not_a_given_b_and_not_b (invars, priors, outvars):
 
        prob_a_given_b = {}
        prob_a_given_not_b = {}
        prob_not_a_given_b = {}
        prob_not_a_given_not_b = {}
         
        dependency_dict = {}
    
        prior_a = list(outvars.items())[0][1]
        
        for vardict,numval_dict in invars:
            for k,varlist in vardict.items():
                #print("k")
                #print(k)
                if k not in dependency_dict:
                    dependency_dict[k]={}
                for v in priors[k]:
                    #print("v")
                    #print(v)
                
                    #print("priors[k][v]")
                    #print(priors[k][v])
                    prior_b = priors[k][v] 
                    if "relative_risk" in numval_dict:
                        if "relative_risk" not in dependency_dict[k]:
                            dependency_dict[k]["relative_risk"]={}
                        if v in varlist:    
                            dependency_dict[k]["relative_risk"][v]= numval_dict["relative_risk"]
                    elif "sensitivity" in numval_dict:
                        if "sensitivity" not in dependency_dict[k]:
                            dependency_dict[k]["sensitivity"] = {}
                            dependency_dict[k]["specificity"] = {}
                        dependency_dict[k]["sensitivity"][v]= numval_dict["sensitivity"]
                        dependency_dict[k]["specificity"][v]= numval_dict["specificity"]
        
        for k,var_dependency_dict in dependency_dict.items():
          
            if k not in prob_a_given_b:
                prob_a_given_b[k] = {}
            if k not in prob_a_given_not_b:
                prob_a_given_not_b[k] = {}
            if k not in prob_not_a_given_b:
                prob_not_a_given_b[k] = {}
            if k not in prob_not_a_given_not_b:
                prob_not_a_given_not_b[k] = {}
            for dependency_type, var_dict in var_dependency_dict.items():
                if dependency_type == "relative_risk":
                    #print ("var_dict")
                    #print(var_dict)
                    #print("prior_a")
                    #print (prior_a)
                    #print(f"priors[{k}]")
                    #print (priors[k])
                    prob_dict = rr_prob_a_and_not_a_given_b_and_not_b(var_dict,prior_a,priors[k])
                    #print("prob_dict")
                    #print(prob_dict)
                    for v,prob_type_dict in prob_dict.items():
                        for prob_type,val in prob_type_dict.items():
                            if prob_type == 'prob_a_given_b':
                                prob_a_given_b[k][v]= val
                            elif prob_type == 'prob_a_given_not_b':
                                prob_a_given_not_b[k][v] =val
                            elif prob_type == 'prob_not_a_given_b':
                                prob_not_a_given_b[k][v] =val
                            elif prob_type == 'prob_not_a_given_not_b':
                                prob_not_a_given_not_b[k][v] =val
                elif dependency_type == "sensitivity":
                    for v,val in var_dict.items():
                        prob_a_given_b[k][v], prob_a_given_not_b[k][v], prob_not_a_given_b[k][v], prob_not_a_given_not_b[k][v] = ( 
                            ss_prob_a_and_not_a_given_b_and_not_b(val,var_dependency_dict["specificity"][v],prior_a,priors[k][v])
                            )
                    


                category = f"relative_risk:{numval_dict['relative_risk']}" if "relative_risk" in numval_dict else (
                        f"sensitivity/specificity:{numval_dict['sensitivity']}/{numval_dict['specificity']}")
                #print(category)
                #print("prob_a_given_not_b[k][v] ")
                #print (prob_a_given_not_b[k][v] )
                #print("prob_a_given_b[k][v] ")
                #print(prob_a_given_b[k][v] )


                #print("prob_not_a_given_not_b[k][v] ")
                #print (prob_not_a_given_not_b[k][v] )
                #print("prob_not_a_given_b[k][v] ")
                #print(prob_not_a_given_b[k][v] )

                    
            

        return prob_a_given_b, prob_a_given_not_b, prob_not_a_given_b, prob_not_a_given_not_b



def get_good_vars(v,invars,bayesianNetwork,var_val_positions = None, var_val_names = None):
        #print ("v")
        #print(v)
        #print("invars")
        #print(invars)
    
    
        if var_val_positions is None:    
            var_val_positions = get_var_val_positions(bayesianNetwork)
        if var_val_names is None:
            var_val_names= get_var_val_names(bayesianNetwork)
        #print("var_val_positions")
        #print(var_val_positions)
        #print("var_val_names")
        #print(var_val_names)

        numvals = len(var_val_positions[v])
        # Find out if there are more non stated items to the right or the left, and then send the 
        # majority .  if there are the same numbe of non stated on the right and left send 
        # those on the right, because on the right are positive values, and most cases compare to 
        # a better situation

        lowest_val = numvals
        highest_val = 0
        for tup in invars:
            if v in tup[0]:
                for val in tup[0][v]:
                    if var_val_positions[v][val]>highest_val:
                        highest_val = var_val_positions[v][val]
                    if var_val_positions[v][val]<lowest_val:
                        lowest_val = var_val_positions[v][val]
        #print("highest_val")
        #print(highest_val)
        #print("lowest_val")
        #print(lowest_val)
        right_side_not_included = numvals-1-highest_val
        left_side_not_included = lowest_val
        good_vars = []
        if left_side_not_included > right_side_not_included:
            good_vars = [var_val_names[v][i] for i in range (0,lowest_val+1)]
        else:
            good_vars = [var_val_names[v][i] for i in range (highest_val+1,len(var_val_positions[v]))]
        return good_vars




def get_good_vars1(v,invars,bayesianNetwork,var_val_positions = None, var_val_names = None):
        print ("v")
        print(v)
        print("invars")
        print(invars)
    
    
        if var_val_positions is None:    
            var_val_positions = get_var_val_positions(bayesianNetwork)
        if var_val_names is None:
            var_val_names= get_var_val_names(bayesianNetwork)
        print("var_val_positions")
        print(var_val_positions)
        print("var_val_names")
        print(var_val_names)
        highest_val = 0
        for tup in invars:
            if v in tup[0]:
                for val in tup[0][v]:
                    if var_val_positions[v][val]>highest_val:
                        highest_val = var_val_positions[v][val]
        print("highest_val")
        print(highest_val)
        good_vars = [var_val_names[v][i] for i in range (highest_val+1,len(var_val_positions[v]))]
        return good_vars


def get_rr_vals(v,invars):
        rr_vals = {}
        for tup in invars:
            if v in tup[0]:
                for val in tup[0][v]:
                    if "relative_risk" in tup[1]:
                        rr_vals[val]=tup[1]["relative_risk"]
        return rr_vals


def replace_rr(invars,new_rr,v,val):
        #print("v")
        #print(v)
        #print("val")
        #print(val)
        for tup in invars:
            if v in tup[0] and val in tup[0][v] and "relative_risk" in tup[1]:
                tup[1]["relative_risk"]=new_rr


def dependency (bayesianNetwork, cpt, invars,outvars, calibrate = True,adjust=False):
        #convert all relative risks to relatvie risk direct.  sort the net by the rr invars place in the tree
        #starting with the highest level in the dag first,
        #and make a copy of the cpt table without each rr variable, add it to the net and get the value of the outvars
        #when he rr var is set, and then whem the best var is set.  the new RR val is then CPT(novar) good * RR / CPT(novar)var turned on
        #add the new RR to the CPT you are constructing , and then compile it
        #
        #First get list of variables and sort according to tree level
        priors = None 
        print("start timing...")
        tic = time.perf_counter()
        varlist=[list(tup[0].keys())[0] for tup in invars if "relative_risk" in tup[1]]
        varlist = list(set(varlist))
        #print("varlist")
        #print(varlist)
        #print("outvars")
        #print(outvars)
        if len(varlist) > 0 and calibrate:
            prevalence_condition_regardless = list(outvars.items())[0][1]
            priors = get_priors(bayesianNetwork,invars,prevalence_condition_regardless,cpt,adjust)
            var_val_positions = get_var_val_positions(bayesianNetwork)
            var_val_names= get_var_val_names(bayesianNetwork)
            copyNetwork = copy.deepcopy(bayesianNetwork)
            #print("cpt")
            #print(cpt)
            copyCPT = copy.deepcopy(cpt)
            discreteDistribution = copyNetwork.discreteDistributions.add()
            discreteDistribution.name = "always_true"
            variable = discreteDistribution.variables.add()
            variable.name = "always_true"
            variable.probability = 0.99999
            variable = discreteDistribution.variables.add()
            variable.name = "no_always_true"
            variable.probability = 0.00001
            #print("copyNetwork")
            #print(copyNetwork)
            newInvars = copy.deepcopy(invars)
            newInvars.append(({'always_true': ['always_true']}, {'relative_risk':1.0}))
            #print ("newInvars")
            #print(newInvars)
            outvar = list(outvars.items())[0][0]
            df = make_tree(bayesianNetwork,False)
            #print("df")
            #print(df)
            order_dict = {}
            
            for i in range(len(df.columns)):
                order_dict[i]=[]
                colname = "level"+str(i)
                for v in varlist:
                    #print("df[colname].tolist()")
                    #print(df[colname].tolist())
                    if v in df[colname].tolist():
                        order_dict[i].append(v)
            #print("order_dict")
            #print(order_dict)
            low_rrs =[] 
            for i in range(len(order_dict)):
                for v in order_dict[i]:
                    #print("v")
                    #print(v)
                    thisNetwork = copy.deepcopy(copyNetwork)
                    for  j in range(len(newInvars)):
                       # print("newInvars[j][0]")
                       # print(newInvars[j][0])
                        if v in newInvars[j][0]:
                            copyInvars = copy.deepcopy(newInvars)
                            popped = copyInvars.pop(j)
                            count = 0
                            for  l in range(len(copyInvars)):
                                if v in copyInvars[l][0]:
                                    count += 1
                            for k in range (count): 
                                for l in range (len(copyInvars)):
                                    if v in copyInvars[l][0]:
                                        copyInvars.pop(l)
                                        break
                            #print("copyInvars")
                            #print(copyInvars)
                            #print("thisNetwork")
                            #print(thisNetwork)
                            copyCPT[outvar]= dependency_direct(thisNetwork,{},copyInvars,outvars)

                            addCpt(thisNetwork,copyCPT)
                            copied = bayesInitialize(thisNetwork)
                            copied.bake()
                            var_val_names_this = get_var_val_names(thisNetwork)
                            good_vars = get_good_vars(v,invars,bayesianNetwork,var_val_positions,var_val_names) 
                            chance_of_outvar_given_good = 0.
                            outvar_chance_dict = {}
                            for g in good_vars:
                                #print ("g")
                                #print (g)
                                chance_of_outvar = query(copied,thisNetwork,{v:g},[outvar],adjust)
                                #print(chance_of_outvar)
                                #print ("var_val_names")
                                #print(var_val_names)
                                #print ("chance_of_outvar[outvar][var_val_names_this[outvar][0]]")
                                #print (chance_of_outvar[outvar][var_val_names_this[outvar][0]])
                                outvar_chance_dict [g]= chance_of_outvar[outvar][var_val_names_this[outvar][0]]#list(chance_of_outvar[outvar].values())[0]
                            prior_sum = 0
                            for val,outvar_chance in outvar_chance_dict.items():
                                chance_of_outvar_given_good += outvar_chance * priors[v][val]
                                prior_sum += priors[v][val]
                            chance_of_outvar_given_good /= prior_sum
                            #print ("chance_of_outvar_given_good")
                            #print(chance_of_outvar_given_good)
                            rr = popped [1]["relative_risk"]
                            chance_of_outvar_given_var = 0.
                            outvar_chance_dict = {}
                            for val in newInvars[j][0][v]:
                                #print("val")
                                #print(val)
                                chance_of_outvar = query(copied,thisNetwork,{v:val}, [outvar],adjust)
                                #print ("chance_of_outvar[outvar][var_val_names_this[outvar][0]]")
                                #print (chance_of_outvar[outvar][var_val_names_this[outvar][0]])
                                outvar_chance_dict[val] = chance_of_outvar[outvar][var_val_names_this[outvar][0]]#list(chance_of_outvar[outvar].values())[0]
                            prior_sum = 0
                            for val,outvar_chance in outvar_chance_dict.items():
                                chance_of_outvar_given_var += outvar_chance * priors[v][val]
                                prior_sum += priors[v][val]
                            #print ("chance_of_outvar_given_var")
                            #print(chance_of_outvar_given_var)
                            new_rr = (chance_of_outvar_given_good * rr* prior_sum)/chance_of_outvar_given_var
                            #print ("rr")
                            #print (rr)
                            #print("new_rr")
                            #print (new_rr)
                            if new_rr > .9 and new_rr < 1.1:
                                low_rrs.append(popped)
                            elif abs(rr-new_rr)>.1:
                                #print ("newInvars before replace")
                                #print (newInvars)
                                replace_rr(newInvars,new_rr,v,val)
                                #print ("newInvars after replace")
                                #print (newInvars)
            for  j in range(len(newInvars)):
                if "always_true"  in newInvars[j][0]:
                    newInvars.pop(j)
                    break
           # print ("newInvars before removing new ones")
           # print (newInvars)
           # print ("low_rrs")
           # print (low_rrs)
            for low in low_rrs:
                try:
                    newInvars.remove(low)
                except ValueError as ve:
                    #print(ve)
                    pass
            #print ("invars")
            #print(invars)
            #print("newInvars")
            #print(newInvars)
        else:
            newInvars = invars

        cpt_rows,keylist,outvars,description= dependency_direct(bayesianNetwork,cpt,newInvars,outvars,priors)

        toc = time.perf_counter()
        diff = toc - tic

        print (f"{outvars}  wrapper took {diff} seconds")
        return (cpt_rows,keylist,outvars,description)


def align_ci(ci,amt):
    ci_z= {80:1.282,85:1.440,90:1.645,95:1.960,99:2.576,99.5:2.807,99.9:3.291}
    new_amt = amt if ci == 99.9 else ci_z[99.9]*amt/ci_z[ci]
    return new_amt

def normalize_ci(maxi,window_dict):
    factor=1.0/maxi
    new_dict = {k: v*factor for k, v in window_dict.items() }
    return new_dict

def get_window(bayesianNetwork,invars):
        var_val_positions = get_var_val_positions(bayesianNetwork)
        window = {}
        for vardict,numval_dict in invars:
            for var, vallist in vardict.items():
                if "ci" in numval_dict:
                    if var not in window:
                        window[var] = {}
                    for val in vallist:
                        window[var][val]= align_ci(numval_dict["ci"],numval_dict["plus_minus"])
                    #print("window")
                    #print(window)
                    maxi= max(window[var].values())
                    #print("maxi")
                    #print(maxi)
                    for val,dummy in var_val_positions[var].items():
                        if val not in window[var]:
                            window[var][val] = maxi
                    window[var] = normalize_ci(maxi,window[var])
        return(window)

def get_stat_info (k,v,invars):
        stattype = stat = ci99 = None
        for vardict,numval_dict in invars:
            if "ci" in numval_dict and k in vardict and v in vardict[k]:
                stattype = "relative_risk" if "relative_risk" in numval_dict else "specificity"
                stat = numval_dict[stattype]
                ci99 = align_ci(numval_dict["ci"],numval_dict["plus_minus"])
                break
        return stattype,stat,ci99

def validation(k,v,probagivenb,condition_val,invars,final_window,window_factor):
        #print("k")
        #print(k)
        #print("v")
        #print(v)
        #print("probagivenb")
        #print(probagivenb)
        #print("final_window")
        #print(final_window)
    
        row = {}
        stattype,stat,ci99 = get_stat_info (k,v,invars)
        if ci99 is not None:
            row["condition"]= condition_val
            row["variable"]=k
            row["value"] = v
            row["statistic"] = stattype
            row["mean"]=stat
            row["ci99"] = ci99
            row["score"] = ((probagivenb + (final_window*window_factor[k][v])) * stat/probagivenb)-stat
        return row


def dependency_direct(bayesianNetwork, cpt, invars, outvars, priors = None,adjust=False):
        import itertools
        from scipy.optimize import linprog
        from qpsolvers import solve_qp

        import time

        validation_row = {}
        print("start timing...")
        tic = time.perf_counter()
        window_factor = get_window(bayesianNetwork,invars)
        #print("window_factor")
        #print(window_factor)
        keyset = OrderedSet([])
        frequency_cache = {}
        prevalence_condition_regardless = list(outvars.items())[0][1]
        condition_val = list(outvars.items())[0][0]
        if priors is None:
            priors = get_priors(bayesianNetwork,invars,prevalence_condition_regardless,cpt,adjust)
        #print("priors")
        #print(priors)
        prob_a_given_b, prob_a_given_not_b, prob_not_a_given_b, prob_not_a_given_not_b =  prob_a_and_not_a_given_b_and_not_b (invars, priors, outvars)

        description = "Against the baseline risks, "
        firsttime = True
        for k,v in outvars.items():                        
                phrase = "" if firsttime else " and "
                description + phrase + k + " of " + str(v) + " , "
                firsttime = False
        firsttime = True
        for vardict,numval_dict in invars:
                for val, varlist in vardict.items():
                        for test,num in numval_dict.items():
                                keyset.add(val)
                                phrase = "" if firsttime else (" , and " if varlist [-1] is val else " , " )

                                description= description + phrase + "the "+ test.replace("_"," ")  +" that {0} will be " + condition_val +" for those in the " + val + " category of " 
                                firsttime1 = True
                                sum_priors = 0
                                for var in varlist:                                
                                        phrase = "" if firsttime1 else " or "
                                        description = description + phrase + var
                                        firsttime1 = False
                                        #print("val var to priors")
                                        #print (f"{val}  : {var}")
                                        sum_priors += priors[val][var]
                                description = description + " is " + str(num)

                                firsttime = False
                                        
        description = description + "."
        
        #print("prob_a_given_not_b")
        #print (prob_a_given_not_b)
        #print("prob_a_given_b")
        #print(prob_a_given_b)


        #print("prob_not_a_given_not_b")
        #print (prob_not_a_given_not_b)
        #print("prob_not_a_given_b")
        #print(prob_not_a_given_b)

        keylist = list(keyset)
        pos = {k:n for n,k in enumerate(keylist)}
        vdict = dictVarsAndValues(bayesianNetwork, cpt)

        #print("vdict")
        #print(vdict)
        val_prev = {}
        not_val_prev = {}
        for k in keylist:
                val_prev[k]={}
                not_val_prev[k] = {}
                previous = None
                previous_not = None
                for v in vdict[k]:
                        #natural order is worse to better, and we want to fill in worse first because better is more accurate
                        if k in prob_a_given_b and v in prob_a_given_b[k]:
                                val_prev[k][v] = prob_a_given_b[k][v] 
                                previous = prob_a_given_not_b[k][v]
                        elif previous is not None:
                                val_prev [k][v] = previous
                        else:
                                val_prev [k][v] = prevalence_condition_regardless
                        if k in prob_not_a_given_b and v in prob_not_a_given_b[k]:
                                not_val_prev[k][v] = prob_not_a_given_b[k][v] 
                                previous_not = prob_not_a_given_not_b[k][v]
                        elif previous_not is not None:
                                not_val_prev [k][v] = previous_not
                        else:
                                not_val_prev [k][v] = prevalence_condition_regardless
        #print("val_prev")                        
        #print(val_prev)                            

        vlist = [vdict[v] for v in keylist]
        #print("vlist")
        #print (vlist)
        cartesian = list(itertools.product(*vlist))
       #in cartesian, worst is first and best comes later
        cpt_rows = []
        lhs_inequality_equation1 = {}
        lhs_inequality_equation2 = {}
        lhs_inequality_equation3 = {}
        lhs_inequality_equation4 = {}
        rhs_inequality_equation1 = {}
        rhs_inequality_equation2 = {}
        rhs_inequality_equation3 = {}
        rhs_inequality_equation4 = {}
        obj = np.ones(2*len(cartesian))

        frequencies = get_frequencies(bayesianNetwork,keylist,cpt,adjust)
        #print ("frequencies")
        #print(frequencies)
        #bnd = [(1.0,1.0)] * len(cartesian)
        bnd = []
 
        lhs_eq = []
        rhs_eq = []
                                
        included_vars = {}                        
        for excluded in keylist:
            included_vars[excluded]= keylist[:pos[excluded]] + keylist[pos[excluded]+1:] 
        for i,c in enumerate(cartesian):
                #print ("i:c")
                #print (i)
                #print (c)
                #print ("frequencies[c]")
                #print(frequencies[c])
                #equation1  (doesnt have every one in it )
                #non elderly hbp prevalence  = 
                #  (prevalence of hbp among adult obese psych) * prevalence of adult obese psych 
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
                #+ (prevalence of hbp among adult obese nonpsych) * prevalence of adult obese nonpsych 
                #+ (prevalence of hbp among youngadult obese nonpsych) * prevalence of youngadult obese nonpsych
                #+ (prevalence of hbp among teen obese nonpsych) * prevalence of teen obese nonpsych
                #+ (prevalence of hbp among child obese nonpsych) * prevalence of child obese nonpsych
                #+ (prevalence of hbp among adult overweight nonpsych) * prevalence of adult overweight nonpsych
                #+ (prevalence of hbp among youngadult overweight nonpsych) * prevalence of youngadult overweight nonpsych
                #+ (prevalence of hbp among teen overweight nonpsych) * prevalence of teen overweight nonpsych
                #+ (prevalence of hbp among child overweight nonpsych) * prevalence of child overweight nonpsych
                #+ (prevalence of hbp among adult healthy nonpsych) * prevalence of adult healthy nonpsych
                #+ (prevalence of hbp among youngadult healthy nonpsych) * prevalence of youngadult healthy nonpsych
                #+ (prevalence of hbp among teen healthy nonpsych) * prevalence of teen healthy nonpsych
                #+ (prevalence of hbp among child healthy nonpsych) * prevalence of child healthy nonpsych
                         
                         
                #equation2 (has the balance)         
                #elderly hbp prevalence  = 
                #  (prevalence of hbp among elderly obese psych) * prevalence of elderly obese psych 
                #+ (prevalence of hbp among elderly overweight psych) * prevalence of elderly overweight psych
                #+ (prevalence of hbp among elderly healthy psych) * prevalence of elderly healthy psych
                #+ (prevalence of hbp among elderly obese nonpsych) * prevalence of elderly obese nonpsych 
                #+ (prevalence of hbp among elderly overweight nonpsych) * prevalence of elderly overweight nonpsych
                #+ (prevalence of hbp among elderly healthy nonpsych) * prevalence of elderly healthy nonpsych
                
                 
                #equation3  (doesnt have every one in it )
                #non elderly non hbp prevalence  = 
                #  (prevalence of non hbp among adult obese psych) * prevalence of adult obese psych 
                #+ (prevalence of non hhbp among youngadult obese psych) * prevalence of youngadult obese psych
                #+ (prevalence of non hhbp among teen obese psych) * prevalence of teen obese psych
                #+ (prevalence of non hhbp among child obese psych) * prevalence of child obese psych
                #+ (prevalence of non hbp among adult overweight psych) * prevalence of adult overweight psych
                #+ (prevalence of non hbp among youngadult overweight psych) * prevalence of youngadult overweight psych
                #+ (prevalence of non hbp among teen overweight psych) * prevalence of teen overweight psych
                #+ (prevalence of non hbp among child overweight psych) * prevalence of child overweight psych
                #+ (prevalence of non hbp among adult healthy psych) * prevalence of adult healthy psych
                #+ (prevalence of non hbp among youngadult healthy psych) * prevalence of youngadult healthy psych
                #+ (prevalence of non hbp among teen healthy psych) * prevalence of teen healthy psych
                #+ (prevalence of non hbp among child healthy psych) * prevalence of child healthy psych
                #+ (prevalence of non hbp among adult obese nonpsych) * prevalence of adult obese nonpsych 
                #+ (prevalence of non hbp among youngadult obese nonpsych) * prevalence of youngadult obese nonpsych
                #+ (prevalence of non hbp among teen obese nonpsych) * prevalence of teen obese nonpsych
                #+ (prevalence of non hbp among child obese nonpsych) * prevalence of child obese nonpsych
                #+ (prevalence of non hbp among adult overweight nonpsych) * prevalence of adult overweight nonpsych
                #+ (prevalence of non hbp among youngadult overweight nonpsych) * prevalence of youngadult overweight nonpsych
                #+ (prevalence of non hbp among teen overweight nonpsych) * prevalence of teen overweight nonpsych
                #+ (prevalence of non hbp among child overweight nonpsych) * prevalence of child overweight nonpsych
                #+ (prevalence of non hbp among adult healthy nonpsych) * prevalence of adult healthy nonpsych
                #+ (prevalence of non hbp among youngadult healthy nonpsych) * prevalence of youngadult healthy nonpsych
                #+ (prevalence of non hbp among teen healthy nonpsych) * prevalence of teen healthy nonpsych
                #+ (prevalence of non hbp among child healthy nonpsych) * prevalence of child healthy nonpsych
                         
                         
                #equation4 (has the balance)         
                #elderly with non hbp prevalence = 
                #  (prevalence of non hbp among elderly obese psych) * prevalence of elderly obese psych 
                #+ (prevalence of non hbp among elderly overweight psych) * prevalence of elderly overweight psych
                #+ (prevalence of non hbp among elderly healthy psych) * prevalence of elderly healthy psych
                #+ (prevalence of non hbp among elderly obese nonpsych) * prevalence of elderly obese nonpsych 
                #+ (prevalence of non hbp among elderly overweight nonpsych) * prevalence of elderly overweight nonpsych
                #+ (prevalence of non hbp among elderly healthy nonpsych) * prevalence of elderly healthy nonpsych
                
                #equations 1-4 are inequalities, but then there are c equalities , equations that say prob a + ~prob a == 1

                rhs_eq.append(1.)
                lhs_eq_list = np.zeros(2*len(cartesian))
                lhs_eq_list[i]=1.
                lhs_eq_list[i+len(cartesian)]=1.
                lhs_eq.append(lhs_eq_list)

               
                for vardict,numval_dict in invars:
                        #relative_risk = numval_dict["relative_risk"] if "relative_risk" in numval_dict else (
                        #    (prevalence_condition_regardless-numval_dict["sensitivity"])/numval_dict["sensitivity"] if "sensitivity" in numval_dict else 1) 
                        for k, varlist in vardict.items():
                        
                                if k not in lhs_inequality_equation1:
                                        lhs_inequality_equation1[k] = {}
                                if k not in lhs_inequality_equation2:
                                        lhs_inequality_equation2[k] = {}
                                if k not in lhs_inequality_equation3:
                                        lhs_inequality_equation3[k] = {}
                                if k not in lhs_inequality_equation4:
                                        lhs_inequality_equation4[k] = {}
                                if k not in rhs_inequality_equation1:
                                        rhs_inequality_equation1[k] = {}
                                if k not in rhs_inequality_equation2:
                                        rhs_inequality_equation2[k] = {}
                                if k not in rhs_inequality_equation3:
                                        rhs_inequality_equation3[k] = {}
                                if k not in rhs_inequality_equation4:
                                        rhs_inequality_equation4[k] = {}
                

                                for v in varlist:
                                        if v not in lhs_inequality_equation1[k]:
                                                lhs_inequality_equation1[k][v] = np.zeros(2*len(cartesian),np.double) #lhs will be list of lists
                                        if v not in lhs_inequality_equation2[k]:
                                                lhs_inequality_equation2[k][v] = np.zeros(2*len(cartesian),np.double)
                                        if v not in lhs_inequality_equation3[k]:
                                                lhs_inequality_equation3[k][v] = np.zeros(2*len(cartesian),np.double) #lhs will be list of lists
                                        if v not in lhs_inequality_equation4[k]:
                                                lhs_inequality_equation4[k][v] = np.zeros(2*len(cartesian),np.double)
                                        if v not in rhs_inequality_equation1[k]:
                                                rhs_inequality_equation1[k][v] = 0 #rhs will be list of floats
                                        if v not in rhs_inequality_equation2[k]:
                                                rhs_inequality_equation2[k][v] = 0
                                        if v not in rhs_inequality_equation3[k]:
                                                rhs_inequality_equation3[k][v] = 0 #rhs will be list of floats
                                        if v not in rhs_inequality_equation4[k]:
                                                rhs_inequality_equation4[k][v] = 0
                                        #print ("c[pos[k]]")
                                        #print (c[pos[k]])
                                        #tup1 = included_vars[k].copy().sort() if len(included_vars[k]) > 0 else ()
                                        #input_tuple = (tup1,v)
                                        #if input_tuple not in frequency_cache:
                                            #prob_others_given_b = get_frequencies(bayesianNetwork,included_vars[k],cpt,preconditionals = {k:v})
                                            #frequency_cache[input_tuple] = prob_others_given_b
                                            #print (f"{input_tuple} stored in frequency cache")
                                        #else:
                                            #prob_others_given_b = frequency_cache[input_tuple]
                                            #print(f"{input_tuple} retrieved from frequency cache of size {len(frequency_cache)}")
                                        #print ("prob_others_given_b")
                                        #print (prob_others_given_b)
                                        #c_no_k = c[:pos[k]]+c[pos[k]+1:]
                                        if c[pos[k]]  == v:
                                                # rhs_equality_equation2[k][v] = priors[k][v]*relative_risk* val_prev[k][v]
                                                rhs_inequality_equation2[k][v] = prob_a_given_b [k][v]
                                                lhs_inequality_equation2[k][v][i] = np.double(frequencies[c]) #prob_others_given_b[c_no_k]
                                                rhs_inequality_equation4[k][v] = prob_not_a_given_b [k][v]  
                                                lhs_inequality_equation4[k][v][i+len(cartesian)] = np.double(frequencies[c])#prob_others_given_b[c_no_k]
                                        else:
                                                # rhs_equality_equation1[k][v] = val_prev[k][v]
                                                rhs_inequality_equation1[k][v] = prob_a_given_not_b[k][v]
                                                lhs_inequality_equation1[k][v][i] = np.double(frequencies[c])  #prob_others_given_b[c_no_k]
                                                rhs_inequality_equation3[k][v] =  prob_not_a_given_not_b [k][v] 
                                                lhs_inequality_equation3[k][v][i+len(cartesian)] = np.double(frequencies[c] )#prob_others_given_b[c_no_k]
                                                                                       

                #make independence the lower bound
                #product = 1
                #for j,k in enumerate(keylist):
                        #product *= 1.-val_prev [k][c[j]] 
                #bnd.append(( 1-product, 1.0))

                minimum = 1.0
                for j,k in enumerate(keylist):
                        if val_prev [k][c[j]] < minimum:
                            minimum = val_prev [k][c[j]]
                #bnd.append((minimum, 1.0))
                bnd.append((0,1.0))

        for i,c in enumerate(cartesian):
                minimum_not = 1.0
                for j,k in enumerate(keylist):
                        if not_val_prev [k][c[j]] < minimum_not:
                            minimum_not = not_val_prev [k][c[j]]
                #bnd.append((minimum_not, 1.0))
                bnd.append((0, 1.0))

        size = 2*len(cartesian)

        #P = np.ones((size,size),np.double)
        #for i in range(size):
                #P[i][i] = 0.
                #for j in range(size):
                    #if i >= size/2 and j< size/2 or j >= size/2 and i < size/2:
                       # P[i][j] = 0.
        P = np.identity(size,np.double) 
        for i in range(len(cartesian)):
                P[i][i] = np.double(i+1)
        for i in range(len(cartesian),size):
                P[i][i] = np.double(size-i)
   
        q = np.zeros (size,np.double)	
        lb = np.zeros(size,np.double)
        ub = np.ones(size,np.double)

        #print("before norm:")       
        #print("rhs_inequality_equation2") 
        #print(rhs_inequality_equation2) 
        #print("lhs_inequality_equation2")
        #print(lhs_inequality_equation2)
        #print("rhs_inequality_equation4") 
        #print(rhs_inequality_equation4) 
        #print("lhs_inequality_equation4")
        #print(lhs_inequality_equation4)
        #print("rhs_inequality_equation1")
        #print(rhs_inequality_equation1)
        #print("lhs_inequality_equation1")
        #print(lhs_inequality_equation1)
        #print("rhs_inequality_equation3")
        #print(rhs_inequality_equation3)
        #print("lhs_inequality_equation3")
        #print(lhs_inequality_equation3)
                                               


        for vardict,numval_dict in invars:
                for k, varlist in vardict.items():
                    for v in varlist:
                        norm = np.sum(lhs_inequality_equation1[k][v])
                        lhs_inequality_equation1[k][v]=lhs_inequality_equation1[k][v]/norm
                        norm = np.sum(lhs_inequality_equation2[k][v])
                        lhs_inequality_equation2[k][v]=lhs_inequality_equation2[k][v]/norm
                        norm = np.sum(lhs_inequality_equation3[k][v])
                        lhs_inequality_equation3[k][v]=lhs_inequality_equation3[k][v]/norm
                        norm = np.sum(lhs_inequality_equation4[k][v])
                        lhs_inequality_equation4[k][v]=lhs_inequality_equation4[k][v]/norm

        #We also want to include that the first half adds to the prevaence of a and the sencond to the prevalence of ~a


        rhs_eq.append(prevalence_condition_regardless)
        rhs_eq.append(1.-prevalence_condition_regardless)
        prev_a = np.zeros(2*len(cartesian),np.double)
        prev_not_a = np.zeros(2*len(cartesian),np.double)
        for i,c in enumerate(cartesian):
                prev_a[i]=np.double(frequencies[c])
                prev_not_a [i+len(cartesian)] = np.double(frequencies[c])
        lhs_eq.append(prev_a)
        lhs_eq.append(prev_not_a)

        #print("after norm:")       
        #print("rhs_inequality_equation2") 
        #print(rhs_inequality_equation2) 
        #print("lhs_inequality_equation2")
        #print(lhs_inequality_equation2)
        #print("rhs_inequality_equation4") 
        #print(rhs_inequality_equation4) 
        #print("lhs_inequality_equation4")
        #print(lhs_inequality_equation4)
        #print("rhs_inequality_equation1")
        #print(rhs_inequality_equation1)
        #print("lhs_inequality_equation1")
        #print(lhs_inequality_equation1)
        #print("rhs_inequality_equation3")
        #print(rhs_inequality_equation3)
        #print("lhs_inequality_equation3")
        #print(lhs_inequality_equation3)
                                               


        #window = 1.0
        window = 1.0
        #cut = 1.0
        cut = 1.0
        lastTrue = None
        #At first test window at 1.0 to ensure that there is a solution at all , then narrow down on it with binary search to get the smallest feasable window
        #while cut > 0.05: 
        while cut > 0.0005:                                
                lhs_ineq = []
                rhs_ineq = []
               # ls_R=np.zeros((size,size),np.double) 
               # ls_s=np.zeros (size,np.double)	
                ls_R=[]
                ls_s=[]
                    
                for vardict,numval_dict in invars:
                        #relative_risk= numval_dict["relative_risk"] if "relative_risk" in numval_dict else (
                         #           (prevalence_condition_regardless-numval_dict["sensitivity"])/numval_dict["sensitivity"] if "sensitivity" in numval_dict else 1) 
                        for k, varlist in vardict.items():
                                if k not in validation_row:
                                    validation_row[k] = {}
                                for v in varlist:
                                        ci_window = window *window_factor[k][v] if k in window_factor and v in window_factor[k] else window
                                        #equality doesnt work
                                        #lhs_eq.append(lhs_equality_equation1[k][v])
                                        #rhs_eq.append(rhs_equality_equation1[k][v])
                                        #lhs_eq.append(lhs_equality_equation2[k][v])
                                        #rhs_eq.append(rhs_equality_equation2[k][v])
                                        
                                        #UB

                                        rhs_ineq1 = 0. if rhs_inequality_equation1[k][v]+ ci_window < 0 else (
                                                1. if rhs_inequality_equation1[k][v] + ci_window > 1 else rhs_inequality_equation1[k][v]+ci_window )
                                        rhs_ineq2 = 0. if rhs_inequality_equation2[k][v] + ci_window  < 0 else (
                                                1. if rhs_inequality_equation2[k][v] + ci_window >  1 else rhs_inequality_equation2[k][v]+ ci_window) 
                                        rhs_ineq3 = 0. if rhs_inequality_equation3[k][v]+ ci_window < 0 else (
                                                1. if rhs_inequality_equation3[k][v] + ci_window > 1 else rhs_inequality_equation3[k][v]+ci_window )
                                        rhs_ineq4 = 0. if rhs_inequality_equation4[k][v] + ci_window < 0 else (
                                                1. if rhs_inequality_equation4[k][v] + ci_window > 1 else rhs_inequality_equation4[k][v]+ci_window )

                                        lhs_ineq.append(np.multiply(lhs_inequality_equation1[k][v],1.))
                                        rhs_ineq.append(rhs_ineq1)
                                        lhs_ineq.append(np.multiply(lhs_inequality_equation2[k][v],1.))
                                        rhs_ineq.append(rhs_ineq2)
                                        lhs_ineq.append(np.multiply(lhs_inequality_equation3[k][v],1.))
                                        rhs_ineq.append(rhs_ineq3)
                                        lhs_ineq.append(np.multiply(lhs_inequality_equation4[k][v],1.))
                                        rhs_ineq.append(rhs_ineq4)


                                        #LB
 
                                        rhs_ineq1 = 0. if rhs_inequality_equation1[k][v]- ci_window  < 0 else (
                                                1. if rhs_inequality_equation1[k][v] - ci_window  > 1 else rhs_inequality_equation1[k][v]-ci_window )
                                        rhs_ineq2 = 0. if rhs_inequality_equation2[k][v] - ci_window  < 0 else (
                                                1. if rhs_inequality_equation2[k][v] - ci_window > 1 else rhs_inequality_equation2[k][v]-ci_window )
                                        rhs_ineq3 = 0. if rhs_inequality_equation3[k][v]- ci_window  < 0 else (
                                                1. if rhs_inequality_equation3[k][v] -ci_window > 1 else rhs_inequality_equation3[k][v]-ci_window )
                                        rhs_ineq4 = 0. if rhs_inequality_equation4[k][v] - ci_window < 0 else (
                                                1. if rhs_inequality_equation4[k][v] - ci_window > 1 else rhs_inequality_equation4[k][v]- ci_window )

                                        lhs_ineq.append(np.multiply(lhs_inequality_equation1[k][v],-1.))
                                        rhs_ineq.append(-rhs_ineq1)
                                        lhs_ineq.append(np.multiply(lhs_inequality_equation2[k][v],-1.))
                                        rhs_ineq.append(-rhs_ineq2)
                                        lhs_ineq.append(np.multiply(lhs_inequality_equation3[k][v],-1.))
                                        rhs_ineq.append(-rhs_ineq3)
                                        lhs_ineq.append(np.multiply(lhs_inequality_equation4[k][v],-1.))
                                        rhs_ineq.append(-rhs_ineq4)


                                        #Objectie Function
                                        ls_R.append(np.multiply(lhs_inequality_equation1[k][v],1.))
                                        ls_s.append(rhs_inequality_equation1[k][v])
                                        ls_R.append(np.multiply(lhs_inequality_equation2[k][v],1.))
                                        ls_s.append(rhs_inequality_equation2[k][v])
                                        ls_R.append(np.multiply(lhs_inequality_equation3[k][v],1.))
                                        ls_s.append(rhs_inequality_equation3[k][v])
                                        ls_R.append(np.multiply(lhs_inequality_equation4[k][v],1.))
                                        ls_s.append(rhs_inequality_equation4[k][v])


                                        row = validation(k,v,rhs_inequality_equation2[k][v],condition_val,invars,window,window_factor)
                                        if len(row)  > 0:
                                            validation_row[k][v] = row
                                            #print("row")
                                            #print(row)
                
                #opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,method="revised simplex")
                #print ("obj")
                #print (obj)
                #print ("P")
                #print(P)
                #print ("q")
                #print (q)

                #print ("lhs_eq")
                #print(lhs_eq)
                #print("rhs_eq")
                #print (rhs_eq)

                #print ("lhs_ineq")
                #print(lhs_ineq)
                #print("rhs_ineq")
                #print (rhs_ineq)
                #print ("bnd")
                #print(bnd)
                #print ("lb")
                #print (lb)
                #print("ub")
                #print (ub)
                lhs_ineq = np.array(lhs_ineq,np.double)
                rhs_ineq = np.array(rhs_ineq,np.double)
                lhs_eq = np.array(lhs_eq,np.double)
                rhs_eq = np.array(rhs_eq,np.double)
                ls_s = np.array(ls_s,np.double)
                ls_R = np.array(ls_R,np.double)

                #print ("lhs_ineq.shape")
                #print (lhs_ineq.shape)
                #print ("rhs_ineq.shape")
                #print (rhs_ineq.shape)
                #print ("lhs_eq.shape")
                #print (lhs_eq.shape)
                #print ("rhs_eq.shape")
                #print (rhs_eq.shape)

                #print ("ls_s.shape")
                #print (ls_s.shape)
                #print ("ls_R.shape")
                #print (ls_R.shape)


                #P = np.add(np.dot(ls_R.T, ls_R), np.multiply(np.identity(size,np.double),1.)) 

                P = np.dot(ls_R.T, ls_R) 
                q = -np.dot(ls_R.T,ls_s )

                #print ("P.shape")
                #print (P.shape)
                #print ("q.shape")
                #print (q.shape)

                #print ("P")
                #print (P)
                #print ("q")
                #print (q)


                #opt = linprog(c=obj, A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,method="revised simplex")
                err = False
                opt = None
                try:
                    opt = solve_qp(P, q, lhs_ineq, rhs_ineq, lhs_eq, rhs_eq,lb,ub,solver="osqp")
                    #opt = solve_qp(P, q, lhs_ineq, rhs_ineq, lhs_eq, rhs_eq,lb,ub)
                    #opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,A_eq=lhs_eq, b_eq=rhs_eq,  bounds=bnd,method="revised simplex")
                except ValueError as ve:
                    print ("ValueError")
                    print(ve)
                    err = True

                        
                #print("opt")
                #print (opt)
                if window == 1.0 and (err) or opt is None: # or not opt.success):
                    break
                cut /= 2
                #window = window - cut if not err and opt.success else window + cut
                window = window - cut if not err  else window + cut
                if not err and opt is not None:# and opt.success:
                    lastTrue = opt
                    #print("lastTrue")
                    #print(lastTrue)
                #print("window")
                #print (window)

        if lastTrue is not None:
            opt = lastTrue
        if opt is not None:
            for i,c in enumerate(cartesian):
                    #there are only two values of outvars for relative risk
                    cpt_row = []
                    cpt_row.extend(c)
                    cpt_row.append(list(outvars.items())[0][0])
                    val = opt[i] #opt.x[i] 
                    cpt_row.append(val)
                    cpt_rows.append(cpt_row)
                    
                    cpt_row = []
                    cpt_row.extend(c)
                    cpt_row.append(list(outvars.items())[1][0])
                    val =  1.0-opt[i]#opt.x[i]
                    cpt_row.append(val)
                    cpt_rows.append(cpt_row)
        #print ("cpt_rows")
        #print(cpt_rows)
        toc = time.perf_counter()
        diff = toc - tic
        #print("validation_row")
        #print(validation_row)
        dflist = [valid_dict for k,v_dict in validation_row.items() for v, valid_dict in v_dict.items()]
        #print("dflist")
        #print(dflist)
        if len (dflist) > 0:
            df = pd.DataFrame(dflist)  
            #print(df)
            df.to_csv(f"{condition_val}_validation.csv", index = False)

        print (f"{invars} ==> {outvars} took {diff} seconds")
        return (cpt_rows,keylist,outvars,description)




