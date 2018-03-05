import sys
import datetime as dt
import numpy as np

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu


class Analyzer():
  def __init__(self, value_file, benchmark_symbol):
    self.value_data = self._parse_value(value_file) # list of [datetime, equity]
    self.start_date = self.value_data[0][0]
    self.end_date = self.value_data[-1][0]
    self.benchmark_symbol = benchmark_symbol


  def Run(self):
    # Read equity and benchamark.
    equity_return = np.array(map(lambda x: x[1], self.value_data))
    ldt_timestamps = du.getNYSEdays(self.start_date, self.end_date + dt.timedelta(days=1), 
                                    dt.timedelta(hours=16))
    dataobj = da.DataAccess('Yahoo')
    ldf_data = dataobj.get_data(ldt_timestamps, [self.benchmark_symbol], ["close"])
    d_data = dict(zip(["close"], ldf_data))
    benchmark_return = d_data['close'].copy()
    benchmark_return = benchmark_return.fillna(method='ffill')
    benchmark_return = benchmark_return.fillna(method='bfill')
    benchmark_return = benchmark_return.values[:, 0]

    # Calculate metrics
    equity_return = equity_return / equity_return[0] 
    benchmark_return = benchmark_return / benchmark_return[0]
    tsu.returnize0(equity_return)
    tsu.returnize0(benchmark_return)
    self.equity_avg_daily_ret = np.average(equity_return)
    self.equity_std_daily_ret = np.std(equity_return)
    self.equity_sharpe = np.sqrt(252) * self.equity_avg_daily_ret / self.equity_std_daily_ret
    self.equity_cul_ret = np.cumprod(equity_return + 1)[-1]

    self.bm_avg_daily_ret = np.average(benchmark_return)
    self.bm_std_daily_ret = np.std(benchmark_return)
    self.bm_sharpe = np.sqrt(252) * self.bm_avg_daily_ret / self.bm_std_daily_ret
    self.bm_cul_ret = np.cumprod(benchmark_return + 1)[-1]


  def ProvideResult(self):
    print "\nThe final value of the protfolio using the sample file is -- ", self.value_data[-1], "\n"

    print "Detail of the performance of the protfolio: "
    print "Data Range: ", self.start_date.isoformat(), " to ", self.end_date.isoformat(), "\n"

    print "Sharpe Ratio of Fund: ", self.equity_sharpe
    print "Sharpe Ratio of ", self.benchmark_symbol, " : ", self.bm_sharpe, "\n"

    print "Total Return of Fund: ", self.equity_cul_ret
    print "Total Return of ", self.benchmark_symbol, " : ", self.bm_cul_ret, "\n"

    print "Standard Deviation of Fund: ", self.equity_std_daily_ret
    print "Standard Deviation of ", self.benchmark_symbol, " : ", self.bm_std_daily_ret, "\n"

    print "Average Daily Return of Fund: ", self.equity_avg_daily_ret
    print "Average Daily Return of ", self.benchmark_symbol, " : ", self.bm_avg_daily_ret, "\n"

  def _parse_value(self, value_file):
    data = []
    for l in open(value_file):
      year, month, day, money = map(lambda x: int(float(x.strip())), l.split(','))
      data.append([dt.datetime(year, month, day), float(money)]) 
    return data 


if __name__ == "__main__":
  # Usage: python analyze.py data/test_order_3.csv \$SPX
  if len(sys.argv) != 3:
    print "Incorrect param number"
  else:
    analyzer = Analyzer(sys.argv[1], sys.argv[2])
    analyzer.Run()
    analyzer.ProvideResult()
    
