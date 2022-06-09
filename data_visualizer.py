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

######################
## HELPER FUNCTIONS ##
######################

def determine_grid_size(n_plots):
    """
    Determines an appropriate multiplot grid size to arange <n_plots> plots.
    """

    i, j = 1, 1
    while i*j < n_plots:
        if i > j+1:
            if (i-1)*(j+1) == n_plots:
                return i-1,j+1
            else:
                j += 1
        else:
            i += 1
    return i,j

#####################
## DATA VISUALIZER ##
#####################

class DataVisualizer:

    def __init__(self, stats_dict:str, plot_config:dict=None):
        
        self.stats_dict = stats_dict
        self.plot_config = plot_config


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

        TO IMPLEMENT: 
        * handle export_path 
        * How to sort bar_plots descending: according to started or finished jobs? 

        """
        
        if split == "full":
            
            start_value = self.stats_dict['full']['basic_stats']['n_start']
            end_value = self.stats_dict['full']['basic_stats']['n_end']

            fig, ax = plt.subplots(figsize=(3,4))

            start_bar = ax.barh(y = 0.2 , width = start_value, color='lightgreen', height=0.1) 
            end_bar = ax.barh(y = 0, width = end_value, color='lightcoral', height=0.1) 

            ax.set_xlabel('Tasks', size=15)

            ax.set_yticks([0,0.2])
            ax.set_yticklabels(['Started', 'Ended'])

            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            ax.bar_label(start_bar, padding=3)
            ax.bar_label(end_bar, padding=3)
            
            fig.tight_layout()

            plt.show()
            
            
        elif split in ["user_split", "partition_split"]:

            if self.stats_dict[split]:
                
                fig, ax = plt.subplots()


                if split == "user_split":
                    y_labels = self.stats_dict['user_split']['user_names'] # user names
                    start_values = self.stats_dict['user_split']['basic_stats']['n_start']
                    end_values = self.stats_dict['user_split']['basic_stats']['n_end']
                    ax.set_xlabel('User names')

                elif split == "partition_split":
                    y_labels = self.stats_dict['partition_split']['partition_names'] # user names
                    start_values = self.stats_dict['partition_split']['basic_stats']['n_start']
                    end_values = self.stats_dict['partition_split']['basic_stats']['n_end']
                    ax.set_xlabel('Partitions')
                
                y = np.arange(len(y_labels))  # the label locations
                height = 0.35

                rects1 = ax.barh(y = y + height/2, width = start_values, color ='lightgreen', height=height, label='Started')
                rects2 = ax.barh(y = y - height/2, width = end_values, color = 'lightcoral', height=height, label='Ended')

                ax.set_xlabel('Tasks')
                ax.set_yticks(y, y_labels)
                ax.invert_yaxis()

                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)

                ax.legend(loc = 'lower right')

                ax.bar_label(rects1, padding=3)
                ax.bar_label(rects2, padding=3)

                fig.tight_layout()

                plt.show()
            

    def plot_task_metrics(self, split:str="full", export_path=None):
        """
        Plots stats on CPUTime, Elapsed time and AllocCPUS in a boxplot.
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Arguments:
        split: str in ["full", "user_split", "partition_split"]
        export_path: None or path to export plot to
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Returns:
        None
        """

        metric_labels = ["AllocCPUS", "ElapsedRaw", "CPUTimeRaw"]
        display_labels = ["Allocated CPUs", "Elapsed Time (min)", "CPU Time (min)"]
        
        # Create plot for full sample
        if split == "full":

            # Load data from dict
            data = np.zeros((len(metric_labels), 6), dtype=int)
            for i, label in enumerate(metric_labels):
                data[i,:] = self.stats_dict["full"]["task_metrics"][label]

            # Convert raw time to minutes
            data[1,:] = data[1,:] / 60 / 60
            data[2,:] = data[2,:] / 60 / 60

            # Start plot
            fig, axs = plt.subplots(3,1)

            for i, label in enumerate(display_labels):
                # Plot
                axs[i].boxplot(data[i,:], usermedians=[data[i,2]],
                whis=[0,100], vert=False)
                # Axes
                axs[i].set_yticks([])
                # Labels
                axs[i].set_xlabel("")
                axs[i].set_yticks([])
                axs[i].set_ylabel(label, rotation=90)
                # Other
                axs[i].xaxis.grid(linestyle=":")
            
            plt.show()

        # Otherwise get split data
        elif split in ["user_split", "partition_split"]:
            
            # Get unique users/partitions
            if split=="user_split":
                split_labels = self.stats_dict["user_split"]["user_names"]
            else:
                split_labels = self.stats_dict["partition_split"]["partition_names"]

            # Load data
            data = np.zeros((len(metric_labels),6,len(split_labels)),dtype=int)
            for i, metric_label in enumerate(metric_labels):
                for j, split_label in enumerate(split_labels):
                    for k in range(6):
                        data[i,k,j] = self.stats_dict[split]["task_metrics"][metric_label][j][k]
            # Convert raw time to minutes
            data[1,:,:] = data[1,:,:] / 60 / 60
            data[2,:,:] = data[2,:,:] / 60 / 60

            # Start plot
            fig, axs = plt.subplots(3,1)

            for i, metric_label in enumerate(metric_labels):
                
                # Plot
                axs[i].boxplot(data[i,:,:], usermedians=data[i,2,:],
                                whis=[0,100], vert=True)
                # Axes
                axs[i].set_ylabel(display_labels[i])
                axs[i].set_xticklabels(split_labels)
                # Labels
                # Other

            plt.show()
                

    def plot_termination_stats(self, export_path=None):
        """
        Plots termination stats in a donut chart.
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Arguments:
        export_path: None or path to export plot to
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Returns:
        None
        """

        termination_stats = self.stats_dict['full']['termination_stats']
        termination_stats_updated = {k:v for k,v in termination_stats.items() if v!=0} # drop entries with value = 0

        names = [att.split('_')[1] for att in list(termination_stats_updated.keys())]
        values = list(termination_stats_updated.values())

        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct*total/100.0))
                return '{v:d}'.format(v=val)
            return my_autopct

        plt.pie(values, labels=names, autopct=make_autopct(values), pctdistance=0.85)
        
        my_circle=plt.Circle( (0,0), 0.7, color='white')
        p=plt.gcf()
        p.gca().add_artist(my_circle)

        plt.show()



