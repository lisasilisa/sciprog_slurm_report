import numpy as np
from pylatex import Document, Tabularx, Document, Section, Subsection, Command, Itemize, Enumerate, Description, Figure, Table, Tabular, Label, Ref, Marker
from pylatex.utils import bold, italic, NoEscape
from stats_extractor import StatsExtractor
from data_visualizer import DataVisualizer

def build_table(doc:Document, data: np.ndarray, col_names: list=None,
                    position_codes:list=None, index:list=None):

    # Get data dimensions
    m, n = data.shape

    # Check if col_names have correct dimension
    if not col_names or len(col_names) != n:
        col_names = [f"col{i}" for i in range(n)]

    # Check if index has correct dimension
    if index and len(index) != m:
        index = None

    # Get (or generate) positional codes
    if not position_codes or len(position_codes) != n:
        position_codes = " ".join("c" for i in range(n))
        if index:
            position_codes = "l | " + position_codes

    # Generate table
    with doc.create(Tabularx(position_codes)) as table:

        # Add header
        if not index:
            table.add_row(col_names, mapper=bold)
        else:
            table.add_row([""] + col_names, mapper=bold)
        table.add_hline()
        #table.end_table_header()
        
        # Add data
        for i in range(m):
            if not index:
                table.add_row([data[i,:]])
            else:
                table.add_row([index[i]] + list(data[i,:]))
        table.add_hline()

def build_document(df, stats_dict, viz_path="fig/", doc_name="slurm_report"):

    # Initialize doc
    geometry_options = {"tmargin":"1.5cm", "lmargin":"3cm", "rmargin":"2.5cm", "bmargin":"1.5cm"}
    doc = Document(doc_name, geometry_options=geometry_options)

    # Write title page
    doc.preamble.append(Command("title","Giessen HPC - User Report"))
    doc.preamble.append(Command("author", "We, the Authors"))
    doc.preamble.append(Command("date", NoEscape(r"\today")))
    doc.append(NoEscape(r"\maketitle"))

    with doc.create(Tabular("l l")) as table:
        table.add_row(["Work Group:", df['Account'].values[0]])
        table.add_row(["Time Frame:", f"{df['PeriodStartDate'].values[0]} - {df['PeriodEndDate'].values[0]}"])

    ## INTRODUCTION ##
    with doc.create(Section("Introduction")):

        doc.append("This report provides an overview of the most meaningful values of cluster usage of one work group in a specific time period. \
                It is divided into three parts:")
        
        with doc.create(Itemize()) as itemize:
            itemize.add_item("Section 2 - 'Basic Stats': Number of started and ended tasks in the given time frame")
            itemize.add_item("Section 3 - 'Task Metrics': Task duration, allocated CPUs, and CPU time")
            itemize.add_item("Section 4 - 'Termination Stats': Reasons for task termination")
        
        doc.append("In addition to the entire working group, Sections 2 and 3 also look at the individual users and the selected hardware.\
                The hardware is specified in partitions, which stand for certain parameters under which computing tasks can run. \
                The following partitions exist: serial, short, regular, debug, single, bigmem and long.")

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
                f"A total of {n_over_ten_jobs} user(s) started and ended at least 10 tasks. \
                Only for those users, boxplots are computed in Section 3."
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
                at least 10 tasks. Only for those partitions, boxplots are computed in Section 3."
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
                f"In the full sample, the task durations ranged from \
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
            data_array[:,1] /= 60
            data_array[:,2] /= 60
            data_array = np.round(data_array).astype(int)
            
            # Build table
            with doc.create(Table(position="h!")) as t:
                build_table(doc=doc, data=data_array, col_names=["Allocated CPUs", "Task Duration (min)", "CPU Time"],
                            position_codes="c c c", index=["min", "5quant", "25quant", "median", "75quant", "95quant", "max", "mean"])
                t.add_caption("Task metrics for the full sample.")
                #Label()
            
            # Display plot
            with doc.create(Figure(position="h!")) as fig:
                fig.add_image("fig/task_metrics_full.jpg", width="400px")
                fig.add_caption("Distributions of task duration, allocated CPUs, and CPU time. Whiskers indicate the 5th and 95th percentiles.")  

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
                    if metric_idx == 0:
                        data_array[user_idx,metric_idx+1] = (round(metric_vals[0]), round(metric_vals[-1]), round(metric_vals[-2]))
                    else:
                        data_array[user_idx,metric_idx+1] = (round(metric_vals[0])/60, round(metric_vals[-1]/60), round(metric_vals[-2]/60))

            #print(data_array)
            
            # Build table
            with doc.create(Table(position="h!")) as t:
                build_table(doc=doc, data=data_array, col_names=["Num Jobs", "Allocated CPUs", "Task Duration", "CPU Time"],
                            position_codes="l c c c", index=user_names)
                t.add_caption("Task metrics for different users. Values in parantheses indicate (min, mean, max). Time is measured in seconds.")

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
                    if metric_idx == 0:
                        data_array[partition_idx,metric_idx+1] = (round(metric_vals[0]), round(metric_vals[-1]), round(metric_vals[-2]))
                    else:
                        data_array[partition_idx,metric_idx+1] = (round(metric_vals[0]/60), round(metric_vals[-1]/60), round(metric_vals[-2]/60))

            #print(data_array)
            
            # Build table
            with doc.create(Table(position="h!")) as t:
                build_table(doc=doc, data=data_array, col_names=["Num Jobs", "Allocated CPUs", "Task Duration", "CPU Time"],
                            position_codes="l c c c", index=partition_names)
                t.add_caption("Task metrics for different partitions. Values in parantheses indicate (min, mean, max). Time is measured in seconds.")

            # Show plot
            with doc.create(Figure(position="h!")) as fig:
                fig.add_image("fig/task_metrics_partition_split.jpg", width="350px")
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
