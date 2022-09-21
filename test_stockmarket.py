from multiprocessing.sharedctypes import Value
import unittest
from stockmarket import StockMarket

stockmarket = StockMarket()

class TestStockMarket(unittest.TestCase):
    """A unit test class for testing all the functions of StockMarket class

        Methods
        -------
        test_calculate_dividend_yield : 
            This method tests the calculate_dividend_yield functionality of StockMarket class
        
        test_calculate_pe_ratio:
            This method tests the calculate_pe_ratio functionality of StockMarket class
        
        test_record_trade:
            This method tests the record_trade functionality of StockMarket class
            
        test_calculate_vws_price:
            This method tests the calculate_vws_price functionality of StockMarket class
            
        test_calculate_gbce:
            This method tests the calculate_gbce functionality of StockMarket class
        
    """
    
    def test_calculate_dividend_yield(self):
        result_preferred = stockmarket.calculate_dividend_yield("GIN", "50")
        result_common = stockmarket.calculate_dividend_yield("POP", 50)
       
        # testing for stocks with 'preferred' as their type
        self.assertEqual(result_preferred, 4)
       
        # testing for stocks with 'common' as their type
        self.assertEqual(result_common, 0.16)
        
        # testing for symbol which doesn't exist in stock exchange
        with self.assertRaises(ValueError):
            stockmarket.calculate_dividend_yield("zzzss", 20)

        # testing for price input as negative
        with self.assertRaises(ValueError):
            stockmarket.calculate_dividend_yield("GIN", -1)
        
        # testing for price input as zero
        with self.assertRaises(ValueError):
            stockmarket.calculate_dividend_yield("POP", 0)

    def test_calculate_pe_ratio(self):

        # testing for case with all arguments right and expected result is 12.5
        self.assertEqual(stockmarket.calculate_pe_ratio("GIN", "50") ,12.5)

        # testing for case when denominator becomes 0
        with self.assertRaises(ValueError):
            stockmarket.calculate_pe_ratio("TEA", 50)

        # testing for case when symbol doesn't exist in stock exchange
        with self.assertRaises(ValueError):
            stockmarket.calculate_pe_ratio("PP", 50)

    def test_record_trade(self):
        # testing case to check whether trade data is recorded successfully
        trade_data = stockmarket.record_trade("GIN", 80, 50,"Buy")
        self.assertIn(trade_data, stockmarket.trades["GIN"])

        # testing for case when symbol doesn't exist in stock exchange
        with self.assertRaises(ValueError):
            stockmarket.record_trade("AIN", 10, 50,"Buy")
        
        # testing for case when order is not equal to 'Buy' or 'Sell'
        with self.assertRaises(ValueError):
            stockmarket.record_trade("GIN", 10, 50,"Boy")

    def test_calculate_vws_price(self):
        # adding some dummy trade records to calculate vws price
        stockmarket.record_trade("GIN", 10, 50,"Buy")
        stockmarket.record_trade("GIN", 20, 20,"Buy")
        stockmarket.record_trade("GIN", 30, 60,"Buy")
        stockmarket.record_trade("TEA", 90, 50,"Buy")

        # testing for case for calculating GIN vws price: result expected -> 45
        self.assertEqual(stockmarket.calculate_vws_price("GIN"), 45)

        # testing for case for calculating TEA vws price: result expected -> 50
        self.assertEqual(stockmarket.calculate_vws_price("TEA"), 50)

    def test_calculate_gbce(self):
        # adding some dummy trade records to calculate gbce price
        stockmarket.record_trade("GIN", 10, 50,"Buy")
        stockmarket.record_trade("GIN", 20, 20,"Buy")
        stockmarket.record_trade("GIN", 30, 60,"Buy")
        stockmarket.record_trade("TEA", 90, 50,"Buy")
    
        # testing for a gbce calculation : result expected -> 47.434
        self.assertEqual(stockmarket.calculate_gbce(), 47.434)

if __name__ =="__main__":
    unittest.main()
