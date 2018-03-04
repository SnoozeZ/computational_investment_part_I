import unittest
import datetime as dt

from marketsim import MarketSimulator


class TestMarketSimulator(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestMarketSimulator, self).__init__(*args, **kwargs)
    
    self.order_file = "data/test_orders.csv"
    self.value_file_name = "data/test_value.csv"
    self.cash = "1000000"

  def test_case_1(self):
    simulator = MarketSimulator(self.cash, \
                                self.order_file, \
                                self.value_file_name)

    # Test parse order method.
    self.assertEqual(simulator.orders[0], \
                    [dt.datetime(2008, 12, 3, 0, 0), \
                    'AAPL', 'BUY', 130])
    self.assertEqual(simulator.orders[-1], \
                    [dt.datetime(2008, 12, 8, 0, 0), \
                    'AAPL', 'SELL', 130])
    self.assertEqual(simulator.start_date, dt.datetime(2008, 12, 3))
    self.assertEqual(simulator.end_date, dt.datetime(2008, 12, 8))

    # Test read market.
    print simulator.market_data
    self.assertEqual(95.49, \
                    simulator.market_data.loc[dt.datetime(2008, 12, 3, 16, 0), 'AAPL'])

    # Test run simulator.
    simulator.Run()
    print simulator.values

    # Test Output.
    simulator.ProvideValue()

  def test_case_2(self):
    self.order_file = "data/test_orders_2.csv"
    self.value_file_name = "data/test_value_2.csv"
    simulator = MarketSimulator(self.cash, self.order_file, self.value_file_name)
    simulator.Run()
    simulator.ProvideValue()


if __name__ == '__main__':
  unittest.main()
