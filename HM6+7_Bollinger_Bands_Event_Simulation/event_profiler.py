'''
(c) 2011, 2012 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on January, 23, 2013

@author: Sourabh Bajaj
@contact: sourabhbajaj@gatech.edu
@summary: Event Profiler Tutorial
'''


import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""

event_threshold = 10.0
window = 20

def find_events(ls_symbols, d_data):
    ''' Finding the event dataframe '''
    df_close = d_data['close']

    print "Finding Events"

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index


    # Generate Bollinger Bands for all symbols:
    rolling_mean = pd.rolling_mean(df_close, window, min_periods=1)
    rolling_std = pd.rolling_std(df_close, window)
    upper_bound = rolling_mean + rolling_std
    lower_bound = rolling_mean - rolling_std
    values = (df_close - rolling_mean) / rolling_std


    f = open("data/event_orders.csv", "w")
    count = 0
    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            yesterday_value = values[s_sym].ix[ldt_timestamps[i-1]]
            today_value = values[s_sym].ix[ldt_timestamps[i]]
            today_value_spy = values['SPY'].ix[ldt_timestamps[i]]

            if yesterday_value >= -2.0 and today_value <= -2.0 and today_value_spy >= 1.4:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1
                count += 1
               
                if i+5 < len(ldt_timestamps):
                    buy_order = ldt_timestamps[i].to_datetime().strftime("%Y, %m, %d") +  ", " +  s_sym + ', BUY, ' + str(100)
                    sell_order = ldt_timestamps[i+5].to_datetime().strftime("%Y, %m, %d") +  ", " +  s_sym + ', SELL, ' + str(100)
                    f.write(buy_order + '\n')
                    f.write(sell_order + '\n')
    print count
    return df_events


if __name__ == '__main__':
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31, 16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')

    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_events = find_events(ls_symbols, d_data)
    print "Creating Study"
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                s_filename='data/MyEventStudy_symbol_2012.pdf', b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')
