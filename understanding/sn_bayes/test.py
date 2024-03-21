import sn_bayes
from sn_bayes.utils import any
from sn_bayes.utils import all
from sn_bayes.utils import avg
from sn_bayes.utils import if_then_else
from sn_bayes.utils import bayesInitialize
from sn_bayes.utils import addCpt

import bayesian_pb2

bayesianNetwork = bayesian_pb2.BayesianNetwork()



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
discreteDistribution.name = "heterosome"
variable = discreteDistribution.variables.add()
variable.name = "other"
variable.probability = 0.0005
variable = discreteDistribution.variables.add()
variable.name = "X"
variable.probability = 0.0005
variable = discreteDistribution.variables.add()
variable.name = "XXY"
variable.probability = 0.0005
variable = discreteDistribution.variables.add()
variable.name = "XYY"
variable.probability = 0.0005
variable = discreteDistribution.variables.add()
variable.name = "XY"
variable.probability = 0.499
variable = discreteDistribution.variables.add()
variable.name = "XX"
variable.probability = 0.499


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


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "education"
variable = discreteDistribution.variables.add()
variable.name = "education_other"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "some_high_school"
variable.probability = 0.2
variable = discreteDistribution.variables.add()
variable.name = "high_school"
variable.probability = 0.2
variable = discreteDistribution.variables.add()
variable.name = "vocational"
variable.probability = 0.2
variable = discreteDistribution.variables.add()
variable.name = "bachelors"
variable.probability = 0.2
variable = discreteDistribution.variables.add()
variable.name = "masters"
variable.probability = 0.1
variable = discreteDistribution.variables.add()
variable.name = "phd"
variable.probability = 0.05


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "employment"
variable = discreteDistribution.variables.add()
variable.name = "unemployed"  #same as seeking opportunities
variable.probability = 0.1
variable = discreteDistribution.variables.add()
variable.name = "employment_other"  #added, covers children, those who dont want work
variable.probability = 0.3
variable = discreteDistribution.variables.add()
variable.name = "retired"
variable.probability = 0.1
variable = discreteDistribution.variables.add()
variable.name = "part_time"
variable.probability = 0.1
variable = discreteDistribution.variables.add()
variable.name = "full_time"
variable.probability = 0.4


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "marital_status"
variable = discreteDistribution.variables.add()
variable.name = "single"
variable.probability = 0.34
variable = discreteDistribution.variables.add()
variable.name = "relationship"
variable.probability = 0.33
variable = discreteDistribution.variables.add()
variable.name = "married"
variable.probability = 0.33


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "number_of_children"
variable = discreteDistribution.variables.add()
variable.name = "three_or_more"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "two_children"
variable.probability = 0.15
variable = discreteDistribution.variables.add()
variable.name = "one_children"
variable.probability = 0.20
variable = discreteDistribution.variables.add()
variable.name = "zero_children"
variable.probability = 0.70


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "income_in_USD"
variable = discreteDistribution.variables.add()
variable.name = "under_25k_USD"
variable.probability = 0.20
variable = discreteDistribution.variables.add()
variable.name = "26_to_50k_USD"
variable.probability = 0.30
variable = discreteDistribution.variables.add()
variable.name = "51_to_100k_USD"
variable.probability = 0.25
variable = discreteDistribution.variables.add()
variable.name = "101_to_200k_USD"
variable.probability = 0.25
variable = discreteDistribution.variables.add()
variable.name = "over_200k_USD"
variable.probability = 0.05


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "community"
variable = discreteDistribution.variables.add()
variable.name = "rural"
variable.probability = 0.20
variable = discreteDistribution.variables.add()
variable.name = "suburban"
variable.probability = 0.40
variable = discreteDistribution.variables.add()
variable.name = "urban"
variable.probability = 0.40


# basics/women questions 


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "pregnancy_in_months"
variable = discreteDistribution.variables.add()
variable.name = "over_six_months_pregnant"
variable.probability = 0.025
variable = discreteDistribution.variables.add()
variable.name = "three_to_six_months_pregnant"
variable.probability = 0.025
variable = discreteDistribution.variables.add()
variable.name = "under_three_months_pregnant"
variable.probability = 0.025
variable = discreteDistribution.variables.add()
variable.name = "not_pregnant"
variable.probability = 0.925


