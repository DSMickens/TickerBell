import yfinance as yf
import yahoo_fin.stock_info as si
import multiprocessing
import time
from Alert import *
from Price import *

def usage():
  """Prints all usages of TickerBell"""
  print()
  print("USAGE:")
  print("    quit")
  print("    price [ticker]")
  print("    alert create [ticker] [price] less/more (optional) on/off (optional)")
  print("    alert delete [ID/ticker]")
  print("    alert on/off  [ID]")
  print("    alert print")
  print("    alert start")
  print("    alert stop")
  print("    alert mode cli/email/text [on/off]")
  print("    alert email add/remove [address]")
  print("    alert text add/remove [phone number] [carrier (spaces removed)]")
  print()

def printBanner():
  """prints the TickerBell welcome banner""" 
  print()
  print("         __________                           _____               ")
  print("        |___    ___|                         |  _  \        _  _  ")
  print("            |  | _   ___  _  __  ____   ____ | | | |  ____ | || | ") 
  print("            |  ||_| / __|| |/ / / _  \ / __ \| |_| / / _  \| || | ")
  print("            |  | _ | |   |   / | |_| || | |_||  _ | | |_| || || | ")
  print("            |  || || |   |   \ | ____|| |    | | | \| ____|| || | ")
  print("            |  || || |__ | |\ \| \___ | |    | |_| || \___ | || | ")
  print("            |__||_| \___||_| \_\\\____||_|    |_____/ \____||_||_| ")
  print()

def main():

  # Introduction Message and Input
  printBanner()
  usage()
  print(">> ", end = ' ')
  inpt = input().strip()
  
  # Input Loop
  while inpt != "quit":
  
    args = inpt.split(' ')
    cmd = args[0]
    
    if ( cmd == "price" ):
      printPrice(inpt[6:])
      
    elif ( cmd == "alert" ):
      if handleAlert(inpt[6:]) == -1:
        usage()
        
    elif ( cmd != "quit" ):
      print("Invalid Input")
      usage()
      
    print(">> ", end = ' ')
    inpt = input()
    
  print("\nThank you for using TickerBell\n")
      
if __name__ == "__main__":
    # execute only if run as a script
    main()
