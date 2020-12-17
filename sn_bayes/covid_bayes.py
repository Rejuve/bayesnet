import sn_bayes
from sn_bayes.utils import any_of
from sn_bayes.utils import all_of
from sn_bayes.utils import avg
from sn_bayes.utils import if_then_else
from sn_bayes.utils import bayesInitialize
from sn_bayes.utils import addCpt


import sn_service.service_spec.bayesian_pb2
from sn_service.service_spec.bayesian_pb2 import BayesianNetwork


def covid_bayes():
	bayesianNetwork = BayesianNetwork()



	#probabilities within distributions must sum to 1.0
	#questions left blank or "prefer not to answer" will be computed

	#anomalies
	
	anomaly = bayesianNetwork.anomalies.add()
	anomaly.varName = "oxygen_anomaly"
	anomaly.high = 200
	anomaly.low =93
	anomaly.high_percent = 0.99
	anomaly.low_percent = 0.10
	anomaly.n = 2
	anomaly.is_all = True
	detectors = anomaly.detectors.add()
	detectors.name = "QuantileAD"
	detectors = anomaly.detectors.add()
	detectors.name = "ThresholdAD"


	anomaly = bayesianNetwork.anomalies.add()
	anomaly.varName = "heart_rate_anomaly"
	anomaly.n_steps = 14
	anomaly.step_size = 24
	anomaly.c = 12.0
	anomaly.n = 24
	anomaly.window = 5
	anomaly.side = "positive"
	anomaly.is_all = False
	detectors = anomaly.detectors.add()
	detectors.name = "AutoregressionAD"
	detectors = anomaly.detectors.add()
	detectors.name = "InterQuartileRangeAD"
	detectors = anomaly.detectors.add()
	detectors.name = "LevelShiftAD"


	anomaly = bayesianNetwork.anomalies.add()
	anomaly.varName = "steps_anomaly"
	anomaly.n_steps = 14
	anomaly.step_size = 24
	anomaly.c = 12.0
	anomaly.n = 2
	anomaly.window = 4
	anomaly.side = "positive"
	anomaly.is_all = False 
	detectors = anomaly.detectors.add()
	detectors.name = "AutoregressionAD"
	detectors = anomaly.detectors.add()
	detectors.name = "InterQuartileRangeAD"
	detectors = anomaly.detectors.add()
	detectors.name = "LevelShiftAD"


	anomaly = bayesianNetwork.anomalies.add()
	anomaly.varName = "hotspot_anomaly"
	anomaly.low = -1
	anomaly.high = 0.00007 # percent new daily cases
	anomaly.n = 30 
	detectors = anomaly.detectors.add()
	detectors.name = "ThresholdAD"


	anomaly = bayesianNetwork.anomalies.add()
	anomaly.varName = "heart_rate_variability_anomaly"
	anomaly.n_steps = 14
	anomaly.step_size = 24
	anomaly.c = 12.0 
	anomaly.n = 24
	anomaly.window = 5
	anomaly.side = "positive"
	anomaly.is_all = False 
	detectors = anomaly.detectors.add()
	detectors.name = "AutoregressionAD"
	detectors = anomaly.detectors.add()
	detectors.name = "InterQuartileRangeAD"
	detectors = anomaly.detectors.add()
	detectors.name = "LevelShiftAD"


        #tests


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "cough_test"
	variable = discreteDistribution.variables.add()
	variable.name = "positive_cough_test"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "negative_cough_test"
	variable.probability = 0.95

	
	# basics/demographics questions 


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "age"
	variable = discreteDistribution.variables.add()
	variable.name = "elderly"
	variable.probability = 0.1
	variable = discreteDistribution.variables.add()
	variable.name = "adult"
	variable.probability = 0.2
	variable = discreteDistribution.variables.add()
	variable.name = "young_adult"
	variable.probability = 0.3
	variable = discreteDistribution.variables.add()
	variable.name = "teen"
	variable.probability = 0.2
	variable = discreteDistribution.variables.add()
	variable.name = "child"
	variable.probability = 0.2


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "sex"
	variable = discreteDistribution.variables.add()
	variable.name = "male"
	variable.probability = 0.5
	variable = discreteDistribution.variables.add()
	variable.name = "female"
	variable.probability = 0.5



	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "height_in_feet"
	variable = discreteDistribution.variables.add()
	variable.name = "height_above_seven"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "height_six_to_seven"
	variable.probability = 0.25
	variable = discreteDistribution.variables.add()
	variable.name = "height_five_to_six"
	variable.probability = 0.3
	variable = discreteDistribution.variables.add()
	variable.name = "height_four_to_five"
	variable.probability = 0.15
	variable = discreteDistribution.variables.add()
	variable.name = "height_under_four"
	variable.probability = 0.25


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "weight_in_pounds"
	variable = discreteDistribution.variables.add()
	variable.name = "weight_over_250"
	variable.probability = 0.15
	variable = discreteDistribution.variables.add()
	variable.name = "weight_175_to_250"
	variable.probability = 0.15
	variable = discreteDistribution.variables.add()
	variable.name = "weight_125_to_175"
	variable.probability = 0.20
	variable = discreteDistribution.variables.add()
	variable.name = "weight_100_to_125"
	variable.probability = 0.25
	variable = discreteDistribution.variables.add()
	variable.name = "weight_under_100"
	variable.probability = 0.25