# basics/sleep questions


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "sleep_quickly"
variable = discreteDistribution.variables.add()
variable.name = "dont_sleep_quickly"
variable.probability = 0.35
variable = discreteDistribution.variables.add()
variable.name = "sleep_quickly"
variable.probability = 0.65


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "sleep_in_hours"
variable = discreteDistribution.variables.add()
variable.name = "under_five_hours_sleep"
variable.probability = 0.1
variable = discreteDistribution.variables.add()
variable.name = "five_or_six_hours_sleep"
variable.probability = 0.2
variable = discreteDistribution.variables.add()
variable.name = "seven_or_eight_hours_sleep"
variable.probability = 0.35
variable = discreteDistribution.variables.add()
variable.name = "nine_or_ten_hours_sleep"
variable.probability = 0.2
variable = discreteDistribution.variables.add()
variable.name = "eleven_to_thirteen_hours_sleep"
variable.probability = 0.1
variable = discreteDistribution.variables.add()
variable.name = "over_thirteen_hours_sleep"
variable.probability = 0.05
# basics/lifestyle questions

discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "sex_per_month"
variable = discreteDistribution.variables.add()
variable.name = "over_twelve_sex_per_month"
variable.probability = 0.1
variable = discreteDistribution.variables.add()
variable.name = "six_to_twelve_sex_per_month"
variable.probability = 0.2
variable = discreteDistribution.variables.add()
variable.name = "three_to_five_sex_per_month"
variable.probability = 0.35
variable = discreteDistribution.variables.add()
variable.name = "two_sex_per_month"
variable.probability = 0.2
variable = discreteDistribution.variables.add()
variable.name = "one_sex_per_month"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "no_sex_per_month"
variable.probability = 0.05


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "cigarettes_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_fifty_cigarettes_per_week"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "eleven_to_fifty_cigarettes_per_week"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "one_to_ten_cigarettes_per_week"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "no_cigarettes_per_week"
variable.probability = 0.85


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "cigars_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_fifty_cigars_per_week"
variable.probability = 0.01
variable = discreteDistribution.variables.add()
variable.name = "six_to_fifty_cigars_per_week"
variable.probability = 0.01
variable = discreteDistribution.variables.add()
variable.name = "one_to_five_cigars_per_week"
variable.probability = 0.01
variable = discreteDistribution.variables.add()
variable.name = "no_cigars_per_week"
variable.probability = 0.97


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "hookah_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_six_hookah_per_week"
variable.probability = 0.005
variable = discreteDistribution.variables.add()
variable.name = "one_to_five_hookah_per_week"
variable.probability = 0.055
variable = discreteDistribution.variables.add()
variable.name = "no_hookah_per_week"
variable.probability = 0.95


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "snuff_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_fifty_snuff_per_week"
variable.probability = 0.001
variable = discreteDistribution.variables.add()
variable.name = "six_to_fifty_snuff_per_week"
variable.probability = 0.002
variable = discreteDistribution.variables.add()
variable.name = "one_to_five_snuff_per_week"
variable.probability = 0.002
variable = discreteDistribution.variables.add()
variable.name = "no_snuff_per_week"
variable.probability = 0.995


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "vapes_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_fifty_vapes_per_week"
variable.probability = 0.01
variable = discreteDistribution.variables.add()
variable.name = "six_to_fifty_vapes_per_week"
variable.probability = 0.02
variable = discreteDistribution.variables.add()
variable.name = "one_to_five_vapes_per_week"
variable.probability = 0.02
variable = discreteDistribution.variables.add()
variable.name = "no_vapes_per_week"
variable.probability = 0.95


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "alchohol_glasses_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_twentyone_glasses_per_week"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "fifteen_to_twenty_glasses_per_week"
variable.probability = 0.1
variable = discreteDistribution.variables.add()
variable.name = "six_to_fourteen_glasses_per_week"
variable.probability = 0.2
variable = discreteDistribution.variables.add()
variable.name = "three_to_five_glasses_per_week"
variable.probability = 0.3
variable = discreteDistribution.variables.add()
variable.name = "zero_to_two_glasses_per_week"
variable.probability = 0.35

discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "adderall_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_fifteen_adderall_per_week"
variable.probability = 0.002
variable = discreteDistribution.variables.add()
variable.name = "one_to_fifteen_adderall_per_week"
variable.probability = 0.008
variable = discreteDistribution.variables.add()
variable.name = "zero_adderall_per_week"
variable.probability = 0.99


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "ritalin_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_fifteen_ritalin_per_week"
variable.probability = 0.002
variable = discreteDistribution.variables.add()
variable.name = "one_to_fifteen_ritalin_per_week"
variable.probability = 0.008
variable = discreteDistribution.variables.add()
variable.name = "zero_ritalin_per_week"
variable.probability = 0.99


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "cocaine_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_five_cocaine_per_week"
variable.probability = 0.002
variable = discreteDistribution.variables.add()
variable.name = "one_to_five_cocaine_per_week"
variable.probability = 0.008
variable = discreteDistribution.variables.add()
variable.name = "zero_cocaine_per_week"
variable.probability = 0.99


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "methamphetamine_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_five_methamphetamine_per_week"
variable.probability = 0.002
variable = discreteDistribution.variables.add()
variable.name = "one_to_five_methamphetamine_per_week"
variable.probability = 0.008
variable = discreteDistribution.variables.add()
variable.name = "zero_methamphetamine_per_week"
variable.probability = 0.99


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "ecstasy_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_five_ecstasy_per_week"
variable.probability = 0.002
variable = discreteDistribution.variables.add()
variable.name = "one_to_five_ecstasy_per_week"
variable.probability = 0.008
variable = discreteDistribution.variables.add()
variable.name = "zero_ecstasy_per_week"
variable.probability = 0.99

discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "speed_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_five_speed_per_week"
variable.probability = 0.002
variable = discreteDistribution.variables.add()
variable.name = "one_to_five_speed_per_week"
variable.probability = 0.008
variable = discreteDistribution.variables.add()
variable.name = "zero_speed_per_week"
variable.probability = 0.99


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "amphetamines_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_fifteen_amphetamines_per_week"
variable.probability = 0.002
variable = discreteDistribution.variables.add()
variable.name = "one_to_fifteen_amphetamines_per_week"
variable.probability = 0.008
variable = discreteDistribution.variables.add()
variable.name = "zero_amphetamines_per_week"
variable.probability = 0.99


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "other_substance_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_fifteen_other_substance_per_week"
variable.probability = 0.002
variable = discreteDistribution.variables.add()
variable.name = "one_to_fifteen_other_substance_per_week"
variable.probability = 0.008
variable = discreteDistribution.variables.add()
variable.name = "zero_other_substance_per_week"
variable.probability = 0.99


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "opiods_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_fifteen_opiods_per_week"
variable.probability = 0.002
variable = discreteDistribution.variables.add()
variable.name = "one_to_fifteen_opiods_per_week"
variable.probability = 0.008
variable = discreteDistribution.variables.add()
variable.name = "zero_opiods_per_week"
variable.probability = 0.99


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "depressants_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_five_depressants_per_week"
variable.probability = 0.002
variable = discreteDistribution.variables.add()
variable.name = "one_to_five_depressants_per_week"
variable.probability = 0.008
variable = discreteDistribution.variables.add()
variable.name = "zero_depressants_per_week"
variable.probability = 0.99


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "cannabis_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_fifteen_cannabis_per_week"
variable.probability = 0.01
variable = discreteDistribution.variables.add()
variable.name = "one_to_fifteen_cannabis_per_week"
variable.probability = 0.09
variable = discreteDistribution.variables.add()
variable.name = "zero_cannabis_per_week"
variable.probability = 0.90


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "hallucinogens_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_fifteen_hallucinogens_per_week"
variable.probability = 0.002
variable = discreteDistribution.variables.add()
variable.name = "one_to_fifteen_hallucinogens_per_week"
variable.probability = 0.008
variable = discreteDistribution.variables.add()
variable.name = "zero_hallucinogens_per_week"
variable.probability = 0.99


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "dissociatives_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_five_dissociatives_per_week"
variable.probability = 0.002
variable = discreteDistribution.variables.add()
variable.name = "one_to_five_dissociatives_per_week"
variable.probability = 0.008
variable = discreteDistribution.variables.add()
variable.name = "zero_dissociatives_per_week"
variable.probability = 0.99


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "inhalants_per_week"
variable = discreteDistribution.variables.add()
variable.name = "over_fifteen_inhalants_per_week"
variable.probability = 0.004
variable = discreteDistribution.variables.add()
variable.name = "one_to_fifteen_inhalants_per_week"
variable.probability = 0.016
variable = discreteDistribution.variables.add()
variable.name = "zero_inhalants_per_week"
variable.probability = 0.98



discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "activity_level"
variable = discreteDistribution.variables.add()
variable.name = "sedentary"
variable.probability = 0.3
variable = discreteDistribution.variables.add()
variable.name = "somewhat_active"
variable.probability = 0.4
variable = discreteDistribution.variables.add()
variable.name = "very_active"
variable.probability = 0.2
variable = discreteDistribution.variables.add()
variable.name = "intense_physical_exercise"
variable.probability = 0.1


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "lonely"
variable = discreteDistribution.variables.add()
variable.name = "often_lonely"
variable.probability = 0.3
variable = discreteDistribution.variables.add()
variable.name = "not_often_lonely"
variable.probability = 0.7


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "close_confidants"
variable = discreteDistribution.variables.add()
variable.name = "no_close_confidants"
variable.probability = 0.3
variable = discreteDistribution.variables.add()
variable.name = "has_close_confidants"
variable.probability = 0.7


# basics/medical questions


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "regular_exams"
variable = discreteDistribution.variables.add()
variable.name = "no_regular_exams"
variable.probability = 0.6
variable = discreteDistribution.variables.add()
variable.name = "regular_exams"
variable.probability = 0.4


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "blood_pressure"
variable = discreteDistribution.variables.add()
variable.name = "very_high_blood_pressure"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "high_blood_pressure"
variable.probability = 0.1
variable = discreteDistribution.variables.add()
variable.name = "borderline_blood_pressure"
variable.probability = 0.2
variable = discreteDistribution.variables.add()
variable.name = "low_blood_pressure"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "normal_blood_pressure"
variable.probability = 0.65


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "blood_pressure_medication"
variable = discreteDistribution.variables.add()
variable.name = "taking_blood_pressure_medication"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "not_taking_blood_pressure_medication"
variable.probability = 0.95


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "cholesterol"
variable = discreteDistribution.variables.add()
variable.name = "high_cholesterol"
variable.probability = 0.10
variable = discreteDistribution.variables.add()
variable.name = "normal_cholesterol"
variable.probability = 0.90


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "heart_attack"
variable = discreteDistribution.variables.add()
variable.name = "had_heart_attack"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "no_heart_attack"
variable.probability = 0.95


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "tiaa"
variable = discreteDistribution.variables.add()
variable.name = "had_tiaa"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "no_tiaa"
variable.probability = 0.95


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "stroke"
variable = discreteDistribution.variables.add()
variable.name = "had_stroke"
variable.probability = 0.01
variable = discreteDistribution.variables.add()
variable.name = "no_stroke"
variable.probability = 0.99


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "peripheral_artery_disease"
variable = discreteDistribution.variables.add()
variable.name = "had_peripheral_artery_disease"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "no_peripheral_artery_disease"
variable.probability = 0.95


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "angina"
variable = discreteDistribution.variables.add()
variable.name = "had_angina"
variable.probability = 0.1
variable = discreteDistribution.variables.add()
variable.name = "no_angina"
variable.probability = 0.90


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "atherosclerotic_cardiovascular_disease"
variable = discreteDistribution.variables.add()
variable.name = "had_atherosclerotic_cardiovascular_disease"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "no_atherosclerotic_cardiovascular_disease"
variable.probability = 0.95


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "diabetes"
variable = discreteDistribution.variables.add()
variable.name = "has_diabetes"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "prediabetes"
variable.probability = 0.95
variable = discreteDistribution.variables.add()
variable.name = "no_diabetes"
variable.probability = 0.95


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "diabetes_medication"
variable = discreteDistribution.variables.add()
variable.name = "insulin"
variable.probability = 0.02
variable = discreteDistribution.variables.add()
variable.name = "oral_medication"
variable.probability = 0.03
variable = discreteDistribution.variables.add()
variable.name = "no_diabetes_medication"
variable.probability = 0.95


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "disability_walk_or_run"
variable = discreteDistribution.variables.add()
variable.name = "have_disability_walk_or_run"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "no_disability_walk_or_run"
variable.probability = 0.95


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "disability_equipment"
variable = discreteDistribution.variables.add()
variable.name = "have_disability_equipment"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "no_disability_equipment"
variable.probability = 0.95


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "mental_disability_cant_work"
variable = discreteDistribution.variables.add()
variable.name = "have_mental_disability_cant_work"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "no_mental_disability_cant_work"
variable.probability = 0.95


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "other_chronic_disease"
variable = discreteDistribution.variables.add()
variable.name = "have_other_chronic_disease"
variable.probability = 0.05
variable = discreteDistribution.variables.add()
variable.name = "no_other_chronic_disease"
variable.probability = 0.95


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
discreteDistribution.name = "new_or_worse_shortness_of_breath"
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
variable.name = "deliveris_no_sanitation_once_or_more_per_week"
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
discreteDistribution.name = "neighbors_social_distancing"
variable = discreteDistribution.variables.add()
variable.name = "no_neighbors_social_distancing"
variable.probability = 0.40
variable = discreteDistribution.variables.add()
variable.name = "neighbors_social_distancing"
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


