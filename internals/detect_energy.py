from influxdb import InfluxDBClient
from requests.exceptions import ConnectionError
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
import argparse
from statsmodels.tsa.stattools import adfuller, kpss
from scipy import signal
from statsmodels.tsa.seasonal import seasonal_decompose
import datetime

def getClient(host,port) : 
    try : 
        client = InfluxDBClient(host,port)
        return client
    except ConnectionError as e : 
        print("No connection")

def main(host='localhost', port=8086, cont_name=""):    
    # Connect to Influxdb
    client = getClient(host,port)
    # Get databases
    database = "powerapi_formula"
    client.switch_database(database)
    # Query
    query='SELECT "power" FROM "power_consumption" WHERE target = \''+cont_name+'\''
    print(query)
    df = doQuery(client,query);
    

def doQuery(client,query) :
    completed_list=[]
    results = client.query(query)
    for result in results:
        for el in result :
            list = [] 
            list.append(el['time'])
            list.append(el['power'])
            completed_list.append(list)
    
    df = pd.DataFrame(columns=["time","power"],data=completed_list)
    print(df)
    df.to_csv("results2.csv")
    return df


def parse_args():
    """Parse the args from main."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    parser.add_argument('--cont_name', type=str, required=True, help='name of the container to be analyzed')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port, cont_name= args.cont_name)
