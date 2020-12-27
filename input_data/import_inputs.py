import pandas as pd

def convert_df_to_dict(df, key_column, value_column):
    output_dict = dict()
    for ii in range(len(df)):
        value = df[value_column].iloc[ii]
        if type(value) == str:
            value = int(value.replace(',', ''))
        output_dict[df[key_column].iloc[ii]] = value

population_df = pd.read_csv('input_data/july_2019_population.csv')
electoral_votes_df = pd.read_csv('input_data/electoral_votes_2020.csv')


population = convert_df_to_dict(population_df, key_column='State', value_column='July 2019 Estimate')
electoral_votes = convert_df_to_dict(electoral_votes_df, key_column='State', value_column='Electoral Votes')

