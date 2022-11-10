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
from labellines import labelLine, labelLines
import matplotx

plt.rcParams["figure.figsize"] = (30,15)
plt.rcParams['font.size'] =  22

def main() : 

    df = pd.read_csv('case_study/results.csv', parse_dates=['time'])
    df['time'] = pd.to_datetime(df.time).dt.tz_localize(None)
    calls = [["2022/11/10 09:18:50",6.639123623],["2022/11/10 09:19:08",0.001741013],["2022/11/10 09:20:10",0.001470028],["2022/11/10 09:20:11",0.001578345],
    ["2022/11/10 09:20:14",0.001668836],["2022/11/10 09:21:00",0.001809]]
    #for i in range(0,len(calls)) : 
     #   plot_a_call(df,calls[i][0],calls[i][1],"call_"+str(i))
    
    plot_all(calls,df)


def plotTimeSeries(dataframe,title,start,end):
    # Plotting the time series of given dataframe
    plt.cla()
    plt.clf()

    plt.plot(dataframe.time, dataframe.power)

    plt.axvline(start,color="red", linestyle="--",label="serverledge start")
    plt.axvline(end,color="red", linestyle="--",label="serverledge end")

    # Giving title to the chart using plt.title
    plt.title(title)
 
    plt.xticks(rotation=45, ha='right')
 
    # Providing x and y label to the chart
    plt.xlabel('Date')
    plt.ylabel('Power')
   # Put a legend below current axis
    plt.legend()
    matplotx.line_labels()  
    
    plt.savefig("internals/"+title+".png")
    
def plot_a_call(df,event_start,event_duration,title) : 
    start = event_start
    print("\nplot ", title)
    date_start = datetime.datetime.strptime(event_start, '%Y/%m/%d %H:%M:%S')
    date_start_1 = date_start
    end = date_start+datetime.timedelta(seconds=event_duration)
    date_end = date_start+datetime.timedelta(seconds=event_duration+3)
    date_start = date_start+datetime.timedelta(seconds=-1.5)
    data_query = df[(df['time'] >= date_start) & (df['time'] <= date_end)]
    plotTimeSeries(data_query, title,date_start_1,end)


def plot_all(calls,df) : 
    colors = ["blue","green","red","cyan","magenta","yellow","black","white"]
    
    start = calls[0][0]
    end_start=calls[len(calls)-1][0]
    date_start = datetime.datetime.strptime(start, '%Y/%m/%d %H:%M:%S')
    date_end = datetime.datetime.strptime(end_start, '%Y/%m/%d %H:%M:%S')
    end_end=calls[len(calls)-1][1] 
    end = date_end+datetime.timedelta(seconds=end_end)
    data_query = df[(df['time'] >= date_start) & (df['time'] <= end)]

     # Plotting the time series of given dataframe
    plt.cla()
    plt.clf()

    plt.plot(data_query.time, data_query.power)

    plt.axvline(date_start,color="red", linestyle="--",label="serverledge start")
    plt.axvline(end,color="red", linestyle="--",label="serverledge end")

    for i in range(0,len(calls)): 
         start = calls[i][0]
         end=calls[i][1]
         date_start = datetime.datetime.strptime(start, '%Y/%m/%d %H:%M:%S')
         date_end = date_start+datetime.timedelta(seconds=end)
         plt.axvline(date_start,color=colors[i], linestyle="--",label=str(i)+"_start")
         plt.axvline(date_end,color=colors[i], linestyle="--",label=str(i)+"_end")

    plt.title("all calls")
 
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Date')
    plt.ylabel('Power')
    plt.legend(bbox_to_anchor=(1, 1), loc="upper left")
   
    plt.savefig("internals/"+"all_calls"+".png")









   
if __name__ == '__main__':
    main() 