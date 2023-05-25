
import pandas as pd
import numpy as np

class IndexCalculator:

    @staticmethod
    def calculate_contributions(group: pd.DataFrame, data: pd.DataFrame, data_source: str = "tse"
    ) -> pd.DataFrame:
        """
        Calculate the vote contributions for each candidate and each municipality.

        This function is used to normalize the number of votes for each candidate and municipality. 
        This normalization is essential for calculating the G index and the RAE index, which measure 
        the concentration of votes.

        Args:
            group (pd.DataFrame): The DataFrame containing the data for a specific candidate.
            data (pd.DataFrame): The original DataFrame containing the data for all candidates.
            data_source (str, optional): The type of data. Defaults to "tse".

        Returns:
            pd.DataFrame: The DataFrame with the calculated contributions.
        """
        valid_votes_col = (
            "qt_votos_nom_validos" if data_source == "tse" else "qt_city_mentions"
        )

        # Calculate the total valid votes for the candidate and calculate the contribution of each municipality to this total
        total_valid_votes_candidate = group[valid_votes_col].sum()
        group["contrib_candidate"] = (
            group[valid_votes_col] / total_valid_votes_candidate
        )

        # Calculate the total valid votes for each municipality and calculate the contribution of each municipality to this total
        total_valid_votes_municipality = data.groupby("nm_municipio")[
            valid_votes_col
        ].sum()
        group["total_votos_validos"] = group["nm_municipio"].map(
            total_valid_votes_municipality
        )

        group["contrib_municipality"] = (
            group["total_votos_validos"] / group["total_votos_validos"].sum()
        )

        return group

    @staticmethod
    def calculate_g_index(group: pd.DataFrame) -> float:
        """
        Calculate the G index.

        The G index measures the concentration of votes by comparing the vote distribution for a candidate
        with the vote distribution in each municipality. A higher G index indicates a higher concentration of votes.

        Args:
            group (pd.DataFrame): The DataFrame containing the data for a specific candidate.

        Returns:
            float: The G index.
        """
        return np.sum(
            np.square(group["contrib_candidate"] - group["contrib_municipality"])
        )

    @staticmethod
    def calculate_rae_index(group: pd.DataFrame) -> float:
        """
        Calculate the RAE index.

        The RAE index measures the concentration of votes by taking the square of the vote share for a candidate.
        A lower RAE index indicates a higher concentration of votes.

        Args:
            group (pd.DataFrame): The DataFrame containing the data for a specific candidate.

        Returns:
            float: The RAE index.
        """
        rae_index = np.sum(np.square(group["contrib_candidate"]))
        # If RAE index is NaN or less than or equal to 0, assign a very small positive value to prevent division by zero in the NEM calculation
        if np.isnan(rae_index) or rae_index <= 0:
            rae_index = 1e-9
        return rae_index

    @staticmethod
    def calculate_nem(rae_index: float) -> float:
        """
        Calculate the NEM (Normalized Effective Number of Municipalities).

        The NEM is the inverse of the RAE index, which measures the dispersion of votes. 
        A higher NEM indicates a greater dispersion of votes.

        Args:
            rae_index (float): The RAE index.

        Returns:
            float: The NEM.
        """
        return 1 / rae_index