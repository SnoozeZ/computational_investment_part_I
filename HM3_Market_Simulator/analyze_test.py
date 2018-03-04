import unittest
import datetime as dt

from analyze import Analyzer


class TestAnalyzer(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestAnalyzer, self).__init__(*args, **kwargs)
    
    self.value_file_name = "data/test_value.csv"
    self.benchmark_symbol = "$SPX"

  def test_case_1(self):
    analyzer = Analyzer(self.value_file_name, self.benchmark_symbol)
    analyzer.Run()
    analyzer.ProvideResult()
   
  def test_case_2(self):
    self.value_file_name = "data/test_value_2.csv"
    analyzer = Analyzer(self.value_file_name, self.benchmark_symbol)
    analyzer.Run()
    analyzer.ProvideResult()


if __name__ == '__main__':
  unittest.main()
