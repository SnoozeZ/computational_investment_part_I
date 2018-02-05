import unittest
import hm1

import datetime as dt

class TestSimulateMethod(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestSimulateMethod, self).__init__(*args, **kwargs)

    # Set the default values of the input params.
    self.start_date = dt.datetime(2011, 1, 1) 
    self.end_date = dt.datetime(2011, 12, 31)
    self.symbols = ['AAPL', 'GLD', 'GOOG', 'XOM']
    self.allocation = [0.4, 0.4, 0.0, 0.2]

  def runSimulate(self):  
    self.std_ret, self.avg_ret, self.sharpe, self.cul_ret = \
      hm1.Simulate(self.start_date, self.end_date, self.symbols, \
      self.allocation)
  
  def checkSimulate(self, std_ret, avg_ret, sharpe, cul_ret):    
    self.assertAlmostEqual(self.std_ret, std_ret, places = 4)
    self.assertAlmostEqual(self.avg_ret, avg_ret, places = 4)
    self.assertAlmostEqual(self.sharpe, sharpe, places = 4)
    self.assertAlmostEqual(self.cul_ret, cul_ret, places = 4)

  def test_case_simulate_portional_allocation(self):
    self.runSimulate()
    self.checkSimulate(std_ret = 0.010146, \
                       avg_ret = 0.0006572, \
                       sharpe = 1.02828, \
                       cul_ret = 1.16487)
  
  def test_case_simulate_bias_allocation(self):
    self.start_date = dt.datetime(2010, 1, 1)
    self.end_date = dt.datetime(2010, 12, 31)
    self.symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']
    self.allocation = [0.0, 0.0, 0.0, 1.0]

    self.runSimulate()
    self.checkSimulate(std_ret = 0.00924299255, \
                       avg_ret = 0.000756285, \
                       sharpe = 1.2988933, \
                       cul_ret = 1.19605)
  
  def test_case_optimize(self):
    # Just run it because we don't have groundtruth. :(
    sharpe_1, alloc_1 =  hm1.Optimize('2011-01-01', \
                                         '2011-12-31', \
                                       ['XOM', 'GOOG', 'AAPL', 'GLD'])

    sharpe_2, alloc_2 =  hm1.Optimize('2011-01-01', \
                                        '2011-12-31', \
                                       ['GOOG', 'AAPL', 'GLD', 'XOM'])
    self.assertAlmostEqual(sharpe_1, sharpe_2)
    self.assertEqual(sorted(alloc_1), sorted(alloc_2))

  def test_case_optimiaze_quiz_1(self):
    print "The result of the quiz 1."
    print hm1.Optimize('2011-01-01', \
                    '2011-12-31', \
                   ['AAPL', 'GOOG', 'IBM', 'MSFT'])

    print hm1.Optimize('2010-01-01', \
                    '2010-12-31', \
                   ['BRCM', 'ADBE', 'AMD', 'ADI'])

    print hm1.Optimize('2011-01-01', \
                    '2011-12-31', \
                   ['BRCM', 'TXN', 'AMD', 'ADI'])

    print hm1.Optimize('2010-01-01', \
                    '2010-12-31', \
                   ['BRCM', 'TXN', 'IBM', 'HNZ'])
    
    print hm1.Optimize('2010-01-01', \
                    '2010-12-31', \
                   ['C', 'GS', 'IBM', 'HNZ'])
    print hm1.Optimize('2011-01-01', \
                    '2011-12-31', \
                   ['AAPL', 'GOOG', 'IBM', 'MSFT'])
    print hm1.Optimize('2011-01-01', \
                    '2011-12-31', \
                   ['BRCM', 'ADBE', 'AMD', 'ADI'])
    print hm1.Optimize('2011-01-01', \
                    '2011-12-31', \
                   ['BRCM', 'TXN', 'AMD', 'ADI'])
    print hm1.Optimize('2010-01-01', \
                    '2010-12-31', \
                   ['BRCM', 'TXN', 'IBM', 'HNZ'])
    print hm1.Optimize('2010-01-01', \
                    '2010-12-31', \
                   ['C', 'GS', 'IBM', 'HNZ'])

    print "Result of quiz 1 done.",


if __name__ == '__main__':
  unittest.main()
