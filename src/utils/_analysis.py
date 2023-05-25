import random
import re
from unidecode import unidecode
import pandas as pd
from dmin import read_data, calculate_dominance_index, aggregate_dominance_index, calculate_concentration
from classify import classify_voting_types
from plot import plot_elected_official_treemap

def identify_city_mentions():
    # Replace 'tweets.csv' with the path to your CSV file containing tweets
    tweets_file = 'data/2022/sp_tweets.csv'
    tweets_df = pd.read_csv(tweets_file)

    # Remove accents from the 'content' column
    tweets_df['content'] = tweets_df['content'].apply(lambda x: unidecode(x))

    # List of city names
    df_domin = read_data("data/sp_dominance.csv")
    city_names = df_domin['nm_municipio'].unique().tolist()

    # Initialize a new DataFrame to store the results
    results = pd.DataFrame(columns=['nm_municipio', 'nm_urna_candidato', 'qt_city_mentions'])

    # Iterate through each row in the tweets DataFrame
    for index, row in tweets_df.iterrows():
        tweet_content = row['content']
        deputy_name = row['nm_urna_candidato']

        # Iterate through each city name
        for city in city_names:
            # Remove accents from the city name
            city_unaccented = unidecode(city)

            # Check if the city name is present in the tweet content
            if city_unaccented.lower() in tweet_content.lower():
                # Check if there is already an entry for the current city and deputy_name in the results DataFrame
                existing_entry = results.loc[(results['nm_municipio'] == city) & (results['nm_urna_candidato'] == deputy_name)]

                if not existing_entry.empty:
                    # If an entry exists, increment the count
                    results.loc[(results['nm_municipio'] == city) & (results['nm_urna_candidato'] == deputy_name), 'qt_city_mentions'] += 1
                else:
                    # If no entry exists, create a new entry with count 1
                    results = results.append({'nm_municipio': city, 'nm_urna_candidato': deputy_name, 'qt_city_mentions': 1}, ignore_index=True)

    # Write the results DataFrame to a CSV file
    results.to_csv('data/2022/sp_city_mentions.csv', index=False)


def add_party_state():
    # Read data from the new CSV file
    
    new_data_df = read_data('data/2022/sp_main.csv')


    results = pd.read_csv('data/2022/sp_city_mentions.csv')
    # Merge the two DataFrames based on the 'deputy_name' column
    merged_results = results.merge(new_data_df[['nm_urna_candidato', 'sg_ue', 'sg_partido']], on='nm_urna_candidato', how='left')

    # Write the merged DataFrame to a CSV file
    merged_results.to_csv('data/2022/sp_city_mentions_enriched.csv', index=False)


def classify_():
    data = pd.read_csv('data/2022/sp_city_mentions_enriched.csv')
    data_with_dominance_index = calculate_dominance_index(data,'')
    dominance_agg = aggregate_dominance_index(data_with_dominance_index)
    # print(dominance_agg)

    concentration = calculate_concentration(data,'')
    # print(concentration)
    merged_data = pd.merge(dominance_agg, concentration, on='nm_urna_candidato')
    print(merged_data)

    # Display the dominance index and concentration for each elected candidate
    # print(merged_data.sort_values(['dominance_index', 'g_index'], ascending=[False, False]))
    # print("\n\n\n\n\n")


    # Classify candidates into quadrants
    classified_candidates = classify_voting_types(merged_data)
    with open('data/2022/sp_voting_type_twitter.csv', 'w') as f:
        f.write(classified_candidates.to_csv(sep=';', index=False))
    # print(classified_candidates)

    

    random_candidate = random.choice(classified_candidates['nm_urna_candidato'].tolist())

    for i in classified_candidates['nm_urna_candidato'].tolist():
        plot_elected_official_treemap(data_with_dominance_index, classified_candidates, i, '')
 

# classify_()

# Select columns to display
columns_to_display = [
    'nm_urna_candidato',
    'sg_ue_tse',
    'sg_partido_tse',
    'dominance_index_diff',
    'nem_diff',
    'g_index_diff',
    'voting_type_tse',
    'voting_type_twitter'
]

# Read CSV files into DataFrames
tse = read_data('data/2022/sp_voting_type_tse.csv')
 = read_data('data/2022/sp_voting_type_twitter.csv')

# Merge the DataFrames on the nm_urna_candidato column
merged_data = tse.merge(, on='nm_urna_candidato', suffixes=('_tse', '_twitter'))
print(merged_data)

# Calculate differences between the relevant columns
merged_data['dominance_index_diff'] = merged_data['dominance_index_tse'] - merged_data['dominance_index_twitter']
merged_data['nem_diff'] = merged_data['g_index_tse'] - merged_data['g_index_twitter']
merged_data['g_index_diff'] = merged_data['g_index_tse'] - merged_data['g_index_twitter']

# Add a new column indicating if voting_type is the same or not
merged_data['voting_type_same'] = merged_data['voting_type_tse'] == merged_data['voting_type_twitter']

# Filter the DataFrame to only show rows where the voting_type differs
different_voting_type = merged_data[merged_data['voting_type_same'] == True]
print(different_voting_type[columns_to_display])

with open('data/2022/sp_voting_type_same.csv', 'w') as f:
    different_voting_type[columns_to_display].to_excel('data/2022/sp_voting_type_same.xls', index=False)
    f.write(different_voting_type[columns_to_display].to_csv(sep=';', index=False))

# Filter the DataFrame to only show rows where the voting_type differs
different_voting_type = merged_data[merged_data['voting_type_same'] == False]
# Display the differences between the two CSV files for cases where voting_type differs
print(different_voting_type[columns_to_display])

# Count the number of same and different voting_types
same_vs_different_voting_types = merged_data['voting_type_same'].value_counts()

# Display the count of same and different voting_types
print("Same voting_type count:", same_vs_different_voting_types.get(True, 0))
print("Different voting_type count:", same_vs_different_voting_types.get(False, 0))

