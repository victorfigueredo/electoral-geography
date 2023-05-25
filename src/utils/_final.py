
import pandas as pd


# Replace 'your_file_path.csv' with the path to your CSV file
file_path = 'data/2022/sp_voting_type_twitter.csv'

# Read the CSV file and create a DataFrame
df = pd.read_csv(file_path, sep=';', encoding='latin-1', engine='python')


# Count the frequencies of each voting_type
voting_type_counts = df['voting_type'].value_counts()

# Calculate the relative frequencies (proportions) of each voting_type
voting_type_relative_freq = df['voting_type'].value_counts(normalize=True)

# Combine the counts and relative frequencies into a single DataFrame
frequency_table = pd.concat([voting_type_counts, voting_type_relative_freq], axis=1)
frequency_table.columns = ['Count', 'Relative Frequency']

# Display the frequency table
print(frequency_table)

frequency_table.to_excel("data/2022/sp_voting_type_tse_twitter_freq.xls", sheet_name='Voting Type Frequency', index_label='Voting Type')

# Assuming 'df' is the DataFrame with the provided data

# Calculate the mean of each numerical column
mean_df = df.mean()

# Calculate the standard deviation of each numerical column
std_df = df.std()

# Calculate the minimum value of each numerical column
min_df = df.min(numeric_only=True)

# Calculate the maximum value of each numerical column
max_df = df.max(numeric_only=True)

# Calculate the median of each numerical column
median_df = df.median()

# Group by 'voting_type' and calculate the mean for each group
grouped_mean = df.groupby('voting_type').mean()

# Group by 'sg_partido' and calculate the mean for each group
party_mean = df.groupby('sg_partido').mean()

# Print the results
print("Mean values:\n", mean_df)
print("\nStandard deviation values:\n", std_df)
print("\nMinimum values:\n", min_df)
print("\nMaximum values:\n", max_df)
print("\nMedian values:\n", median_df)
print("\nMean values by voting type:\n", grouped_mean)
print("\nMean values by party:\n", party_mean)
