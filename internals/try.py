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
from sklearn.metrics import r2_score, median_absolute_error, mean_absolute_error
from sklearn.metrics import median_absolute_error, mean_squared_error, mean_squared_log_error
import ruptures as rpt
plt.style.use('fivethirtyeight')
plt.rcParams["figure.figsize"] = (30,20)
plt.rcParams['font.size'] =  20
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Ubuntu Mono'
plt.rcParams['figure.titlesize'] = 24
import warnings
warnings.filterwarnings('ignore')
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

def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def plotTimeSeries(dataframe,title,start,end):
    plt.cla()
    plt.clf()
    fig, axs = plt.subplots(2)
    fig.suptitle(title)
    axs[0].plot(dataframe.time, dataframe.power, label='power')
    axs[0].axvline(start,color="gray", linestyle=":",label="serverledge start")
    axs[0].axvline(end,color="gray", linestyle=":",label="serverledge end") 
    axs[0].plot(dataframe.time,dataframe['power'].rolling(2).mean(),label='rolling_mean',color='green')
    axs[0].set_title("power model")
    axs[0].set_xlabel(xlabel='Date', ha='right')
    axs[0].set_ylabel('Power')
    axs[1].plot(dataframe.time, dataframe['power'].cumsum(skipna=False),  label='Cum sum')
    axs[1].set_title("Cumulative sum of power")
    axs[1].set_xlabel(xlabel='Date', ha='right')
    axs[1].set_ylabel('Cumulative power')
    scale=1.96
    rolling_mean = dataframe['power'].rolling(window=2).mean()
    mae = mean_absolute_error(dataframe['power'][2:], rolling_mean[2:])
    deviation = np.std(dataframe['power'][1:] - rolling_mean[2:])
    lower_bound = rolling_mean - (mae + scale * deviation)
    upper_bound = rolling_mean + (mae + scale * deviation)
    axs[0].plot(dataframe.time,upper_bound, 'r--', label='Upper bound / Lower bound')
    axs[0].plot(dataframe.time,lower_bound, 'r--')
    axs[0].legend()
    axs[1].legend()
    plt.savefig("internals/"+title+".png")
    '''

     #Convert the time series values to a numpy 1D array
    points=np.array(dataframe['power'])
    print(points)
    #Changepoint detection with dynamic programming search method
    algo = rpt.Pelt(model="rbf").fit(points)
    my_bkps = algo.predict(pen=1)
    rpt.show.display(points, my_bkps,figsize=(10,10))
    plt.title('Change Point Detection: Pelt Search Search Method :'+ title)
    plt.savefig("internals/cp_"+title+".png")
   '''
    
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
    axs[0].set_xlabel(xlabel='Date', ha='right')
    axs[0].set_ylabel('Power')
    axs[1].plot(dataframe.time, dataframe['power'].cumsum(skipna=False),  label='Cum sum')
    axs[1].set_title("Cumulative sum of power")
    axs[0].plot(dataframe.time,dataframe['power'].rolling(2).mean(),label='rolling_mean',color='green')
    axs[0].legend()
    axs[1].legend()
    axs[1].set_xlabel(xlabel='Date', ha='right')
    axs[1].set_ylabel('Cumulative power')
    plt.savefig("internals/all.png")
    plt.cla()
    plt.clf()
    '''
    #Convert the time series values to a numpy 1D array
    points=np.array(dataframe['power'])
    #Changepoint detection with dynamic programming search method
    model = "l2"  
    algo = rpt.Window(width=40, model=model).fit(points)
    my_bkps = algo.predict(n_bkps=15)
    rpt.show.display(points, my_bkps, figsize=(10, 6))
    plt.savefig("internals/cp_all.png")
    for i in my_bkps:
        print(dataframe.iloc[i-1])
    '''

    


  

    

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
