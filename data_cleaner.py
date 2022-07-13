import pandas as pd
from datetime import date
from datetime import datetime, timedelta

"""
Cleans dataframe and prepare for further processing (e.g. to extracts stats)
-- -- -- -- -- -- -- -- -- -- -- -- -- -- --
IN: dataframe
OUT: cleaned dataframe
"""

def data_cleaner(dataset: pd.DataFrame, account:str, period_start_date:str, period_end_date:str):
    """
    Execution of the individual steps to clean up the dataframe:
        * get relevant columns
        * update to consistent column names
        * get start and end days of tasks from timestamps and add them as new columns
        * clean column 'State' to have consistent terminations reasons
        * filter out data to get tasks which start or/and end in period
        * add period start and end days as new columns to filtered data
        * filter out data from one account
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Arguments:
    dataset: pd.DataFrame
    period_start_date: str; format='yyyy-mm-dd'
    period_end_date: str; format='yyyy-mm-dd'
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Returns:
    dataset: pd.DataFrame
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    """
    subset = get_rel_cols(dataset) 
    subset = update_to_consistent_cols_names(subset)
    subset = add_start_and_end_date_cols(subset)
    subset = clean_state_col(subset)
    subset = get_rel_time_data(subset, period_start_date, period_end_date)
    subset = add_per_start_and_end_date_cols(subset, period_start_date, period_end_date)
    subset = get_account_data(subset, account)
    return subset


def get_rel_cols(dataset: pd.DataFrame):
    """
    Define relevant columns of the dataframe
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Arguments:
    dataset: pd.DataFrame
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Returns:
    dataset: pd.DataFrame
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    """
    dataset = dataset[['Account', 'User', 'Partition', 'Start', 'End', 'CPUTime', 'CPUTimeRAW', 'Elapsed',  
                    'ElapsedRaw',  'AllocCPUS', 'State']]
    return dataset


def get_account_data(dataset: pd.DataFrame, account: str):
    """
    Filter out data from one account
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Arguments:
    dataset: pd.DataFrame
    account: str
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Returns:
    dataset: pd.DataFrame
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    """
    dataset = dataset[dataset['Account'] == account]
    return dataset


def update_to_consistent_cols_names(dataset: pd.DataFrame):
    """
    Name columns consistently, e.g. always Raw instead of RAW
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Arguments:
    dataset: pd.DataFrame
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Returns:
    dataset: pd.DataFrame
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    """
    dataset = dataset.rename(columns = {'CPUTimeRAW':'CPUTimeRaw'})
    return dataset
    

def add_start_and_end_date_cols(dataset: pd.DataFrame):
    """
    Add columns containing start and end days of tasks as datetime objects
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Arguments:
    dataset: pd.DataFrame
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Returns:
    dataset: pd.DataFrame
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    """
    start_date = dataset['Start'].str.split('T').str[0]  
    start_date_datetime = pd.to_datetime(start_date)
    dataset.insert(4, 'StartDate', start_date_datetime)
     
    end_date = dataset['End'].str.split('T').str[0]  
    end_date_datetime = pd.to_datetime(end_date)
    dataset.insert(6, 'EndDate', end_date_datetime)
    
    return dataset

def add_per_start_and_end_date_cols(dataset: pd.DataFrame, period_start_date:str, period_end_date:str):
    """
    Add columns for period start and end days and fill whole columns with the passing string values
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Arguments:
    dataset: pd.DataFrame
    period_start_date: str
    period_end_date: str
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Returns:
    dataset: pd.DataFrame
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    """
    dataset.insert(5, 'PeriodStartDate', period_start_date)
    dataset.insert(8, 'PeriodEndDate', period_end_date)
    return dataset

    

def get_rel_time_data(dataset: pd.DataFrame, period_start_date:str, period_end_date:str):
    """ 
    Filter out data to get tasks which start or/and end in period
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Arguments:
    dataset: pd.DataFrame
    period_start_date: str
    period_end_date: str
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Returns:
    dataset: pd.DataFrame
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    """
    period_start_date_dt = pd.to_datetime(period_start_date)
    period_end_date_dt = pd.to_datetime(period_end_date)

    subset = dataset[(dataset['StartDate'] < period_start_date_dt) | (dataset['StartDate'] >= period_end_date_dt + timedelta(days=1))] # tasks that do not start in period
    subset = subset[(subset['EndDate'] < period_start_date_dt) | (subset['EndDate'] >= period_end_date_dt + timedelta(days=1))] # tasks that additionally also do not end in period
    dataset = dataset[~dataset.index.isin(subset.index)] # all tasks except those that neither start nor end in period

    return dataset


def clean_state_col(dataset: pd.DataFrame):
    """
    Replace 'CANCELLED by INDEX' entries in column State with 'CANCELLED'
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Arguments:
    dataset: pd.DataFrame
    period_start_date: str
    period_end_date: str
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Returns:
    dataset: pd.DataFrame
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    """
    mask = dataset['State'].str.startswith('CANCELLED')
    dataset.loc[mask,'State'] = 'CANCELLED'
    return dataset