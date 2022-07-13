# 1. Project Summary
This tool generates usage reports for users of the justHPC high-performance-computing cluster of the University of Gießen. Any account can request a usage report for a given time frame. This report summarizes the number of tasks performed and gives insights into task durations and CPU usage as well as into the reasons for task terminations. If multiple users were active, most metrics are also reported for each individual user. In the same way, metrics are reported for different computation partitions which were used to process tasks. The report is based on a specific dataset which can be queried by the justHPC team. From this dataset, a pdf report with text, visualizations, and tables is generated and exported.
# 2. Requirements
In order to run this tool, we recommend you to install Python 3.9.7 as well as these libraries:
* numpy 1.20.0
* pandas 1.3.4
* pylatex 1.4.1
* matplotlib 3.4.3

However, conflicts are unlikely to emerge even with slightly older or newer versions of Python or any of the libraries. <br>

Because the report is generated using LaTeX, we recommend to install the TeX distribution [TeX Live](https://www.tug.org/texlive/). Other TeX distributions like [MiKTeX](https://miktex.org/) may also work, but were not tested.

# 3. Modular Structure
The data pipeline was implemented by setting up the code in a modular way:

dataset &rarr; Data Cleaner - Stats Extractor - Data Visualizer - Document Builder &rarr; PDF-report.

Each module represents a part of the functionality of the program. This design decision makes it easy to extend the individual modules.

## 3.1. Data Cleaner
The Data Cleaner gets the dump of the database as input. This dataset is cleaned up so that it contains only the content needed for further processing. The cleanup includes: getting relevant columns, updating to consistent column names, generalizing termination reasons, converting time information as well as filtering after one account and for a specific time period. These operations result in a subset of the dataset which is passed to the Stats Extractor.

## 3.2. Stats Extractor
The Stats Extractor computes all statistics needed for the report (e.g. for tables and visualizations) from the passing cleaned dataset. Those statistics are stored in a dictionary, which consits of three parts: the first one contains the statistics for the whole work group (account), the second for the individual users of the work group (user_split), the third for the used partitions (partition_split). The statistics itself can be devided in basic_stats, task_metrics and termination_stats. Basic_stats contains the information about the number of tasks, task_metrics the metrics of the CPU usage and termination_stats the termination reasons. The dictionary is gradually filled with the parts and these parts in turn with the statistics. This allows you to omit the parts that are not needed. If there are less than two users then the second part (user_split) is skipped. The same applies to the partitions. The finished dictionary is given to the Data Visualizer.

## 3.3. Data Visualizer
The Data Visualizer scanns the passed dictionary and creates visualizations depending on which parts are contained in the dictionary. In order to obtain consistent images, general parameters are defined in the plot_config file. These include the color scheme, as well as font sizes, etc. Using the values from basic_stats, bar plots are generated for the started and finished jobs. For the work group there is only one started and one ended bar in the plot, for the user_split/partition_split there are started and ended bars for each user/partition. From the values of task_metrics boxplots are created for each attribute of CPU usage (Allocated CPUs, Task Duration, CPU Time). In this case we need a multi-plot-frame, because the attributes have different value ranges. Those axes can be shared for multiple users/partitions for the user_split/partition_split. A donut chart is created for the termination reasons from the termination_stats. All created images are stored in a folder called fig. The Document Builder can access them when it creates the document.

## 3.4. Document Builder

# 4. Usage

# 5. Example
# 6. License