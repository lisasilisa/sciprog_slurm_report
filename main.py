from data_cleaner import data_cleaner
import pandas as pd
import numpy as np


def main():
    dataset = pd.read_csv("slurmaccountdata_2020-01-01T00_00_00-2022-03-31T23_59_59_processed.csv",sep="|", index_col=0)
    cleaned_dataset = data_cleaner(dataset, account='59628c0f-aa89-4a69-bc2c-cb789395022f', period_start_date ='2020-02-14', period_end_date='2020-02-18') # Beispieldaten
    print(cleaned_dataset[['Account', 'StartDate', 'EndDate']])

if __name__ == "__main__":
    main()
