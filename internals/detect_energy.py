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
    plotTimeSeries(df)

def doQuery(client,query) :
    completed_list=[]
    results = client.query(query)
    for result in results:
        for el in result :
            list = [] 
            list.append(el['time'].split("T")[1])
            list.append(el['power'])
            completed_list.append(list)
    
    df = pd.DataFrame(columns=["time","power"],data=completed_list)
    print(df)
    df.to_csv("results.csv")
    return df

def plotDetrend(df) : 
    # Time Series Decomposition
    result_mul = seasonal_decompose(df['power'], model='multiplicative', extrapolate_trend='freq')

    # Deseasonalize
    deseasonalized = df.power.values / result_mul.seasonal

    plt.savefig("deseasonalized.png")
    
def statTest(df) : 
    # ADF Test
    result = adfuller(df.power.values, autolag='AIC')
    print(f'ADF Statistic: {result[0]}')
    print(f'p-value: {result[1]}')
    for key, value in result[4].items():
        print('Critial Values:')
        print(f'   {key}, {value}')

    # KPSS Test
    result = kpss(df.power.values, regression='c')
    print('\nKPSS Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    for key, value in result[3].items():
        print('Critial Values:')
        print(f'   {key}, {value}')

def plotTimeSeries(dataframe):
    # Plotting the time series of given dataframe
    plt.plot(dataframe.time, dataframe.power)
 
    # Giving title to the chart using plt.title
    plt.title('Power by Date')
 
    plt.xticks(rotation=30, ha='right')
 
    # Providing x and y label to the chart
    plt.xlabel('Date')
    plt.ylabel('Power')
    
    plt.savefig("query.png")
   

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
