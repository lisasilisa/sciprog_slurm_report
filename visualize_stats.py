"""
Dev script for using the data_visualizer module. Loads the cleaned dataframe, computes statistics and visualizes them.
"""

import pandas as pd

from stats_extractor import StatsExtractor
from data_visualizer import DataVisualizer
from plot_config import set_plot_config

# Load df
df = pd.read_csv("dev_df_v2.csv")

# Initialize StatExtractor
S = StatsExtractor(df)

# Get stats dict
stats_dict = S.extract_stats()

print(stats_dict["full"]["task_metrics"])

# Intialize visualizer

#print(stats_dict["user_split"]["task_metrics"].keys())

Viz = DataVisualizer(stats_dict, set_plot_config())

#################
## FULL SAMPLE ##
#################

# Basic stats
Viz.plot_basic_stats(split="full", export_path="fig/basic_stats_full.jpg")
Viz.plot_basic_stats(split="user_split", export_path="fig/basic_stats_user_split.jpg")
Viz.plot_basic_stats(split="partition_split", export_path="fig/basic_stats_partition_split.jpg")

# Task Metrics
Viz.plot_task_metrics(split="full", export_path="fig/task_metrics_full.jpg")
Viz.plot_task_metrics(split="user_split", export_path="fig/task_metrics_user_split.jpg")
Viz.plot_task_metrics(split="partition_split", export_path="fig/task_metrics_partition_split.jpg")

# Termination Stats
Viz.plot_termination_stats(export_path="fig/termination_stats_full.jpg")