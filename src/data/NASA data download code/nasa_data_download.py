import os, sys, time, json, urllib3, requests, multiprocessing
import pandas as pd 
urllib3.disable_warnings()
import yaml
from typing import Dict
from from_root import from_root


        

#desitnation folder to save the data

dest_dir='./data/' 
#file path containing location of Italy lat and lang with city names
locations_file_path ='./it_locations.csv'
#file path for the parameter to dowanlod from NASA website, add or remove parameters from this file 
paramters_file_path = './params.csv'
start_date =  '20220101' #format YYYYMMDD
end_date =  '20220930'   #format YYYYMMDD


def download_function(collection):
    ''' '''

    request, filepath = collection
    response = requests.get(url=request, verify=False, timeout=30.00).json()

    with open(filepath, 'w') as file_object:
        json.dump(response, file_object)




class Process():
    def __init__(self):

        self.processes = 5 # Please do not go more than five concurrent requests.
        # req =  /api/temporal/hourly/point?parameters=WS10M,WD10M,T2MDEW,T2MWET,T2M,V10M,RH2M,PS,PRECTOT,QV2M,U10M&community=SB&longitude=0&latitude=0&start=20170101&end=20170102&format=CSV
        self.request_template = r"https://power.larc.nasa.gov/api/temporal/daily/point?parameters={parameters}&community=AG&longitude={longitude}&latitude={latitude}&start={start_date}&end={end_date}&format=JSON&time-standard=UTC"
        self.filename_template = "{dir}{loc_name}_Lat_{latitude}_Lon_{longitude}.csv"

        self.messages = []
        self.times = {}
        

    def execute(self,dir,locations_file_path,parameters_file_path,start_date,end_date):
        locations = pd.read_csv(locations_file_path)
        parameters = ','.join([x for x in pd.read_csv(parameters_file_path).Param_Code.values.tolist()])
        dir ='./data/'
        Start_Time = time.time()

        # locations = [(39.9373, -83.0485), (10.9373, -50.0485)]

        requests = []
        for idx,row in locations.iterrows():
            loc_name=row['city']
            latitude,longitude=row['lat'], row['lng']
           
        # for latitude, longitude in locations:
            request = self.request_template.format(parameters = parameters,latitude=latitude, longitude=longitude,start_date=start_date,end_date=end_date)
            filename = self.filename_template.format(dir=dir,loc_name=loc_name,latitude=latitude, longitude=longitude)
            requests.append((request, filename))

        requests_total = len(requests)

        pool = multiprocessing.Pool(self.processes)
        x = pool.imap_unordered(download_function, requests)

        for i, df in enumerate(x, 1):
            sys.stderr.write('\rExporting {0:%}'.format(i/requests_total))

        self.times["Total Script"] = round((time.time() - Start_Time), 2)

        print ("\n")
        print ("Total Script Time:", self.times["Total Script"])        


def main():
    os.makedirs(dest_dir, exist_ok=True)

    #Italy city data with lat and lang
    Process().execute(
        dir = dest_dir,
        locations_file_path = locations_file_path,
        parameters_file_path = paramters_file_path, 
        start_date = start_date,
        end_date = end_date)
        


if __name__ == "__main__":
    main()


    
