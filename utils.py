import re 
from datetime import datetime
import pandas as pd
import numpy as np

diff = lambda r,s: (datetime.strptime(r,'%H:%M:%S.%f') - datetime.strptime(s,'%H:%M:%S.%f')).total_seconds() * 1000

def prepare_data(path):
    REGEX = "\[(?:\d|\:|\-)+ ((?:\d|\:|\.|\-| )+)\]  \[\_\_agents\.ue\_tasks\.py\_\_\]  \[INFO\] - Task UECam Agent ue\_(\d) / Message recieved \: \{\"ue\"\: (\d)\, \"time\"\: \"((?:\d|\:|\.)+)\".*"

    data = {}

    
    with open(path) as infile:
        for line in infile:
            r = re.match(REGEX,line)
            if r:            
                reception_time,ue_reciever,ue_sender,sending_time = r.group(1,2,3,4)
                if(ue_sender != ue_reciever):
                    if not ue_sender in data.keys():
                        data[ue_sender]={}
                    if not (sending_time in data[ue_sender].keys()):
                        data[ue_sender][sending_time]=[]
                    data[ue_sender][sending_time].append(diff(reception_time,sending_time))
    return data
def e2e_latency_by_ue(data,ue):
    current = np.array([])
    for t in data[ue].keys():
        current = np.append(current,data[ue][t])
    
    return pd.DataFrame({ue:current})

def e2e_latency_all_ue(data):
    dataframe=pd.DataFrame()
    for ue in data.keys():
        dataframe = dataframe.append(e2e_latency_by_ue(data,ue))
    return dataframe
def e2e_latency(data):
    latencies = np.array([])
    for ue in data.keys():
        for t in data[ue].keys():
            latencies = np.append(latencies,data[ue][t])
    return pd.DataFrame({"latency":latencies})

def update_delay(data,ue):
    date_format = '%H:%M:%S.%f'
    to_date = lambda x : datetime.strptime(x, date_format)
    times = list(data[ue].keys())
    times = sorted(list(map(to_date,times)))
    ud=[]
    for i in range(1,len(times)):
        
        ud.append((times[i]-times[i-1]).total_seconds() * 1000)
    return ud
