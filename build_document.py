from distutils.command.build import build
from mailbox import NotEmptyError
import pandas as pd
import numpy as np

from stats_extractor import StatsExtractor
from data_visualizer import DataVisualizer
from document_builder import build_table

from pylatex import Document, Section, Subsection, Command, Itemize, Enumerate, Description, Figure, Table, Label, Ref, Marker
from pylatex.utils import italic, NoEscape

###########
## SETUP ##
###########

# Load df
df = pd.read_csv("dev_df_v2.csv")
account_id = '59628c0f-aa89-4a69' # id associated with the dev df

# Initialize StatExtractor
S = StatsExtractor(df)

# Get stats dict
stats_dict = S.extract_stats()

##############
## DOCUMENT ##
##############

geometry_options = {"tmargin":"1.5cm", "lmargin":"3cm", "rmargin":"2.5cm", "bmargin":"1.5cm"}
doc = Document("text_doc", geometry_options=geometry_options)

# Write title page
doc.preamble.append(Command("title", f"User Report: {account_id}"))
doc.preamble.append(Command("author", "We, the Authors"))
doc.preamble.append(Command("date", NoEscape(r"\today")))
doc.append(NoEscape(r"\maketitle"))


## INTRODUCTION ##
with doc.create(Section("Introduction")):
    doc.append("Explain here:")
    with doc.create(Itemize()) as itemize:
        itemize.add_item("what the report is about")
        itemize.add_item("how the user and partition splits work")
        itemize.add_item("what a partition is (lol)")
        itemize.add_item("how many and which users and partitions were included")

## BASIC STATS ##
doc.append(NoEscape(r"\pagebreak"))
with doc.create(Section("Basic Stats")):

    with doc.create(Subsection("Full Sample")):

        data = stats_dict["full"]["basic_stats"]
        
        doc.append(
            f"In the given time frame, {data['n_start']} tasks were started \
            and {data['n_end']} ended. {data['n_start_end']} \
            ({round(data['n_start_end'] / (data['n_end']+data['n_start']-data['n_start_end'])*100,2)} %) \
            of them started and ended within the given time frame."
        )

        with doc.create(Figure(position="h!")) as fig:
            fig.add_image("fig/basic_stats_full.jpg", width="250px")
            fig.add_caption("Number of started and ended tasks.")

    with doc.create(Subsection("User Split")):
        
        user_names = stats_dict["user_split"]["user_names"]
        user_counts = stats_dict["user_split"]["user_counts"]
        n_over_ten_jobs = sum([1 for x in user_counts if x >=10])
        data = stats_dict["user_split"]["basic_stats"]

        doc.append(
            f"The number of tasks (started and ended) ranged from \
            {data['n_start_end'][0]} by {user_names[0]} to \
            {data['n_start_end'][-1]} by {user_names[-1]}. "
        )

        doc.append(
            f"A total of {n_over_ten_jobs} user(s) started and ended at least 10 jobs. \
            The task metrics in Section 3 could only be calculated for these users."
        )

        with doc.create(Figure(position="h!")) as fig:
            fig.add_image("fig/basic_stats_user_split.jpg", width="275px")
            fig.add_caption("Number of started and ended tasks by different users.")  

    with doc.create(Subsection("Partition Split")):

        partition_names = stats_dict["partition_split"]["partition_names"]
        partition_counts = stats_dict["partition_split"]["partition_counts"]
        n_over_ten_jobs = sum([1 for x in partition_counts if x >=10])
        data = stats_dict["partition_split"]["basic_stats"]

        doc.append(
            f"The number of tasks (started and ended) ranged from \
            {data['n_start_end'][0]} on the {partition_names[0]} partiton to \
            {data['n_start_end'][-1]} on {partition_names[-1]}. "
        )

        doc.append(
            f"A total of {n_over_ten_jobs} partition(s) were used to complete (start and end) \
            at least 10 jobs. The task metrics in Section 3 could only be calculated for these partitions."
        )

        data = stats_dict["partition_split"]["basic_stats"]

        with doc.create(Figure(position="h!")) as fig:
            fig.add_image("fig/basic_stats_partition_split.jpg", width="275px")
            fig.add_caption("Number of started and ended tasks on different partitions.")  

## TASK METRICS ##

