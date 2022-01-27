"""
    row : {
        "vehicle_id": {
            #[(time,[1,2,3,4,5]),(t2,latency).....]
            time : []
            }
    }
"""
import re 
from datetime import datetime


REGEX = "\[(?:\d|\:|\-)+ ((?:\d|\:|\.|\-| )+)\]  \[\_\_agents\.ue\_tasks\.py\_\_\]  \[INFO\] - Task UECam Agent ue\_(\d) / Message recieved \: \{\"ue\"\: (\d)\, \"time\"\: \"((?:\d|\:|\.)+)\".*"

data = {}

diff = lambda r,s: (datetime.strptime(r,'%H:%M:%S.%f') - datetime.strptime(s,'%H:%M:%S.%f')).total_seconds() * 1000
with open("SIM-01-26-2022-15:29.log") as infile:
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
                
               
print(data['3']['15:30:32.378200'])
        