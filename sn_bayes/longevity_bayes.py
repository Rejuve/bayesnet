import sn_bayes
from sn_bayes.utils import any_of
from sn_bayes.utils import all_of
from sn_bayes.utils import avg
from sn_bayes.utils import if_then_else
from sn_bayes.utils import bayesInitialize
from sn_bayes.utils import addCpt
from sn_bayes.utils import dependency
from sn_bayes.utils import non_cpt_descriptions

import sn_service.service_spec.bayesian_pb2
from sn_service.service_spec.bayesian_pb2 import BayesianNetwork


def longevity_bayes():
        bayesianNetwork = BayesianNetwork()



        outstr = '' 
                
        #probabilities within distributions must sum to 1.0
    #questions left blank or "prefer not to answer" will be computed

    #anomalies
        
                # increasing variability in step is associated with 
                # loss of resiliance , the root of aging
                # https://www.nature.com/articles/s41467-021-23014-1
                
                #variablility of number of steps within a day
                
        anomaly = bayesianNetwork.anomalies.add()
        anomaly.varName = "step_variability_anomaly"
        anomaly.side = "positive"
        anomaly.c = 3.0 
        anomaly.window = 5
        detectors = anomaly.detectors.add()
        detectors.name = "VolatilityShiftAD"
                
                #apple mobility measurements
                

        anomaly = bayesianNetwork.anomalies.add()
        anomaly.varName = "double_support_stepping_anomaly"
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
        anomaly.varName = "step_assymetry_anomaly"
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

                
                
                # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4627774/
                # variability of stride and intraday speed predicts Parkinsons
                
                
        anomaly = bayesianNetwork.anomalies.add()
        anomaly.varName = "stride_variability_anomaly"
        anomaly.side = "positive"
        anomaly.c = 3.0 
        anomaly.window = 5
        detectors = anomaly.detectors.add()
        detectors.name = "VolatilityShiftAD"
                
                
        anomaly = bayesianNetwork.anomalies.add()
        anomaly.varName = "walking_speed_variability_anomaly"
        anomaly.side = "positive"
        anomaly.c = 3.0 
        anomaly.window = 5
        detectors = anomaly.detectors.add()
        detectors.name = "VolatilityShiftAD"
                
                
                

                #Walking speed

                

        anomaly = bayesianNetwork.anomalies.add()
        anomaly.varName = "walking_speed_anomaly"
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
        anomaly.varName = "sleep_anomaly"
        anomaly.low = 6
        anomaly.high = 13
        anomaly.n = 30 
        detectors = anomaly.detectors.add()
        detectors.name = "ThresholdAD"
        

#Input nodes


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "age"
        variable = discreteDistribution.variables.add()
        variable.name = "elderly"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "adult"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "young_adult"
        variable.probability = 0.3
        variable = discreteDistribution.variables.add()
        variable.name = "teen"
        variable.probability = 0.2
        variable = discreteDistribution.variables.add()
        variable.name = "child"
        variable.probability = 0.2



#Cardiovascular Disease
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "daily_asprin_prescription"
        variable = discreteDistribution.variables.add()
        variable.name = "daily_asprin_prescription_yes"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "daily_asprin_prescription_no"
        variable.probability = 0.95

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "daily_aspirin_compliance"
        variable = discreteDistribution.variables.add()
        variable.name = "daily_aspirin_compliance_no"
        variable.probability = 0.30
        variable = discreteDistribution.variables.add()
        variable.name = "daily_aspirin_compliance_yes"
        variable.probability = 0.70




        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "angina"
        variable = discreteDistribution.variables.add()
        variable.name = "angina_yes"
        variable.probability = 0.03
        variable = discreteDistribution.variables.add()
        variable.name = "angina_no"
        variable.probability = 0.97

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "blood_relative_heart_attack_before_age_50"
        variable = discreteDistribution.variables.add()
        variable.name = "blood_relative_heart_attack_before_50_yes"
        variable.probability = 0.13
        variable = discreteDistribution.variables.add()
        variable.name = "blood_relative_heart_attack_before_50_no"
        variable.probability = 0.87



        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "chest_pain"
        variable = discreteDistribution.variables.add()
        variable.name = "chest_pain_yes"
        variable.probability = 0.30
        variable = discreteDistribution.variables.add()
        variable.name = "chest_pain_no"
        variable.probability = 0.70
        


#Resting heart rate
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "resting_heart_rate"
        variable = discreteDistribution.variables.add()
        variable.name = "resting_heart_rate_very_high_91_and_above"
        variable.probability = 0.09
        variable = discreteDistribution.variables.add()
        variable.name = "resting_heart_rate_high_81_to_90"
        variable.probability = 0.15
        variable = discreteDistribution.variables.add()
        variable.name = "resting_heart_rate_normal_under_80"
        variable.probability = 0.67

#Hypertension
        
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "high_blood_pressure_patient_prescription"
        variable = discreteDistribution.variables.add()
        variable.name = "high_blood_pressure_patient_prescription_yes"
        variable.probability = 0.85
        variable = discreteDistribution.variables.add()
        variable.name = "high_blood_pressure_patient_prescription_no"
        variable.probability = 0.15

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "high_blood_pressure_medication_compliance"
        variable = discreteDistribution.variables.add()
        variable.name = "high_blood_pressure_medication_compliance_no"
        variable.probability = 0.27
        variable = discreteDistribution.variables.add()
        variable.name = "high_blood_pressure_medication_compliance_yes"
        variable.probability = 0.73


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "diastolic"
        variable = discreteDistribution.variables.add()
        variable.name = "diastolic_120_or_higher_crisis"
        variable.probability = 0.01
        variable = discreteDistribution.variables.add()
        variable.name = "diastolic_90_to_119_high_stage_2"
        variable.probability = 0.06
        variable = discreteDistribution.variables.add()
        variable.name = "diastolic_80_to_89_high_stage_1"
        variable.probability = 0.17
        variable = discreteDistribution.variables.add()
        variable.name = "diastolic_less_than_80_normal"
        variable.probability = 0.76


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "systolic"
        variable = discreteDistribution.variables.add()
        variable.name = "systolic_180_over_crisis"
        variable.probability = 0.02
        variable = discreteDistribution.variables.add()
        variable.name = "systolic_140_to_179_high_stage_2"
        variable.probability = 0.18
        variable = discreteDistribution.variables.add()
        variable.name = "systolic_130_to_139_high_stage_1"
        variable.probability = 0.14
        variable = discreteDistribution.variables.add()
        variable.name = "systolic_120_to_129_elevated"
        variable.probability = 0.16
        variable = discreteDistribution.variables.add()
        variable.name = "systolic_less_than_120_normal"
        variable.probability = 0.50
        
        

#Cancer 


#UV light causes inflammatory cascade

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "sun_exposure_half_hour"
        variable = discreteDistribution.variables.add()
        variable.name = "sun_exposure_half_hour_severe_sunburn_blisters"
        variable.probability = 0.02
        variable = discreteDistribution.variables.add()
        variable.name = "sun_exposure_half_hour_severe_sunburn_peeling"
        variable.probability = 0.08
        variable = discreteDistribution.variables.add()
        variable.name = "sun_exposure_half_hour_mild_burn_tanning"
        variable.probability = 0.22
        variable = discreteDistribution.variables.add()
        variable.name = "sun_exposure_half_hour_darker_no_burn"
        variable.probability = 0.24
        variable = discreteDistribution.variables.add()
        variable.name = "sun_exposure_half_hour_no_tan_or_burn"
        variable.probability = 0.44
        variable = discreteDistribution.variables.add()
        

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "time_spent_outdoors"
        variable = discreteDistribution.variables.add()
        variable.name = "time_spent_outdoors_none"
        variable.probability = 0.21
        variable = discreteDistribution.variables.add()
        variable.name = "time_spent_outdoors_a_half_hour_per_day"
        variable.probability = 0.16
        variable = discreteDistribution.variables.add()
        variable.name = "time_spent_outdoors_1_hour_per_day"
        variable.probability = 61
        variable.name = "time_spent_outdoors_2_or_3_hours_per_day"
        variable.probability = 0.18
        variable = discreteDistribution.variables.add()
        variable.name = "time_spent_outdoors_4_to_6_hours_per_day"
        variable.probability = 0.11
        variable = discreteDistribution.variables.add()
        variable.name = "time_spent_outdoors_7_or_more_hours_per_day"
        variable.probability = 0.18
        


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "sun_exposure_use_sunscreen"
        variable = discreteDistribution.variables.add()
        variable.name = "sun_exposure_use_sunscreen_never"
        variable.probability = 0.40
        variable = discreteDistribution.variables.add()
        variable.name = "sun_exposure_use_sunscreen_rarely"
        variable.probability = 0.18
        variable = discreteDistribution.variables.add()
        variable.name = "sun_exposure_use_sunscreen_sometimes"
        variable.probability = 0.21
        variable = discreteDistribution.variables.add()
        variable.name = "sun_exposure_use_sunscreen_most_of_the_time"
        variable.probability = 0.12
        variable = discreteDistribution.variables.add()
        variable.name = "sun_exposure_use_sunscreen_always"
        variable.probability = 0.09

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "sunburn_last_year"
        variable = discreteDistribution.variables.add()
        variable.name = "sunburn_last_year_yes"
        variable.probability = 0.33
        variable = discreteDistribution.variables.add()
        variable.name = "sunburn_last_year_no"
        variable.probability = 0.67


#obesity

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "weight_at_25"
        variable = discreteDistribution.variables.add()
        variable.name = "weight_at_25_above_300.00"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "weight_at_25_above_180.00_to_300.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "weight_at_25_above_150.00_to_180.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "weight_at_25_above_125.00_to_150.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "weight_at_25_125.00_and_below"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "greatest_weight"
        variable = discreteDistribution.variables.add()
        variable.name = "greatest_weight_above_315.00"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "greatest_weight_above_230.00_to_315.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "greatest_weight_above_190.00_to_230.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "greatest_weight_above_160.00_to_190.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "greatest_weight_160.00_and_below"
        variable.probability = 0.25



        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "bmi"
        variable = discreteDistribution.variables.add()
        variable.name = "bmi_over_40_high_risk"
        variable.probability = 0.08
        variable = discreteDistribution.variables.add()
        variable.name = "bmi_35_to_39_moderate_risk"
        variable.probability = 0.10
        variable = discreteDistribution.variables.add()
        variable.name = "bmi_30_to_34_low_risk"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "bmi_25_to_29_overweight"
        variable.probability = 0.30
        variable = discreteDistribution.variables.add()
        variable.name = "bmi_under_25_healthy"
        variable.probability = 0.32

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "hip"
        variable = discreteDistribution.variables.add()
        variable.name = "hip_above_133.30"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "hip_above_112.70_to_133.30_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "hip_above_103.10_to_112.70_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "hip_above_95.20_to_103.10_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "hip_95.20_and_below"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "height"
        variable = discreteDistribution.variables.add()
        variable.name = "height_150.50_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "height_above_150.50_to_158.50_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "height_above_158.50_to_165.50_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "height_above_165.50_to_173.40_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "height_above_173.40"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "waist"
        variable = discreteDistribution.variables.add()
        variable.name = "waist_above_129.70"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "waist_above_109.00_to_129.70_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "waist_above_96.70_to_109.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "waist_above_84.50_to_96.70_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "waist_84.50_and_below"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "weight"
        variable = discreteDistribution.variables.add()
        variable.name = "weight_above_123.90"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "weight_above_92.60_to_123.90_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "weight_above_76.70_to_92.60_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "weight_above_63.60_to_76.70_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "weight_63.60_and_below"
        variable.probability = 0.25




