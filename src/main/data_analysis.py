"""
Module to perform analysis on election data to assess dominance and concentration of votes.
It reads the input data, calculates several indices (dominance, G-index, RAE-index, NEM), and generates visualizations.
"""

import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, List
from src.utils.classifier import Classifier
from src.utils.visualize import Visualize
from src.utils.calculator import IndexCalculator
from src.utils.export_data import ExportData


class DataAnalysis:
    """
    Class to perform analysis on Twitter and TSE election data to assess dominance and concentration of votes.
    It reads the input data, calculates several indices (dominance, G-index, RAE-index, NEM), and generates visualizations.
    """

    def __init__(self, file_name: str, data_source: str = "tse"):
        """
        Initialize the ElectionAnalysis class.

        Args:
            file_name (str): The path to the file to analyze.
        """
        self.data_source = data_source
        # Specify the appropriate separator based on the data_source
        if self.data_source == "twitter":
            sep = ","
            encoding = "utf-8"
        else:
            sep = ";"
            encoding = "latin-1"
        self.original_data = pd.read_csv(
            file_name, sep=sep, encoding=encoding, engine="python"
        )
        self.dominance_data: Optional[pd.DataFrame] = None
        self.concentration_data: Optional[pd.DataFrame] = None
        self.elected_candidates: Optional[pd.DataFrame] = None
        self.dominance_agg: Optional[pd.DataFrame] = None
        self.merged_indices_data: Optional[pd.DataFrame] = None
        self.classified_data: Optional[pd.DataFrame] = None
        self.city_names: Optional[pd.DataFrame] = None
         

    def calculate_dominance_index(self) -> pd.DataFrame:
        """
        Calculate the dominance index for each candidate in each city.

        Args:
            data_source (str): The type of data, either 'tse' or 'twitter'.

        Returns:
            pd.DataFrame: The DataFrame with the dominance index calculated for each candidate in each city.
        """
        assert self.data_source in [
            "tse",
            "twitter",
        ], "Invalid data_source, should be 'tse' or 'twitter'."

        data_copy = self.original_data.copy()

        # Determine which column contains votes/mentions based on data type
        column_votes = (
            "qt_votos_nom_validos" if self.data_source == "tse" else "qt_city_mentions"
        )

        # Calculate various indices used to calculate dominance index
        data_copy["total_counts_city"] = data_copy.groupby("nm_municipio")[
            column_votes
        ].transform("sum")
        data_copy["perc_counts"] = (
            data_copy[column_votes] / data_copy["total_counts_city"]
        ) * 100
        data_copy["city_contribution"] = data_copy[column_votes] / data_copy.groupby(
            "sg_partido"
        )[column_votes].transform("sum")
        data_copy["total_cities"] = data_copy.groupby("sg_ue")[
            "nm_municipio"
        ].transform("nunique")

        # Calculate the dominance index for each candidate in each city
        data_copy["dominance_index"] = (
            data_copy["perc_counts"] * data_copy["city_contribution"]
        ) / 100

        # Round the dominance index to up to 6 decimal places
        data_copy["dominance_index"] = data_copy["dominance_index"].round(6)

        self.dominance_data = data_copy
        self._extract_city_names()
        return data_copy

    def _extract_city_names(self) -> List[str]:
        """
        Extract unique city names from the DataFrame.

        Returns:
            List[str]: List of unique city names.
        """
        self.city_names = self.dominance_data['nm_municipio'].unique().tolist()
        return self.city_names
            

    def filter_elected_candidates(self) -> pd.DataFrame:
        """
        Filter candidates with the value 'Eleito' for the column 'ds_sit_totalizacao'.
        """
        if self.data_source == 'twitter':
            self.elected_candidates = self.dominance_data
        else:
            self.elected_candidates = self.dominance_data[
                self.dominance_data["ds_sit_totalizacao"] == "Eleito"
            ]

        return self.elected_candidates



    def aggregate_dominance_index(self) -> pd.DataFrame:
        """
        Aggregate the dominance index for each candidate across all municipalities.
        """
        dominance_agg = (
            self.dominance_data.groupby("nm_urna_candidato")["dominance_index"]
            .sum()
            .reset_index()
        )
        dominance_agg["dominance_index"] /= 100
        dominance_agg["dominance_index"] = dominance_agg["dominance_index"].round(6)

        self.dominance_agg = dominance_agg
        return dominance_agg


    def calculate_concentration(self) -> pd.DataFrame:
        """
        Calculate the concentration of votes for each candidate in the state.
        """
        assert self.data_source in [
            "tse",
            "twitter",
        ], "Invalid data_source, should be 'tse' or 'twitter'."
        column_votes = (
            "qt_votos_nom_validos" if self.data_source == "tse" else "qt_city_mentions"
        )

        data_copy = self.elected_candidates.copy()
        grouped_data = data_copy.groupby("nm_urna_candidato")
        concentration_agg = pd.DataFrame()

        for candidate, group in grouped_data:
            total_valid_votes_candidate = group[column_votes].sum()
            group["contrib_candidate"] = (
                group[column_votes] / total_valid_votes_candidate
            )

            group = IndexCalculator.calculate_contributions(group, data_copy, self.data_source)
            g_index = IndexCalculator.calculate_g_index(group)
            rae_index = IndexCalculator.calculate_rae_index(group)
            nem = IndexCalculator.calculate_nem(rae_index)

            concentration_agg = concentration_agg.append(
                {"nm_urna_candidato": candidate, "nem": nem, "g_index": g_index},
                ignore_index=True,
            )

        concentration_agg["sg_ue"] = concentration_agg["nm_urna_candidato"].map(
            data_copy.drop_duplicates("nm_urna_candidato").set_index(
                "nm_urna_candidato"
            )["sg_ue"]
        )
        concentration_agg["sg_partido"] = concentration_agg["nm_urna_candidato"].map(
            data_copy.drop_duplicates("nm_urna_candidato").set_index(
                "nm_urna_candidato"
            )["sg_partido"]
        )

        data_copy = concentration_agg[
            ["nm_urna_candidato", "sg_ue", "sg_partido", "nem", "g_index"]
        ]
        self.concentration_data = data_copy
        return data_copy


    def merge_indices(self) -> None:
        """
        Merge dominance and concentration dataframes and assign the result to an attribute.

        Raises:
            ValueError: If dominance and concentration calculations have not been performed.
        """
        if self.dominance_agg is None or self.concentration_data is None:
            raise ValueError("Please run dominance and concentration calculations before merging.")

        # Merge the dominance and concentration dataframes
        merged_data = pd.merge(self.dominance_agg, self.concentration_data, on='nm_urna_candidato')

        # Reorder the columns
        desired_columns_order = ['nm_urna_candidato', 'sg_ue', 'sg_partido', 'dominance_index', 'g_index', 'nem']
        self.merged_indices_data = merged_data.reindex(columns=desired_columns_order)
        return self.merged_indices_data


    def process_and_visualize_data(self) -> None:
        """
        Processes the data by classifying voting types, exports the classified data to CSV,
        and generates visualizations based on the data.
        """
        # Classify voting types
        self.classified_data = Classifier.classify_voting_types(self.merged_indices_data)

        # Export the classified data to CSV
        output_path = f"./output/{self.data_source}/voting_types.csv"  # Customize this path as needed
        ExportData(self.classified_data).to_csv(output_path)

        # Generate visualizations
        Visualize(self.dominance_data, self.classified_data).generate_visualizations(self.data_source)

        print(f"Data processing and visualization for '{self.data_source}' completed.")

    def run_main_analysis(self):
        try:
            self.calculate_dominance_index()
            self.filter_elected_candidates()
            self.aggregate_dominance_index()
            self.calculate_concentration()
            self.merge_indices()
            self.process_and_visualize_data()
        except Exception as e:
            print(f"An error occurred during the analysis: {str(e)}")
            return None
        else:
            return self.classified_data

    def run_analysis(self):
        """
        Run the full analysis workflow.
        """
        return self.run_main_analysis()