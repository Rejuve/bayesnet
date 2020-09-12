import sn_bayes
from sn_bayes.utils import any
from sn_bayes.utils import all
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



	#basics/init

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "acute_medical_condition"
	variable = discreteDistribution.variables.add()
	variable.name = "acute_medical_condition"
	variable.probability = 0.02
	variable = discreteDistribution.variables.add()
	variable.name = "no_acute_medical_condition"
	variable.probability = 0.98

	# basics/demographics questions 


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "age"
	variable = discreteDistribution.variables.add()
	variable.name = "elderly"
	variable.probability = 0.1
	variable = discreteDistribution.variables.add()
	variable.name = "adult"
	variable.probability = 0.3
	variable = discreteDistribution.variables.add()
	variable.name = "young_adult"
	variable.probability = 0.2
	variable = discreteDistribution.variables.add()
	variable.name = "teen"
	variable.probability = 0.1
	variable = discreteDistribution.variables.add()
	variable.name = "child"
	variable.probability = 0.1


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
	variable.name = "weight_175_to_220"
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


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "ethnicity"
	variable = discreteDistribution.variables.add()
	variable.name = "african_american"
	variable.probability = 0.15
	variable = discreteDistribution.variables.add()
	variable.name = "hispanic"
	variable.probability = 0.2
	variable = discreteDistribution.variables.add()
	variable.name = "ethnicity_other"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "african"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "middle_eastern"
	variable.probability = 0.025
	variable = discreteDistribution.variables.add()
	variable.name = "native_american"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "pacific_islander"
	variable.probability = 0.025
	variable = discreteDistribution.variables.add()
	variable.name = "asian"
	variable.probability = 0.1
	variable = discreteDistribution.variables.add()
	variable.name = "caucasian"
	variable.probability = 0.35


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
	variable.probability = 0.3
	variable = discreteDistribution.variables.add()
	variable.name = "no_kidney_disase"
	variable.probability = 0.7

#cancer = 5.5%
#https://ourworldindata.org/cancer#:~:text=Prevalence%20of%20cancer%20ranges%20from,countries%20shown%20in%20light%20yellow.

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "cancer"
	variable = discreteDistribution.variables.add()
	variable.name = "cancer"
	variable.probability = 0.3
	variable = discreteDistribution.variables.add()
	variable.name = "no_cancer"
	variable.probability = 0.7
	
#immunocompromised=2.7%
#https://www.healio.com/news/infectious-disease/20161101/nearly-3-of-us-adult-population-immunosuppressed#:~:text=Among%20them%2C%202.8%25%20(n,CI%2C%202.9%2D3.3).

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "immunocompromised"
	variable = discreteDistribution.variables.add()
	variable.name = "immunocompromised"
	variable.probability = 0.3
	variable = discreteDistribution.variables.add()
	variable.name = "not_immunocompromised"
	variable.probability = 0.7

