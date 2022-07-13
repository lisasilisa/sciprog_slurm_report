"""
Notes:
- make sure visualization path exists (i.e. fig/)
"""

from data_cleaner import data_cleaner
from stats_extractor import StatsExtractor
from data_visualizer import DataVisualizer
from document_builder import build_document
from plot_config import set_plot_config

import pandas as pd
import numpy as np

import json
import os


DATASET_PATH = "../dataset/slurmaccountdata/slurmaccountdata_shortened.csv"
#ACCOUNT_NAME = "59628c0f-aa89-4a69"
ACCOUNT_NAME = "627bc058-c28d-4680"
START_DATE = "2021-08-01"
END_DATE = "2021-08-31"

def main():

    print("... loading dataset ... (1/5)")
    dataset = pd.read_csv(DATASET_PATH,sep="|", index_col=0)

    print("... cleaning dataset ... (2/5)")
    cleaned_dataset = data_cleaner(dataset, account=ACCOUNT_NAME, period_start_date =START_DATE, period_end_date=END_DATE) # Beispieldaten
    #cleaned_dataset.to_csv("dev_df.csv", index=False)

    if len(cleaned_dataset) == 0:
        print("No tasks for this account were recorded in the given time frame.")
        return

    print("... extracting stats ... (3/5)")
    S = StatsExtractor(cleaned_dataset)
    stats_dict = S.extract_stats()
    #print(stats_dict)

    print("... creating visualizations ... (4/5)")
    if not os.path.isdir("./fig"):
        os.mkdir("./fig/")
        
    Viz = DataVisualizer(stats_dict, set_plot_config())
    Viz.plot_all()

    print("... building document ... (5/5)")
    with open("doc_config.json", "r") as file:
        doc_config = json.load(file)
    build_document(cleaned_dataset, stats_dict, doc_config)
    
    print("... report finished ...")

if __name__ == "__main__":
    main()
