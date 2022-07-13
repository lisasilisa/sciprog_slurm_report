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

Dataset &rarr; Data Cleaner - Stats Extractor - Data Visualizer - Document Builder &rarr; PDF-report.

Each module represents a part of the functionality of the program. This design decision makes it easy to extend the individual modules.

## 3.1. Data Cleaner
The ```DataCleaner``` gets the dump of the database as input. This dataset is cleaned up so that it contains only the content needed for further processing. The cleanup includes: getting relevant columns, updating to consistent column names, generalizing termination reasons, converting time information as well as filtering by account and time period. These operations result in a subset of the dataset which is passed to the Stats Extractor. <br>
```data_cleaner.py``` implements no class, but the following functions:
* ```data_cleaner```(_dataset_: pd.DataFrame, _account_: str, _period_start_date_: str, _period_end_date_: str) $\rightarrow$ pd.DataFrame
    * Calls all of the following sub functions to perform a full clean of the dataset:
* ```get_rel_cols```(_dataset_: pd.DataFrame) $\rightarrow$ pd.DataFrame
* ```get_account_data```(_dataset_: pd.DataFrame, _account_: str) $\rightarrow$ pd.DataFrame
* ```update_to_consistent_col_names```(_dataset_: pd.DataFrame) $\rightarrow$ pd.DataFrame
* ```add_start_and_end_date_cols```(_dataset_: pd.DataFrame) $\rightarrow$ pd.DataFrame
* ```get_rel_time_data```(_dataset_: pd.DataFrame, _period_start_date_: str, _period_end_date_: str) $\rightarrow$ pd.DataFrame
* ```clean_state_col```(_dataset_: pd.DataFrame) $\rightarrow$ pd.DataFrame

## 3.2. Stats Extractor
The ```StatsExtractor``` computes all statistics needed for the report (e.g. for tables and visualizations) based on the cleaned dataset. Those statistics are stored in a dictionary, which consits of three parts: the first one contains the statistics for the whole work group (_account_), the second for the individual users of the work group (_user_split_), the third for the used partitions (_partition_split_). The statistics can be divided in _basic_stats_, _task_metrics_, and _termination_stats_. Basic_stats contain the information about the number of tasks, task_metrics the metrics of the CPU usage and termination_stats the termination reasons. The dictionary is gradually filled with the parts and these parts in turn with the statistics. This allows you to omit the parts that are not needed. If there are less than two users then the second part (user_split) is skipped. The same applies to the partitions. The finished dictionary is passed to the Data Visualizer. An schematic overview of the stats dictionary can be found in the ```StatsExtractor```'s module docstring.<br>
```stats_extractor.py``` includes a class ```StatsExtractor``` with the following methods:
* ```__init__```(_self_, _df_: pd.DataFrame) $\rightarrow$ None
* ```extract_stats```(_self_) $\rightarrow$ dict
    * Calls all of the following sub methods to build the full stats_dict:
* ```get_basic_stats```(_self_, _split_: str) $\rightarrow$ dict
* ```get_task_metrics```(_self_, _split_: str) $\rightarrow$ dict
* ```get_termination_stats```(_self_) $\rightarrow$ dict

## 3.3. Data Visualizer
The ```DataVisualizer``` reads the passed stats dictionary and creates visualizations depending on which parts are contained in the dictionary. In order to obtain consistent images, general parameters are defined in the ```plot_config.py``` file. These include the color scheme, as well as font sizes, etc. Using the values from basic_stats, bar plots are generated for the started and finished jobs. For the work group there is only one started and one ended bar in the plot, for the user_split/partition_split there are started and ended bars for each user/partition. From the values of task_metrics boxplots are created for each attribute of CPU usage (Allocated CPUs, Task Duration, CPU Time). In this case we need a multi-plot-frame, because the attributes have different value ranges. Those axes can be shared for multiple users/partitions for the user_split/partition_split. A donut chart is created for the termination reasons from the termination_stats. All created images are stored in a folder called ```fig/```. The ```DocumentBuilder``` can access them when it creates the document. <br>
```data_visualizer.py``` implements a ```DataVisualizer``` class with the following methods:
* ```__init```(_self_, _stats_dict_: dict, _plot_config_: dict)
    * Takes the stats_dict generated with ```StatsExtractor``` and the plot_config generated with ```plot_config.py``` as arguments.
* ```plot_all```(_self_)
    * Calls the appropriate sub methods to generate a suitable set of visualizations for a given request.
* ```plot_basic_stats```(_self_, _split_: str, _export_path_: str)
* ```plot_task_metrics```(_self_, _split_: str, _export_path_: str)
* ```plot_termination_stats```)(_self_, _export_path_: str)
<br>

```plot_config.py``` implements ```set_plot_config```() which generates a dictionary which can be used an an input argument for the initialization of a DataVisualizer object.


## 3.4. Document Builder
The ```document_builder.py``` creates a pdf report based on the stats extracted, the visualizations generated, and a ```doc_config.json``` which holds information like margin sizes, author, and title. Using the ```pylatex```library, a LaTeX report is generated. The Document Builder's job is to present the extracted stats in tables, figures, and short paragraphs, and to structure them into sections and subsections.<br>

```document_builder.py``` does not contain a class, but two methods:
* ```build_table```(_doc_: pylatex.Document, _data_: np.ndarray, _col_names_: list, _index_: list, _position_codes_: list) $\rightarrow$ None
    * Transforms a 2D numpy array into a LaTeX table and adds it to the document.
* ```build_document```(_df_: pd.DataFrame, _stats_dict_: dict, _doc_config_: dict) $\rightarrow$ None
    * Builds the full pdf report with text, tables, and figures.


# 4. Usage

Please use ```main.py``` to generate reports. There, please assign the following variables to match your specific request:
* ```DATASET_PATH```: str; path to input csv file
* ```ACCOUNT_NAME```: str; name of account requesting report
* ```START_DATE```: str; begin of time frame to consider; format: YYYY-MM-DD
* ```END_DATE```: str; end of time frame to consider; format: YYYY-MM--DD
<br>

From there on, the report is generated in 5 steps:
1. load dataset
2. clean dataset
3. extract stats
4. create visualizations
5. build document
<br>

If you want to write your own main script, please consider that ```main.py``` does not only call the modules in the appropriate order, but includes two important checks:
1. If the cleaned dataset has no entries, the script is terminated and the user is informed through a console output.
2. Is is ensured that the ```fig/``` directory is available, since this location is hard-coded. 

# 5. Example

Please find an example report named ```my_report.pdf``` in the ```example/``` directory of this repository. It was generated for the user name "627bc058-c28d-4680" (anonymized) and the date range ["2021-08-01", "2021-08-31"].

# 6. Credit

This project, including the design and implementation of all its source code, was built by Lisa Soboth and Max Hilsdorf for a study project in their bachelor's program in Data Science at University of Giessen, GER. The project was supervised by Philipp Risius and Marcel Giar.