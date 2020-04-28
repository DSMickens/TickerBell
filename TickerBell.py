import yfinance as yf
import yahoo_fin.stock_info as si
import multiprocessing
import time
from Alert import *
from Price import *

def usage():
  ''' Prints all usages of TickerBell '''
  print("")
  print("USAGE:")
  print("    quit")
  print("    price [ticker]")
  print("    alert create [ticker] [price]")
  print("    alert start")
  print("    alert stop")
  print("    alert print")
  print("")

def main():
  # Introduction Message and Input
  print("*****  Welcome to TickerBell  *****\n")
  usage()
  print(">> ", end = ' ')
  inpt = input()
  
  # Input Loop
  while inpt != "quit":
    args = inpt.split(' ')
    if args[0] == "price":
      printPrice(inpt)
    elif args[0] == "alert":
      if handleAlert(inpt) == -1:
        usage()
    elif args[0] != "quit":
      print("Invalid Input")
      usage()
    print(">> ", end = ' ')
    inpt = input()
    
  print("\nThank you for using TickerBell\n")
      
if __name__ == "__main__":
    # execute only if run as a script
    main()
