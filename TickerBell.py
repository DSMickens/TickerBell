import yfinance as yf
import yahoo_fin.stock_info as si
import json
"""
def usage():
  print("
"""

def main():
  inpt = ""
  print("Enter 'quit' to terminate")
  while inpt != "quit":
    print("Ticker Symbol:", end = ' ')
    inpt = input()
    if inpt != "quit":
      try: 
        price = si.get_live_price(inpt)
        print("{0} Price: {1:.4f}".format(inpt, price))
      except:
        print("Ticker Symbol does not exist")
    else:
      print("\nThank you for using TickerBell\n")
      
if __name__ == "__main__":
    # execute only if run as a script
    main()
