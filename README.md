# Bayesian Network Service

## Introduction

This Bayesian Net GRPC service creates a pomegranate Bayesian neural network in python, with functions to simplify the expression of manually entered rules, augment with adtk anomaly detection, and explain the result. A detailed example of its use in healthcare, specifically Covid-19, is given in the covid_bayesnet.ipynb jupyter notebook.  

Bayesian networks keep track of probabilities in data, in particular, how they have change given known facts.  The main advantage of a Bayesian network is the ability to express causal relations and perform causal types of inference on them, for example, counterfactual reasoning or "explaining away".  These type of inferences are of interest to medicine and any science in which causal reasoning is needed to determine best policy.  It works on a small abount of data, and if the relations between data are set up right, can impute data that the user has not filled in, guessing based on the data that the user has filled in.

Another advantage of the Bayesian net is that it can be used for entering expert knowledge about probabilities into an expert system as well as for either learning the details within the expert's framework, or learning an entirely new framework.  Thus, it can be used in situations where there is no data at first, but as more data comes in the expert's opinions of the data can be gradually replaced with the actual probabilities associated with the data.  As even more data comes in, entirely new relations can be explored.

The advantage of including anomaly detection in the bayesian network, is that, in cases where the significance of an anomaly is unknown, it can be computed given its relation to other variables of interest.  This is true even with techniques of low sensitivity or specificity:  the better the technique is in predicting variables we care about,  the higher probabilities, however less certain techniques can be included as well.  This allows us to include new data, like that of wearables, into a calculation of risk of covid.  Although  the science is new, users can have their wearables contribute to calculating their risk of covid given other factors.

Finally, Bayesian networks are transparant and thus explainable.  We offer an explanation function, which tests the sensitivity of individual variables to outcomes of interest given facts that the user has entered.  

Our philosophy in choosing pomegranate and adtk, as well as the design of the explanation function,  is to maximize speed, enabling it to be used in user friendly apps. 

We present functions, each with one example that occurs in our covid project.  All the functions described below are located in the utils.py file.


## Functions that help to enter data

The user creates a protobuf bayesian network in a python file.  There is an option, StartNet (and EndNet) with the service to save the bayesian network users create.  Before it is saved  or used it must pass a complexity check, that it is no bigger than 300 nodes and that each variable has less than 10 values, and depends on 4 or fewer other variables for speeds sake. Then the user can add evidence and query values of interest on the saved net with AskNet.  There is a stateless version in which the net is not saved, but has to be reconstructed with every query, StatelessNet.  

Conditional Probability Tables (CPTs) are notoriously hard to fill in by hand.  We offer 4 functions (in util.py)  with which to express knowledge on the probabilistic relations between variables. In cases they dont cover, a detailed CPT can be created with CPT protobuf functions.  A good example of how these are used is in file covid_bayes.py, which creates the net that is used in notebook covid_bayesnet.ipynb.  Discrete distributions are made with protobuf functions, that tell the probability of "leaf" variables that are not derived from other variables, given no other information (the "priors").  

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
		discreteDistribution.name = "cough"
		variable = discreteDistribution.variables.add()
		variable.name = "cough_up_blood"
		variable.probability = 0.01
		variable = discreteDistribution.variables.add()
		variable.name = "cough_with_green_phlegm"
		variable.probability = 0.04
		variable = discreteDistribution.variables.add()
		variable.name = "cough_with_clear_spitum"
		variable.probability = 0.05
		variable = discreteDistribution.variables.add()
		variable.name = "no_cough"
		variable.probability = 0.90



CPTs are made from these variables and the variables in other CPTs.  We offer an "all" function, which is true when all of the input variables have values stated in a list (in this case, a python set).  This and the other functions list the output values.  If all have values in their respective lists, then the first value is true, else the second value.  "all" can thus have only two output values:  

	cpt["testing_compliance"] = all (bayesianNetwork,cpt,
		{
		"tested":{"not_tested"},
		"covid_risk":{"high_covid_risk"}
		},
		["poor_testing_compliance","testing_compliance"]
		)



we also offer an  "any" function that is true if any of the input variables have values stated in a list.  The "any" function can only have two values:  

	cpt["high_covid_risk"] =any(bayesianNetwork,cpt,
			{
			"covid_symptom_level":{"high_covid"},
			"covid_test":{"positive_covid_test"},
			"covid_environment":{"high_risk_covid_environment"}
			},
			["high_covid_risk","other_covid_risk"]
			)


