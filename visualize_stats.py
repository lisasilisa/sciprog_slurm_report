"""
Dev script for using the data_visualizer module. Loads the cleaned dataframe, computes statistics and visualizes them.
"""

import pandas as pd

from stats_extractor import StatsExtractor
from data_visualizer import DataVisualizer

# Load df
df = pd.read_csv("dev_df.csv")

# Initialize StatExtractor
S = StatsExtractor(df)

# Get stats dict
stats_dict = S.extract_stats()

# Intialize visualizer
Viz = DataVisualizer(stats_dict)

#################
## FULL SAMPLE ##
#################

# Basic stats
Viz.plot_basic_stats(split="full")
