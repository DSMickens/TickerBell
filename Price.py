import yahoo_fin.stock_info as si
from TickerBell import usage

def getPrice(ticker):
  """Get and return the price of a stock from the ticker"""
  try:
    return si.get_live_price(ticker)
  except:
    print("Invalid Ticker Symbol: {0}".format(ticker))
    return None

def printPrice(inpt):
  """
  Handles the user input for the price command
  
  Params:
  inpt (string): The input line for price command not including 'price'
  """
  price = getPrice(inpt)
  if price is not None:  
    print("{0} price: {1:.4f}".format(inpt, price))