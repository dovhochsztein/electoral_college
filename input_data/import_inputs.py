import pandas as pd
from math import isnan

def convert_df_to_dict(df, key_column, value_column):
    output_dict = dict()
    for ii in range(len(df)):
        value = df[value_column].iloc[ii]
        if type(value) == str:
            value = int(value.replace(',', ''))
        output_dict[df[key_column].iloc[ii]] = value
    output_dict = {k: output_dict[k] for k, v in output_dict.items() if (type(k) is not float or not isnan(k)) and (type(v) is not float or not isnan(v))}
    return output_dict


def process_special_state(special_state_dict, state_name):
    output_dict = dict()
    for key, value in special_state_dict.items():
        output_dict[state_name + '_' + str(int(key))] = value
    return output_dict


population_df = pd.read_csv('input_data/july_2019_population.csv')
# https://www.infoplease.com/us/states/state-population-by-rank
electoral_votes_df = pd.read_csv('input_data/electoral_votes_2020.csv')

maine_districts_df = pd.read_csv('input_data/maine_districts.csv')
nebraska_districts_df = pd.read_csv('input_data/nebraska_districts.csv')
# https://www.census.gov/mycd/

population = convert_df_to_dict(population_df, key_column='State', value_column='July 2019 Estimate')
electoral_votes = convert_df_to_dict(electoral_votes_df, key_column='State', value_column='Electoral Votes')
maine_districts = convert_df_to_dict(maine_districts_df, key_column='Maine District', value_column='Population')
maine_districts = process_special_state(maine_districts, 'Maine')
nebraska_districts = convert_df_to_dict(nebraska_districts_df, key_column='Nebraska District', value_column='Population')
nebraska_districts = process_special_state(nebraska_districts, 'Nebraska')
