import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import pandas as pd
import numpy as np

def Simulate(start_date, end_date, symbols, allocation):
	# Set up date.
	time_of_day = dt.timedelta(hours=16)
	time_stamps = du.getNYSEdays(start_date, end_date, time_of_day)
	
	# Set up data source and read data.
	data_obj = da.DataAccess('Yahoo')
	keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
	ldf_data = data_obj.get_data(time_stamps, symbols, keys)
	d_data = dict(zip(keys, ldf_data))
	
	# Calculate daily return.
	df_rets = d_data['close'].copy()
	df_rets = df_rets.fillna(method = 'ffill')
	df_rets = df_rets.fillna(method = 'bfill')
	na_rets = df_rets.values
	
	# Calculate portional daily return
	na_rets = na_rets / na_rets[0, :] 	# Need to normalize first.
	na_portional_ret = np.sum(na_rets * allocation, axis = 1)
	tsu.returnize0(na_portional_ret)

	std_return = np.std(na_portional_ret)
	avg_daily_return = np.average(na_portional_ret)
	sharpe_ratio = np.sqrt(252) * avg_daily_return / std_return
	cumulative_return = np.cumprod(na_portional_ret + 1)[-1]
	# Return reresults. 
	return std_return, avg_daily_return, sharpe_ratio, cumulative_return 

def Optimize(start_date, end_date, symbols):
	# Return the best allocation of a portfolio. *best* means highest 
	# Sharpe ratio.
	dt_start = dt.datetime.strptime(start_date, '%Y-%m-%d')
	dt_end = dt.datetime.strptime(end_date, '%Y-%m-%d')
	
	max_sharpe = -100.0
	max_allocation = []
	for aloc_1 in range(0, 11):
		for aloc_2 in range(0, 11 - aloc_1):
			for aloc_3 in range(0, 11 - aloc_1 - aloc_2):
				aloc_4 = 10 - aloc_1 - aloc_2 - aloc_3
				allocation = [aloc_1, aloc_2, aloc_3, aloc_4]
				allocation[:] = [x / 10.0 for x in allocation]
				_, _, sharpe, _ = Simulate(dt_start, dt_end, symbols, allocation)
				if sharpe > max_sharpe:
					max_sharpe = sharpe
					max_allocation = allocation

	return max_sharpe, max_allocation

if __name__ == "__main__":
	print "Done"
