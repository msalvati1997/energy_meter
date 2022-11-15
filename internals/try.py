import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
import argparse
from statsmodels.tsa.stattools import adfuller, kpss
from scipy import signal
from statsmodels.tsa.seasonal import seasonal_decompose
from labellines import labelLine, labelLines
import matplotx
from peak_detection import *
import pylab

plt.rcParams["figure.figsize"] = (30,20)
plt.rcParams['font.size'] =  12

def main() : 
    df = pd.read_csv('case_study/results.csv', parse_dates=['time'])
    df['time'] = pd.to_datetime(df.time).dt.tz_localize(None)
    calls = [
    ["09:18:50",6.639123623], #START # DURATION
    ["09:19:08",0.001741013],
    ["09:20:10",0.001470028],
    ["09:20:11",0.001578345],
    ["09:20:14",0.001668836],
    ["09:21:00",0.001809],
    ]
    for i in range(0,len(calls)) : 
        plot_a_call(df,calls[i][0],calls[i][1],"call_"+str(i))
    plot_all(df)


def plotTimeSeries(dataframe,title,start,end):
    
    plt.cla()
    plt.clf()
    fig, axs = plt.subplots(2)
    fig.suptitle(title)
    axs[0].plot(dataframe.time, dataframe.power, label='power')
    axs[0].axvline(start,color="red", linestyle="--",label="serverledge start")
    axs[0].axvline(end,color="red", linestyle="--",label="serverledge end")
    axs[0].set_title("power model")
    axs[0].set_xlabel(xlabel='Date', rotation=45, ha='right')
    axs[0].set_ylabel('Power')
    axs[1].plot(dataframe.time, dataframe['power'].cumsum(skipna=False),  label='Cum sum')
    axs[1].set_title("Cumulative sum of power")
    axs[0].legend()
    
    plt.savefig("internals/"+title+".png")
  
    
def plot_a_call(df,event_start,event_duration,title) : 
    print("\nplot ", title)
    date_start = pd.to_datetime(event_start).tz_localize(None)
    date_end = date_start+datetime.timedelta(seconds=event_duration+2.5)
    date_start = date_start+datetime.timedelta(seconds=-0.5)
    data_query = df[(df['time'] >= date_start) & (df['time'] <= date_end)]
    start = date_start+datetime.timedelta(seconds=0.6)
    end = start+datetime.timedelta(seconds=event_duration+0.6)
    plotTimeSeries(data_query, title,start,end)


def plot_all(dataframe) : 
    plt.cla()
    plt.clf()
    fig, axs = plt.subplots(2)
    fig.suptitle("all")
    axs[0].plot(dataframe.time, dataframe.power, label='power')
    axs[0].set_title("power model")
    axs[0].set_xlabel(xlabel='Date', rotation=45, ha='right')
    axs[0].set_ylabel('Power')
    axs[1].plot(dataframe.time, dataframe['power'].cumsum(skipna=False),  label='Cum sum')
    axs[1].set_title("Cumulative sum of power")
    axs[0].legend()
    plt.savefig("internals/all.png")


    

def plot_peaks(y,lag,threshold,influence,title) : 
    result = thresholding_algo(y, lag=lag, threshold=threshold, influence=influence)
    pylab.subplot(211)
    pylab.plot(np.arange(1, len(y)+1), y)
    pylab.plot(np.arange(1, len(y)+1),
            result["avgFilter"], color="cyan", lw=2)
    pylab.plot(np.arange(1, len(y)+1),
            result["avgFilter"] + threshold * result["stdFilter"], color="green", lw=2)
    pylab.plot(np.arange(1, len(y)+1),
            result["avgFilter"] - threshold * result["stdFilter"], color="green", lw=2)
    pylab.subplot(212)
    pylab.step(np.arange(1, len(y)+1), result["signals"], color="red", lw=2)
    pylab.ylim(-1.5, 1.5)
    pylab.title(title)
    pylab.savefig("internals/"+title+"peaks.png")

   
if __name__ == '__main__':
    main()