#psychiatric disorders 17.6%
#https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3997379/#:~:text=Period%20prevalence%20of%20common%20mental,CI%2C%2025.9%E2%80%9332.6%25).

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "psychological_disorders"
	variable = discreteDistribution.variables.add()
	variable.name = "psychological_disorders"
	variable.probability = 0.3
	variable = discreteDistribution.variables.add()
	variable.name = "no_psychological_disorders"
	variable.probability = 0.7


	# covid symptoms questions in discrete distributions


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "body_temperature"
	variable = discreteDistribution.variables.add()
	variable.name = "body_temperature_above_102F"
	variable.probability = 0.015
	variable = discreteDistribution.variables.add()
	variable.name = "body_temperature_above_99F"
	variable.probability = 0.035
	variable = discreteDistribution.variables.add()
	variable.name = "normal_body_temperature"
	variable.probability = 0.95



	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "low_oxygen_symptoms"
	variable = discreteDistribution.variables.add()
	variable.name = "have_low_oxygen_symptoms"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "no_low_oxygen_symptoms"
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
	variable.name = "dry_cough"
	variable.probability = 0.04
	variable = discreteDistribution.variables.add()
	variable.name = "cough_with_spitum"
	variable.probability = 0.05
	variable = discreteDistribution.variables.add()
	variable.name = "no_cough"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "colored_spots_on_toes"
	variable = discreteDistribution.variables.add()
	variable.name = "colored_spots_on_toes"
	variable.probability = 0.02
	variable = discreteDistribution.variables.add()
	variable.name = "no_colored_spots_on_toes"
	variable.probability = 0.98


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "hx_lung_disease"
	variable = discreteDistribution.variables.add()
	variable.name = "hx_lung_disease"
	variable.probability = 0.1
	variable = discreteDistribution.variables.add()
	variable.name = "no_hx_lung_disease"
	variable.probability = 0.90



	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "hx_family_lung_disease"
	variable = discreteDistribution.variables.add()
	variable.name = "hx_family_lung_disease"
	variable.probability = 0.1
	variable = discreteDistribution.variables.add()
	variable.name = "no_hx_family_lung_disease"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "muscle_weakness"
	variable = discreteDistribution.variables.add()
	variable.name = "muscle_weakness_cant_move"
	variable.probability = 0.01
	variable = discreteDistribution.variables.add()
	variable.name = "new_or_worse_muscle_weakness"
	variable.probability = 0.09
	variable = discreteDistribution.variables.add()
	variable.name = "no_muscle_weakness"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "difficulty_moving"
	variable = discreteDistribution.variables.add()
	variable.name = "difficulty_moving"
	variable.probability = 0.1
	variable = discreteDistribution.variables.add()
	variable.name = "no_difficulty_moving"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "neck_stiffness"
	variable = discreteDistribution.variables.add()
	variable.name = "neck_stiffness"
	variable.probability = 0.1
	variable = discreteDistribution.variables.add()
	variable.name = "no_neck_stiffness"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "low_urine"
	variable = discreteDistribution.variables.add()
	variable.name = "low_urine"
	variable.probability = 0.1
	variable = discreteDistribution.variables.add()
	variable.name = "normal_urine"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "frequent_diarrhea"
	variable = discreteDistribution.variables.add()
	variable.name = "frequent_diarrhea"
	variable.probability = 0.1
	variable = discreteDistribution.variables.add()
	variable.name = "not_frequent_diarrhea"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "nausea"
	variable = discreteDistribution.variables.add()
	variable.name = "nausea"
	variable.probability = 0.2
	variable = discreteDistribution.variables.add()
	variable.name = "no_nausea"
	variable.probability = 0.80


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "vomiting"
	variable = discreteDistribution.variables.add()
	variable.name = "vomiting"
	variable.probability = 0.1
	variable = discreteDistribution.variables.add()
	variable.name = "no_vomiting"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "decreased_smell_or_taste"
	variable = discreteDistribution.variables.add()
	variable.name = "decreased_smell_or_taste"
	variable.probability = 0.1
	variable = discreteDistribution.variables.add()
	variable.name = "no_decreased_smell_or_taste"
	variable.probability = 0.90


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "sore_throat"
	variable = discreteDistribution.variables.add()
	variable.name = "sore_throat"
	variable.probability = 0.2
	variable = discreteDistribution.variables.add()
	variable.name = "no_sore_throat"
	variable.probability = 0.80


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "pink_eye"
	variable = discreteDistribution.variables.add()
	variable.name = "pink_eye"
	variable.probability = 0.01
	variable = discreteDistribution.variables.add()
	variable.name = "no_pink_eye"
	variable.probability = 0.99


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "headache"
	variable = discreteDistribution.variables.add()
	variable.name = "headache"
	variable.probability = 0.20
	variable = discreteDistribution.variables.add()
	variable.name = "no_headache"
	variable.probability = 0.80


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


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "exposure"
	variable = discreteDistribution.variables.add()
	variable.name = "exposure_in_family_not_isolated"
	variable.probability = 0.01
	variable = discreteDistribution.variables.add()
	variable.name = "exposure_in_family"
	variable.probability = 0.02
	variable = discreteDistribution.variables.add()
	variable.name = "exposure_healthcare_worker"
	variable.probability = 0.03
	variable = discreteDistribution.variables.add()
	variable.name = "known_exposure"
	variable.probability = 0.02
	variable = discreteDistribution.variables.add()
	variable.name = "exposure_high_risk_worker"
	variable.probability = 0.02
	variable = discreteDistribution.variables.add()
	variable.name = "no_exposure"
	variable.probability = 0.90


	# covid/social distance rules


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "isolation_space"
	variable = discreteDistribution.variables.add()
	variable.name = "no_isolation_space"
	variable.probability = 0.20
	variable = discreteDistribution.variables.add()
	variable.name = "have_isolation_space"
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
	variable.name = "high_risk_place_no_sanitizer_over_three_per_week"
	variable.probability = 0.10
	variable = discreteDistribution.variables.add()
	variable.name = "high_risk_place_no_sanitizer_once_or_more_per_week"
	variable.probability = 0.30
	variable = discreteDistribution.variables.add()
	variable.name = "high_risk_place_sanitizer_two_or_three_per_week"
	variable.probability = 0.30
	variable = discreteDistribution.variables.add()
	variable.name = "high_risk_place_sanitizer_once_per_week"
	variable.probability = 0.20
	variable = discreteDistribution.variables.add()
	variable.name = "high_risk_place_zero_per_week"
	variable.probability = 0.10


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "deliveries_per_week"
	variable = discreteDistribution.variables.add()
	variable.name = "deliveries_no_sanitation_over_three_per_week"
	variable.probability = 0.10
	variable = discreteDistribution.variables.add()
	variable.name = "deliveries_no_sanitation_once_or_more_per_week"
	variable.probability = 0.30
	variable = discreteDistribution.variables.add()
	variable.name = "deliveries_sanitation_two_or_three_per_week"
	variable.probability = 0.30
	variable = discreteDistribution.variables.add()
	variable.name = "deliveries_sanitation_once_per_week"
	variable.probability = 0.20
	variable = discreteDistribution.variables.add()
	variable.name = "deliveries_zero_per_week"
	variable.probability = 0.10


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "mask"
	variable = discreteDistribution.variables.add()
	variable.name = "no_mask"
	variable.probability = 0.40
	variable = discreteDistribution.variables.add()
	variable.name = "surgical_mask"
	variable.probability = 0.50
	variable = discreteDistribution.variables.add()
	variable.name = "n95_mask"
	variable.probability = 0.10


	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "public_transportation_per_week"
	variable = discreteDistribution.variables.add()
	variable.name = "public_transportation_over_three_per_week"
	variable.probability = 0.20
	variable = discreteDistribution.variables.add()
	variable.name = "public_transportation_one_to_three_per_week"
	variable.probability = 0.10
	variable = discreteDistribution.variables.add()
	variable.name = "public_transportation_zero_per_week"
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
	discreteDistribution.name = "local_govt_social_distancing"
	variable = discreteDistribution.variables.add()
	variable.name = "no_local_govt_social_distancing"
	variable.probability = 0.40
	variable = discreteDistribution.variables.add()
	variable.name = "local_govt_social_distancing"
	variable.probability = 0.60


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
	discreteDistribution.name = "severe_neck_pain"
	variable = discreteDistribution.variables.add()
	variable.name = "severe_neck_pain"
	variable.probability = 0.02
	variable = discreteDistribution.variables.add()
	variable.name = "no_severe_neck_pain"
	variable.probability = 0.98
		

	discreteDistribution = bayesianNetwork.discreteDistributions.add()
	discreteDistribution.name = "tested"
	variable = discreteDistribution.variables.add()
	variable.name = "tested"
	variable.probability = 0.02
	variable = discreteDistribution.variables.add()
	variable.name = "not_tested"
	variable.probability = 0.98
	

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

	
	cpt["covid_test"] = any(bayesianNetwork,cpt,
	{
	"swab_test":{"swab_test_positive"},
	"antibody_test":{"antibody_test_positive"},
	"saliva_test":{"saliva_test_positive"}
	},
	["positive_covid_test","negative_covid_test"]

	)
	
	
	cpt["metabolic_disease"] = any(bayesianNetwork,cpt,
	{
	"cardiovascular_disease":{"cardiovascular_disease"},
	"diabetes":{"diabetes"},
	"hypertension":{"hypertension"}
	},
	["metabolic_disease","no_metabolic_disease"]

	)
	
	
	cpt["chronic_conditions"] = any(bayesianNetwork,cpt,
	{
	"lung_disease":{"lung_disease"},
	"cancer":{"cancer"},
	"kidney_disease":{"kidney_disease"},
	"immunocompromised":{"immunocompromised"}
	},
	["chronic_conditions","no_chronic_conditions"]

	)

	
	cpt["demographics"] = avg(bayesianNetwork,cpt,
	[
	"age",
	"ethnicity",
	"bmi"
	],
	["demographics","no_demographics"]

	)
	
	cpt["comorbidities"] = any(bayesianNetwork,cpt,
	{
	"chronic_conditions":{"chronic_conditions"},
	"metabolic_disease":{"metabolic_disease"},
	"demographics":{"demographics"}
	},
	["comorbidities","no_comorbidities"]

	)
	
	cpt["specific_covid_symptoms"] = avg(bayesianNetwork,cpt,
	[
	"colored_spots_on_toes",
	"decreased_smell_or_taste"
	],
	[ "significant_specific_covid_symptoms","mild_specific_covid_symptoms","no_specific_covid_symptoms"]
	)

	cpt["head_and_neck_covid_symptoms"] = avg(bayesianNetwork,cpt,
	[
	"neck_stiffness",
	"sore_throat",
	"pink_eye",
	"headache"
	],
	[ "significant_head_and_neck_covid_symptoms","mild_head_and_neck_covid_symptoms","no_head_and_neck_covid_symptoms"]
	)

	cpt["gastrointestinal_covid_symptoms"] = avg(bayesianNetwork,cpt,
	[
	"low_urine",
	"nausea",
	"vomiting",
	],
	[ "significant_gastrointestinal_covid_symptoms","mild_gastrointestinal_covid_symptoms","no_gastrointestinal_covid_symptoms"]
	)

	cpt["covid_symptoms"] = any(bayesianNetwork,cpt,
	{
	"gastrointestinal_covid_symptoms":{"significant_gastrointestinal_covid_symptoms"},
	"specific_covid_symptoms":{"significant_specific_covid_symptoms"},
	"head_and_neck_covid_symptoms":{"significant_head_and_neck_covid_symptoms"}
	},
	[ "significant_covid_symptoms","no_significant_covid_symptoms"]
	)

	cpt["personal_social_distancing"]= avg(bayesianNetwork,cpt,
	[
	"isolation_space",
	"deliveries_per_week",
	"mask",
	"wash_hands_per_day"
	],
	["no_personal_social_distancing","some_personal_social_distancing","safe_personal_social_distancing"]
	)



	cpt["social_distancing_connectedness"]= avg(bayesianNetwork,cpt,
	[
	"visits_per_week",
	"leaving_house_per_day",
	"high_risk_place_per_week",
	"public_transportation_per_week"
	],
	["no_social_distancing_connectedness","some_social_distancing_connectedness","safe_social_distancing_connectedness"]
	)


	cpt["social_distancing_environment"]= avg(bayesianNetwork,cpt,
	[
	"workplace_social_distancing",
	"daily_contacts_social_distancing",
	"local_govt_social_distancing"
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
	"social_distancing_environment",
	"personal_social_distancing",
	"social_distancing_connectedness"	
	],
	["no_social_distancing", "social_distancing"]
	)


	cpt["wearables"] = any(bayesianNetwork,cpt,
	{
	"heart_rate_variability_anomaly":{"heart_rate_variability_anomaly"},
	"oxygen_anomaly":{"oxygen_anomaly"},
	"heart_rate_anomaly":{"heart_rate_anomaly"}
	},
	["anomalous","normal"]
	)


	cpt["possible_dehydration"] = any(bayesianNetwork,cpt,
	{
	"low_urine":{"low_urine"},
	"vomiting":{"vomiting"},
	"frequent_diarrhea":{"frequent_diarrhea"}
	},
	["possible_dehydration","no_dehydration"]
	)


	cpt["possible_meningitis"] = all(bayesianNetwork,cpt,
		{"neck_stiffness":{"neck_stiffness"}, 
		"severe_neck_pain":{"severe_neck_pain"},
		"body_temperature":{"body_temperature_above_102F","body_temperature_above_99F"}},
		["possible_meningitis","no_meningitis"]
		)


	cpt["serious_shortness_of_breath"] = all(bayesianNetwork,cpt,
		{"shortness_of_breath":{"new_or_worse_painful_shortness_of_breath","new_or_worse_shortness_of_breath"}, 
		"comorbidities":{"comorbidities"}},
		["serious_shortness_of_breath","no_serious_shortness_of_breath"]
		)


	cpt["covid_vulnerabilities"] = avg(bayesianNetwork,cpt,
		[
		"covid_symptoms",
		"social_distancing",
		"wearables"
		],
		["severe_covid_vulnerabilities", "moderate_covid_vulnerabilites","some_covid_vulnerabilites", "insignificant_covid_vulnerabilities"]
		)


	cpt["low_covid"] = any(bayesianNetwork,cpt,
		{
		"shortness_of_breath": {"new_or_worse_shortness_of_breath"},
		"body_temperature":{"body_temperature_above_99F"},
		"covid_vulnerabilities":{"some_covid_vulnerabilites"}
		},
		["low_covid","other_covid"]
		)


	cpt["medium_covid"]= any(bayesianNetwork,cpt,
		{
		"serious_shortness_of_breath":{"serious_shortness_of_breath"},
		"body_temperature":{"body_temperature_above_102F"},
		"muscle_weakness":{"new_or_worse_muscle_weakness"},
		"covid_vulnerabilities":{"moderate_covid_vulnerabilites"} 
		},
		["medium_covid","other_covid"]
		)


	cpt["high_covid"] = any(bayesianNetwork,cpt,
		{
		"cough":{"cough_up_blood"},
		"muscle_weakness":{"muscle_weakness_cant_move"},
		"low_oxygen_symptoms":{"have_low_oxygen_symptoms"},
		"covid_vulnerabilities": {"severe_covid_vulnerabilites"}
		},
		["high_covid","other_covid"]
		)


	cpt["covid_environment"] = avg(bayesianNetwork,cpt,
		[
		"exposure",
		"hotspot_anomaly"
		],
		["high_risk_covid_environment", "medium_risk_covid_environment", "low_risk_covid_environment","no_risk_covid_environment"]
		) 


	cpt["covid_symptom_level"] = if_then_else(bayesianNetwork,cpt,
		{
		"high_covid":{"high_covid"},
		"medium_covid":{"medium_covid"},
		"low_covid":{"low_covid"},
		},
		["high_covid", "medium_covid","low_covid","no_covid"]
		) 

	cpt["high_covid_risk"] =any(bayesianNetwork,cpt,
		{
		"covid_symptom_level":{"high_covid"},
		"covid_test":{"positive_covid_test"},
		"covid_environment":{"high_risk_covid_environment"}
		},
		["high_covid_risk","other_covid_risk"]
		)
	
	cpt["medium_covid_risk"] =any(bayesianNetwork,cpt,
		{
		"covid_symptom_level":{"medium_covid"},
		"covid_environment":{"medium_risk_covid_environment"}
		},
		["medium_covid_risk","other_covid_risk"]
		)
		
	cpt["low_covid_risk"] =any(bayesianNetwork,cpt,
		{	
		"covid_symptom_level":{"low_covid"},
		"covid_environment":{"low_risk_covid_environment"}
		},
		["low_covid_risk","other_covid_risk"]
		)

	
	#output variable conditional probability distributions


	cpt["emergency_treatment"] = any(bayesianNetwork,cpt,
	{
	"possible_dehydration":{"possible_dehydration"},
	"possible_meningitis":{"possible_meningitis"},
	"acute_medical_condition":{"acute_medical_condition"}
	},
	["emergency_treatment","no_emergency_treatment"]
	)



	cpt["covid_risk"] = if_then_else(bayesianNetwork,cpt,
		{
		"high_covid_risk":{"high_covid_risk"},
		"medium_covid_risk":{"medium_covid_risk"},
		"low_covid_risk":{"low_covid_risk"},
		},
		["high_covid_risk", "medium_covid_risk","low_covid_risk","no_covid_risk"]
		) 


	cpt["covid_risk_binary"] = avg(bayesianNetwork,cpt,
		[
		"covid_symptom_level",
		"covid_environment"
		],
		["covid_risk","no_covid_risk"]
		)


	cpt["covid_severity"] = avg(bayesianNetwork,cpt,
		[
		"age",
		"comorbidities"
		],
		["high_covid_severity","medium_covid_severity","low_covid_severity","no_covid_severity"]
		)
		
		
	cpt["covid_severity_binary"] = avg(bayesianNetwork,cpt,
		[
		"age",
		"comorbidities"
		],
		["covid_severity","no_covid_severity"]
		)



	addCpt(bayesianNetwork,cpt)
	return(bayesianNetwork)

if __name__ == '__main__':
	covid_bayes()
