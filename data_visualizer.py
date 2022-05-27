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
import matplotlib.ticker as ticker

class DataVisualizer:

    def __init__(self, stats_dict:str, plot_config:dict):
        
        self.stats_dict = stats_dict
        self.plot_config = plot_config


    def __plotting_helper(self, ax, values:dict):
        """
        Creates the plot for one user/partition or for the whole account
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Arguments:
        ax: axes object
        values: dict in format {'n_start_end': 200, 'n_start': 2569, 'n_end': 2586}
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Returns:
        axes object
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        """
        
        start = ax.bar(0, values['n_start'], color='lightgreen', width=0.2, label='Started \ Ended: ' + str(values['n_start']-values['n_start_end'])) 
        
        end = ax.bar(0.4, values['n_end'], color='lightcoral',width=0.2, label='Ended \ Started: ' + str(values['n_end']-values['n_start_end']))
        
        start_and_end = ax.bar(0, values['n_start_end'], color='green', width=0.2, alpha=0.8, label='Started + Ended: ' + str(values['n_start_end'])) 
        
        end_and_start = ax.bar(0.4, values['n_start_end'], color='brown', width=0.2, alpha=0.8, label ='Started + Ended: ' + str(values['n_start_end'])) 
        
        ax.set_xlabel(None)
        ax.set_xticks([0,0.4], ['Started', 'Ended'], fontsize=12)
        ax.set_ylabel('Tasks', fontsize=15)
        ax.tick_params(bottom=False, left=True)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        
        rects = ax.patches
        labels = [values['n_start'], values['n_end']]

        for rect, label in zip(rects, labels):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2, height, label, ha="center", va="bottom")
        
        ax.legend(loc = 'center', handles = [start, start_and_end, end, end_and_start])
        return ax
   
    
    def plot_basic_stats(self, split:str="full", export_path=None):    
        """
        Plots stats on the number of started/ended jobs in a barchart.
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Arguments:
        split: str in ["full", "user_split", "partition"_split"]
        export_path: None or path to export plot to
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Returns:
        None
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

        TO IMPLEMENT: handle export_path 
        """
        
        if split == "full":
            fig, ax = plt.subplots(figsize=(6,6))
            values = self.stats_dict['full']['basic_stats'] 
            ax = self.__plotting_helper(ax, values)
            ax.plot()
            plt.show()
            
            
        elif split =="user_split":
            if self.stats_dict[split]:
                amount_of_users = len(self.stats_dict['user_split']['user_names'])

                for i in range(amount_of_users):
                    values = {}
                    for start, amount in self.stats_dict['user_split']['basic_stats'].items():
                        values[start] = amount[i]
                    
                    fig, ax = plt.subplots(figsize=(6,6))
                    ax.title.set_text('User: ' + str(self.stats_dict['user_split']['user_names'][i])) 
                    ax = self.__plotting_helper(ax, values)
                    ax.plot()
                plt.show()
                    
        elif split == "partition_split":
            if self.stats_dict[split]:
                amount_of_partitions = len(self.stats_dict['partition_split']['partition_names'])
                
                for i in range(amount_of_partitions):
                    values = {}
                    for start, amount in self.stats_dict['partition_split']['basic_stats'].items():
                        values[start] = amount[i]
                    
                    fig, ax = plt.subplots(figsize=(6,6))
                    ax.title.set_text('Partition: ' + str(self.stats_dict['partition_split']['partition_names'][i])) 
                    ax = self.__plotting_helper(ax, values)
                    ax.plot()
                plt.show()
            

    def plot_task_metrics(self, split:str="full", export_path=None):
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

    def plot_termination_stats(self, export_path=None):
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


