import sn_bayes
from sn_bayes.utils import any_of
from sn_bayes.utils import all_of
from sn_bayes.utils import avg
from sn_bayes.utils import if_then_else
from sn_bayes.utils import bayesInitialize
from sn_bayes.utils import addCpt
from sn_bayes.utils import relative_risk
from sn_bayes.utils import non_cpt_descriptions

import sn_service.service_spec.bayesian_pb2
from sn_service.service_spec.bayesian_pb2 import BayesianNetwork


def longevity_bayes_short():
        bayesianNetwork = BayesianNetwork()



        outstr = '' 
        
        cpt={}
        
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "gender"
        variable = discreteDistribution.variables.add()
        variable.name = "male"
        variable.probability = 0.49
        variable = discreteDistribution.variables.add()
        variable.name = "female"
        variable.probability = 0.51
        
        
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



                
        #probabilities within distributions must sum to 1.0
    #questions left blank or "prefer not to answer" will be computed
	
	
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
        discreteDistribution.name = "shortness_of_breath_exertion"
        variable = discreteDistribution.variables.add()
        variable.name = "shortness_of_breath_exertion_yes"
        variable.probability = 0.38
        variable = discreteDistribution.variables.add()
        variable.name = "shortness_of_breath_exertion_no"
        variable.probability = 0.62


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
        discreteDistribution.name = "hearing_frustration_how_often"
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
        discreteDistribution.name = "work_limiting_problem"
        variable = discreteDistribution.variables.add()
        variable.name = "work_limiting_problem_yes"
        variable.probability = 0.26
        variable = discreteDistribution.variables.add()
        variable.name = "work_limiting_problem_no"
        variable.probability = 0.74
		
		
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
        
		
		

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "chest_pain"
        variable = discreteDistribution.variables.add()
        variable.name = "chest_pain_yes"
        variable.probability = 0.30
        variable = discreteDistribution.variables.add()
        variable.name = "chest_pain_no"
        variable.probability = 0.70
		
		

        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "blood_relative_heart_attack_before_age_50"
        variable = discreteDistribution.variables.add()
        variable.name = "blood_relative_heart_attack_before_50_yes"
        variable.probability = 0.13
        variable = discreteDistribution.variables.add()
        variable.name = "blood_relative_heart_attack_before_50_no"
        variable.probability = 0.87


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "liver_condition"
        variable = discreteDistribution.variables.add()
        variable.name = "liver_condition_yes"
        variable.probability = 0.05
        variable = discreteDistribution.variables.add()
        variable.name = "liver_condition_no"
        variable.probability = 0.95
        
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "osteoporosis"
        variable = discreteDistribution.variables.add()
        variable.name = "osteoporosis_yes"
        variable.probability = 0.13
        variable = discreteDistribution.variables.add()
        variable.name = "osteoporosis_no"
        variable.probability = 0.87
		
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "asthma_attack_last_year"
        variable = discreteDistribution.variables.add()
        variable.name = "asthma_attack_last_year_yes"
        variable.probability = 0.41
        variable = discreteDistribution.variables.add()
        variable.name = "asthma_attack_last_year_no"
        variable.probability = 0.58


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "artificial_joints"
        variable = discreteDistribution.variables.add()
        variable.name = "artificial_joints_yes"
        variable.probability = 0.30
        variable = discreteDistribution.variables.add()
        variable.name = "artificial_joints_no"
        variable.probability = 0.70



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
        discreteDistribution.name = "floss_days_per_week"
        variable = discreteDistribution.variables.add()
        variable.name = "floss_days_per_week_none"
        variable.probability = 0.34
        variable = discreteDistribution.variables.add()
        variable.name = "floss_days_per_week_1_to_3"
        variable.probability = 0.22
        variable = discreteDistribution.variables.add()
        variable.name = "floss_days_per_week_4_to_6"
        variable.probability = 0.09
        variable = discreteDistribution.variables.add()
        variable.name = "floss_days_per_week_7.0"
        variable.probability = 0.34


        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "dental_bone_loss"
        variable = discreteDistribution.variables.add()
        variable.name = "dental_bone_loss_yes"
        variable.probability = 0.17
        variable = discreteDistribution.variables.add()
        variable.name = "dental_bone_loss_no"
        variable.probability = 0.82
		
		
        discreteDistribution = bayesianNetwork.discreteDistributions.add()
        discreteDistribution.name = "gum_disease"
        variable = discreteDistribution.variables.add()
        variable.name = "gum_disease_yes"
        variable.probability = 0.19
        variable = discreteDistribution.variables.add()
        variable.name = "gum_disease_no"
        variable.probability = 0.80



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
        discreteDistribution.name = "cancer"
        variable = discreteDistribution.variables.add()
        variable.name = "cancer"
        variable.probability = 0.055
        variable = discreteDistribution.variables.add()
        variable.name = "no_cancer"
        variable.probability = 0.945
        
        
	
        cpt["obesity"] = avg(bayesianNetwork,cpt,
        [
        "bmi",
        "greatest_weight",
		"weight_at_25"
        ],
        ["obesity","no_obesity"]

        )
		
		
        cpt["hypertension"] = avg(bayesianNetwork,cpt,
        [
        "high_blood_pressure_patient_prescription",
		"high_blood_pressure_medication_compliance"
        ],
        ["hypertension","no_hypertension"]

        )
		
		
		
        cpt["poor_oral_health"] = any_of(bayesianNetwork,cpt,
        {
        "teeth_health":{"teeth_health_poor"},
        "gum_disease":{"gum_disease_yes"},
        "floss_days_per_week":{"floss_days_per_week_none"},
        "times_brush_teeth_daily":{"times_brush_teeth_daily_none"},
        "mouth_pain_last_year":{"mouth_pain_last_year_very_often"}
        },
        ["poor_oral_health","no_poor_oral_health"]

        )

		
		
        cpt["inflammation"] = avg(bayesianNetwork,cpt,
        [
        "cancer",
		"asthma_attack_last_year",
		"poor_oral_health",
		"hypertension",
		"obesity"
        ],
        ["inflammation","no_inflammation"]

        )

		
		
		
        cpt["cardiovascular_dysfunction"] = avg(bayesianNetwork,cpt,
        [
        "daily_asprin_prescription",
		"daily_aspirin_compliance",
		"shortness_of_breath_exertion",
		"chest_pain",
		"blood_relative_heart_attack_before_age_50"
        ],
        ["cardiovascular_dysfunction","no_cardiovascular_dysfunction"]

        )

        cpt["general_aging_signs"] = any_of(bayesianNetwork,cpt,
        {
        "urine_leakage_bother":{"urine_leakage_bother_greatly","urine_leakage_bother_very_much"},
        "osteoporosis":{"osteoporosis_yes"},
        "artificial_joints":{"artificial_joints_yes"},
        "dental_bone_loss":{"dental_bone_loss_yes"}
        },
        ["general_aging_signs","no_general_aging_signs"]

        )

		
        
		
        cpt["hearing_difficulty"] = avg(bayesianNetwork,cpt,
        [
        "hearing_difficulty_how_often",
		"hearing_frustration_how_often",
		"wear_hearing_aid",
		"loud_noise_job",
		"loud_music"
        ],
        ["hearing_difficulty","no_hearing_difficulty"]

        )
		
		
        cpt["sarcopenia_movement"] = avg(bayesianNetwork,cpt,
        [
        "walking_difficulty",
		"two_hour_standing_difficulty",
		"stand_from_sit_difficulty",
		"ten_stairs_difficulty",
		"two_hour_sitting_difficulty"
        ],
        ["sarcopenia_movement","no_sarcopenia_movement"]

        )
		
        cpt["sarcopenia_function"] = avg(bayesianNetwork,cpt,
        [
        "chore_difficulty",
		"social_activity_difficulty",
		"work_limiting_problem",
		"birth_weight"
		
        ],
        ["sarcopenia_function","no_sarcopenia_function"]

        )


        cpt["sarcopenia"] = any_of(bayesianNetwork,cpt,
        {
        "sarcopenia_movement":{"sarcopenia_movement"},
        "sarcopenia_function":{"sarcopenia_function"}
        },
        ["sarcopenia","no_sarcopenia"]

        )


		
		
		
		
        cpt["frailty"] = avg(bayesianNetwork,cpt,
        [
		"general_aging_signs",
		"hearing_difficulty",
		"sarcopenia"
        ],
        ["frailty","no_frailty"]

        )
		
		
		
        cpt["hallmark_1_genomic_instability"] = avg(bayesianNetwork,cpt,
        [
		"frailty",
		"cancer"
        ],
        ["hallmark_1_genomic_instability","no_hallmark_1_genomic_instability"]

        )
		
		
        #cpt["hallmark_1_genomic_instability"] = any_of(bayesianNetwork,cpt,
        #{
        #"frailty":{"frailty"},
        #"cancer":{"cancer"}
        #},
        #["hallmark_1_genomic_instability","no_hallmark_1_genomic_instability"]

        #)

		
		
        cpt["hallmark_2_telomere_attrition"] = avg(bayesianNetwork,cpt,
        [
		"frailty",
		"gender"
        ],
        ["hallmark_2_telomere_attrition","no_hallmark_2_telomere_attrition"]

        )
		
        #cpt["hallmark_2_telomere_attrition"] = any_of(bayesianNetwork,cpt,
        #{
        #"frailty":{"frailty"},
        #"gender":{"male_gender"}
        #},
        #["hallmark_2_telomere_attrition","no_hallmark_2_telomere_attrition"]

        #)

		
        cpt["hallmark_3_epigenetic_alterations"] = any_of(bayesianNetwork,cpt,
        {
        "liver_condition":{"liver_condition_yes"}
        },
        ["hallmark_3_epigenetic_alterations","no_hallmark_3_epigenetic_alterations"]

        )
		
		
		
        cpt["hallmark_4_loss_of_proteostasis"] = any_of(bayesianNetwork,cpt,
        {
        "cardiovascular_dysfunction":{"cardiovascular_dysfunction"}
        },
        ["hallmark_4_loss_of_proteostasis","no_hallmark_4_loss_of_proteostasis"]

        )
		
		
		
        cpt["hallmark_5_deregulated_nutrient_sensing"] = any_of(bayesianNetwork,cpt,
        {
        "frailty":{"frailty"}
        },
        ["hallmark_5_deregulated_nutrient_sensing","no_hallmark_5_deregulated_nutrient_sensing"]

        )
		
		
		
        cpt["hallmark_6_mitochondrial_dysfunction"] = any_of(bayesianNetwork,cpt,
        {
        "inflammation":{"inflammation"}
        },
        ["hallmark_6_mitochondrial_dysfunction","no_hallmark_6_mitochondrial_dysfunction"]

        )
		
		
		
        cpt["hallmark_7_cellular_senescence"] = any_of(bayesianNetwork,cpt,
        {
        "cancer":{"cancer"},
        "inflammation":{"inflammation"},
	"cardiovascular_dysfunction":{"cardiovascular_dysfunction"}
        },
        ["hallmark_7_cellular_senescence","no_hallmark_7_cellular_senescence"]

        )
		
		
		
        cpt["hallmark_8_stem_cell_exhaustion"] = avg(bayesianNetwork,cpt,
        [
		"frailty",
		"inflammation"
        ],
        ["hallmark_8_stem_cell_exhaustion","no_hallmark_8_stem_cell_exhaustion"]

        )
		
		
		
        cpt["hallmark_9_altered_intercellular_communication"] = avg(bayesianNetwork,cpt,
        [
		"cancer",
		"inflammation"
        ],
        ["hallmark_9_altered_intercellular_communication","no_hallmark_9_altered_intercellular_communication"]

        )
		
		
		
        cpt["hallmark_10_extracellular_matrix_dysfunction"] = avg(bayesianNetwork,cpt,
        [
		"cancer",
		"inflammation",
		"cardiovascular_dysfunction"
        ],
        ["hallmark_10_extracellular_matrix_dysfunction","no_hallmark_10_extracellular_matrix_dysfunction"]

        )
		
		

		
        
        
        outstr = outstr + non_cpt_descriptions(bayesianNetwork)
        outstr = outstr + addCpt(bayesianNetwork,cpt) 
        return(bayesianNetwork,outstr)

if __name__ == '__main__':
        covid_bayes()