We also offer an if_then_else function in which the existance of the first input variable in a stated list would set the first output value to true, and if not present, the next would be tested, etc, with the last output var set to true if none of the input were true:

	cpt["covid_symptom_level"] = if_then_else(bayesianNetwork,cpt,
			{
			"high_covid":{"high_covid"},
			"medium_covid":{"medium_covid"},
			"low_covid":{"low_covid"},
			},
			["high_covid", "medium_covid","low_covid","no_covid"]
			) 


We offer an average function "avg" , that requires that all the input variable values represent increasing or decreasing quantities and  are all put in the same "direction"  (for example, values that lower the variable of interest are on the left and those that increase the variables of interest are on the right) .  The output variable can have any number of output values.  As many bins as are values in the output variable are made, and for each row in a cartesian product of row values, the number of values in each position is added to corresponding bins.  The computed output value for the row is the max bin, or the middle of the two farthest apart but max bins in case more than one are the same max value.  For example, if the output var has 5 values, and there are 2 boolean input variables, and we are computing the output value for a row which has the first input variable as a false and the second as a true, the middle output variable 2  would be set to true.  This is because the first input var's "false" would add a 1 to output var bins 0, 1, and 2, and the second input var's "true" would add a 1 to output var bins 2, 3, and 4, so that bin 2 would be worth 2 and the rest worth 1.  

	cpt["cold_symptoms"] = avg(bayesianNetwork,cpt,
		[
		"fatigue",
		"congestion",
		"feeling_well",
		"inflammation_symptoms",
		"breathing_problems_at_night"
		],
		[ "significant_cold_symptoms","mild_cold_symptoms","no_cold_symptoms"]
		)

	
	
## The Explanation Function

The explanation function, "explain", tests the effect of each other variable in the net , when it is moved in the direction that would improve the variable of interest, on the variable of interest.  Each internal variable and modified input variable in the net is changed one value over (assuming that the variable values represent an increasing/decreasing quantity), then the output value of the variable of interest is measured and subtracted from the output value it had before the value had changed, but with the other evidence set that was set before.  The difference in probability is output :  if the probability of the value increases it would have a negative value.  However, sensitivity is what we mostly care about, and the absolute value of the output can be taken for ranking the variables of the most effect were they to change.  One may object that a good explaination needs more than one variable at a time tested.  We chose to move one only in a tradeoff, but although each variable is moved individually for speed's sake, the internal variables contain interesting combinations of variables that we care about as well, and so much is explained. We use the explanation function to rank output messages in our app, and so speed is important.


## The Anomaly Detection function

We offer three functions from the ADTK, which are sufficient for basic medical signal problems.  As no patient data is ever saved, all the data must be sent through the protobuf for individual detection.  If an anomaly is detected, a designated variable in the bayesian network is set to true (and can be observed if this variable is output). The first function, "detect_anomalies" is traditional anomaly detection, using two functions that must both have an anomaly for the anomaly to set a variable in the Bayesian network to true.    One is the interquartile, the most often used method, and the next is an autoregression, that works with cyclic data such as day and night, by subtracting off the cyclic phonemena to see the residual alone.  This is useful on signals that are very individual for a person, such as heart rate in wearables.  


	anomaly = bayesianNetwork.anomalies.add()
	anomaly.varName = "heart_rate_anomaly"
	

The second function is called from the protobuf if you send it a threshold range, and it is a straight threshold that is good for signals that are relatively consistent across people, like temperature.  


	anomaly = bayesianNetwork.anomalies.add()
	anomaly.varName = "hotspot_anomaly"
	anomaly.low = -1
	anomaly.high = 0.00007 # percent new daily cases

If you send both a threshold and a percent range, it uses both the threshold and the percent over a personal baseline, for signals like SPO2 that have a normal amount, but can be calculated from a baseline for exceptions, in this case, those with chronic conditions.  


	anomaly = bayesianNetwork.anomalies.add()
	anomaly.varName = "oxygen_anomaly"
	anomaly.high = 200
	anomaly.low =93
	anomaly.high_percent = 0.99
	anomaly.low_percent = 0.01
	
## References

Pomegranate:  https://github.com/jmschrei/pomegranate
ADTK:  https://github.com/arundo/adtk