#Type 2 diabetes
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "a1c"
        variable = discreteDistribution.variables.add()
        variable.name = "a1c_diabetes_6.5_and_above"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "a1c_prediabetes_low_5.7_to_6.4"
        variable.probability = 0.27
        variable = discreteDistribution.variables.add()
        variable.name = "a1c_high_normal_5.3_to_5.6"
        variable.probability = 0.35
        variable = discreteDistribution.variables.add()
        variable.name = "a1c_low_normal_below_5.3"
        variable.probability = 0.25

#PTSD
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "anxious_how_often"
        variable = discreteDistribution.variables.add()
        variable.name = "anxious_daily"
        variable.probability = 0.15
        variable = discreteDistribution.variables.add()
        variable.name = "anxious_weekly"
        variable.probability = 0.14
        variable = discreteDistribution.variables.add()
        variable.name = "anxious_monthly"
        variable.probability = 0.12
        variable = discreteDistribution.variables.add()
        variable.name = "anxious_a_few_times_per_year"
        variable.probability = 0.34
        variable = discreteDistribution.variables.add()
        variable.name = "anxious_never"
        variable.probability = 0.25
        
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "marital_status"
        variable = discreteDistribution.variables.add()
        variable.name = "widowed"
        variable.probability = 0.08
        variable = discreteDistribution.variables.add()
        variable.name = "separated"
        variable.probability = 0.04
        variable = discreteDistribution.variables.add()
        variable.name = "divorced"
        variable.probability = 0.11
        variable = discreteDistribution.variables.add()
        variable.name = "never_married"
        variable.probability = 0.18
        variable = discreteDistribution.variables.add()
        variable.name = "living_with_partner-or_married"
        variable.probability = 0.59

     
#Frailty


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "birth_weight"
        variable = discreteDistribution.variables.add()
        variable.name = "birth_weight_under_5_lbs"
        variable.probability = 0.21
        variable = discreteDistribution.variables.add()
        variable.name = "birth_weight_5_to_6_lbs"
        variable.probability = 0.23
        variable = discreteDistribution.variables.add()
        variable.name = "birth_weight_7_to_8_lbs"
        variable.probability = 0.22
        variable = discreteDistribution.variables.add()
        variable.name = "birth_weight_9_to_11_lbs"
        variable.probability = 0.14
        variable = discreteDistribution.variables.add()
        variable.name = "birth_weight_above_11_lbs"
        variable.probability = 0.17
        
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "asthma_attack_last_year"
        variable = discreteDistribution.variables.add()
        variable.name = "asthma_attack_last_year_yes"
        variable.probability = 0.41
        variable = discreteDistribution.variables.add()
        variable.name = "asthma_attack_last_year_no"
        variable.probability = 0.58

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "liver_condition"
        variable = discreteDistribution.variables.add()
        variable.name = "liver_condition_yes"
        variable.probability = 0.00
        variable = discreteDistribution.variables.add()
        variable.name = "liver_condition_no"
        variable.probability = 1.00
        

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "fatiqued_in_2_weeks"
        variable = discreteDistribution.variables.add()
        variable.name = "fatiqued_in_2_weeks_nearly_everyday"
        variable.probability = 0.08
        variable = discreteDistribution.variables.add()
        variable.name = "fatiqued_in_2_weeks_more_than_half_the_days"
        variable.probability = 0.09
        variable = discreteDistribution.variables.add()
        variable.name = "fatiqued_in_2_weeks_several_days"
        variable.probability = 0.32
        variable = discreteDistribution.variables.add()
        variable.name = "fatiqued_in_2_weeks_none"
        variable.probability = 0.51


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "osteoporosis"
        variable = discreteDistribution.variables.add()
        variable.name = "osteoporosis_yes"
        variable.probability = 0.13
        variable = discreteDistribution.variables.add()
        variable.name = "osteoporosis_no"
        variable.probability = 0.87

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "artificial_joints"
        variable = discreteDistribution.variables.add()
        variable.name = "artificial_joints_yes"
        variable.probability = 0.30
        variable = discreteDistribution.variables.add()
        variable.name = "artificial_joints_no"
        variable.probability = 0.70