#cardiovascular_disease 9%
#https://www.sciencedaily.com/releases/2019/01/190131084238.htm

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "cardiovascular_disease"
	variable = discreteDistribution.variables.add()
	variable.name = "cardiovascular_disease"
	variable.probability = 0.09
	variable = discreteDistribution.variables.add()
	variable.name = "no_cardiovascular_disease"
	variable.probability = 0.91
	
	
#diabetes 12%
#https://www.healio.com/news/endocrinology/20200730/prevalence-of-diabetes-hypertension-among-covid19-patients-likely-lower-than-reported

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "diabetes"
	variable = discreteDistribution.variables.add()
	variable.name = "diabetes"
	variable.probability = 0.12
	variable = discreteDistribution.variables.add()
	variable.name = "no_diabetes"
	variable.probability = 0.88
	
#hypertension 17%
#https://www.healio.com/news/endocrinology/20200730/prevalence-of-diabetes-hypertension-among-covid19-patients-likely-lower-than-reported

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "hypertension"
	variable = discreteDistribution.variables.add()
	variable.name = "hypertension"
	variable.probability = 0.17
	variable = discreteDistribution.variables.add()
	variable.name = "no_hypertension"
	variable.probability = 0.83

#37M/328M = 11%
#https://www.lung.org/about-us/mission-impact-and-history/our-impact

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "lung_disease"
	variable = discreteDistribution.variables.add()
	variable.name = "lung_disease"
	variable.probability = 0.11
	variable = discreteDistribution.variables.add()
	variable.name = "no_lung_disease"
	variable.probability = 0.89
	
#kidney disease = 14%
#https://www.niddk.nih.gov/health-information/health-statistics/kidney-disease#:~:text=The%20overall%20prevalence%20of%20CKD,661%2C000%20Americans%20have%20kidney%20failure.

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "kidney_disease"
	variable = discreteDistribution.variables.add()
	variable.name = "kidney_disease"
	variable.probability = 0.14
	variable = discreteDistribution.variables.add()
	variable.name = "no_kidney_disease"
	variable.probability = 0.86

#cancer = 5.5%
#https://ourworldindata.org/cancer#:~:text=Prevalence%20of%20cancer%20ranges%20from,countries%20shown%20in%20light%20yellow.

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "cancer"
	variable = discreteDistribution.variables.add()
	variable.name = "cancer"
	variable.probability = 0.055
	variable = discreteDistribution.variables.add()
	variable.name = "no_cancer"
	variable.probability = 0.945
	
