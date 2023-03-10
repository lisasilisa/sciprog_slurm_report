import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import matplotlib.colors as colors
import matplotlib.cm as cmx

#####################
## DATA VISUALIZER ##
#####################

class DataVisualizer:

    def __init__(self, stats_dict:dict, plot_config:dict=None):
        
        self.stats_dict = stats_dict
        self.plot_config = plot_config

    def plot_all(self):
        """
        Generates all visualizations suitable for a report based on its stats_dict.
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Arguments:
        None
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Returns:
        None
        """
        
        # Basic stats
        self.plot_basic_stats(split="full", export_path="fig/basic_stats_full.jpg")
        if "user_split" in self.stats_dict.keys():
            self.plot_basic_stats(split="user_split", export_path="fig/basic_stats_user_split.jpg")
        if "partition_split" in self.stats_dict.keys():
            self.plot_basic_stats(split="partition_split", export_path="fig/basic_stats_partition_split.jpg")

        # Task metrics
        self.plot_task_metrics(split="full", export_path="fig/task_metrics_full.jpg")
        if "user_split" in self.stats_dict.keys() and any([count>=10 for count in self.stats_dict["user_split"]["user_counts"]]):
            self.plot_task_metrics(split="user_split", export_path="fig/task_metrics_user_split.jpg")
        if "partition_split" in self.stats_dict.keys() and any([count>=10 for count in self.stats_dict["partition_split"]["partition_counts"]]):
            self.plot_task_metrics(split="partition_split", export_path="fig/task_metrics_partition_split.jpg")

        # Termination stats
        self.plot_termination_stats(export_path="fig/termination_stats_full.jpg")


    def plot_basic_stats(self, split:str="full", export_path:str=None):
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
        
        if split == "full":
            
            start_value = self.stats_dict['full']['basic_stats']['n_start']
            end_value = self.stats_dict['full']['basic_stats']['n_end']

            fig, ax = plt.subplots() #figsize=(3,4)

            end_bar = ax.barh(y = 0.2, width = end_value, color=self.plot_config['c_map'](0.8), height=self.plot_config['bar_width']) 
            start_bar = ax.barh(y = 0.8 , width = start_value, color=self.plot_config['c_map'](0.2), height=self.plot_config['bar_width']) 

            ax.set_xlabel('Tasks', fontsize=self.plot_config['label_font_size'], labelpad=self.plot_config['label_pad'])

            ax.set_yticks([0.2,0.8])
            ax.set_yticklabels(['Ended', 'Started'], fontsize = self.plot_config['tick_font_size'])

            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            ax.bar_label(start_bar, padding=3)
            ax.bar_label(end_bar, padding=3)
            
            fig.tight_layout()
            
            
        elif split in ["user_split", "partition_split"]:

            if self.stats_dict[split]:
                
                fig, ax = plt.subplots()

                if split == "user_split":
                    y_labels = self.stats_dict['user_split']['user_names'] # user names
                    start_values = self.stats_dict['user_split']['basic_stats']['n_start']
                    end_values = self.stats_dict['user_split']['basic_stats']['n_end']
                    ax.set_xlabel('User names')

                elif split == "partition_split":
                    y_labels = self.stats_dict['partition_split']['partition_names'] # partition names
                    start_values = self.stats_dict['partition_split']['basic_stats']['n_start']
                    end_values = self.stats_dict['partition_split']['basic_stats']['n_end']
                    ax.set_xlabel('Partitions')
                
                y = np.arange(len(y_labels))  # the label locations

                rects1 = ax.barh(y = y - self.plot_config['bar_width']/2, width = start_values, color = self.plot_config['c_map'](0.8), height=self.plot_config['bar_width'], label='Started')
                rects2 = ax.barh(y = y + self.plot_config['bar_width']/2, width = end_values, color = self.plot_config['c_map'](0.2), height=self.plot_config['bar_width'], label='Ended')
                
                ax.set_xlabel('Tasks', fontsize=self.plot_config['label_font_size'], labelpad=self.plot_config['label_pad'])
                ax.set_yticks(ticks=y)
                ax.set_yticklabels(y_labels, rotation=0, fontsize = self.plot_config['tick_font_size'])
                ax.invert_yaxis()

                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)

                ax.legend(loc = self.plot_config['leg_loc'], fontsize = self.plot_config['leg_font_size'])

                ax.bar_label(rects1, padding=3)
                ax.bar_label(rects2, padding=3)

                fig.tight_layout()

        # Export plot if requested, else just display it
        if export_path:
            # If export path has no file ending, add one
            if export_path.split(".")[-1] == "jpg":
                plt.savefig(export_path, dpi=self.plot_config['dpi'])
            else:
                plt.savefig(export_path+".jpg", dpi=self.plot_config['dpi'])
        else:
            plt.show()
            

    def plot_task_metrics(self, split:str="full", export_path:str=None):
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
        display_labels = ["Allocated CPUs", "Task Duration (min)", "CPU Time (min)"]
        medianprops = dict(color=self.plot_config['c_map'](0.7))
        
        # Create plot for full sample
        if split == "full":

            # Load data from dict
            data = np.zeros((len(metric_labels), 5), dtype=int)
            for i, label in enumerate(metric_labels):
                data[i,:] = self.stats_dict["full"]["task_metrics"][label][1:-2]

            # Convert raw time to minutes
            data[1,:] = data[1,:] / 60
            data[2,:] = data[2,:] / 60

            # Start plot
            fig, axs = plt.subplots(1,3, figsize=(9,4))

            for i, label in enumerate(display_labels):
                # Plot

                axs[i].boxplot(data[i,:], usermedians=[data[i,2]],
                whis=[0,100], vert=True, medianprops=medianprops)
                # Axes
                offset = 0.1*data[i,3]
                axs[i].set_ylim(0-offset,data[i,-1]+offset)
                # Labels
                axs[i].set_xlabel("")
                axs[i].set_xticks([])
                #axs[i].set_ylabel(label, rotation=90)
                axs[i].set_title(label)
                # Other
                axs[i].yaxis.grid(linestyle=":")

            fig.tight_layout()


        # Otherwise get split data
        elif split in ["user_split", "partition_split"]:
            
            # Get unique users/partitions
            if split=="user_split":
                split_labels = self.stats_dict["user_split"]["user_names"]
                split_counts = self.stats_dict["user_split"]["user_counts"]  
            else:
                split_labels = self.stats_dict["partition_split"]["partition_names"]
                split_counts = self.stats_dict["partition_split"]["partition_counts"]

            # Keep only partitions/users with minimum of 10 tasks
            split_labels = [label for label, count in zip(split_labels, split_counts) if count >= 10]

            # Load data
            data = np.zeros((len(metric_labels),6,len(split_labels)),dtype=int)

            for i, metric_label in enumerate(metric_labels):
                for j, split_label in enumerate(split_labels):
                    for k in range(6):
                        data[i,k,j] = self.stats_dict[split]["task_metrics"][metric_label][j][k]
            

            # Convert raw time to minutes
            data[1,:,:] = data[1,:,:] / 60
            data[2,:,:] = data[2,:,:] / 60

            # Start plot
            fig, axs = plt.subplots(3,1) #,figsize=(4,12)

            for i, metric_label in enumerate(metric_labels):
                
                # Plot
                axs[i].boxplot(x=data[i,:,:], usermedians=data[i,2,:], whis=[0,100], vert=True, medianprops=medianprops)
                # Axes
                axs[i].set_ylabel(display_labels[i])
                offset = 0.5*np.max(data[i,4,:])
                y_min, y_max = 0, np.max(data[i,-1,:])
                axs[i].set_ylim(y_min-offset, y_max+offset)
                # Labels
                if i == len(metric_labels)-1:
                    axs[i].set_xticklabels(split_labels)
                else:
                    axs[i].set_xticks([])
                # Other
                axs[i].yaxis.grid(linestyle=":")

            fig.tight_layout()
            fig.align_ylabels()

            if split == 'user_split' and len(split_labels) > 3:
                fig.autofmt_xdate()
    
        # Export plot if requested, else just display it
        if export_path:
            # If export path has no file ending, add one
            if export_path.split(".")[-1] == "jpg":
                plt.savefig(export_path, dpi=self.plot_config['dpi'])
            else:
                plt.savefig(export_path+".jpg", dpi=self.plot_config['dpi'])
        else:
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
        
        color_range = range(len(values))
        cNorm  = colors.Normalize(vmin=0, vmax=color_range[-1])
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=self.plot_config['c_map'])

        color_list = []
        for i in color_range:
            colorVal = scalarMap.to_rgba(i)
            color_list.append(colorVal)
        
        fig, ax = plt.subplots(1)

        patches, _ = plt.pie(values, colors = color_list) #labels=names, autopct=make_autopct(values), pctdistance=0.85,
        labels = [f"{i}: {j}" for i,j in zip(names, values)]

        patches, labels, _ =  zip(*sorted(zip(patches, labels, values),key=lambda x: x[2], reverse=True))

        plt.legend(patches, labels, loc='center', frameon = False) # bbox_to_anchor=(1.3, 0.8))
           
        my_circle=plt.Circle((0,0), 0.7, color='white')
        p=plt.gcf()
        p.gca().add_artist(my_circle)

        plt.tight_layout()
        # Export plot if requested, else just display it
        if export_path:
            # If export path has no file ending, add one
            if export_path.split(".")[-1] == "jpg":
                plt.savefig(export_path, dpi=self.plot_config['dpi'])
            else:
                plt.savefig(export_path+".jpg", dpi=self.plot_config['dpi'])
        else:
            plt.show()