#Labs


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "lymphocite_number"
        variable = discreteDistribution.variables.add()
        variable.name = "lymphocite_number_below_normal_under_1"
        variable.probability = 0.01
        variable = discreteDistribution.variables.add()
        variable.name = "lymphocite_number_low_normal_1_to 1.9"
        variable.probability = 0.36
        variable = discreteDistribution.variables.add()
        variable.name = "lymphocite_number_mid_normal_2_to_2.9"
        variable.probability = 0.47
        variable = discreteDistribution.variables.add()
        variable.name = "lymphocite_number_high_normal_3_to_4.8"
        variable.probability = 0.14
        variable = discreteDistribution.variables.add()
        variable.name = "lymphocite_number_above_normal_above_4.8"
        variable.probability = 0.14
        
        

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "mchc"
        variable = discreteDistribution.variables.add()
        variable.name = "mchc_34.6_and_above"
        variable.probability = 0.14
        variable = discreteDistribution.variables.add()
        variable.name = "mchc_34.0_to_34.5"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "mchc_33.4_to_33.9"
        variable.probability = 0.30
        variable = discreteDistribution.variables.add()
        variable.name = "mchc_33.0_to_33.3"
        variable.probability = 0.16
        variable = discreteDistribution.variables.add()
        variable.name = "mchc_below_33"
        variable.probability = 0.20

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "nucleated_red_blood_cells"
        variable = discreteDistribution.variables.add()
        variable.name = "nucleated_red_blood_cells_high_0.2"
        variable.probability = 0.09
        variable = discreteDistribution.variables.add()
        variable.name = "nucleated_red_blood_cells_high_normal_0.1"
        variable.probability = 0.56
        variable = discreteDistribution.variables.add()
        variable.name = "nucleated_red_blood_cells_low_normal_0.0"
        variable.probability = 0.32

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "blood_urea_nitrogen"
        variable = discreteDistribution.variables.add()
        variable.name = "blood_urea_nitrogen_20.0_and_above"
        variable.probability = 0.12
        variable = discreteDistribution.variables.add()
        variable.name = "blood_urea_nitrogen_15.0_to_19.0"
        variable.probability = 0.28
        variable = discreteDistribution.variables.add()
        variable.name = "blood_urea_nitrogen_10.0_to_14"
        variable.probability = 0.45
        variable = discreteDistribution.variables.add()
        variable.name = "blood_urea_nitrogen_below_9.0"
        variable.probability = 0.15
        
        
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "chloride"
        variable = discreteDistribution.variables.add()
        variable.name = "chloride_low_below_96.0"
        variable.probability = 0.02
        variable.name = "chloride_normal_low_96.0_to_99.0"
        variable.probability = 0.24
        variable = discreteDistribution.variables.add()
        variable.name = "chloride_normal_medium_100.0_to_103.0"
        variable.probability = 0.56
        variable = discreteDistribution.variables.add()
        variable.name = "chloride_normal_high_104.0_to_106.0"
        variable.probability = 0.16
        variable = discreteDistribution.variables.add()
        variable.name = "chloride_high_above_106.0"
        variable.probability = 0.02

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "globulin"
        variable = discreteDistribution.variables.add()
        variable.name = "globulin_high_3.6 and_higher"
        variable.probability = 0.13
        variable = discreteDistribution.variables.add()
        variable.name = "globulin_3.1_to_3.5"
        variable.probability = 0.38
        variable = discreteDistribution.variables.add()
        variable.name = "globulin_2.6_TO_3.0"
        variable.probability = 0.40
        variable = discreteDistribution.variables.add()
        variable.name = "globulin_low_2.5_and_below"
        variable.probability = 0.08
        
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "sodium"
        variable = discreteDistribution.variables.add()
        variable.name = "sodium_below_135"
        variable.probability = 0.01
        variable = discreteDistribution.variables.add()
        variable.name = "sodium_135.0_to_140.0"
        variable.probability = 0.51
        variable = discreteDistribution.variables.add()
        variable.name = "sodium_141.0_to_145.0"
        variable.probability = 0.44
        variable = discreteDistribution.variables.add()
        variable.name = "sodium_146.0_and_higher"
        variable.probability = 0.02

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "bilirubin"
        variable = discreteDistribution.variables.add()
        variable.name = "bilirubin_0.6_and_above"
        variable.probability = 0.26
        variable = discreteDistribution.variables.add()
        variable.name = "bilirubin_0.4_to_0.5"
        variable.probability = 0.33
        variable = discreteDistribution.variables.add()
        variable.name = "bilirubin_0.3"
        variable.probability = 0.22
        variable = discreteDistribution.variables.add()
        variable.name = "bilirubin_below_0.2"
        variable.probability = 0.19
        
        
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "total_protein"
        variable = discreteDistribution.variables.add()
        variable.name = "total_protein_below_6.9"
        variable.probability = 0.22
        variable = discreteDistribution.variables.add()
        variable.name = "total_protein_6.9_to_7.1"
        variable.probability = 0.26
        variable = discreteDistribution.variables.add()
        variable.name = "total_protein_7.2_to_7.4"
        variable.probability = 0.28
        variable = discreteDistribution.variables.add()
        variable.name = "total_protein_7.5_and_above"
        variable.probability = 0.24
        

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "toxins_in_blood"
        variable = discreteDistribution.variables.add()
        variable.name = "toxins_in_blood_above_0.006"
        variable.probability = 0.07
        variable = discreteDistribution.variables.add()
        variable.name = "toxins_in_blood_0.005_to_0.006"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "toxins_in_blood_0.004_and_below"
        variable.probability = 0.87

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "segmented_neutrophils"
        variable = discreteDistribution.variables.add()
        variable.name = "segmented_neutrophils_high_above_6"
        variable.probability = 0.12
        variable = discreteDistribution.variables.add()
        variable.name = "segmented_neutrophils_normal_2.5_to_6"
        variable.probability = 0.74
        variable = discreteDistribution.variables.add()
        variable.name = "segmented_neutrophils_low_under_2.5"
        variable.probability = 0.14

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "cadmium"
        variable = discreteDistribution.variables.add()
        variable.name = "cadmium_high_above_5"
        variable.probability = 0.00
        variable = discreteDistribution.variables.add()
        variable.name = "cadmium_high_normal_2_to_5"
        variable.probability = 0.02
        variable = discreteDistribution.variables.add()
        variable.name = "cadmium_normal"
        variable.probability = 0.22
        variable = discreteDistribution.variables.add()
        variable.name = "cadmium_low"
        variable.probability = 0.76

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "cobolt"
        variable = discreteDistribution.variables.add()
        variable.name = "cobolt_high_above_1.8"
        variable.probability = 0.00
        variable = discreteDistribution.variables.add()
        variable.name = "cobolt_high_normal_1.0_to_1.8"
        variable.probability = 0.00
        variable = discreteDistribution.variables.add()
        variable.name = "cobolt_normal_below_1"
        variable.probability = 1.00

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "chromium"
        variable = discreteDistribution.variables.add()
        variable.name = "chromium_0.29_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "chromium_above_0.29_to_0.29_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "chromium_above_0.29_to_0.29_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "chromium_above_0.29_to_0.29_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "chromium_above_0.29"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "mercury"
        variable = discreteDistribution.variables.add()
        variable.name = "mercury_above_4.04"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "mercury_above_1.07_to_4.04_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "mercury_above_0.42_to_1.07_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "mercury_above_0.18_to_0.42_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "mercury_0.18_and_below"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "manganese"
        variable = discreteDistribution.variables.add()
        variable.name = "manganese_high_above_36.6"
        variable.probability = 0.00
        variable = discreteDistribution.variables.add()
        variable.name = "manganese_normal_high_18.3_to_36.6"
        variable.probability = 0.03
        variable = discreteDistribution.variables.add()
        variable.name = "manganese_normal_4.7_to_below_18.3"
        variable.probability = 0.94
        variable = discreteDistribution.variables.add()
        variable.name = "manganese_low_below_4.7"
        variable.probability = 0.03

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "lead"
        variable = discreteDistribution.variables.add()
        variable.name = "lead_above_2.95"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "lead_above_1.38_to_2.95_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "lead_above_0.83_to_1.38_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "lead_above_0.48_to_0.83_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "lead_0.48_and_below"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "selenium"
        variable = discreteDistribution.variables.add()
        variable.name = "selenium_152.66_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "selenium_above_152.66_to_173.56_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "selenium_above_173.56_to_188.11_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "selenium_above_188.11_to_204.17_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "selenium_above_204.17"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "cotinine"
        variable = discreteDistribution.variables.add()
        variable.name = "cotinine_above_323.00"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "cotinine_above_1.01_to_323.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "cotinine_above_0.03_to_1.01_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "cotinine_above_0.01_to_0.03_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "cotinine_0.01_and_below"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "eosinophils_percent"
        variable = discreteDistribution.variables.add()
        variable.name = "eosinophils_percent_above_6.70"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "eosinophils_percent_above_3.50_to_6.70_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "eosinophils_percent_above_2.30_to_3.50_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "eosinophils_percent_above_1.50_to_2.30_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "eosinophils_percent_1.50_and_below"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "ferritin"
        variable = discreteDistribution.variables.add()
        variable.name = "ferritin_high_above_336"
        variable.probability = 0.08
        variable = discreteDistribution.variables.add()
        variable.name = "ferritin_normal_11_to_336"
        variable.probability = 0.87
        variable = discreteDistribution.variables.add()
        variable.name = "ferritin_low_below_11"
        variable.probability = 0.05

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "fasting_glucose"
        variable = discreteDistribution.variables.add()
        variable.name = "fasting_glucose_high_above_100"
        variable.probability = 0.57
        variable = discreteDistribution.variables.add()
        variable.name = "fasting_glucose_normal_70_to_100"
        variable.probability = 0.43
        variable = discreteDistribution.variables.add()
        variable.name = "fasting_glucose_low_below_70"
        variable.probability = 0.00

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "hemoglobin"
        variable = discreteDistribution.variables.add()
        variable.name = "hemoglobin_severe_amemia_below_8"
        variable.probability = 0.00
        variable = discreteDistribution.variables.add()
        variable.name = "hemoglobin_moderate_amemia_8_tto_10"
        variable.probability = 0.01
        variable = discreteDistribution.variables.add()
        variable.name = "hemoglobin_slight_anemia_above_10_to_12"
        variable.probability = 0.08
        variable = discreteDistribution.variables.add()
        variable.name = "hemoglobin_normal_above_12"
        variable.probability = 0.89


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "serum_iron"
        variable = discreteDistribution.variables.add()
        variable.name = "serum_iron_35.00_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "serum_iron_above_35.00_to_61.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "serum_iron_above_61.00_to_82.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "serum_iron_above_82.00_to_106.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "serum_iron_above_106.00"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "lymphocyte"
        variable = discreteDistribution.variables.add()
        variable.name = "lymphocyte_18.00_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "lymphocyte_above_18.00_to_25.60_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "lymphocyte_above_25.60_to_31.30_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "lymphocyte_above_31.30_to_37.40_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "lymphocyte_above_37.40"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "mean_cell_volume"
        variable = discreteDistribution.variables.add()
        variable.name = "mean_cell_volume_77.40_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "mean_cell_volume_above_77.40_to_84.80_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "mean_cell_volume_above_84.80_to_88.40_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "mean_cell_volume_above_88.40_to_91.70_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "mean_cell_volume_above_91.70"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "segmented_neutrophils_percent"
        variable = discreteDistribution.variables.add()
        variable.name = "segmented_neutrophils_percent_above_71.90"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "segmented_neutrophils_percent_above_63.10_to_71.90_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "segmented_neutrophils_percent_above_57.00_to_63.10_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "segmented_neutrophils_percent_above_50.40_to_57.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "segmented_neutrophils_percent_50.40_and_below"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "red_cell_distribution_ width"
        variable = discreteDistribution.variables.add()
        variable.name = "red_cell_distribution_ width_above_16.30"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "red_cell_distribution_ width_above_14.20_to_16.30_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "red_cell_distribution_ width_above_13.50_to_14.20_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "red_cell_distribution_ width_above_13.00_to_13.50_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "red_cell_distribution_ width_13.00_and_below"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "alkaline_phosphatase"
        variable = discreteDistribution.variables.add()
        variable.name = "alkaline_phosphatase_high_above_147"
        variable.probability = 0.07
        variable = discreteDistribution.variables.add()
        variable.name = "alkaline_phosphatase_normal_147_to_44"
        variable.probability = 0.90
        variable = discreteDistribution.variables.add()
        variable.name = "alkaline_phosphatase_low_below_44"
        variable.probability = 0.03

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "aspartate_aminotransferase"
        variable = discreteDistribution.variables.add()
        variable.name = "aspartate_aminotransferase_high_above_33"
        variable.probability = 0.07
        variable = discreteDistribution.variables.add()
        variable.name = "aspartate_aminotransferase_normal_8_to_33"
        variable.probability = 0.93
        variable = discreteDistribution.variables.add()
        variable.name = "aspartate_aminotransferase_low_below_8"
        variable.probability = 0.00

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "alanine_aminotransferase"
        variable = discreteDistribution.variables.add()
        variable.name = "alanine_aminotransferase_high_above_36"
        variable.probability = 0.11
        variable = discreteDistribution.variables.add()
        variable.name = "alanine_aminotransferase_medium_4_to_36"
        variable.probability = 0.89
        variable = discreteDistribution.variables.add()
        variable.name = "alanine_aminotransferase_low_below_4"
        variable.probability = 0.00

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "creatine_phosphokinase"
        variable = discreteDistribution.variables.add()
        variable.name = "creatine_phosphokinase_high_above_192"
        variable.probability = 0.23
        variable = discreteDistribution.variables.add()
        variable.name = "creatine_phosphokinase_normal_26_to_192"
        variable.probability = 0.77
        variable = discreteDistribution.variables.add()
        variable.name = "creatine_phosphokinase_low_under_26"
        variable.probability = 0.00

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "creatinine"
        variable = discreteDistribution.variables.add()
        variable.name = "creatinine_high_above_1.2"
        variable.probability = 0.08
        variable = discreteDistribution.variables.add()
        variable.name = "creatinine_normal_0.6_to_1.2"
        variable.probability = 0.79
        variable = discreteDistribution.variables.add()
        variable.name = "creatinine_low_below_0.6"
        variable.probability = 0.13


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "glucose_serum"
        variable = discreteDistribution.variables.add()
        variable.name = "glucose_serum_above_155.00"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "glucose_serum_above_101.00_to_155.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "glucose_serum_above_92.00_to_101.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "glucose_serum_above_86.00_to_92.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "glucose_serum_86.00_and_below"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "gamma_glutamyl_transferase"
        variable = discreteDistribution.variables.add()
        variable.name = "gamma_glutamyl_transferase_high_above_30"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "gamma_glutamyl_transferase_normal_30_to_10"
        variable.probability = 0.75
        variable = discreteDistribution.variables.add()
        variable.name = "gamma_glutamyl_transferase_low_below_10"
        variable.probability = 0.00

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "iron"
        variable = discreteDistribution.variables.add()
        variable.name = "iron_36.00_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "iron_above_36.00_to_62.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "iron_above_62.00_to_83.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "iron_above_83.00_to_107.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "iron_above_107.00"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "triglycerides"
        variable = discreteDistribution.variables.add()
        variable.name = "triglycerides_high_above_199"
        variable.probability = 0.16
        variable = discreteDistribution.variables.add()
        variable.name = "triglycerides_medium_199_to_150"
        variable.probability = 0.14
        variable = discreteDistribution.variables.add()
        variable.name = "triglycerides_low_below_150"
        variable.probability = 0.70

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "uric_acid"
        variable = discreteDistribution.variables.add()
        variable.name = "uric_acid_high_above_8.5"
        variable.probability = 0.03
        variable = discreteDistribution.variables.add()
        variable.name = "uric_acid_medium_2.7_to_8.5"
        variable.probability = 0.96
        variable = discreteDistribution.variables.add()
        variable.name = "uric_acid_low_below_2.7"
        variable.probability = 0.01

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "total_cholesterol"
        variable = discreteDistribution.variables.add()
        variable.name = "total_cholesterol_high_above_200"
        variable.probability = 0.30
        variable = discreteDistribution.variables.add()
        variable.name = "total_cholesterol_normal_125_to_200"
        variable.probability = 0.64
        variable = discreteDistribution.variables.add()
        variable.name = "total_cholesterol_low_below_125"
        variable.probability = 0.06

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "benzonitrile"
        variable = discreteDistribution.variables.add()
        variable.name = "benzonitrile_above_0.17"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "benzonitrile_above_0.11_to_0.17_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "benzonitrile_above_0.11_to_0.11_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "benzonitrile_above_0.11_to_0.11_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "benzonitrile_0.11_and_below"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "vitamin_C"
        variable = discreteDistribution.variables.add()
        variable.name = "vitamin_C_low_below_0.6"
        variable.probability = 0.28
        variable = discreteDistribution.variables.add()
        variable.name = "vitamin_C_medium_0.6_to_2"
        variable.probability = 0.70
        variable = discreteDistribution.variables.add()
        variable.name = "vitamin_C_high_above_2"
        variable.probability = 0.02

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "white_blood_cell_count"
        variable = discreteDistribution.variables.add()
        variable.name = "white_blood_cell_count_low_below_3.4"
        variable.probability = 0.01
        variable = discreteDistribution.variables.add()
        variable.name = "white_blood_cell_count_normal_3.4_to_9.6"
        variable.probability = 0.86
        variable = discreteDistribution.variables.add()
        variable.name = "white_blood_cell_count_high_above_9.6"
        variable.probability = 0.13

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "albumin_creatinine_ratio"
        variable = discreteDistribution.variables.add()
        variable.name = "albumin_creatinine_ratio_high_above_300"
        variable.probability = 0.02
        variable = discreteDistribution.variables.add()
        variable.name = "albumin_creatinine_ratio_elevated_30_to_300"
        variable.probability = 0.11
        variable = discreteDistribution.variables.add()
        variable.name = "albumin_creatinine_ratio_normal_below_30"
        variable.probability = 0.87

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "volitile_organic_compound"
        variable = discreteDistribution.variables.add()
        variable.name = "volitile_organic_compound_above_309028.71"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "volitile_organic_compound_above_93803.69_to_309028.71_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "volitile_organic_compound_above_51906.89_to_93803.69_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "volitile_organic_compound_above_29036.52_to_51906.89_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "volitile_organic_compound_29036.52_and_below"
        variable.probability = 0.25




