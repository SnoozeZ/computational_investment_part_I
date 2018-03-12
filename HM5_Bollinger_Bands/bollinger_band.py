import pandas as pd
import numpy as np
import sys

import datetime as dt
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu

class BollingerBands():
  def __init__(self, symbol, window='20'):
    print "Initialize Bollinger Bands."

    self.window = int(window)
    self.symbol = symbol
    self.start_date = dt.datetime(2010, 01, 01)
    self.end_date = dt.datetime(2010, 12, 31)

    self._read_market()

  def Run(self):
    print "Generate Bollinger Bands."
    self.rolling_mean = pd.rolling_mean(self.data, self.window, min_periods=1)

    self.rolling_std = pd.rolling_apply(self.data, self.window, lambda l: np.std(l, ddof=1), min_periods=1)

    self.upper_bound = self.rolling_mean + self.rolling_std
    
    self.lower_bound = self.rolling_mean - self.rolling_std

    self.values = (self.data - self.rolling_mean) / self.rolling_std

  def Output(self, file_path):
    print "Output result."
    self.values.to_csv(file_path, index=True) 


  def _read_market(self):
    ldt_timestamps = du.getNYSEdays(self.start_date, self.end_date, dt.timedelta(hours=16))
    data_object = da.DataAccess('Yahoo')
    ldf_data = data_object.get_data(ldt_timestamps, [self.symbol], ["close"])
    d_data = dict(zip(["close"], ldf_data))

    for key in ["close"]:
      d_data[key] = d_data[key].fillna(method='ffill')
      d_data[key] = d_data[key].fillna(method='bfill')
      d_data[key] = d_data[key].fillna(1.0)

    self.data = d_data["close"]



if __name__ == "__main__":
  if len(sys.argv) != 4:
    print "Invalid Param Number."
  else:
    bollinger_bands = BollingerBands(sys.argv[1], sys.argv[2])
    bollinger_bands.Run()
    bollinger_bands.Output(sys.argv[3])
