import pandas as pd
import numpy as np

import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu

import sys

class MarketSimulator():
  def __init__(self, cash, order_file_name, value_file_name):
    print "Initialize MarketSimulator"
    self.cash = float(cash)
    self.value_file_name = value_file_name
    # orders: list of [date, symbol, action, ammount]
    self.orders = self._parse_order(order_file_name)
    self.order_num = len(self.orders)
    self.start_date = self.orders[0][0]
    self.end_date = self.orders[-1][0]
    self.day_nums = (self.end_date - self.start_date).days
    self.symbol_list = list(set([order[1] for order in self.orders]))

    self.market_data = self._read_market(self.start_date, \
                                         self.end_date, \
                                         self.symbol_list)
    self.values = dict() # date: (dict{symbol:amount}, cash)

  def Run(self):
    print "Simulator Run."
    last_stock = dict()
    last_cash = self.cash
    for date, symbol, action, amount in self.orders:
      cost = self.market_data.loc[date + dt.timedelta(hours=16) , symbol] * amount
      if action == "BUY":
        last_cash -= cost
        if symbol in last_stock:
          last_stock[symbol] += amount
        else:
          last_stock[symbol] = amount
      elif action == "SELL":
        last_cash += cost
        if symbol in last_stock:
          last_stock[symbol] -= amount
        else:
          last_stock[symbol] = 0 - amount
      else:
        print "Invalid action mode"

      self.values[date] = [dict(last_stock), last_cash]
  
  def ProvideValue(self):
    print "Simulator Provide Value."
    f = open(self.value_file_name, "w")
    last_value = []
    for date in map(lambda x: x.to_pydatetime(), 
                    du.getNYSEdays(self.start_date, self.end_date)): 
      wealth = 0.0
      if date in self.values:
        wealth = self._cal_daily_wealth(date, self.values[date])
        last_value = self.values[date]
      else: 
        wealth = self._cal_daily_wealth(date, last_value)

      f.write('{}, {}, {}, {}\n'.format(date.year, date.month, 
                                        date.day, wealth))
  
  def _cal_daily_wealth(self, date, value):
    wealth = value[1]
    for symbol, amount in value[0].items():
      wealth += self.market_data.loc[date + dt.timedelta(hours=16), symbol] * amount
    return wealth
    

  def _parse_order(self, order_file_name):
    f = open(order_file_name, 'r')
    self.orders = []
    for l in f:
      if len(l)<2:
        continue
      l = l[:-2] if (l[-2] == ',') else l
      year, month, day, symbol, action, amount = map(lambda x: x.strip(), l.split(","))
      date = dt.datetime(int(year), int(month), int(day))
      self.orders.append([date, symbol, action.upper(), int(amount)])
    self.orders = sorted(self.orders, key=lambda order : order[0]) # sort by date
    return self.orders

  def _read_market(self, start_date, end_date, symbols):
    ldt_timestamps = du.getNYSEdays(start_date, 
                                    end_date + dt.timedelta(days=1),   
                                    dt.timedelta(hours=16))
    dataobj = da.DataAccess('Yahoo')
    ldf_data = dataobj.get_data(ldt_timestamps, symbols, ["close"])
    d_data = dict(zip(["close"], ldf_data))

    for key in ["close"]:
      d_data[key] = d_data[key].fillna(method='ffill')
      d_data[key] = d_data[key].fillna(method='bfill')
      d_data[key] = d_data[key].fillna(1.0)

    return d_data["close"]

if __name__ == "__main__":
  # usage: python marketsim.py 1000000 data/orders.csv data/values.csv
  if len(sys.argv) != 4:
    print "Param number is incorrect."
  else:
    simulator = MarketSimulator(sys.argv[1], sys.argv[2], sys.argv[3])
    simulator.Run()
    simulator.ProvideValue()

