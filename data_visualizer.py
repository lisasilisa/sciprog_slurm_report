"""

Basic Stats (Full Sample):
    barplot with 2 bars (started, ended),
    both indicating the share of not-ended started or not-started ended tasks.

TaskMetrics (Full Sample):
    Boxplot in multi-plot-frame for AllocCPUs, ElapsedRaw, CPUTimeRaw

Termination Stats:
    Pie/donut chart
"""

import numpy as np
import matplotlib.pyplot as plt

class DataVisualizer:

    def __init__(self, stats_dict:str, plot_config:dict):
        
        self.stats_dict = stats_dict
        self.plot_config = plot_config

    
    def plot_basic_stats(split:str="full", export_path=None):
        """
        Plots stats on the number of started/ended jobs in a barchart.
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Arguments:
        split: str in ["full", "user_split", "partition"_split"]
        export_path: None or path to export plot to
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Returns:
        None
        """
        pass

    def plot_task_metrics(split:str="full", export_path=None):
        """
        Plots stats on CPUTime, Elapsed time and AllocCPUS in a boxplot.
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Arguments:
        split: str in ["full", "user_split", "partition"_split"]
        export_path: None or path to export plot to
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Returns:
        None
        """
        pass

    def plot_termination_stats(export_path=None):
        """
        Plots termination stats in a donut chart.
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Arguments:
        split: str in ["full", "user_split", "partition"_split"]
        export_path: None or path to export plot to
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Returns:
        None
        """
        pass


