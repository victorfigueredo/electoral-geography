import pandas as pd
from typing import List
from unidecode import unidecode
from .export_data import ExportData  # Assuming this is the correct import for your setup

class CityMentionAnalyzer:
    """
    This class is used to analyze city mentions in tweets data.
    """

    def __init__(self, tweets_file_path: str, city_names: List[str]):
        """
        Initialize CityMentionAnalyzer with the file path to tweets data and a list of city names.

        Args:
            tweets_file_path (str): Path to the CSV file containing tweets data.
            city_names (List[str]): List of city names.
        """
        self.tweets_file_path = tweets_file_path
        self.city_names = city_names

    def identify_city_mentions(self) -> pd.DataFrame:
        """
        Identify city mentions in the tweets.

        Returns:
            pd.DataFrame: DataFrame with city mentions information.
        """
        tweets_df = pd.read_csv(self.tweets_file_path)
        tweets_df['content'] = tweets_df['content'].apply(unidecode)

        results = pd.DataFrame(columns=['nm_municipio', 'nm_urna_candidato', 'qt_city_mentions'])
        for index, row in tweets_df.iterrows():
            tweet_content = row['content']
            deputy_name = row['nm_urna_candidato']

            for city in self.city_names:
                city_unaccented = unidecode(city)
                if city_unaccented.lower() in tweet_content.lower():
                    existing_entry = results.loc[(results['nm_municipio'] == city) & (results['nm_urna_candidato'] == deputy_name)]
                    if not existing_entry.empty:
                        results.loc[(results['nm_municipio'] == city) & (results['nm_urna_candidato'] == deputy_name), 'qt_city_mentions'] += 1
                    else:
                        results = results.append({'nm_municipio': city, 'nm_urna_candidato': deputy_name, 'qt_city_mentions': 1}, ignore_index=True)
        return results

    @staticmethod
    def merge_with_main_data(df: pd.DataFrame, main_data_file_path: str) -> pd.DataFrame:
        """
        Merge DataFrame with main data based on the 'deputy_name' column.

        Args:
            df (pd.DataFrame): DataFrame with city mentions information.
            main_data_file_path (str): Path to the main data file.

        Returns:
            pd.DataFrame: Merged DataFrame.
        """
        main_data_df = pd.read_csv(main_data_file_path)
        return df.merge(main_data_df[['nm_urna_candidato', 'sg_ue', 'sg_partido']], on='nm_urna_candidato', how='left')

# # Usage
# analyzer = CityMentionAnalyzer('data/2022/sp_tweets.csv', city_names)
# results = analyzer.identify_city_mentions()
# merged_results = analyzer.merge_with_main_data(results, 'data/2022/sp_main.csv')
