"""
To classify the values of both dominance index and Gini coefficient into 4 quadrants, we can use the following approach:

Determine the median value of dominance index and Gini coefficient in the dataset.

Based on the median values, divide the values into two groups for each index: high and low.

Combine the two groups of each index to form four quadrants:

Quadrant 1 - Concentrada dominante (High dominance, High inequality): Candidates with high dominance index and high Gini coefficient are in this quadrant.
Quadrant 2 - Concentrada-compartilhada (Low dominance, High inequality): Candidates with low dominance index and high Gini coefficient are in this quadrant.
Quadrant 3 - Dispersa-dominante (High dominance, Low inequality): Candidates with high dominance index and low Gini coefficient are in this quadrant.
Quadrant 4 - Dispersa-compartilhada (Low dominance, Low inequality): Candidates with low dominance index and low Gini coefficient are in this quadrant.

"""

import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple, List
import pandas as pd
import numpy as np


class Classifier:

    @staticmethod
    def classify_voting_types(data) -> pd.DataFrame:
        """
        Classify candidates into four quadrants or 'voting types' based on dominance and concentration indices data.

        This function begins by calculating the mean (average) and standard deviation for both the dominance and 
        NEM indices present in the data. These statistical measurements are used to define thresholds for what 
        constitutes high and low dominance and fragmentation.

        Using these thresholds, each candidate is classified into one of the four voting types: 'Dispersa Dominante', 
        'Concentrada Dominante', 'Dispersa Compartilhada', or 'Concentrada Compartilhada'. The specific type is 
        determined by their respective dominance and fragmentation values.

        Returns:
            pd.DataFrame: A DataFrame with an added 'voting_type' column, classifying the voting types for each candidate.
        """
        # Create a copy of the DataFrame to prevent altering the original data
        data_copy = data.copy()

        # The mean is the central tendency or the average of the data points, it's calculated by adding up all the 
        # values and then dividing by the number of values. The standard deviation measures the amount of variation
        # or dispersion of a set of values. A low standard deviation indicates that the values tend to be close
        # to the mean of the set, while a high standard deviation indicates that the values are spread out over
        # a wider range.
        dominance_mean = data_copy['dominance_index'].mean()
        dominance_std = data_copy['dominance_index'].std()

        # Here, we apply the natural logarithm to the NEM values before calculating the mean and standard deviation.
        # Log-transformation is a tool to handle skewed data and after transformation, the data follows normal 
        # distribution more closely.
        nem_log_mean = np.log(data_copy['nem']).mean()
        nem_log_std = np.log(data_copy['nem']).std()

        std_dev = 0.0000005
        # We define the thresholds for high and low dominance and fragmentation using mean and standard deviation.
        # The threshold for high dominance, for example, is calculated by adding the product of a small constant 
        # and the standard deviation of the dominance to the mean of the dominance. This means that any dominance value
        # greater than this threshold is considered 'high'. Similarly, we subtract the product of the constant and the
        # standard deviation from the mean to get the 'low' threshold. The same logic applies for the fragmentation thresholds.
        high_dominance = dominance_mean + (std_dev * dominance_std)
        low_dominance = dominance_mean - (std_dev * dominance_std)
        high_fragmentation = nem_log_mean + (std_dev * nem_log_std)
        low_fragmentation = nem_log_mean - (std_dev * nem_log_std)

        # We then classify the candidates into four categories depending on their dominance and fragmentation values.
        # The categories are: Dispersa Dominante, Concentrada Dominante, Dispersa Compartilhada, Concentrada Compartilhada.
        # 'Dispersa Dominante' means a candidate with high dominance and high fragmentation, 'Concentrada Dominante' means 
        # a candidate with high dominance but low fragmentation, 'Dispersa Compartilhada' means a candidate with low dominance
        # but high fragmentation, and 'Concentrada Compartilhada' means a candidate with low dominance and low fragmentation.
        data_copy['voting_type'] = 'Unclassified'

        data_copy.loc[(data_copy['dominance_index'] > high_dominance) & (np.log(data_copy['nem']) > high_fragmentation), 'voting_type'] = 'Dispersa Dominante'
        data_copy.loc[(data_copy['dominance_index'] > high_dominance) & (np.log(data_copy['nem']) < low_fragmentation), 'voting_type'] = 'Concentrada Dominante'
        data_copy.loc[(data_copy['dominance_index'] < low_dominance) & (np.log(data_copy['nem']) > high_fragmentation), 'voting_type'] = 'Dispersa Compartilhada'
        data_copy.loc[(data_copy['dominance_index'] < low_dominance) & (np.log(data_copy['nem']) < low_fragmentation), 'voting_type'] = 'Concentrada Compartilhada'

        return data_copy
