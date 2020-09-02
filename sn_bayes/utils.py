from pomegranate import DiscreteDistribution
from pomegranate import BayesianNetwork
from pomegranate import Node
from pomegranate import ConditionalProbabilityTable
import json
import copy
import pandas as pd
import sn_service.service_spec.bayesian_pb2
from sn_service.service_spec.bayesian_pb2 import Query

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
	max_size_in_bytes = 2560000,	     
	allowed_number_nodes = 300,
	allowed_number_variables= 4,
	allowed_number_variable_values= 9):

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
	for i,dist in enumerate(bayesianNetwork.discreteDistributions):
		var_positions[dist.name]=i
	start = len(var_positions)
	for j,table in enumerate(bayesianNetwork.conditionalProbabilityTables):
		var_positions[table.name] = j+ start
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



def get_evidence_and_outvars(query, bayesianNetwork):
	#print("query in get_evidence_and_outvars")
	#print(query)
	var_val_names = get_var_val_names(bayesianNetwork)
	var_names = get_var_names(bayesianNetwork)
	#print("var_names")
	#print(var_names)
	evidence_dict = {}
	for e in query.evidence:
		if e.var_num in var_names and var_names[e.var_num] in var_val_names and e.response in var_val_names[ var_names[e.var_num]]:
			var_name = var_names[e.var_num]
			var_val_name = var_val_names[var_name][e.response]
			evidence_dict[var_name] = var_val_name 
	outvar_list =[var_names[o.var_num] for o in query.outvars if o.var_num in var_names]
	explainvars =[var_names[o.var_num] for o in query.explainvars if o.var_num in var_names]
	reverse_explain_list =[var_names[o.var_num] for o in query.reverse_explainvars if o.var_num in var_names]
	reverse_evidence =[var_names[o.var_num] for o in query.reverse_evidence if o.var_num in var_names]
	return(evidence_dict, outvar_list, explainvars, reverse_explain_list, reverse_evidence)

	
def create_query (bayesianNetwork,evidence_dict,outvar_list,explainvars=[],reverse_explainvars=[],reverse_evidence=[]):
	#print("evidence_dict")
	#print(evidence_dict)
	#print("outvar_list")
	#print(outvar_list)
	query = Query()
	var_val_positions = get_var_val_positions(bayesianNetwork)
	#print ("var_val_positions")
	#print (var_val_positions)
	var_positions = get_var_positions(bayesianNetwork)
	#print ("var_positions")
	#print (var_positions)
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
	return query
			


def query(baked_net, netspec, evidence,out_var_list):
	answer = {}
	var_positions = get_var_positions(netspec)
	description = baked_net.predict_proba(evidence)
	for dist_name in out_var_list:
		answer[dist_name] = (json.loads(description[var_positions[dist_name]].to_json()))['parameters'][0]
	return answer

	
def explain(baked_net, netspec, evidence,explain_list, reverse_explain_list = [], reverse_evidence = [] ):
	#explain_list lists output variables to tell what input variable would make them less likely (for example covid severity)
	#reverse_explain_list tells which of those out vars to explain more likely rather than less likely  (for example social distancing)
	#reverse_evidence_list tells which of the evidence to explain should perturb one val to the left rather than the right (the default)
	
	#first make a list of all the pertubations to make
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
		if new_pos is not None:
			new_evidence = copy.deepcopy(evidence)
			new_val = var_val_names[var][new_pos]
			new_evidence[var]=new_val
			evidence_perturbations[var]= new_evidence
			
	# add in the internal nodes that arent the input nodes
	internal_var_val_positions = get_internal_var_val_positions(netspec)
	exclusion_list = [var for var, val in internal_var_val_positions.items()]
	internal_result = query(baked_net,netspec,evidence,exclusion_list)
	
	internal_winners = {}
	for key,val_dict in internal_result.items():
		winner = max(val_dict,key=val_dict.get)
		winner_val = val_dict[winner]
		internal_winners[key] = (winner,winner_val)
	internal_evidence = {k:tup[0] for k,tup in internal_winners.items() }
	
	more_evidence = {}
	for var, val in internal_evidence.items():
		firsts = copy.deepcopy(evidence)
		more_evidence[var] = firsts.update({var:val})
	evidence_perturbations.update(more_evidence)
		
	#next run each, obtaining the values of vars to be explained.  
	#find the difference between these outputvalues and the output values from the original evidence input
	result = query(baked_net,netspec,evidence,explain_list)
	winners = {}
	explanation = {}
	for key,val_dict in result.items():
		winner = max(val_dict,key=val_dict.get)
		winner_val = val_dict[winner]
		winners[key] = (winner,winner_val)
		explanation[key] = {}
		
	
	for explaining_var, evidence in evidence_perturbations.items():
		result = query(baked_net,netspec,evidence,explain_list)
		for key in explain_list:
			diff = result[key][winners[key][0]]-winners[key][1] if key in reverse_explain_list else winners[
			key][1] - result[key][winners[key][0]]
			if diff > 0.05:
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
	for name,cpt_tuple in cpt.items():
		#print('name')
		#print(name)
		#print('cpt_tuple')
		#print(cpt_tuple)
		varsAndValues[name]= cpt_tuple[2]
	return varsAndValues

def any(bayesianNetwork, cpt, invars, outvars):
	#print (outvars)
	import itertools

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
	return (cpt_rows,keylist, outvars)



def all(bayesianNetwork, cpt, invars, outvars):
	#print (outvars)
	import itertools

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
	return (cpt_rows,keylist,outvars)


def avg(bayesianNetwork, cpt, invars, outvars):
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
			for p in addset:
				if p not in bins:
					bins[p] = 0
				bins[p]+= 1
		#print("c")
		#print(c)
		#print("bins")
		#print(bins)
		maxv = 0
		maxk = 0
		for k,v in bins.items():
			if v > maxv:
				maxv = v
				maxk = k
		mink = len(outvars)
		maxkinline = 0
		for k,v in bins.items():
			if v == maxv and k < mink:
				mink = k
			if v == maxv and k > maxkinline:
				maxkinline = k
		winner = int( (mink + maxkinline)/2.)
			
		for i,o in enumerate(outvars):
			cpt_row = []
			cpt_row.extend(c)
			cpt_row.append(o)
			val = 1.0 if (winner == i) else 0.0
			cpt_row.append(val)
			cpt_rows.append(cpt_row)
	return (cpt_rows,keylist,outvars)




def if_then_else(bayesianNetwork, cpt, invars, outvars):
	#print (outvars)
	import itertools

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
	return (cpt_rows,keylist,outvars)





def addCpt(bayesianNetwork, cpt):

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