#Sarcopenia

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "work_limiting_problem"
        variable = discreteDistribution.variables.add()
        variable.name = "work_limiting_problem_yes"
        variable.probability = 0.26
        variable = discreteDistribution.variables.add()
        variable.name = "work_limiting_problem_no"
        variable.probability = 0.74

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "ten_stairs_difficulty"
        variable = discreteDistribution.variables.add()
        variable.name = "ten_stairs_difficulty_unable"
        variable.probability = 0.01
        variable = discreteDistribution.variables.add()
        variable.name = "ten_stairs_difficulty_much"
        variable.probability = 0.03
        variable = discreteDistribution.variables.add()
        variable.name = "ten_stairs_difficulty_some"
        variable.probability = 0.15
        variable = discreteDistribution.variables.add()
        variable.name = "ten_stairs_difficulty_none"
        variable.probability = 0.80
        
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "chore_difficulty"
        variable = discreteDistribution.variables.add()
        variable.name = "chore_difficulty_unable"
        variable.probability = 0.03
        variable = discreteDistribution.variables.add()
        variable.name = "chore_difficulty_much"
        variable.probability = 0.07
        variable = discreteDistribution.variables.add()
        variable.name = "chore_difficulty_some"
        variable.probability = 0.26
        variable = discreteDistribution.variables.add()
        variable.name = "chore_difficulty_none"
        variable.probability = 0.64

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "walking_difficulty"
        variable = discreteDistribution.variables.add()
        variable.name = "walking_difficulty_unable"
        variable.probability = 0.01
        variable = discreteDistribution.variables.add()
        variable.name = "walking_difficulty_much"
        variable.probability = 0.03
        variable = discreteDistribution.variables.add()
        variable.name = "walking_difficulty_some"
        variable.probability = 0.13
        variable = discreteDistribution.variables.add()
        variable.name = "walking_difficulty_none"
        variable.probability = 0.83

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "stand_from_sit_difficulty"
        variable = discreteDistribution.variables.add()
        variable.name = "stand_from_sit_difficulty_unable"
        variable.probability = 0.02
        variable = discreteDistribution.variables.add()
        variable.name = "stand_from_sit_difficulty_much"
        variable.probability = 0.06
        variable = discreteDistribution.variables.add()
        variable.name = "stand_from_sit_difficulty_some"
        variable.probability = 0.24
        variable = discreteDistribution.variables.add()
        variable.name = "stand_from_sit_difficulty_none"
        variable.probability = 0.68
        
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "two_hour_standing_difficulty"
        variable = discreteDistribution.variables.add()
        variable.name = "two_hour_standing_difficulty_unable"
        variable.probability = 0.10
        variable = discreteDistribution.variables.add()
        variable.name = "two_hour_standing_difficulty_much"
        variable.probability = 0.16
        variable = discreteDistribution.variables.add()
        variable.name = "two_hour_standing_difficulty_some"
        variable.probability = 0.27
        variable = discreteDistribution.variables.add()
        variable.name = "two_hour_standing_difficulty_none"
        variable.probability = 0.47
        

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "two_hour_sitting_difficulty"
        variable = discreteDistribution.variables.add()
        variable.name = "two_hour_sitting_difficulty_unable"
        variable.probability = 0.02
        variable = discreteDistribution.variables.add()
        variable.name = "two_hour_sitting_difficulty_much"
        variable.probability = 0.08
        variable = discreteDistribution.variables.add()
        variable.name = "two_hour_sitting_difficulty_some"
        variable.probability = 0.23
        variable = discreteDistribution.variables.add()
        variable.name = "two_hour_sitting_difficulty_none"
        variable.probability = 0.67

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "social_activity_difficulty"
        variable = discreteDistribution.variables.add()
        variable.name = "social_activity_difficulty_unable"
        variable.probability = 0.03
        variable = discreteDistribution.variables.add()
        variable.name = "social_activity_difficulty_much"
        variable.probability = 0.06
        variable = discreteDistribution.variables.add()
        variable.name = "social_activity_difficulty_some"
        variable.probability = 0.19
        variable = discreteDistribution.variables.add()
        variable.name = "social_activity_difficulty_none"
        variable.probability = 0.72


#Incontinence

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "urine_leakage_bother"
        variable = discreteDistribution.variables.add()
        variable.name = "urine_leakage_bother_greatly"
        variable.probability = 0.12
        variable = discreteDistribution.variables.add()
        variable.name = "urine_leakage_bother_very_much"
        variable.probability = 0.21
        variable = discreteDistribution.variables.add()
        variable.name = "urine_leakage_bother_somewhat"
        variable.probability = 0.32
        variable = discreteDistribution.variables.add()
        variable.name = "urine_leakage_bother_none"
        variable.probability = 0.34
        


        #Hearing
                

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "hearing_difficulty_how_often"
        variable = discreteDistribution.variables.add()
        variable.name = "hearing_difficulty_always"
        variable.probability = 0.08
        variable = discreteDistribution.variables.add()
        variable.name = "hearing_difficulty_usually"
        variable.probability = 0.12
        variable = discreteDistribution.variables.add()
        variable.name = "hearing_difficulty_about_half_the_time"
        variable.probability = 0.19
        variable = discreteDistribution.variables.add()
        variable.name = "hearing_difficulty_seldom"
        variable.probability = 0.33
        variable = discreteDistribution.variables.add()
        variable.name = "hearing_difficulty_never"
        variable.probability = 0.29


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "hearing_frustration_how_ofter"
        variable = discreteDistribution.variables.add()
        variable.name = "hearing_frustration_always"
        variable.probability = 0.04
        variable = discreteDistribution.variables.add()
        variable.name = "hearing_frustration_usually"
        variable.probability = 0.06
        variable = discreteDistribution.variables.add()
        variable.name = "hearing_frustration_about_half_the_time"
        variable.probability = 0.10
        variable = discreteDistribution.variables.add()
        variable.name = "hearing_frustration_seldom"
        variable.probability = 0.22
        variable = discreteDistribution.variables.add()
        variable.name = "hearing_frustration_never"
        variable.probability = 0.58


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "wear_hearing_aid"
        variable = discreteDistribution.variables.add()
        variable.name = "wear_hearing_aid_yes"
        variable.probability = 0.09
        variable = discreteDistribution.variables.add()
        variable.name = "wear_hearing_aid_no"
        variable.probability = 0.91


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "loud_noise_job"
        variable = discreteDistribution.variables.add()
        variable.name = "loud_noise_job_yes"
        variable.probability = 0.30
        variable = discreteDistribution.variables.add()
        variable.name = "loud_noise_job_no"
        variable.probability = 0.7

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "loud_music"
        variable = discreteDistribution.variables.add()
        variable.name = "loud_music_yes"
        variable.probability = 0.11
        variable = discreteDistribution.variables.add()
        variable.name = "loud_music_no"
        variable.probability = 0.89



#Low HDL

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "direct_HDL"
        variable = discreteDistribution.variables.add()
        variable.name = "direct_HDL_low_below_40"
        variable.probability = 0.19
        variable = discreteDistribution.variables.add()
        variable.name = "direct_HDL_normal_40_to_60"
        variable.probability = 0.56
        variable = discreteDistribution.variables.add()
        variable.name = "direct_HDL_high_above_60"
        variable.probability = 0.25


#Folic acid

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "folic_acid"
        variable = discreteDistribution.variables.add()
        variable.name = "folic_acid_low_below_4.5"
        variable.probability = 0.97
        variable = discreteDistribution.variables.add()
        variable.name = "folic_acid_normal_4.5_to_45.3"
        variable.probability = 0.03
        variable = discreteDistribution.variables.add()
        variable.name = "folic_acid_high_above_45.3"
        variable.probability = 0.00

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "folate"
        variable = discreteDistribution.variables.add()
        variable.name = "folate_low_below_4.5"
        variable.probability = 0.00
        variable = discreteDistribution.variables.add()
        variable.name = "folate_normal_4.5_to_45.3"
        variable.probability = 0.68
        variable = discreteDistribution.variables.add()
        variable.name = "folate_high_above_45.3"
        variable.probability = 0.32

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "folate_mefox"
        variable = discreteDistribution.variables.add()
        variable.name = "folate_mefox_0.41_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "folate_mefox_above_0.41_to_0.74_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "folate_mefox_above_0.74_to_1.19_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "folate_mefox_above_1.19_to_2.10_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "folate_mefox_above_2.10"
        variable.probability = 0.25

#Smoking
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "second_hand_smoke"
        variable = discreteDistribution.variables.add()
        variable.name = "second_hand_smoke_yes"
        variable.probability = 0.31
        variable = discreteDistribution.variables.add()
        variable.name = "second_hand_smoke_no"
        variable.probability = 0.69


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "five_days_smoke_cigarettes"
        variable = discreteDistribution.variables.add()
        variable.name = "five_days_smoke_cigarettes_yes"
        variable.probability = 0.19
        variable = discreteDistribution.variables.add()
        variable.name = "five_days_smoke_cigarettes_no"
        variable.probability = 0.81

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "ever_vaped"
        variable = discreteDistribution.variables.add()
        variable.name = "ever_vaped_yes"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "ever_vaped_no"
        variable.probability = 0.80





#Male gender 

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "gender"
        variable = discreteDistribution.variables.add()
        variable.name = "male"
        variable.probability = 0.49
        variable = discreteDistribution.variables.add()
        variable.name = "female"
        variable.probability = 0.51
        

#Poor sleep
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "work_schedule"
        variable = discreteDistribution.variables.add()
        variable.name = "work_schedule_evenings_or_nights"
        variable.probability = 0.13
        variable = discreteDistribution.variables.add()
        variable.name = "work_schedule_variable"
        variable.probability = 0.36
        variable = discreteDistribution.variables.add()
        variable.name = "work_schedule_early_mornings"
        variable.probability = 0.15
        variable = discreteDistribution.variables.add()
        variable.name = "work_schedule_9_to_5"
        variable.probability = 0.36
        

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "workday_sleep_hours_per_night"
        variable = discreteDistribution.variables.add()
        variable.name = "workday_sleep_under_5"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "workday_sleep_5.0_to_6.5"
        variable.probability = 0.21
        variable = discreteDistribution.variables.add()
        variable.name = "workday_sleep_7.0_to_8.5"
        variable.probability = 0.50
        variable = discreteDistribution.variables.add()
        variable.name = "workday_sleep_9.0_to_10.5"
        variable.probability = 0.21
        variable = discreteDistribution.variables.add()
        variable.name = "workday_sleep_11_or_more"
        variable.probability = 0.03


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "weekday_sleep_hours_per_night"
        variable = discreteDistribution.variables.add()
        variable.name = "weekday_sleep_under_5"
        variable.probability = 0.02
        variable = discreteDistribution.variables.add()
        variable.name = "weekday_sleep_5.0_to_6.5"
        variable.probability = 0.12
        variable = discreteDistribution.variables.add()
        variable.name = "weekday_sleep_7.0_to_8.5"
        variable.probability = 0.42
        variable = discreteDistribution.variables.add()
        variable.name = "weekday_sleep_9.0_to_10.5"
        variable.probability = 0.34
        variable = discreteDistribution.variables.add()
        variable.name = "weekday_sleep_11_or_more"
        variable.probability = 0.09
        