doc.append(NoEscape(r"\pagebreak"))
with doc.create(Section("Task Metrics")):

    with doc.create(Subsection("Full Sample")):
        
        data = stats_dict["full"]["task_metrics"]

        doc.append(
            f"In the full sample, the job durations ranged from \
            {round(data['ElapsedRaw'][0]/60)} to {round(data['ElapsedRaw'][-2]/60)} minutes \
            (M = {round(data['ElapsedRaw'][-1]/60)} min). "
        )
    
        doc.append(
            f"The number of allocated CPUs ranged from \
            {round(data['AllocCPUS'][0])} to {round(data['AllocCPUS'][-2])} \
            (M = {round(data['AllocCPUS'][-1])}). "
        )

        doc.append(
            f"Finally, the CPU Time (job duration * allocated CPUs) ranged from \
            {round(data['CPUTimeRaw'][0]/60)} to {round(data['CPUTimeRaw'][-2]/60)} minutes \
            (M = {round(data['CPUTimeRaw'][-1]/60)} min). \n"
        )

        # Prepare data for table
        data_array = np.zeros((8,3))
        for i, k in enumerate(data.keys()):
            data_array[:,i] = data[k]
        data_array[:,0] /= 60
        data_array[:,2] /= 60
        data_array = np.round(data_array).astype(int)
        
        # Build table
        with doc.create(Table(position="h!")) as t:
            build_table(doc=doc, data=data_array, col_names=["Job Duration", "Allocated CPUs", "CPU Time"],
                        position_codes="c c c", index=["min", "5quant", "25quant", "median", "75quant", "95quant", "max", "mean"])
            t.add_caption("Task metrics for the full sample.")
            #Label()
        
        # Display plot
        with doc.create(Figure(position="h!")) as fig:
            fig.add_image("fig/task_metrics_full.jpg", width="400px")
            fig.add_caption("Distributions of job duration, allocated CPUs, and CPU time. Whiskers indicate the 5th and 95th percentiles.")  

    doc.append(NoEscape(r"\pagebreak"))
    with doc.create(Subsection("User Split")):

        data = stats_dict["user_split"]["task_metrics"]

        # Some text?
        doc.append("Below, you can find the distributions of the task metrics for each user. In the table, all users are listed. Boxplots are only generated for users with at least 10 jobs.\n")

        # Prepare data for table
        data_array = np.zeros((len(user_names),4), dtype=tuple)
        data_array[:,0] = user_counts
        for user_idx in range(len(user_names)):
            for metric_idx, metric in enumerate(data.keys()):
                metric_vals = data[metric][user_idx]
                if metric_idx == 1:
                    data_array[user_idx,metric_idx+1] = (round(metric_vals[0]), round(metric_vals[-1]), round(metric_vals[-2]))
                else:
                    data_array[user_idx,metric_idx+1] = (round(metric_vals[0]/60), round(metric_vals[-1]/60), round(metric_vals[-2]/60))

        #print(data_array)
        
        # Build table
        with doc.create(Table(position="h!")) as t:
            build_table(doc=doc, data=data_array, col_names=["Num Jobs", "Job Duration", "Allocated CPUs", "CPU Time"],
                        position_codes="l c c c", index=user_names)
            t.add_caption("Task metrics for different users. Values in parantheses indicate (min, mean, max).")

        # Show plot
        with doc.create(Figure(position="h!")) as fig:
            fig.add_image("fig/task_metrics_user_split.jpg", width="350px")
            fig.add_caption("Distributions of job duration, allocated CPUs, and CPU time for different users. Whiskers indicate the 5th and 95th percentiles.") 

    doc.append(NoEscape(r"\pagebreak"))
    with doc.create(Subsection("Partition Split")):

        data = stats_dict["partition_split"]["task_metrics"]

        # Some text?
        doc.append("Below, you can find the distributions of the task metrics for each partition. In the table, all partitions are listed. Boxplots are only generated for partitions with at least 10 jobs.\n")

        # Prepare data for table
        data_array = np.zeros((len(partition_names),4), dtype=tuple)
        data_array[:,0] = partition_counts
        for partition_idx in range(len(partition_names)):
            for metric_idx, metric in enumerate(data.keys()):
                metric_vals = data[metric][partition_idx]
                if metric_idx == 1:
                    data_array[partition_idx,metric_idx+1] = (round(metric_vals[0]), round(metric_vals[-1]), round(metric_vals[-2]))
                else:
                    data_array[partition_idx,metric_idx+1] = (round(metric_vals[0]/60), round(metric_vals[-1]/60), round(metric_vals[-2]/60))

        #print(data_array)
        
        # Build table
        with doc.create(Table(position="h!")) as t:
            build_table(doc=doc, data=data_array, col_names=["Num Jobs", "Job Duration", "Allocated CPUs", "CPU Time"],
                        position_codes="l c c c", index=partition_names)
            t.add_caption("Task metrics for different partitions. Values in parantheses indicate (min, mean, max).")

        # Show plot
        with doc.create(Figure(position="h!")) as fig:
            fig.add_image("fig/task_metrics_user_split.jpg", width="350px")
            fig.add_caption("Distributions of job duration, allocated CPUs, and CPU time for different partitions. Whiskers indicate the 5th and 95th percentiles.") 


## TERMINATION STATS ##
doc.append(NoEscape(r"\pagebreak"))
with doc.create(Section("Termination Stats")):
    
    # Prepare data
    data = stats_dict["full"]["termination_stats"]

    # Write text
    doc.append(
        f"From the {sum(data.values())} jobs that started and ended in the given time frame,\
        {data['n_complete']} were completed successfully,\
        {data['n_cancelled']} were actively cancelled,\
        {data['n_timeout']} were ended due to a timeout,\
        and {data['n_failed']} failed for other reasons."
        )
    
    # Add figure
    with doc.create(Figure(position="h!")) as fig:
        fig.add_image("fig/termination_stats_full.jpg", width="300px")
        fig.add_caption("Termination stats for the full sample.")



# Export pdf
doc.generate_pdf(clean_tex=False)
#doc.generate_tex()

