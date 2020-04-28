import yahoo_fin.stock_info as si

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
  inpt (string): The input line for price command including 'price'
  """
  args = inpt.split(' ')
  if (len(args) != 2):
    print("Invalid Input")
    usage()
  else:
    price = getPrice(args[1])
    if price is not None:  
      print("{0} price: {1:.4f}".format(args[1], price))