#Lack of exercise

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "shortness_of_breath_exertion"
        variable = discreteDistribution.variables.add()
        variable.name = "shortness_of_breath_exertion_yes"
        variable.probability = 0.38
        variable = discreteDistribution.variables.add()
        variable.name = "shortness_of_breath_exertion_no"
        variable.probability = 0.62

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "daily_walk_or_bicycle_travel"
        variable = discreteDistribution.variables.add()
        variable.name = "daily_walk_or_bicycle_travel_less_than_30_minutes"
        variable.probability = 0.34
        variable = discreteDistribution.variables.add()
        variable.name = "daily_walk_or_bicycle_travel_30_to_59_minutes"
        variable.probability = 0.30
        variable = discreteDistribution.variables.add()
        variable.name = "daily_walk_or_bicycle_travel_60_minutes_or_more"
        variable.probability = 0.36
        
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "daily_time_sitting"
        variable = discreteDistribution.variables.add()
        variable.name = "daily_time_sitting_12_or_more_hours"
        variable.probability = 0.08
        variable = discreteDistribution.variables.add()
        variable.name = "daily_time_sitting_over_6_but_less_than_12_hours"
        variable.probability = 0.36
        variable = discreteDistribution.variables.add()
        variable.name = "daily_time_sitting_over_2_but_less_than_6_hours"
        variable.probability = 0.49
        variable = discreteDistribution.variables.add()
        variable.name = "daily_time_sitting_less_than_2_hours"
        variable.probability = 0.06

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "physical_work"
        variable = discreteDistribution.variables.add()
        variable.name = "physical_work_no"
        variable.probability = 0.76
        variable = discreteDistribution.variables.add()
        variable.name = "physical_work_yes"
        variable.probability = 0.24

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "ten_minutes_daily_workout"
        variable = discreteDistribution.variables.add()
        variable.name = "ten_minutes_daily_workout_no"
        variable.probability = 0.60
        variable = discreteDistribution.variables.add()
        variable.name = "ten_minutes_daily_workout_yes"
        variable.probability = 0.40

#Poor diet

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "fish_last_month"
        variable = discreteDistribution.variables.add()
        variable.name = "fish_last_month_no"
        variable.probability = 0.36
        variable = discreteDistribution.variables.add()
        variable.name = "fish_last_month_yes"
        variable.probability = 0.64

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "tuna_eaten_times_per_month"
        variable = discreteDistribution.variables.add()
        variable.name = "tuna_eaten_per_month_8_or_more"
        variable.probability = 0.06
        variable = discreteDistribution.variables.add()
        variable.name = "tuna_eaten_per_month_4_to_7"
        variable.probability = 0.15
        variable = discreteDistribution.variables.add()
        variable.name = "tuna_eaten_per_month_2_to_3"
        variable.probability = 0.44
        variable = discreteDistribution.variables.add()
        variable.name = "tuna_eaten_per_month_0_or_1"
        variable.probability = 0.36


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "salt_how_often"
        variable = discreteDistribution.variables.add()
        variable.name = "salt_very_often"
        variable.probability = 0.18
        variable = discreteDistribution.variables.add()
        variable.name = "salt_occasionally"
        variable.probability = 0.29
        variable = discreteDistribution.variables.add()
        variable.name = "salt_rarely"
        variable.probability = 0.53
        

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "eat_out_how_many_times_per_week"
        variable = discreteDistribution.variables.add()
        variable.name = "eat_out_more_than_7_times_per_week"
        variable.probability = 0.08
        variable = discreteDistribution.variables.add()
        variable.name = "eat_out_5_to_7 times_per_week"
        variable.probability = 0.14
        variable = discreteDistribution.variables.add()
        variable.name = "eat_out_3_or_4_times_per_week"
        variable.probability = 0.21
        variable = discreteDistribution.variables.add()
        variable.name = "eat_out_1_or_2_times_per_week"
        variable.probability = 0.34
        variable = discreteDistribution.variables.add()
        variable.name = "eat_out_no_times_per_week"
        variable.probability = 0.22



        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "how_healthy_diet"
        variable = discreteDistribution.variables.add()
        variable.name = "how_healthy_diet_poor"
        variable.probability = 0.07
        variable = discreteDistribution.variables.add()
        variable.name = "how_healthy_diet_fair"
        variable.probability = 0.27
        variable = discreteDistribution.variables.add()
        variable.name = "how_healthy_diet_good"
        variable.probability = 0.39
        variable = discreteDistribution.variables.add()
        variable.name = "how_healthy_diet_very_good"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "how_healthy_diet_excellent"
        variable.probability = 0.08

#Nutritional Information

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_alpha_carotene"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_alpha_carotene_0.00_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_alpha_carotene_above_0.00_to_7.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_alpha_carotene_above_7.00_to_39.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_alpha_carotene_above_39.00_to_179.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_alpha_carotene_above_179.00"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_alpha_tocopherol"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_alpha_tocopherol_1.98_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_alpha_tocopherol_above_1.98_to_4.58_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_alpha_tocopherol_above_4.58_to_7.23_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_alpha_tocopherol_above_7.23_to_11.07_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_alpha_tocopherol_above_11.07"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_beta_carotene"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_beta_carotene_46.00_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_beta_carotene_above_46.00_to_257.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_beta_carotene_above_257.00_to_726.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_beta_carotene_above_726.00_to_2220.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_beta_carotene_above_2220.00"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_caffeine"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_caffeine_0.00_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_caffeine_above_0.00_to_4.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_caffeine_above_4.00_to_72.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_caffeine_above_72.00_to_173.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_caffeine_above_173.00"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_calcium"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_calcium_226.00_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_calcium_above_226.00_to_515.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_calcium_above_515.00_to_805.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_calcium_above_805.00_to_1176.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_calcium_above_1176.00"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_carbohydrate"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_carbohydrate_above_477.91"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_carbohydrate_above_311.79_to_477.91_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_carbohydrate_above_226.00_to_311.79_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_carbohydrate_above_161.15_to_226.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_carbohydrate_161.15_and_below"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_choline"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_choline_85.70_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_choline_above_85.70_to_178.90_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_choline_above_178.90_to_274.30_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_choline_above_274.30_to_417.10_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_choline_above_417.10"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_cholesterol"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_cholesterol_39.00_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_cholesterol_above_39.00_to_124.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_cholesterol_above_124.00_to_227.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_cholesterol_above_227.00_to_403.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_cholesterol_above_403.00"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_copper"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_copper_above_2.31"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_copper_above_1.40_to_2.31_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_copper_above_1.01_to_1.40_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_copper_above_0.70_to_1.01_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_copper_0.70_and_below"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_folate"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_folate_119.00_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_folate_above_119.00_to_264.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_folate_above_264.00_to_410.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_folate_above_410.00_to_622.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_folate_above_622.00"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_fiber"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_fiber_3.80_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_fiber_above_3.80_to_9.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_fiber_above_9.00_to_14.20_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_fiber_above_14.20_to_21.20_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_fiber_above_21.20"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_iron"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_iron_above_29.59"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_iron_above_17.42_to_29.59_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_iron_above_12.13_to_17.42_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_iron_above_8.24_to_12.13_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_iron_8.24_and_below"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_energy"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_energy_above_3939.00"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_energy_above_2612.00_to_3939.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_energy_above_1930.00_to_2612.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_energy_above_1399.00_to_1930.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_energy_1399.00_and_below"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_lycopene"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_lycopene_0.00_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_lycopene_above_0.00_to_0.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_lycopene_above_0.00_to_1547.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_lycopene_above_1547.00_to_5498.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_lycopene_above_5498.00"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_lutein"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_lutein_72.00_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_lutein_above_72.00_to_315.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_lutein_above_315.00_to_694.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_lutein_above_694.00_to_1395.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_lutein_above_1395.00"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_magnesium"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_magnesium_101.00_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_magnesium_above_101.00_to_186.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_magnesium_above_186.00_to_258.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_magnesium_above_258.00_to_355.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_magnesium_above_355.00"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_epa"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_epa_0.00_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_epa_above_0.00_to_0.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_epa_above_0.00_to_0.01_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_epa_above_0.01_to_0.02_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_epa_above_0.02"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_potassium"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_potassium_850.00_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_potassium_above_850.00_to_1591.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_potassium_above_1591.00_to_2277.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_potassium_above_2277.00_to_3125.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_potassium_above_3125.00"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_retinol"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_retinol_21.00_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_retinol_above_21.00_to_140.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_retinol_above_140.00_to_304.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_retinol_above_304.00_to_539.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_retinol_above_539.00"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_selenium"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_selenium_32.20_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_selenium_above_32.20_to_67.80_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_selenium_above_67.80_to_98.50_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_selenium_above_98.50_to_140.40_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_selenium_above_140.40"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_sodium"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_sodium_above_6872.00"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_sodium_above_4297.00_to_6872.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_sodium_above_3069.00_to_4297.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_sodium_above_2111.00_to_3069.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_sodium_2111.00_and_below"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_thiamin"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_thiamin_0.48_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_thiamin_above_0.48_to_0.95_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_thiamin_above_0.95_to_1.37_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_thiamin_above_1.37_to_1.97_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_thiamin_above_1.97"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_b12"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_b12_0.50_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_b12_above_0.50_to_1.76_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_b12_above_1.76_to_3.37_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_b12_above_3.37_to_5.79_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_b12_above_5.79"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_riboflavin"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_riboflavin_0.56_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_riboflavin_above_0.56_to_1.16_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_riboflavin_above_1.16_to_1.70_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_riboflavin_above_1.70_to_2.38_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_riboflavin_above_2.38"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_vitamin_C"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_vitamin_C_2.70_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_vitamin_C_above_2.70_to_17.80_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_vitamin_C_above_17.80_to_45.30_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_vitamin_C_above_45.30_to_104.20_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_vitamin_C_above_104.20"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_zinc"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_zinc_2.98_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_zinc_above_2.98_to_6.07_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_zinc_above_6.07_to_9.04_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_zinc_above_9.04_to_13.12_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_zinc_above_13.12"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "water_drank_yesterday"
        variable = discreteDistribution.variables.add()
        variable.name = "water_drank_yesterday_0.00_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "water_drank_yesterday_above_0.00_to_330.00_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "water_drank_yesterday_above_330.00_to_870.00_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "water_drank_yesterday_above_870.00_to_1633.50_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "water_drank_yesterday_above_1633.50"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_pfa"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_pfa_3.79_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_pfa_above_3.79_to_9.38_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_pfa_above_9.38_to_15.26_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_pfa_above_15.26_to_23.19_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_pfa_above_23.19"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_fat"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_fat_above_160.14"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_fat_above_98.77_to_160.14_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_fat_above_69.25_to_98.77_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_fat_above_44.92_to_69.25_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_fat_44.92_and_below"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dietary_b6"
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_b6_0.47_and_below"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_b6_above_0.47_to_1.04_and_below"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_b6_above_1.04_to_1.63_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_b6_above_1.63_to_2.40_and_below"
        variable.probability = 0.25
        variable = discreteDistribution.variables.add()
        variable.name = "dietary_b6_above_2.40"
        variable.probability = 0.25

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "alcohol_consumption_last_year"
        variable = discreteDistribution.variables.add()
        variable.name = "alcohol_daily"
        variable.probability = 0.06
        variable = discreteDistribution.variables.add()
        variable.name = "alcohol_2_to_4_times_per_week"
        variable.probability = 0.13
        variable = discreteDistribution.variables.add()
        variable.name = "alcohol_once_per_week_to_once_per_year"
        variable.probability = 0.57
        variable = discreteDistribution.variables.add()
        variable.name = "alcohol_never"
        variable.probability = 0.23


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "num_alcoholic_drinks_when_drinking"
        variable = discreteDistribution.variables.add()
        variable.name = "num_alcohol_8_or_more"
        variable.probability = 0.04
        variable = discreteDistribution.variables.add()
        variable.name = "num_alcohol_5_to_7"
        variable.probability = 0.08
        variable = discreteDistribution.variables.add()
        variable.name = "num_alcohol_3_to_4"
        variable.probability = 0.21
        variable = discreteDistribution.variables.add()
        variable.name = "num_alcohol_1_to_2"
        variable.probability = 0.68


