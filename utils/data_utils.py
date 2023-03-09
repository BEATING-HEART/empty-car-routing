import pandas as pd
from datetime import datetime

COLNAME = [
    'order_id', 
    'driver_id', 
    'passenger_id', 
    'start_district_hash', 
    'dest_district_hash', 
    'price', 
    'time'
]

def read_realdata(
    date: int, start_hour: int, end_hour: int, region_list: list
) -> None:
    
    assert start_hour < end_hour
    file_path = f"./data/order_data_2016-01-{date:02}"
    start =  datetime(2016, 1, date, start_hour)
    end = datetime(2016, 1, date, end_hour)
    
    data = pd.read_csv(
        file_path,
        sep='\t', 
        header=None, 
        names=COLNAME,
        encoding='utf-8-sig',
        parse_dates=['time']
    )
    
    target = data[(data['time'] >= start) & (data['time'] < end)]
    sorted = target.sort_values(by=['time']) 
    return sorted
