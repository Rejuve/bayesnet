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

	 cpt["covid_risk"] = if_then_else(bayesianNetwork,cpt,
                {
                "high_covid":{"high_covid"},
                "medium_exposure":{"medium_exposure"},
                "covid_environment":{"high_risk_covid_environment","medium_risk_covid_environment,low_risk_covid_environment"}
                },
                ["high_covid_risk", "medium_covid_risk","low_covid_risk","no_covid_risk"]
                )



We offer an average function "avg" , that requires that all the input variable values represent increasing or decreasing quantities and  are all put in the same "direction"  (for example, values that lower the variable of interest are on the left and those that increase the variables of interest are on the right) .  The output variable can have any number of output values.  As many bins as are values in the output variable are made, and for each row in a cartesian product of row values, the number of values in each position is added to corresponding bins, divided by how many bins they are being added to.  The bin that ones is the one in which half of the sum of all the bins is hit when adding the bins from left to right.  It is point where half of the area under the curve is hit, the mean. For example, if the output var has 5 values, and there are 2 boolean input variables, and we are computing the output value for a row which has the first input variable as a false and the second as a true, the middle output variable 2  would be set to true.  This is because the first input var's "false" would add a 0.33 to output var bins 0, 1, and 2, and the second input var's "true" would add a 0.33 to output var bins 2, 3, and 4.  The totals in each bin are 0:0.33, 1:0.33, 2:0.66, 3:0.33, 4:0.33.  The total is 2, half of that is one, and if you add the bins from left to right, 1 is hit in in bin 2.  

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

The explanation function, "explain", tests the effect of each other variable in the net , when it is moved in the direction that would improve the variable of interest, on the variable of interest.  Each internal variable and modified input variable in the net is changed one value over (assuming that the variable values represent an increasing/decreasing quantity), then the output value of the variable of interest is measured and subtracted from the output value it had before the value had changed, but with the other evidence set that was set before.  The difference in probability is output :  if the probability of the value increases it would have a negative value.  However, sensitivity is what we mostly care about, and the absolute value of the output can be taken for ranking the variables of the most effect were they to change.  One may object that a good explaination needs more than one variable at a time tested.  We chose to move one only in a tradeoff, but although each variable is moved individually for speed's sake, the internal variables contain interesting combinations of variables that we care about as well, and so much is explained. We use the explanation function to rank output messages in our app, and so speed is important.  The explanation function is called from the proto if a list of variables to explain is given.  Since some variables are improved when increased (such as social distancing in covid) and some are improved when lowered (such as risk of getting covid) , the default is to test what would make variable values of lower probability, and there is an option to indicate if the variables are improved when higher (ie social distancing.


	explain_results =  explain(covid,bayesianNetwork,evidence,outvars,reverse_explain_list = ['social_distancing', 'social_distancing_binary'])



## The Anomaly Detection function

To detect anomalies use detect_anomalies, a routine which will detect an anomaly in any or all of four ways: autoregression for cycle based anomaly detection, interquartile algorithms for traditional anomaly detection, hard threshold, and percentile based threshold for rule based anomaly. The user may indicate more than one, and also that an anomaly must be considered an anomaly by any of the algoritms listed or by all the algorithms listed to be output as an anomaly. The user can adjust the parameters based on the data, for example hourly readings may require a step size of 24 for autoregression cycles every 24 hours, and 7 steps may be required for a weeks worth of hourly data. The c parameter tells how far outside the sample we may want to define an anomaly. The routines output a high and low which are the percentiles it is set to find in an individual's data, or the individual's normal range as defined by the interquartile algorithms. These values are returned for explanations. The bayes net is set to have an anomaly only if there exist an anomaly in the n most recent readings. To do simple rule based threshold, set "ThresholdAD" as a detector in detect_anomalies , and to do either a threshold or a percent over a baseline, use both "ThresholdAD" and "QuantileAD", with hard threshold entered through 'high' and 'low', and percentile thresholds entered through 'high_percent' and 'low_percent', settin "is_all" to False (the default) so as to ensure that an anomaly in either algorithm would be flagged as an anomaly. This combination is useful to medicine, for example, oxygen SPO3 should be above 90, or in the case of a chronic condition, 3% above baseline. All these parameters are set in the protofile. See the ADTK documentation for more information on the parameters.  


	anomaly = bayesianNetwork.anomalies.add()
	anomaly.varName = "heart_rate_anomaly"
	




	anomaly = bayesianNetwork.anomalies.add()
	anomaly.varName = "hotspot_anomaly"
	anomaly.low = -1
	anomaly.high = 0.00007 # percent new daily cases




	anomaly = bayesianNetwork.anomalies.add()
	anomaly.varName = "oxygen_anomaly"
	anomaly.high = 200
	anomaly.low =93
	anomaly.high_percent = 0.99
	anomaly.low_percent = 0.01
	
	
	
## References

Pomegranate:  https://github.com/jmschrei/pomegranate

ADTK:  https://github.com/arundo/adtk

watch data used for anomaly detection in notebook:  https://physionet.org/content/sleep-accel/1.0.0/