#Low socioeconomic status

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "race"
        variable = discreteDistribution.variables.add()
        variable.name = "race_black"
        variable.probability = 0.23
        variable = discreteDistribution.variables.add()
        variable.name = "race_hispanic"
        variable.probability = 0.23
        variable = discreteDistribution.variables.add()
        variable.name = "race_other"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "race_white"
        variable.probability = 0.34




        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "education_level"
        variable = discreteDistribution.variables.add()
        variable.name = "education_level_less_than_9th_grade"
        variable.probability = 0.41
        variable = discreteDistribution.variables.add()
        variable.name = "education_level_9th_to_11th_grade"
        variable.probability = 0.40
        variable = discreteDistribution.variables.add()
        variable.name = "education_level_high_school_GED"
        variable.probability = 0.12
        variable = discreteDistribution.variables.add()
        variable.name = "education_level_at_least_some_college"
        variable.probability = 0.07
        
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "have_health_insurance"
        variable = discreteDistribution.variables.add()
        variable.name = "have_health_insurance_no"
        variable.probability = 0.14
        variable = discreteDistribution.variables.add()
        variable.name = "have_health_insurance_yes"
        variable.probability = 0.86

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "prescription_health_insurance"
        variable = discreteDistribution.variables.add()
        variable.name = "prescription_health_insurance_no"
        variable.probability = 0.07
        variable = discreteDistribution.variables.add()
        variable.name = "prescription_health_insurance_yes"
        variable.probability = 0.93

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "how_many_times_saw_doctor_last_year"
        variable = discreteDistribution.variables.add()
        variable.name = "saw_doctor_none_last_year"
        variable.probability = 0.16
        variable = discreteDistribution.variables.add()
        variable.name = "saw_doctor_1_or_2_times_last_year"
        variable.probability = 0.5
        variable = discreteDistribution.variables.add()
        variable.name = "saw_doctor_3_or_4_times_last_year"
        variable.probability = 0.21
        variable = discreteDistribution.variables.add()
        variable.name = "saw_doctor_over_4_times_last_year"
        variable.probability = 0.20
        

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "how_long_since_saw_doctor"
        variable = discreteDistribution.variables.add()
        variable.name = "never_saw_a_doctor"
        variable.probability = 0.04
        variable = discreteDistribution.variables.add()
        variable.name = "saw_doctor_more_than_5_years_ago"
        variable.probability = 0.15
        variable = discreteDistribution.variables.add()
        variable.name = "saw_doctor_2_to_5_years_ago"
        variable.probability = 0.29
        variable = discreteDistribution.variables.add()
        variable.name = "saw_doctor_1_to_2_years_ago"
        variable.probability = 0.35
        variable = discreteDistribution.variables.add()
        variable.name = "saw_doctor_6_to_12_months_ago"
        variable.probability = 0.08
        variable = discreteDistribution.variables.add()
        variable.name = "saw_doctor_less_than_6_months_ago"
        variable.probability = 0.08
        



        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "what_is_your_annual_household_income"
        variable = discreteDistribution.variables.add()
        variable.name = "under_20K"
        variable.probability = 0.21
        variable = discreteDistribution.variables.add()
        variable.name = "20K_to_55K"
        variable.probability = 0.34
        variable = discreteDistribution.variables.add()
        variable.name = "56K_to_100K"
        variable.probability = 0.21
        variable = discreteDistribution.variables.add()
        variable.name = "over_100K"
        variable.probability = 0.18
        
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "employment"
        variable = discreteDistribution.variables.add()
        variable.name = "employment_not_working"
        variable.probability = 0.42
        variable = discreteDistribution.variables.add()
        variable.name = "employment_unemployed"
        variable.probability = 0.04
        variable = discreteDistribution.variables.add()
        variable.name = "employment_associated"
        variable.probability = 0.02
        variable = discreteDistribution.variables.add()
        variable.name = "employment_working"
        variable.probability = 0.51


        

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "age_at_first_child"
        variable = discreteDistribution.variables.add()
        variable.name = "age_at_first_child_19_and_below"
        variable.probability = 0.35
        variable = discreteDistribution.variables.add()
        variable.name = "age_at_first_child_20_through_24"
        variable.probability = 0.37
        variable = discreteDistribution.variables.add()
        variable.name = "age_at_first_child_25_through_29"
        variable.probability = 0.20
        variable = discreteDistribution.variables.add()
        variable.name = "age_at_first_child_30_through_33"
        variable.probability = 0.06
        variable = discreteDistribution.variables.add()
        variable.name = "age_at_first_child_34_or_older"
        variable.probability = 0.04


#inflammation

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "c_reactive_protein"
        variable = discreteDistribution.variables.add()
        variable.name = "c_reactive_protein_high_above_2"
        variable.probability = 0.45
        variable = discreteDistribution.variables.add()
        variable.name = "c_reactive_protein_low_2_and_below"
        variable.probability = 0.55


#Gum disease causes inflammation


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "last_dentist_visit"
        variable = discreteDistribution.variables.add()
        variable.name = "last_dentist_visit_never"
        variable.probability = 0.02
        variable = discreteDistribution.variables.add()
        variable.name = "last_dentist_visit_2_or_more_years"
        variable.probability = 0.27
        variable = discreteDistribution.variables.add()
        variable.name = "last_dentist_visit_more_than_1_year_less_than_2_years"
        variable.probability = 0.13
        variable = discreteDistribution.variables.add()
        variable.name = "last_dentist_visit_7_months_to_a_year"
        variable.probability = 0.15
        variable = discreteDistribution.variables.add()
        variable.name = "last_dentist_visit_6_months_or_less"
        variable.probability = 0.41
        


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "mouth_pain_last_year"
        variable = discreteDistribution.variables.add()
        variable.name = "mouth_pain_last_year_very_often"
        variable.probability = 0.04
        variable = discreteDistribution.variables.add()
        variable.name = "mouth_pain_last_year_fairly_often"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "mouth_pain_last_year_occasionally_or_hardly_ever"
        variable.probability = 0.48
        variable = discreteDistribution.variables.add()
        variable.name = "mouth_pain_last_year_never"
        variable.probability = 0.44

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "gum_disease"
        variable = discreteDistribution.variables.add()
        variable.name = "gum_disease_yes"
        variable.probability = 0.19
        variable = discreteDistribution.variables.add()
        variable.name = "gum_disease_no"
        variable.probability = 0.80


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "teeth_health"
        variable = discreteDistribution.variables.add()
        variable.name = "teeth_health_poor"
        variable.probability = 0.09
        variable = discreteDistribution.variables.add()
        variable.name = "teeth_health_fair"
        variable.probability = 0.21
        variable = discreteDistribution.variables.add()
        variable.name = "teeth_health_good"
        variable.probability = 0.57
        variable = discreteDistribution.variables.add()
        variable.name = "teeth_health_excellent"
        variable.probability = 0.13

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "times_brush_teeth_daily"
        variable = discreteDistribution.variables.add()
        variable.name = "times_brush_teeth_daily_none"
        variable.probability = 0.00
        variable = discreteDistribution.variables.add()
        variable.name = "times_brush_teeth_daily_1"
        variable.probability = 0.31
        variable = discreteDistribution.variables.add()
        variable.name = "times_brush_teeth_daily_2"
        variable.probability = 0.61
        variable = discreteDistribution.variables.add()
        variable.name = "times_brush_teeth_daily_3_or_more"
        variable.probability = 0.08

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dental_bone_loss"
        variable = discreteDistribution.variables.add()
        variable.name = "dental_bone_loss_yes"
        variable.probability = 0.17
        variable = discreteDistribution.variables.add()
        variable.name = "dental_bone_loss_no"
        variable.probability = 0.82

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "floss_days_per_week"
        variable = discreteDistribution.variables.add()
        variable.name = "none"
        variable.probability = 0.34
        variable = discreteDistribution.variables.add()
        variable.name = "1_to_3"
        variable.probability = 0.22
        variable = discreteDistribution.variables.add()
        variable.name = "4_to_6"
        variable.probability = 0.09
        variable = discreteDistribution.variables.add()
        variable.name = "7.0"
        variable.probability = 0.34

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "oral_cancer_exam"
        variable = discreteDistribution.variables.add()
        variable.name = "oral_cancer_exam_yes"
        variable.probability = 0.18
        variable = discreteDistribution.variables.add()
        variable.name = "oral_cancer_exam_no"
        variable.probability = 0.82



        
        
