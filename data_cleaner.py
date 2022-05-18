import pandas as pd
from datetime import date
from datetime import datetime


def data_cleaner(dataset, account:str, period_start_date:str, period_end_date:str):
    """
    Ausführung der einzelnen Schritte, um Datensatz zu bereinigen
    """
    subset = get_rel_cols(dataset) 
    subset = update_to_consistent_cols_names(subset)
    subset = add_start_and_end_date_cols(subset)
    subset = clean_state_col(subset)
    subset = get_rel_time_data(subset, period_start_date, period_end_date)
    subset = get_account_data(subset, account)
    return subset


def get_rel_cols(dataset):
    """
    relevante Spalten des Datensatzs definieren
    """
    dataset = dataset[['Account', 'User', 'Partition', 'Start', 'End', 'CPUTime', 'CPUTimeRAW', 'Elapsed',  
                    'ElapsedRaw',  'AllocCPUS', 'State']]
    return dataset


def get_account_data(dataset, account):
    """
    Datenset nach Arbeitsgruppe vorslicen
    """
    dataset = dataset[dataset['Account'] == account]
    return dataset


def update_to_consistent_cols_names(dataset):
    """
    Spaltennamen konsistent benennen, z.B. immer Raw anstatt RAW
    """
    dataset = dataset.rename(columns = {'CPUTimeRAW':'CPUTimeRaw'})
    return dataset
    

def add_start_and_end_date_cols(dataset):
    """
    Spalten hinzufügen, welche Start und Endtag als datetime Objekte enthalten
    """
    start_date = dataset['Start'].str.split('T').str[0]  

    start_date_datetime = pd.to_datetime(start_date)
    dataset.insert(4, 'StartDate', start_date_datetime)
    
    end_date = dataset['End'].str.split('T').str[0]  
    end_date_datetime = pd.to_datetime(end_date)
    dataset.insert(6, 'EndDate', end_date_datetime)
    
    return dataset
    

def get_rel_time_data(dataset, period_start_date:str, period_end_date:str):
    """ 
    Datensatz auf Einträge slicen, welche innerhalb des Zeitraums angefangen oder beendet wurden
    """
    period_start_date_dt = pd.to_datetime(period_start_date)
    period_end_date_dt = pd.to_datetime(period_end_date)

    subset = dataset[(dataset['StartDate'] < period_start_date_dt) | (dataset['StartDate'] > period_end_date_dt)] # Aufträge die nicht in Zeitspanne starten
    subset = subset[(subset['EndDate'] < period_start_date_dt) | (subset['EndDate'] > period_end_date_dt)] # Aufträge die zusätzlich auch nicht in Zeitspanne enden
    dataset = dataset[~dataset.index.isin(subset.index)] # alle Aufträge außer denen die weder in Zeitspanne anfangen oder enden 


    return dataset


def clean_state_col(dataset):
    """
    'CANCELLED by INDEX' Einträge in Spalte State mit CANCELLED abkürzen
    User ID ist nicht von Interesse
    """
    mask = dataset['State'].str.startswith('CANCELLED')
    dataset.loc[mask,'State'] = 'CANCELLED'
    return dataset