#immunocompromised=2.7%
#https://www.healio.com/news/infectious-disease/20161101/nearly-3-of-us-adult-population-immunosuppressed#:~:text=Among%20them%2C%202.8%25%20(n,CI%2C%202.9%2D3.3).

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "immunocompromised"
	variable = discreteDistribution.variables.add()
	variable.name = "immunocompromised"
	variable.probability = 0.027
	variable = discreteDistribution.variables.add()
	variable.name = "not_immunocompromised"
	variable.probability = 0.973


	# covid symptoms questions in discrete distributions


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "body_temperature"
	variable = discreteDistribution.variables.add()
	variable.name = "body_temperature_above_102F"
	variable.probability = 0.015
	variable = discreteDistribution.variables.add()
	variable.name = "body_temperature_above_100F"
	variable.probability = 0.035
	variable = discreteDistribution.variables.add()
	variable.name = "normal_body_temperature"
	variable.probability = 0.95



	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "shortness_of_breath"
	variable = discreteDistribution.variables.add()
	variable.name = "new_or_worse_painful_shortness_of_breath"
	variable.probability = 0.01
	variable = discreteDistribution.variables.add()
	variable.name = "new_or_worse_shortness_of_breath"
	variable.probability = 0.04
	variable = discreteDistribution.variables.add()
	variable.name = "new_or_worse_shortness_of_breath_after_activity"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "no_shortness_of_breath"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "cough"
	variable = discreteDistribution.variables.add()
	variable.name = "cough_up_blood"
	variable.probability = 0.01
	variable = discreteDistribution.variables.add()
	variable.name = "dry_cough_or_cough_with_green_phlegm"
	variable.probability = 0.04
	variable = discreteDistribution.variables.add()
	variable.name = "cough_with_clear_spitum"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "no_cough"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "rash_or_skin_discoloration"
	variable = discreteDistribution.variables.add()
	variable.name = "rash_or_skin_discoloration"
	variable.probability = 0.02
	variable = discreteDistribution.variables.add()
	variable.name = "no_rash_or_skin_discoloration"
	variable.probability = 0.98



	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "muscle_weakness"
	variable = discreteDistribution.variables.add()
	variable.name = "new_or_worse_or_severe_muscle_weakness"
	variable.probability = 0.01
	variable = discreteDistribution.variables.add()
	variable.name = "moderate_muscle_weakness"
	variable.probability = 0.09
	variable = discreteDistribution.variables.add()
	variable.name = "no_muscle_weakness"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "difficulty_moving"
	variable = discreteDistribution.variables.add()
	variable.name = "new_or_worse_or_severe_difficulty_moving"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "moderate_difficulty_moving"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "no_difficulty_moving"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "neck_stiffness"
	variable = discreteDistribution.variables.add()
	variable.name = "new_or_worse_or_severe_neck_stiffness"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "moderate_neck_stiffness"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "no_neck_stiffness"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "low_urine"
	variable = discreteDistribution.variables.add()
	variable.name = "new_or_worse_or_severe_low_urine"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "moderate_low_urine"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "normal_urine"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "frequent_diarrhea"
	variable = discreteDistribution.variables.add()
	variable.name = "new_or_worse_or_severe_frequent_diarrhea"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "moderate_frequent_diarrhea"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "not_frequent_diarrhea"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "nausea"
	variable = discreteDistribution.variables.add()
	variable.name = "new_or_worse_or_severe_nausea"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "moderate_nausea"
	variable.probability = 0.15
	variable = discreteDistribution.variables.add()
	variable.name = "no_nausea"
	variable.probability = 0.80


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "vomiting"
	variable = discreteDistribution.variables.add()
	variable.name = "new_or_worse_or_severe_vomiting"
	variable.probability =0.05
	variable = discreteDistribution.variables.add()
	variable.name = "moderate_vomiting"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "no_vomiting"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "decreased_smell_or_taste"
	variable = discreteDistribution.variables.add()
	variable.name = "new_or_worse_or_severe_decreased_smell_or_taste"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "moderate_decreased_smell_or_taste"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "no_decreased_smell_or_taste"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "sore_throat"
	variable = discreteDistribution.variables.add()
	variable.name = "new_or_worse_or_severe_sore_throat"
	variable.probability = 0.1
	variable = discreteDistribution.variables.add()
	variable.name = "moderate_sore_throat"
	variable.probability = 0.1
	variable = discreteDistribution.variables.add()
	variable.name = "no_sore_throat"
	variable.probability = 0.80


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "pink_eye"
	variable = discreteDistribution.variables.add()
	variable.name = "new_or_worse_or_severe_pink_eye"
	variable.probability = 0.025
	variable = discreteDistribution.variables.add()
	variable.name = "moderate_pink_eye"
	variable.probability = 0.025
	variable = discreteDistribution.variables.add()
	variable.name = "no_pink_eye"
	variable.probability = 0.95


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "headache"
	variable = discreteDistribution.variables.add()
	variable.name = "new_or_worse_or_severe_headache"
	variable.probability = 0.10
	variable = discreteDistribution.variables.add()
	variable.name = "moderate_headache"
	variable.probability = 0.10
	variable = discreteDistribution.variables.add()
	variable.name = "no_headache"
	variable.probability = 0.80
	
	####
	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "feeling_well"
	variable = discreteDistribution.variables.add()
	variable.name = "not_feeling_well"
	variable.probability = 0.20
	variable = discreteDistribution.variables.add()
	variable.name = "feeling_well"
	variable.probability = 0.80
	
	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "congestion"
	variable = discreteDistribution.variables.add()
	variable.name = "congestion"
	variable.probability = 0.20
	variable = discreteDistribution.variables.add()
	variable.name = "no_congestion"
	variable.probability = 0.80
	
	
	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "fatigue"
	variable = discreteDistribution.variables.add()
	variable.name = "fatigue"
	variable.probability = 0.10
	variable = discreteDistribution.variables.add()
	variable.name = "no_fatigue"
	variable.probability = 0.90
	
	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "muscle_aches_or_body_pain"
	variable = discreteDistribution.variables.add()
	variable.name = "muscle_aches_or_body_pain"
	variable.probability = 0.10
	variable = discreteDistribution.variables.add()
	variable.name = "no_muscle_aches_or_body_pain"
	variable.probability = 0.90
	

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "abdominal_pain"
	variable = discreteDistribution.variables.add()
	variable.name = "abdominal_pain"
	variable.probability = 0.10
	variable = discreteDistribution.variables.add()
	variable.name = "no_abdominal_pain"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "own_thermometer"
	variable = discreteDistribution.variables.add()
	variable.name = "dont_own_thermometer"
	variable.probability = 0.01
	variable = discreteDistribution.variables.add()
	variable.name = "own_thermometer"
	variable.probability = 0.99
	

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "breathing_problems_at_night"
	variable = discreteDistribution.variables.add()
	variable.name = "breathing_problems_at_night"
	variable.probability = 0.01
	variable = discreteDistribution.variables.add()
	variable.name = "breathing_problems_at_night_relieved_with_pillows"
	variable.probability = 0.01
	variable = discreteDistribution.variables.add()
	variable.name = "no_breathing_problems_at_night"
	variable.probability = 0.98
	
	



	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "bmi"
	variable = discreteDistribution.variables.add()
	variable.name = "morbidly_obese"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "obese"
	variable.probability = 0.1
	variable = discreteDistribution.variables.add()
	variable.name = "overweight"
	variable.probability = 0.25
	variable = discreteDistribution.variables.add()
	variable.name = "normal"
	variable.probability = 0.5
	variable = discreteDistribution.variables.add()
	variable.name = "underweight"
	variable.probability = 0.1


	# covid/social distance rules
	
	

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "known_exposure"
	variable = discreteDistribution.variables.add()
	variable.name = "known_exposure"
	variable.probability = 0.07
	variable = discreteDistribution.variables.add()
	variable.name = "no_known_exposure"
	variable.probability = 0.93

	

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "employment_risk"
	variable = discreteDistribution.variables.add()
	variable.name = "health_care_worker_or_first_responder"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "high_volume_employment"
	variable.probability = 0.25
	variable = discreteDistribution.variables.add()
	variable.name = "low_employment_risk"
	variable.probability = 0.70
	
	


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "social_distancing_following"
	variable = discreteDistribution.variables.add()
	variable.name = "no_social_distancing_following"
	variable.probability = 0.50
	variable = discreteDistribution.variables.add()
	variable.name = "social_distance_following"
	variable.probability = 0.50
	
	

	

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "close_contact_unknown_exposure"
	variable = discreteDistribution.variables.add()
	variable.name = "close_contact_unknown_exposure"
	variable.probability = 0.50
	variable = discreteDistribution.variables.add()
	variable.name = "no_close_contact_unknown_exposure"
	variable.probability = 0.50
	

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "chest_pain_independent_of_breath"
	variable = discreteDistribution.variables.add()
	variable.name = "chest_pain_independent_of_breath"
	variable.probability = 0.02
	variable = discreteDistribution.variables.add()
	variable.name = "no_chest_pain_independent_of_breath"
	variable.probability = 0.98
	
	
	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "self_quarantine_two_weeks"
	variable = discreteDistribution.variables.add()
	variable.name = "no_self_quarantine_two_weeks"
	variable.probability = 0.50
	variable = discreteDistribution.variables.add()
	variable.name = "self_quarantine_two_weeks"
	variable.probability = 0.50
	

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "isolation_space"
	variable = discreteDistribution.variables.add()
	variable.name = "no_isolation_space"
	variable.probability = 0.20
	variable = discreteDistribution.variables.add()
	variable.name = "isolation_space"
	variable.probability = 0.80


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "leaving_house_per_day"
	variable = discreteDistribution.variables.add()
	variable.name = "leave_house_more_than_twice_per_day"
	variable.probability = 0.20
	variable = discreteDistribution.variables.add()
	variable.name = "leave_house_once_or_twice_per_day"
	variable.probability = 0.70
	variable = discreteDistribution.variables.add()
	variable.name = "leave_house_zero_per_day"
	variable.probability = 0.10


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "high_risk_place_per_week"
	variable = discreteDistribution.variables.add()
	variable.name = "high_risk_place_over_three_per_week"
	variable.probability = 0.30
	variable = discreteDistribution.variables.add()
	variable.name = "high_risk_place_two_or_three_per_week"
	variable.probability = 0.40
	variable = discreteDistribution.variables.add()
	variable.name = "high_risk_place_once_per_week"
	variable.probability = 0.20
	variable = discreteDistribution.variables.add()
	variable.name = "high_risk_place_zero_per_week"
	variable.probability = 0.10


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "disinfection_of_communal_objects_or_hand_sanitizer"
	variable = discreteDistribution.variables.add()
	variable.name = "no_disinfection_of_communal_objects_or_hand_sanitizer"
	variable.probability = 0.60
	variable = discreteDistribution.variables.add()
	variable.name = "disinfection_of_communal_objects_or_hand_sanitizer"
	variable.probability = 0.40



	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "deliveries_per_week"
	variable = discreteDistribution.variables.add()
	variable.name = "deliveries_over_three_per_week"
	variable.probability = 0.30
	variable = discreteDistribution.variables.add()
	variable.name = "deliveries_two_or_three_per_week"
	variable.probability = 0.40
	variable = discreteDistribution.variables.add()
	variable.name = "deliveries_once_per_week"
	variable.probability = 0.20
	variable = discreteDistribution.variables.add()
	variable.name = "deliveries_zero_per_week"
	variable.probability = 0.10



	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "sanitization_of_deliveries"
	variable = discreteDistribution.variables.add()
	variable.name = "no_sanitization_of_deliveries"
	variable.probability = 0.60
	variable = discreteDistribution.variables.add()
	variable.name = "sanitization_of_deliveries"
	variable.probability = 0.40



	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "mask"
	variable = discreteDistribution.variables.add()
	variable.name = "no_mask"
	variable.probability = 0.40
	variable = discreteDistribution.variables.add()
	variable.name = "surgical_mask_or_untrained_n95"
	variable.probability = 0.50
	variable = discreteDistribution.variables.add()
	variable.name = "n95_mask"
	variable.probability = 0.10


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "public_transportation_per_two_weeks"
	variable = discreteDistribution.variables.add()
	variable.name = "public_transportation_over_three_per_two_weeks"
	variable.probability = 0.20
	variable = discreteDistribution.variables.add()
	variable.name = "public_transportation_one_to_three_per_two_weeks"
	variable.probability = 0.10
	variable = discreteDistribution.variables.add()
	variable.name = "public_transportation_zero_per_two_weeks"
	variable.probability = 0.70




	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "workplace_social_distancing"
	variable = discreteDistribution.variables.add()
	variable.name = "no_workplace_social_distancing"
	variable.probability = 0.20
	variable = discreteDistribution.variables.add()
	variable.name = "workplace_social_distancing"
	variable.probability = 0.80


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "daily_contacts_social_distancing"
	variable = discreteDistribution.variables.add()
	variable.name = "no_daily_contacts_social_distancing"
	variable.probability = 0.40
	variable = discreteDistribution.variables.add()
	variable.name = "daily_contacts_social_distancing"
	variable.probability = 0.60


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "visits_per_week"
	variable = discreteDistribution.variables.add()
	variable.name = "visits_more_than_twice_per_week"
	variable.probability = 0.25
	variable = discreteDistribution.variables.add()
	variable.name = "visits_once_or_twice_per_week"
	variable.probability = 0.50
	variable = discreteDistribution.variables.add()
	variable.name = "visits_zero_per_week"
	variable.probability = 0.25


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "wash_hands_per_day"
	variable = discreteDistribution.variables.add()
	variable.name = "wash_hands_zero_per_day"
	variable.probability = 0.20
	variable = discreteDistribution.variables.add()
	variable.name = "wash_hands_once_or_twice_per_day"
	variable.probability = 0.30
	variable = discreteDistribution.variables.add()
	variable.name = "wash_hands_three_to_five_per_day"
	variable.probability = 0.30
	variable = discreteDistribution.variables.add()
	variable.name = "wash_hands_over_five_per_day"
	variable.probability = 0.20


		

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "tested"
	variable = discreteDistribution.variables.add()
	variable.name = "not_tested"
	variable.probability = 0.92
	variable = discreteDistribution.variables.add()
	variable.name = "tested"
	variable.probability = 0.08
	

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "swab_test"
	variable = discreteDistribution.variables.add()
	variable.name = "swab_test_positive"
	variable.probability = 0.02
	variable = discreteDistribution.variables.add()
	variable.name = "swab_test_negative"
	variable.probability = 0.98
	
	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "antibody_test"
	variable = discreteDistribution.variables.add()
	variable.name = "antibody_test_positive"
	variable.probability = 0.02
	variable = discreteDistribution.variables.add()
	variable.name = "antibody_test_negative"
	variable.probability = 0.98
	

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "saliva_test"
	variable = discreteDistribution.variables.add()
	variable.name = "saliva_test_positive"
	variable.probability = 0.02
	variable = discreteDistribution.variables.add()
	variable.name = "saliva_test_negative"
	variable.probability = 0.98
	
	#anomalies
	
	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "hotspot_anomaly"
	variable = discreteDistribution.variables.add()
	variable.name = "hotspot_anomaly"
	variable.probability = 0.15
	variable = discreteDistribution.variables.add()
	variable.name = "no_hotspot_anomaly"
	variable.probability = 0.85
	
		
	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "heart_rate_anomaly"
	variable = discreteDistribution.variables.add()
	variable.name = "heart_rate_anomaly"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "no_heart_rate_anomaly"
	variable.probability = 0.95


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "steps_anomaly"
	variable = discreteDistribution.variables.add()
	variable.name = "steps_anomaly"
	variable.probability = 0.15
	variable = discreteDistribution.variables.add()
	variable.name = "no_steps_anomaly"
	variable.probability = 0.85
	
	
	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "heart_rate_variability_anomaly"
	variable = discreteDistribution.variables.add()
	variable.name = "heart_rate_variability_anomaly"
	variable.probability = 0.1
	variable = discreteDistribution.variables.add()
	variable.name = "no_heart_rate_variability_anomaly"
	variable.probability = 0.90
	
	
	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "oxygen_anomaly"
	variable = discreteDistribution.variables.add()
	variable.name = "oxygen_anomaly"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "no_oxygen_anomaly"
	variable.probability = 0.95

	# conditional probability tables

	cpt ={} 

	
	cpt["covid_test"] = any_of(bayesianNetwork,cpt,
	{
	"swab_test":{"swab_test_positive"},
	"antibody_test":{"antibody_test_positive"},
	"saliva_test":{"saliva_test_positive"}
	},
	["positive_covid_test","negative_covid_test"]

	)
	
	
	cpt["metabolic_disease"] = any_of(bayesianNetwork,cpt,
	{
	"cardiovascular_disease":{"cardiovascular_disease"},
	"diabetes":{"diabetes"},
	"hypertension":{"hypertension"}
	},
	["metabolic_disease","no_metabolic_disease"]

	)
	
	
	cpt["chronic_conditions"] = any_of(bayesianNetwork,cpt,
	{
	"lung_disease":{"lung_disease"},
	"cancer":{"cancer"},
	"kidney_disease":{"kidney_disease"},
	"immunocompromised":{"immunocompromised"}
	},
	["chronic_conditions","no_chronic_conditions"]

	)

	
	cpt["comorbidities"] = any_of(bayesianNetwork,cpt,
	{
	"chronic_conditions":{"chronic_conditions"},
	"metabolic_disease":{"metabolic_disease"},
	"bmi":{"obese","morbidly_obese"}
	},
	["comorbidities","no_comorbidities"]

	)
	
	cpt["inflammation_symptoms"] = any_of(bayesianNetwork,cpt,
	{
	"rash_or_skin_discoloration":{"rash_or_skin_discoloration"},
	"muscle_aches_or_body_pain":{"muscle_aches_or_body_pain"},
	"muscle_weakness":{"new_or_worse_or_severe_muscle_weakness","moderate_muscle_weakness"}
        },
	["inflammation_symptoms","no_inflammation_symptoms"]
	)
	
	cpt["head_and_neck_symptoms"] = any_of(bayesianNetwork,cpt,
                {
            "neck_stiffness":{"neck_stiffness"},
            "pink_eye":{"new_or_worse_or_severe_pink_eye"},
            "headache":{"new_or_worse_or_severe_headache"}
        },
	[ "head_and_neck_symptoms","no_head_and_neck_symptoms"]
	)



	cpt["cold_symptoms"] = avg(bayesianNetwork,cpt,
	[
	"fatigue",
	"congestion",
	"feeling_well",
	"inflammation_symptoms",
	"breathing_problems_at_night",
        "head_and_neck_symptoms"
	],
	[ "significant_cold_symptoms","mild_cold_symptoms","no_cold_symptoms"]
	)
	
	cpt["specific_covid_symptoms"] = avg(bayesianNetwork,cpt,
	[
	"decreased_smell_or_taste"
	],
	[ "significant_specific_covid_symptoms","mild_specific_covid_symptoms","no_specific_covid_symptoms"]
	)


	cpt["gastrointestinal_symptoms"] = any_of(bayesianNetwork,cpt,
        {
            "low_urine":{"low_urine"},
            "nausea":{"new_or_worse_or_severe_nausea"},
            "vomiting":{"vomiting"},
	    "abdominal_pain":{"abdominal_pain"}
        },
	[ "gastrointestinal_symptoms","no_gastrointestinal_symptoms"]
	)
	
	
	cpt["covid_symptoms"] = any_of(bayesianNetwork,cpt,
        {	
            "sore_throat":{"new_or_worse_or_severe_sore_throat"},
            "gastrointestinal_symptoms":{"gastrointestinal_symptoms"},
            "cold_symptoms":{"significant_cold_symptoms"}
        },
	[ "covid_symptoms","no_covid_symptoms"]
	)
		
	cpt["delivery_safety"] = avg(bayesianNetwork,cpt,
	[
	"sanitization_of_deliveries",
	"deliveries_per_week"
	],
	["no_delivery_safety","delivery_safety"]

	)

	cpt["high_risk_place_safety"] = avg(bayesianNetwork,cpt,
	[
	"disinfection_of_communal_objects_or_hand_sanitizer",
	"high_risk_place_per_week"
	],
	["no_high_risk_place_safety","high_risk_place_safety"]

	)

	cpt["personal_social_distancing"]= avg(bayesianNetwork,cpt,
	[
	"delivery_safety",
	"mask",
	"wash_hands_per_day",
	"social_distancing_following",
	"close_contact_unknown_exposure"
	],
	["no_personal_social_distancing","some_personal_social_distancing","safe_personal_social_distancing"]
	)



	cpt["social_distancing_connectedness"]= any_of(bayesianNetwork,cpt,
        {
            "visits_per_week":{"visits_more_than_twice_per_week"},
            "leaving_house_per_day":{"leaving_house_more_than_twice_per_day"},
            "high_risk_place_safety":{"no_high_risk_place_safety"},
            "public_transportation_per_two_weeks":{"public_transportation_over_three_per_two_weeks"},
            "employment_risk":{"health_care_worker_or_first_responder","high_volume_employment"}
        },
	["no_social_distancing_connectedness","social_distancing_connectedness"]
	)


	cpt["social_distancing_environment"]= avg(bayesianNetwork,cpt,
	[
	"workplace_social_distancing",
	"daily_contacts_social_distancing"
	],
	["no_social_distancing_environnment","some_social_distancing_environment","safe_social_distancing_environment"]
	)


	cpt["social_distancing"]= avg(bayesianNetwork,cpt,
	[
	"social_distancing_environment",
	"personal_social_distancing",
	"social_distancing_connectedness"	
	],
	["no_social_distancing","low_social_distancing","medium_social_distancing", "high_social_distancing"]
	)
	
	cpt["social_distancing_binary"]= avg(bayesianNetwork,cpt,
	[
	"social_distancing"	
	],
	["no_social_distancing", "social_distancing"]
	)


	cpt["normal_activity_heart_rate_anomaly"] = all_of(bayesianNetwork,cpt,
		{"heart_rate_anomaly":{"heart_rate_anomaly"}, 
		"steps_anomaly":{"no_steps_anomaly"}},
		["normal_activity_heart_rate_anomaly","no_normal_activity_heart_rate_anomaly"]
		)



	cpt["wearables"] = avg(bayesianNetwork,cpt,
	[
        "heart_rate_variability_anomaly",
	"oxygen_anomaly",
	"normal_activity_heart_rate_anomaly"
	],
	["high_anomalous_wearables","medium_anomalous_wearables","low_anomalous_wearables","no_anomalous_wearables"]
	)

	cpt["wearables_binary"] = avg(bayesianNetwork,cpt,
	[
	"wearables"
	],
	["anomalous_wearables","no_anomalous_wearables"]
	)



	cpt["possible_dehydration"] = any_of(bayesianNetwork,cpt,
	{
	"low_urine":{"low_urine"},
	"vomiting":{"vomiting"},
	"frequent_diarrhea":{"frequent_diarrhea"}
	},
	["possible_dehydration","no_dehydration"]
	)


	cpt["possible_meningitis"] = all_of(bayesianNetwork,cpt,
		{"neck_stiffness":{"neck_stiffness"}, 
		"body_temperature":{"body_temperature_above_102F","body_temperature_above_99F"}},
		["possible_meningitis","no_meningitis"]
		)


	cpt["serious_shortness_of_breath"] = all_of(bayesianNetwork,cpt,
		{"shortness_of_breath":{"new_or_worse_painful_shortness_of_breath","new_or_worse_shortness_of_breath"}, 
		"comorbidities":{"comorbidities"}},
		["serious_shortness_of_breath","no_serious_shortness_of_breath"]
		)


	cpt["covid_vulnerabilities"] = avg(bayesianNetwork,cpt,
                {		
		"covid_symptoms",
		"social_distancing",
		"wearables"
                },
		["severe_covid_vulnerabilities", "moderate_covid_vulnerabilites","some_covid_vulnerabilites", "insignificant_covid_vulnerabilities"]
		)

	cpt["covid_symptom_level"] = avg(bayesianNetwork,cpt,
		[
                "serious_shortness_of_breath",
		"body_temperature",
		"cough",
                "specific_covid_symptoms",
		"covid_vulnerabilities"
		],
		["high_covid", "medium_covid","low_covid","no_covid"]

		)


	cpt["covid_environment"] = avg(bayesianNetwork,cpt,
		[
		"social_distancing",
		"covid_symptom_level"
		],
		["high_risk_covid_environment", "medium_risk_covid_environment", "low_risk_covid_environment","no_risk_covid_environment"]
		) 

	cpt["high_exposure"] = all_of(bayesianNetwork,cpt,
                {
                    "hotspot_anomaly":{"hotspot_anomaly"},
                    "covid_environment":{"high_risk_covid_environment"}
                },
        ["high_exposure","other_than_high_exposure"]
        )

	cpt["high_covid"] = any_of(bayesianNetwork,cpt,
        {
            "known_exposure":{"known_exposure"},
            "covid_test":{"positive_covid_test"},
            "high_exposure":{"high_exposure"},
            "cough_test":{"positive_cough_test"}
        },
        ["high_covid","other_than_high_covid"]
        )

	cpt["medium_exposure"]= all_of(bayesianNetwork,cpt,
                {
                    "hotspot_anomaly":{"hotspot_anomaly"},
                    "covid_environment":{"medium_risk_covid_environment"}
                },
        ["medium_exposure","other_than_medium_exposure"]
        )


	cpt["cardiopulmonary_emergency"] = any_of(bayesianNetwork,cpt,
         {
        "breathing_problems_at_night":{"breathing_problems_at_night_relieved_with_pillows"},
        "chest_pain_independent_of_breath":{"chest_pain_independent_of_breath"},
        "cough":{"cough_up_blood"},
        "serious_shortness_of_breath":{"serious_shortness_of_breath"}       
	}, 
        ["cardiopulmonary_emergency","no_cardiopulmonary_emergency"]
        )

	cpt["other_emergency"] = any_of(bayesianNetwork,cpt,
         {
        "muscle_weakness":{"new_or_worse_or_severe_muscle_weakness"},
	"possible_dehydration":{"possible_dehydration"},
	"possible_meningitis":{"possible_meningitis"},
        "vomiting":{"new_or_worse_or_severe_vomiting"},
	},
        ["other_emergency","no_other_emergency"]
        )
        

	
	#output variable conditional probability distributions


	cpt["emergency_treatment"] = any_of(bayesianNetwork,cpt,
        {
        "cardiopulmonary_emergency":{"cardiopulmonary_emergency"},
        "other_emergency":{"other_emergency"}       
	},
	["emergency_treatment","no_emergency_treatment"]
	)

	cpt["covid_risk"] = if_then_else(bayesianNetwork,cpt,
		{
		"high_covid":{"high_covid"},
		"medium_exposure":{"medium_exposure"},
		"covid_environment":{"high_risk_covid_environment","medium_risk_covid_environment,low_risk_covid_environment"}
		},
		["high_covid_risk", "medium_covid_risk","low_covid_risk","no_covid_risk"]
		) 
        


	cpt["covid_risk_binary"] = avg(bayesianNetwork,cpt,
		[
		"covid_risk"
		],

		["covid_risk","no_covid_risk"]
		) 

	cpt["testing_compliance"] = all_of(bayesianNetwork,cpt,
        {
        "tested":{"not_tested"},
        "covid_risk":{"high_covid_risk"}
        },
        ["poor_testing_compliance","testing_compliance"]
        )


 

	cpt["quarantine_compliance"] = all_of(bayesianNetwork,cpt,
        {
        "self_quarantine_two_weeks":{"no_self_quarantine_two_weeks"},
        "covid_risk":{"high_covid_risk"}
        },
        ["poor_quarantine_compliance","quarantine_compliance"]
        )


  
 

	cpt["self_care"] = any_of(bayesianNetwork,cpt,
        {
        "isolation_space":{"no_isolation_space"},
        "testing_compliance":{"poor_testing_compliance"},
        "quarantine_compliance":{"poor_quarantine_compliance"},
        "own_thermometer":{"dont_own_thermometer"}
        },
        ["poor_self_care","self_care"]
        )


	cpt["covid_severity"] = avg(bayesianNetwork,cpt,
        	[	
		"age",
                "comorbidities",
                "covid_risk"
		],
		["high_covid_severity","medium_covid_severity","low_covid_severity","no_covid_severity"]
		)
		

		
	cpt["covid_severity_binary"] = avg(bayesianNetwork,cpt,
		[
                    "covid_severity"
                ],
		["covid_severity","no_covid_severity"]
		)



	addCpt(bayesianNetwork,cpt)
	return(bayesianNetwork)

if __name__ == '__main__':
	covid_bayes()