#chronic conditions        
        
                
#psychological_disorders 9%

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "psychological_disorders"
        variable = discreteDistribution.variables.add()
        variable.name = "psychological_disorders"
        variable.probability = 0.09
        variable = discreteDistribution.variables.add()
        variable.name = "no_psychological_disorders"
        variable.probability = 0.91
        

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
 #anomalies
                       
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "heart_rate_anomaly"
        variable = discreteDistribution.variables.add()
        variable.name = "heart_rate_anomaly"
        variable.probability = 0.03
        variable = discreteDistribution.variables.add()
        variable.name = "no_heart_rate_anomaly"
        variable.probability = 0.97


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "steps_anomaly"
        variable = discreteDistribution.variables.add()
        variable.name = "steps_anomaly"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "no_steps_anomaly"
        variable.probability = 0.95
        
       # conditional probability tables

        cpt ={} 
 
        #discreteDistribution = bayesianNetwork.discreteDistributions.add()
        #discreteDistribution.name = "heart_rate_variability_anomaly"
        #variable = discreteDistribution.variables.add()
        #variable.name = "heart_rate_variability_anomaly"
        #variable.probability = 0.05
        #variable = discreteDistribution.variables.add()
        #variable.name = "no_heart_rate_variability_anomaly"
        #variable.probability = 0.95
        
        
        #discreteDistribution = bayesianNetwork.discreteDistributions.add()
        #discreteDistribution.name = "oxygen_anomaly"
        #variable = discreteDistribution.variables.add()
        #variable.name = "oxygen_anomaly"
        #variable.probability = 0.02
        #variable = discreteDistribution.variables.add()
        #variable.name = "no_oxygen_anomaly"
        #variable.probability = 0.98


        cpt["heart_rate_variability_anomaly"] = dependency(bayesianNetwork,cpt,
        [
            ({"heart_rate_anomaly":["heart_rate_anomaly"]},{"sensitivity":0.8})
        ],
        {"heart_rate_variability_anomaly":0.05,"no_heart_rate_variability_anomaly":0.95}
        )


        cpt["oxygen_anomaly"] = dependency(bayesianNetwork,cpt,
        [
            ({"heart_rate_anomaly":["heart_rate_anomaly"]},{"sensitivity":0.2})
        ],
        {"oxygen_anomaly":0.02,"no_oxygen_anomaly":0.98}
        )


        cpt["hypertension"] = dependency(bayesianNetwork,cpt,
        [
            ({"age":["elderly"]},{"relative_risk":3.5}),
            ({"age":["adult"]},{"relative_risk":2}),
            ({"bmi":["bmi_35_to_39_moderate_risk","bmi_30_to_34_low_risk","bmi_over_40_high_risk"]},{"relative_risk":2.17}),
            ({"bmi":["bmi_25_to_29_overweight"]},{"relative_risk":1.52}),
            ({"psychological_disorders":["psychological_disorders"]},{"relative_risk":1.1})
        ],
        {"hypertension":0.17,"no_hypertension":0.83}
        )
        
        outstr = outstr + addCpt(bayesianNetwork,cpt)
        cpt={}

        cpt["kidney_disease"] = dependency(bayesianNetwork,cpt,
        [
            ({"bmi":["bmi_over_40_high_risk","bmi_35_to_39_moderate_risk","bmi_30_to_34_low_risk"]},{"relative_risk":2.14}),
            ({"bmi":["bmi_25_to_29_overweight"]},{"relative_risk":1.21}),
            ({"hypertension":["hypertension"]},{"relative_risk":2})
        ],
        {"kidney_disease":0.14,"no_kidney_disease":0.86}
        )
        


        cpt["diabetes"] = dependency(bayesianNetwork,cpt,
        [
            ({"age":["elderly"]},{"relative_risk":4.5}),
            ({"bmi":["bmi_over_40_high_risk"]},{"relative_risk":5.1}),
            ({"bmi":["bmi_35_to_39_moderate_risk"]},{"relative_risk":3.6}),
            ({"bmi":["bmi_30_to_34_low_risk"]},{"relative_risk":2.5}),
            ({"bmi":["bmi_25_to_29_overweight"]},{"relative_risk":1.5}),
            ({"hypertension":["hypertension"]},{"relative_risk":3.8}),
            ({"psychological_disorders":["psychological_disorders"]},{"relative_risk":1.7})
        ],
        {"diabetes":0.12,"no_diabetes":0.88}
        )
        outstr = outstr + addCpt(bayesianNetwork,cpt) 
        cpt = {}
                
        cpt["cardiovascular_disease"] = dependency(bayesianNetwork,cpt,
        [
            ({"age":["elderly"]},{"relative_risk":7}),
            ({"diabetes":["diabetes"]},{"relative_risk":3}),
            ({"bmi":["bmi_35_to_39_moderate_risk","bmi_30_to_34_low_risk","bmi_over_40_high_risk"]},{"relative_risk":2}),
            ({"bmi":["bmi_25_to_29_overweight"]},{"relative_risk":1.12}),
            ({"hypertension":["hypertension"]},{"relative_risk":3.15}),
        ],
        {"cardiovascular_disease":0.09,"no_cardiovascular_disease":0.91}
        )
        
                
          
        
        cpt["low_socioeconomic_status_demography"] = avg(bayesianNetwork,cpt,
                [
                        "race",
                        "education_level",
                        "what_is_your_annual_household_income",
                        "employment"
                ],
                ["low_socioeconomic_status_demography","no_low_socioeconomic_status_demography"]

                )
                        

        cpt["low_socioeconomic_status_health_insurance"] = avg(bayesianNetwork,cpt,
                [
                        "have_health_insurance",
                        "prescription_health_insurance"
                ],
                ["low_socioeconomic_status_health_insurance","no_low_socioeconomic_status_health_insurance"]

                )
                        

        cpt["low_socioeconomic_status_healthcare"] = avg(bayesianNetwork,cpt,
                [
                        "how_many_times_saw_doctor_last_year",
                        "how_long_since_saw_doctor",
                        "age_at_first_child"
                ],
                ["low_socioeconomic_status_healthcare","no_low_socioeconomic_status_healthcare"]

                )
                        

        cpt["low_socioeconomic_status_health"] = avg(bayesianNetwork,cpt,
                [
                        "low_socioeconomic_status_health_insurance",
                        "low_socioeconomic_status_healthcare"
                ],
                ["low_socioeconomic_status_health","no_low_socioeconomic_status_health"]

                )
                        

        cpt["low_socioeconomic_status"] = any_of(bayesianNetwork,cpt,
                {
                "low_socioeconomic_status_health":{"low_socioeconomic_status_health"},
                "low_socioeconomic_status_demography":{"low_socioeconomic_status_demography"}
                },
                ["low_socioeconomic_status","no_low_socioeconomic_status"]

                )
                        

           
        cpt["poor_diet_minerals_1"] = any_of(bayesianNetwork,cpt,
                {
         "dietary_iron":{"dietary_iron_above_29.59"},
         "dietary_magnesium":{ "dietary_magnesium_101.00_and_below"},
         "dietary_potassium":{"dietary_potassium_850.00_and_below"}
         },
         ["poor_diet_minerals_1","no_poor_diet_minerals_1"]
         )
         
        cpt["poor_diet_minerals_2"] = any_of(bayesianNetwork,cpt,
                {
         "dietary_zinc":{"dietary_zinc_2.98_and_below"},
         "dietary_copper":{"dietary_copper_above_2.31"}
         },
         ["poor_diet_minerals_2","no_poor_diet_minerals_2"]
         )
         
        cpt["poor_diet_minerals"] = any_of(bayesianNetwork,cpt,
                {
         "poor_diet_minerals_1":{"poor_diet_minerals_1"},
         "poor_diet_minerals_2":{"poor_diet_minerals_2"}
         },
         ["poor_diet_minerals","no_poor_diet_minerals"]
         )
         
        cpt["poor_diet_vitamin_a"] = any_of(bayesianNetwork,cpt,
                {
         "dietary_retinol":{"dietary_retinol_21.00_and_below"},
         "dietary_alpha_carotene":{"dietary_alpha_carotene_0.00_and_below"},
         "dietary_beta_carotene":{"dietary_beta_carotene_46.00_and_below"}
         },
         ["poor_diet_vitamin_a","no_poor_diet_vitamin_a"]
         )
           
        cpt["poor_diet_vitamin_b_1"] = any_of(bayesianNetwork,cpt,
                {
         "dietary_b6":{"dietary_b6_0.47_and_below"},
         "dietary_folate":{"dietary_folate_119.00_and_below"}
         },
         ["poor_diet_vitamin_b_1","no_poor_diet_vitamin_b_1"]
         )

        cpt["poor_diet_vitamin_b_2"] = any_of(bayesianNetwork,cpt,
                {
         "dietary_thiamin":{"dietary_thiamin_0.48_and_below"},
         "dietary_riboflavin":{"dietary_riboflavin_0.56_and_below"},
         "dietary_b12":{"dietary_b12_0.50_and_below"}
         },
         ["poor_diet_vitamin_b_2","no_poor_diet_vitamin_b_2"]
         )

        cpt["poor_diet_vitamin_b"] = any_of(bayesianNetwork,cpt,
                {
         "poor_diet_vitamin_b_1":{"poor_diet_vitamin_b_1"},
         "poor_diet_vitamin_b_2":{"poor_diet_vitamin_b_2"}
         },
         ["poor_diet_vitamin_b","no_poor_diet_vitamin_b"]
         )
         
        cpt["poor_diet_vitamin_other"] = any_of(bayesianNetwork,cpt,
                {
         "dietary_vitamin_C":{"dietary_vitamin_C_2.70_and_below"},
         "dietary_alpha_tocopherol":{"dietary_alpha_tocopherol_1.98_and_below"},
         "dietary_calcium":{"dietary_calcium_226.00_and_below"}
         },
         ["poor_diet_vitamin_other","no_poor_diet_vitamin_other"]
         )
         
         
        cpt["poor_diet_vitamins_and_minerals"] = any_of(bayesianNetwork,cpt,
                {
         "poor_diet_minerals":{"poor_diet_minerals"},
         "poor_diet_vitamin_a":{"poor_diet_vitamin_a"},
         "poor_diet_vitamin_b":{"poor_diet_vitamin_b"},
         "poor_diet_vitamin_other":{"poor_diet_vitamin_other"}
         },
         ["poor_diet_vitamins_and_minerals","no_poor_diet_vitamins_and_minerals"]
         )
         
        cpt["poor_diet_fats"] = any_of(bayesianNetwork,cpt,
                {
         "dietary_epa":{"dietary_epa_0.00_and_below"},
         "dietary_pfa":{"dietary_pfa_3.79_and_below"},
         "dietary_fat":{"dietary_fat_above_160.14"},
         "dietary_cholesterol":{"dietary_cholesterol_39.00_and_below"}
         },
         ["poor_diet_fats","no_poor_diet_fats"]
         )
         
        cpt["poor_diet_basics"] = any_of(bayesianNetwork,cpt,
                {
         "water_drank_yesterday":{"water_drank_yesterday_0.00_and_below"},
         "dietary_fiber":{"dietary_fiber_3.80_and_below"},
         "dietary_carbohydrate":{"dietary_carbohydrate_above_477.91"},
         "dietary_energy":{"dietary_energy_above_3939.00"}
         },
         ["poor_diet_basics","no_poor_diet_basics"]
         )
         
        cpt["poor_diet_supplements"] = any_of(bayesianNetwork,cpt,
                {
         "dietary_lycopene":{"dietary_lycopene_0.00_and_below"},
         "dietary_lutein":{"dietary_lutein_72.00_and_below"},
         "dietary_selenium":{"dietary_selenium_32.20_and_below"},
         "dietary_choline":{"dietary_choline_85.70_and_below"}
         },
         ["poor_diet_supplements","no_poor_diet_supplements"]
         )
         
                        
        cpt["poor_diet_substances"] = any_of(bayesianNetwork,cpt,
                {
         "dietary_caffeine":{"dietary_caffeine_0.00_and_below"},
         "dietary_sodium":{"dietary_sodium_above_6872.00"},
         "alcohol_consumption_last_year":{"alcohol_daily"},
         "num_alcoholic_drinks_when_drinking":{"num_alcohol_8_or_more"}
         },
         ["poor_diet_substances","no_poor_diet_substances"]
         )
         
           
        cpt["poor_diet_quantity"] = any_of(bayesianNetwork,cpt,
                {
         "poor_diet_substances":{"poor_diet_substances"},
         "poor_diet_supplements":{"poor_diet_supplements"},
         "poor_diet_basics":{"poor_diet_basics"}
         },
         ["poor_diet_quantity","no_poor_diet_quantity"]
         )

        cpt["poor_diet_food"] = any_of(bayesianNetwork,cpt,
                {
         "poor_diet_fats":{"poor_diet_fats"},
         "poor_diet_vitamins_and_minerals":{"poor_diet_vitamins_and_minerals"}
         },
         ["poor_diet_food","no_poor_diet_food"]
         )

                        
        cpt["poor_diet_flag"] = any_of(bayesianNetwork,cpt,
                {
         "poor_diet_quantity":{"poor_diet_quantity"},
         "poor_diet_food":{"poor_diet_food"}
         },
         ["poor_diet_flag","no_poor_diet_flag"]
         )
         
           
         
        cpt["diet_minerals_1"] = avg(bayesianNetwork,cpt,
         [
         "dietary_iron",
         "dietary_magnesium",
         "dietary_potassium"
         ],
         ["deficient_diet_minerals_1","below_average_diet_minerals_1","average_diet_minerals_1","above_average_diet_minerals_1","excellent_diet_minerals_1"]
         )
         

         
        cpt["diet_minerals_2"] = avg(bayesianNetwork,cpt,
         [
         "dietary_zinc",
         "dietary_copper"
         ],
         ["deficient_diet_minerals_2","below_average_diet_minerals_2","average_diet_minerals_2","above_average_diet_minerals_2","excellent_diet_minerals_2"]
         )
         

         
        cpt["diet_minerals"] = avg(bayesianNetwork,cpt,
         [
         "diet_minerals_1",
         "diet_minerals_2"
         ],
         ["deficient_diet_minerals","below_average_diet_minerals","average_diet_minerals","above_average_diet_minerals","excellent_diet_minerals"]
         )
         
        cpt["diet_vitamin_a"] = avg(bayesianNetwork,cpt,
         [
         "dietary_retinol",
         "dietary_alpha_carotene",
         "dietary_beta_carotene"
         ],
         ["deficient_diet_vitamin_a","below_average_diet_vitamin_a","average_diet_vitamin_a","above_average_diet_vitamin_a","excellent_diet_vitamin_a"]
         )
           
        cpt["diet_vitamin_b_1"] = avg(bayesianNetwork,cpt,
         [
         "dietary_b6",
         "dietary_folate"
         ],
         ["deficient_diet_vitamin_b_1","below_average_diet_vitamin_b_1","average_diet_vitamin_b_1","above_average_diet_vitamin_b_1","excellent_diet_vitamin_b1"]
         )
         

        cpt["diet_vitamin_b_2"] = avg(bayesianNetwork,cpt,
         [
         "dietary_thiamin",
         "dietary_riboflavin",
         "dietary_b12"
         ],
         ["deficient_diet_vitamin_b_2","below_average_diet_vitamin_b_2","average_diet_vitamin_b_2","above_average_diet_vitamin_b_2","excellent_diet_vitamin_b_2"]
         )
         

        cpt["diet_vitamin_b"] = avg(bayesianNetwork,cpt,
         [
         "diet_vitamin_b_1",
         "diet_vitamin_b_2"
         ],
         ["deficient_diet_vitamin_b","below_average_diet_vitamin_b","average_diet_vitamin_b","above_average_diet_vitamin_b","excellent_diet_vitamin_b"]
         )
         
        cpt["diet_vitamin_other"] = avg(bayesianNetwork,cpt,
                [
         "dietary_vitamin_C",
         "dietary_alpha_tocopherol",
         "dietary_calcium"
         ],
         ["deficient_diet_vitamin_other","below_average_diet_vitamin_other","average_diet_vitamin_other","above_average_diet_vitamin_other","excellent_diet_vitamin_other"]
         )
         
         
        cpt["diet_vitamins_and_minerals"] = avg(bayesianNetwork,cpt,
          [
         "diet_minerals",
         "diet_vitamin_a",
         "diet_vitamin_b",
         "diet_vitamin_other"
         ],
         ["deficient_diet_vitamins_and_minerals","below_average_diet_vitamins_and_minerals","average_diet_vitamins_and_minerals","above_average_diet_vitamins_and_minerals","excellent_diet_vitamins_and_minerals"]
         )
         
        cpt["diet_fats"] = avg(bayesianNetwork,cpt,
          [
         "dietary_epa",
         "dietary_pfa",
         "dietary_fat",
         "dietary_cholesterol"
         ],
         ["deficient_diet_fats","below_average_diet_fats","avg_diet_fats","above_average_diet_fats","excellent_diet_fats"]
         )
         
        cpt["diet_basics"] = avg(bayesianNetwork,cpt,
          [
         "water_drank_yesterday",
         "dietary_fiber",
         "dietary_carbohydrate",
         "dietary_energy"
         ],
         ["deficient_diet_basics","below_average_diet_basics","avg_diet_basics","above_average_diet_basics","excellent_diet_basics"]
         )
         
        cpt["diet_supplements"] = avg(bayesianNetwork,cpt,
          [
         "dietary_lycopene",
         "dietary_lutein",
         "dietary_selenium",
         "dietary_choline"
         ],
         ["deficient_diet_supplements","below_average_diet_supplements","avg_diet_supplements","above_average_diet_supplements","excellent_diet_supplements"]
         )
                        
        cpt["diet_substances"] = avg(bayesianNetwork,cpt,
          [
         "dietary_caffeine",
         "dietary_sodium",
         "alcohol_consumption_last_year",
         "num_alcoholic_drinks_when_drinking"
         ],
         ["deficient_diet_substances","below_average_diet_substances","avg_diet_substances","above_average_diet_substances","excellent_diet_substances"]
         )
                        
           
        cpt["diet_quality_food"] = avg(bayesianNetwork,cpt,
          [
         "diet_fats",
         "diet_vitamins_and_minerals"
         ],
         ["deficient_diet_quality_food","below_average_diet_quality_food","avg_diet_quality_food","above_average_diet_quality_food","excellent_diet_quality_food"]
         )

        cpt["diet_quantity"] = avg(bayesianNetwork,cpt,
          [
         "diet_substances",
         "diet_supplements",
         "diet_basics"
         ],
         ["deficient_diet_quantity","below_average_diet_quantity","avg_diet_quantity","above_average_diet_quantity","excellent_diet_quantity"]
         )

                        
        cpt["diet_quality"] = avg(bayesianNetwork,cpt,
          [
         "diet_quantity",
         "diet_quality_food"
         ],
         ["deficient_diet_quality","below_average_diet_quality","avg_diet_quality","above_average_diet_quality","excellent_diet_quality"]
         )
         
         
        outstr = outstr + addCpt(bayesianNetwork,cpt) 
        cpt = {}
         
                        

        cpt["poor_diet"] = dependency(bayesianNetwork,cpt,
                        [
                            ({"low_socioeconomic_status":["low_socioeconomic_status"]},{"relative_risk":1.66}),
                            ({"diet_quality":["deficient_diet_quality"]},{"sensitivity":0.99}),
                            ({"diet_quality":["below_average_diet_quality"]},{"sensitivity":0.8}),
                            ({"poor_diet_flag":["poor_diet_flag"]},{"sensitivity":0.5})
                        ],
                        {"poor_diet":0.07,"no_poor_diet":0.93}
                        )
 
        cpt["smoking"] = any_of(bayesianNetwork,cpt,
                {
         "second_hand_smoke":{"second_hand_smoke_yes"},
         "five_days_smoke_cigarettes":{"five_days_smoke_cigarettes_yes"},
         "ever_vaped":{"ever_vaped_yes"}
         },
         ["smoking","no_smoking"]
         )
         
 
        outstr = outstr + addCpt(bayesianNetwork,cpt) 
        cpt = {}
         

        cpt["inactivated_sirtuins"] = dependency(bayesianNetwork,cpt,
                [
                    ({"dietary_energy":["dietary_energy_above_3939.00","dietary_energy_above_2612.00_to_3939.00_and_below",
                        "dietary_energy_above_1930.00_to_2612.00_and_below","dietary_energy_above_1399.00_to_1930.00_and_below"]},{"sensitivity":0.9}),
                    ({"diet_quality": ["deficient_diet_quality","below_average_diet_quality","avg_diet_quality","above_average_diet_quality"]},{"sensitivity":0.85})
                    ],
                {"inactivated_sirtuins":0.8,"no_inactivated_sirtuins":0.2}
                )

        


        cpt["hallmark_1_genomic_instability"] = dependency(bayesianNetwork,cpt,
                [
                    ({"age":["elderly"]},{"sensitivity":0.4}),
                    ({"age":["adult"]},{"sensitivity":0.2}),
                    ({"poor_diet":["poor_diet"]},{"sensitivity":0.3}),
                    ({"smoking":["smoking"]},{"sensitivity":0.3})
                ],
                {"hallmark_1_genomic_instability":0.1, "no_halmark_1_genomic_instability":0.9}
                )
  
        outstr = outstr + addCpt(bayesianNetwork,cpt) 
        cpt = {}
                 
      
        cpt["cancer"] = dependency(bayesianNetwork,cpt,
        [
            ({"age":["elderly"]},{"relative_risk":5.8}),
            ({"hallmark_1_genomic_instability":["hallmark_1_genomic_instability"]},{"sensitivity":0.3})
        ],
        {"cancer":0.055,"no_cancer":0.945}
        )


        cpt["metabolic_disease"] = avg(bayesianNetwork,cpt,
        [
        "cardiovascular_disease",
        "diabetes",
        "hypertension"
        ],
        ["metabolic_disease","no_metabolic_disease"]

        )
        
        cpt["cancer_related"] = avg(bayesianNetwork,cpt,
        [
        "cancer",
        "immunocompromised",
        ],
        ["cancer_related","no_cancer_related"]

        )


        cpt["lung_or_kidney_disease"] = any_of(bayesianNetwork,cpt,
        {
        "lung_disease":{"lung_disease"},
        "kidney_disease":{"kidney_disease"},
        },
        ["lung_or_kidney_disease","no_lung_or_kidney_disease"]

        )


        cpt["chronic_conditions"] = any_of(bayesianNetwork,cpt,
        {
        "lung_or_kidney_disease":{"lung_or_kidney_disease"},
        "cancer_related":{"cancer_related"},
        "psychological_disorders":{"psychological_disorders"}
        },
        ["chronic_conditions","no_chronic_conditions"]

        )


        cpt["comorbidities"] = avg(bayesianNetwork,cpt,
        [
        "chronic_conditions",
        "metabolic_disease",
        "bmi"
        ],
        ["comorbidities","no_comorbidities"]

        )
        
        cpt["frailty"] = dependency(bayesianNetwork,cpt,
                [
                    ({"age":["elderly"]},{"sensitivity":0.5}),
                    ({"inactivated_sirtuins":["inactivated_sirtuins"]},{"sensitivity":0.3}),
                    ({"hallmark_1_genomic_instability":["hallmark_1_genomic_instability"]},{"sensitivity":0.4})
                    ],
                {"frailty":0.15, "no_frailty":0.85}
                )


        # cpt["poor_diet"] = relative_risk(bayesianNetwork,cpt,
        #                [
        #                ({"low_socioeconomic_status":["low_socioeconomic_status"]},1.66)
        #                ],
        #                {"poor_diet":0.07,"no_poor_diet":0.93}
        #                )


         #cpt["poor_diet"] = relative_risk(bayesianNetwork,cpt,
                #        [
                #        ({"diet_quality":["deficient_diet_quality"]},10)
                #        ],
                #        {"poor_diet":0.07,"no_poor_diet":0.93}
                #        )


         #cpt["poor_diet"] = relative_risk(bayesianNetwork,cpt,
                #        [
                #        ({"diet_quality":["below_average_diet_quality"]},5)
                #        ],
                #        {"poor_diet":0.07,"no_poor_diet":0.93}
                #        )


         #cpt["poor_diet"] = relative_risk(bayesianNetwork,cpt,
                #        [
                #        ({"poor_diet_flag":["poor_diet_flag"]},2)
                #        ],
                #        {"poor_diet":0.07,"no_poor_diet":0.93}
                #        )

        outstr = outstr + non_cpt_descriptions(bayesianNetwork)
        outstr = outstr + addCpt(bayesianNetwork,cpt) 
        return(bayesianNetwork,outstr)

if __name__ == '__main__':
        covid_bayes()
