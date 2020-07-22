from pomegranate import DiscreteDistribution
from pomegranate import BayesianNetwork
from pomegranate import Node
from pomegranate import ConditionalProbabilityTable
import json
import service.service_spec.bayesian_pb2
from service.service_spec.bayesian_pb2 import Query

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
	return var_val_positions


def get_var_names(bayesianNetwork):
	var_names = {}
	for i,dist in enumerate(bayesianNetwork.discreteDistributions):
		var_names[i]=dist.name
	return var_names

def get_var_val_names(bayesianNetwork):
	var_val_names = {}
	for dist in bayesianNetwork.discreteDistributions:
		var_val_names[dist.name]={}
		for pos,var in enumerate(dist.variables):
			var_val_names[dist.name][pos] = var.name
	return var_val_names



def get_evidence_and_outvars(query, bayesianNetwork):
	var_val_names = get_var_val_names(bayesianNetwork)
	var_names = get_var_names(bayesianNetwork)
	evidence_dict = {}
	for e in query.evidence:
		if e.var_num in var_names and var_names[e.var_num] in var_val_names and e.response in var_val_names[ var_names[e.var_num]]:
			var_name = var_names[e.var_num]
			var_val_name = var_val_names[var_name][e.response]
			evidence_dict[var_name] = var_val_name 
	outvar_list =[var_names[o] for o in query.outvars if o in var_names]
	return(evidence_dict, outvar_list)
		
def create_query (evidence_dict, outvar_list,bayesianNetwork):
	print("evidence_dict")
	print(evidence_dict)
	print("outvar_list")
	print(outvar_list)
	query = Query()
	var_val_positions = get_var_val_positions(bayesianNetwork)
	print ("var_val_positions")
	print (var_val_positions)
	var_positions = get_var_positions(bayesianNetwork)
	print ("var_positions")
	print (var_positions)
	for k,v in evidence_dict.items():
		if k in var_positions and k in var_val_positions and v in var_val_positions[k]:
			evidence= query.evidence.add()
			evidence.var_num = var_positions[k]
			evidence.response = var_val_positions[k][v]
			print("evidence")
			print(evidence)
	for v in outvar_list:
		if v in var_positions:
			outvar = query.outvars.add()
			outvar.var_num = var_positions[v]
			print ("outvar")
			print(outvar)
	return query
			


def query(baked_net, netspec, evidence,out_var_list):
	answer = {}
	var_positions = get_var_positions(netspec)
	description = baked_net.predict_proba(evidence)
	for dist_name in out_var_list:
		answer[dist_name] = (json.loads(description[var_positions[dist_name]].to_json()))['parameters'][0]
	return answer
	

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
