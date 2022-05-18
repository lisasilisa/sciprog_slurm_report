from datetime import date
from datetime import datetime


def data_cleaner(dataset, period_start_date:str, period_end_date:str, **slice_params):
    """
    Ausführung der einzelnen Schritte, um Datensatz zu bereinigen
    """
    subset = get_rel_cols(dataset)   
    subset = update_to_consistent_cols_names(subset)
    subset = add_start_and_end_date_cols(subset)
    subset = clean_state_col(subset)
    subset = get_rel_time_data(subset, period_start_date, period_end_date)
    subset = get_rel_data(subset, **slice_params)
    return subset
    

def get_rel_cols(dataset):
    """
    relevante Spalten des Datensatzs definieren
    """
    dataset = dataset[['Account', 'User', 'Partition', 'Start', 'End', 'CPUTime', 'CPUTimeRAW', 'Elapsed',  
                    'ElapsedRaw',  'AllocCPUS', 'Timelimit', 'TimelimitRaw', 'State']]
    return dataset


def get_rel_data(dataset, **slice_params):
    """
    Datensatz auf bestimmte Einträge in Spalten slicen;
    testet auf Gleichheit
    z.B. User, Account
    """
    print('slice_params', slice_params)
    for param, value in slice_params.items():
        dataset = dataset[dataset[param] == value]
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
    start_date_datetime = start_date.apply(lambda x: datetime.strptime(x, "%Y-%m-%d").date())
    #start_day_datetime = datetime.strptime(start_day, "%Y-%m-%d").date()
    dataset.insert(4, 'StartDate', start_date_datetime)
    
    end_date = dataset['End'].str.split('T').str[0]  
    end_date_datetime = end_date.apply(lambda x: datetime.strptime(x, "%Y-%m-%d").date())
    #end_day_datetime = datetime.strptime(end_day, "%Y-%m-%d").date()
    dataset.insert(6, 'EndDate', end_date_datetime)
    
    return dataset
    

def get_rel_time_data(dataset, period_start_date:str, period_end_date:str):
    """ 
    Datensatz auf Einträge slicen, welche innerhalb des Zeitraums angefangen und beendet wurden
    """
    period_start_date_dt = datetime.strptime(period_start_date, "%Y-%m-%d").date() # dt steht für datetime Objekt
    period_end_date_dt = datetime.strptime(period_end_date, "%Y-%m-%d").date()
    dataset = dataset[dataset['StartDate'] >= period_start_date_dt][dataset['EndDate'] <= period_end_date_dt]
    return dataset


def clean_state_col(dataset):
    """
    'CANCELLED by INDEX' Einträge in Spalte State mit CANCELLED abkürzen
    User ID ist nicht von Interesse
    """
    mask = dataset['State'].str.startswith('CANCELLED')
    dataset.loc[mask,'State'] = 'CANCELLED'
    return dataset