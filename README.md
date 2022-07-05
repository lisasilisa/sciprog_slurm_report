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
## 3.1. Data Cleaner
## 3.2. Stats Extractor
## 3.3. Data Visualizer
## 3.4. Document Builder
# 4. Usage
# 5. Example
# 6. License