#wearable anomalies


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "heart_rate_variability"
variable = discreteDistribution.variables.add()
variable.name = "abnormally_low_heart_rate_variability"
variable.probability = 0.02
variable = discreteDistribution.variables.add()
variable.name = "low_heart_rate_variabiliity"
variable.probability = 0.15
variable = discreteDistribution.variables.add()
variable.name = "normal_heart_rate_variability"
variable.probability = 0.66
variable = discreteDistribution.variables.add()
variable.name = "high_heart_rate_variability"
variable.probability = 0.17



discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "oxygen"
variable = discreteDistribution.variables.add()
variable.name = "abnormally_low_oxygen"
variable.probability = 0.02
variable = discreteDistribution.variables.add()
variable.name = "low_oxygen"
variable.probability = 0.15
variable = discreteDistribution.variables.add()
variable.name = "normal_oxygen"
variable.probability = 0.83


#hotspot anomaly


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "hotspot"
variable = discreteDistribution.variables.add()
variable.name = "abnormally_high_hotspot"
variable.probability = 0.02
variable = discreteDistribution.variables.add()
variable.name = "high_hotspot"
variable.probability = 0.15
variable = discreteDistribution.variables.add()
variable.name = "normal_hotspot"
variable.probability = 0.66
variable = discreteDistribution.variables.add()
variable.name = "low_hotspot"
variable.probability = 0.17


discreteDistribution = bayesianNetwork.discreteDistributions.add()
discreteDistribution.name = "severe_neck_pain"
variable = discreteDistribution.variables.add()
variable.name = "severe_neck_pain"
variable.probability = 0.02
variable = discreteDistribution.variables.add()
variable.name = "no_severe_neck_pain"
variable.probability = 0.98


# conditional probability tables

cpt ={} 

cpt["wearables"] = avg(bayesianNetwork,cpt,
{
"heart_rate_variability":{"abnormally_low_heart_rate_variability","low_heart_rate_variabiliity"},
"oxygen":{"abnormally_low_oxygen","low_oxygen"}
},
["anomalous","slight_anomaly","normal"]
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

cpt["untreated_blood_pressure"] = all(bayesianNetwork,cpt,
	{
	 "blood_pressure":{"very_high_blood_pressure","high_blood_pressure"},
	 "blood_pressure_medication":{"not_taking_blood_pressure_medication"}
	},
	["untreated_blood_pressure", "other_blood_pressure"]
	)
	
	
cpt["untreated_diabetes"] = all(bayesianNetwork,cpt,
	{
	 "diabetes":{"has_diabetes"},
	 "blood_pressure_medication":{"no_diabetes_medication"}
	},
	["untreated_diabetes", "other_diabetes"]
	)
	
	
cpt["metabolic_disease"] = if_then_else(bayesianNetwork,cpt,
	{
	"untreated_diabetes":{"untreated_diabetes"},
	"diabetes_medication":{"insulin","oral_diabetes_medication"},
	"untreated_blood_pressure":{"untreated_blood_pressure"},
	"diabetes":{"prediabetes"}
	},
	["severe_metabolic_disease","high_metabolic_disease", "medium_metabolic_disease","low_metabolic_disease","no_metabolic_disease"]
	) 


	
	

cpt["emergency_treatment"] = any(bayesianNetwork,cpt,
{
"possible_dehydration":{"possible_dehydration"},
"possible_meningitis":{"possible_meningitis"},
"acute_medical_condition":{"acute_medical_condition"}
},
["emergency_treatment","no_emergency_treatment"]
)



	
addCpt(bayesianNetwork,cpt)
covid = bayesInitialize(bayesianNetwork, "covid")
