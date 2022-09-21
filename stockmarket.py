import datetime

class StockMarket:
    
    """
        Class for Global Beverage Corporation Exchange.
        
        Attributes
        ----------
        
        exchange_data : dict 
            A dictionary to store sample data from Global Beverage Corporation Exchange
        
        trades : dict
            A dictionary to record and store all the trades including details such as timestamp, quantity, price and buy/sell indicator
        
        Methods
        -------
        validate_stock_symbol:
            A function to validate the stock symbol. It checks whether the symbol exist in exchange_data
        
        str_to_float:
            A function to convert all strings to float. Helps to convert price and quantity to float if user input is in string format
        
        validate_order:
            A function to validate sell order and buy order in function argument
        
        calculate_dividend_yield:
            This function calculates dividend yield by taking stock symbol and price as arguments.
        
        calculate_pe_ratio:
            This function calculates P/E ratio by taking stock symbol and price as arguments.
        
        record_trade:
            This function records a trade and store in trades dictionary.
        
        calculate_vws_price:
            This function calculates volume weighted stock price by taking stock symbol as argument
        
        calculate_gbce:
            This function calculates GBCE all share index  
        
    """
    
    def __init__(self) -> None:
        
        # initiating dictionary with all the trading pairs of the exchange
        self.exchange_data = {
            "TEA":{
                "type": "Common",
                "last_dividend": 0,
                "fixed_dividend": None,
                "par_value": 100
            },
            "POP":{
                "type": "Common",
                "last_dividend": 8,
                "fixed_dividend": None,
                "par_value": 100
            },
            "ALE":{
                "type": "Common",
                "last_dividend": 23,
                "fixed_dividend": None,
                "par_value": 60
            },
            "GIN":{
                "type": "Preferred",
                "last_dividend": 8,
                "fixed_dividend": 2,
                "par_value": 100
            },
            "JOE":{
                "type": "Common",
                "last_dividend": 13,
                "fixed_dividend": None,
                "par_value": 250
            }

        }
        
        # initiating empty dictionary for storing all trade records 
        self.trades = {}
    
    def validate_stock_symbol(self, symbol:str) -> str:
       
        """A method to validate whether the stock symbol is present in stock exchange data. This function prevents any wrong symbols 
           being entered to the function

        Args:
            symbol (str): unique symbol of stock 

        Raises:
            ValueError: if the symbol provided as argument does not exist in stock exchange data, a ValueError is raised

        Returns:
            str: returns the stock symbol present in stock exchange data 
        """
        
        if symbol not in self.exchange_data.keys():
            raise ValueError("Symbol does not exist in stock exchange")
        return symbol
    
    def str_to_float(self, value: int | float | str) -> int | float:
        
        """A method to convert string values to float. This helps to convert price and quantity to float when they '
           are provided in string format

        Args:
            value (int | float | str): It takes any value and converts to float only if the type of value is string

        Returns:
            float | int: returns the value in float or int format
        """
        
        if type(value)==str:
            return float(value)
        return value
    
    def validate_order(self, order: str) -> str:
        """This method helps to validate the order type. when this method is used for validation only 'Sell' and 'Buy' are 
           allowed to be passed as an argument

        Args:
            order (_type_): _description_

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        if order != "Buy" and order != "Sell":
            raise ValueError("Order should be either 'Sell' or 'Buy'")
        return order

    def calculate_dividend_yield(self, symbol:str, price:float | int) -> float | int:
        
        """Given any symbol and price as input, this method calculates the dividend yield

        Args:
            symbol (str): This is the symbol of stocks
            price (float | int): This is the price of stock

        Raises:
            ValueError: if price provided as argument is zero or less than zero, this ValueError is raised. This prevents the method 
            to have price value as zero or negative

        Returns:
            float | int: returns the calculated dividend yield in integer or float format depending on stock type is 'Common' or 'Preferred'
        """
        
        # validating all the arguments provided to this method
        symbol = self.validate_stock_symbol(symbol)
        price = self.str_to_float(price)
        
        stock = self.exchange_data[symbol]
        if price<=0:
            raise ValueError("Price is invalid")
        return stock["last_dividend"] / price if (stock["type"]=="Common") else stock["fixed_dividend"] * stock["par_value"] / price

    def calculate_pe_ratio(self, symbol:str, price:float | int) -> float | int:
        
        """Given any price as input, this method calculate the P/E Ratio
        
         Args:
            symbol (str): This is the symbol of stocks
            price (float | int): This is the price of stock

        Raises:
            ValueError: if the dividend value of a stock is zero, then P/E ratio cannot be find out. So, cannot divide by zero ValueError 
            is raised in cases where dividend becomes zero 

        Returns:
            float| int: returns the calculated P/E ratio in float or integer format.
        """
        
        # validating all the arguments provided to this method
        symbol = self.validate_stock_symbol(symbol)
        price = self.str_to_float(price)
        
        dividend = self.calculate_dividend_yield(symbol, price)
        if dividend == 0:
            raise ValueError("Cannot divide by zero")
        return price/dividend
    
    def record_trade(self, symbol:str, quantity:float | int, price:float | int, order:str = "Buy"):
        
        """This method records a trade, with timestamp, quantity, buy or sell indicator and price and store in a dictionary
        
         Args:
            symbol (str): This is the symbol of stocks
            quantity(float | int): This is the quantity of stocks traded
            price (float | int): This is the price of stock
            order (str): This is the trade type, whether the trade performed is sell order or buy order

        Returns:
            dict: This method returns a dictionary with trade data (timestamp, order, quantity, traded_price)
        """
        
        # validating all the arguments provided to this method
        symbol = self.validate_stock_symbol(symbol)
        quantity = self.str_to_float(quantity)
        price = self.str_to_float(price)
        order = self.validate_order(order)
        
        trade_data = {
        "timestamp": datetime.datetime.now().timestamp(),
        "order": "Buy" if order=="Buy" else "Sell",
        "quantity": quantity,
        "traded_price": price
        }
        
        if symbol not in self.trades:
            self.trades[symbol] = [trade_data]
        else:
            self.trades[symbol].append(trade_data)
        
        return trade_data


    def calculate_vws_price(self, symbol:str) -> float | int:
        
        """This method calculate Volume Weighted Stock Price based on trades in past 5 minutes
        
         Args:
            symbol (str): This is the symbol of stocks

        Raises:
            ValueError: if total traded quantity is zero in any case, a ValueError is raised

        Returns:
            int | float: returns the calculated volume weighted price in integer or float format
        """
        
        # validating all the arguments provided to this method
        symbol = self.validate_stock_symbol(symbol)
        
        time_before_5_min = (datetime.datetime.now() - datetime.timedelta(minutes=5)).timestamp()
        total_trade_amount = 0
        total_qty = 0
        if symbol in self.trades.keys():
            for trades in self.trades[symbol]:
                if trades["timestamp"]>=time_before_5_min:
                    total_trade_amount += trades["traded_price"] * trades["quantity"]
                    total_qty += trades["quantity"]
        
            if total_qty==0:
                raise ValueError("No result - because total traded quantity is 0")
            return total_trade_amount/total_qty
        return 0

    def calculate_gbce(self) -> int | float:
        
        """This method calculate the GBCE All Share Index using the geometric mean of the Volume Weighted Stock Price for all stocks

        Returns:
            int | float: returns the calculated GBCE value in integer or float format with maximum 3 decimals
        """
        
        total_vws_price = 1
        if self.trades:
            for symbol in self.trades.keys():
                total_vws_price*= self.calculate_vws_price(symbol)
        gbce = total_vws_price**(1/len(self.trades.keys()))
        return round(gbce,3)
           


