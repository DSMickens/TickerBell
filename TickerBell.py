import yfinance as yf
import yahoo_fin.stock_info as si
import multiprocessing
import time
import Alert
import Price
import TIO

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
  print("    io import/export [filename]")
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
  
def handleInput(inpt):
  """
  handles the user input line for stdin or from a file
  
  Params:
  inpt (String): user input line
  Return: fails if line can't be read in
  """
  args = inpt.split(' ')
  cmd = args[0]
  
  if ( cmd == "price" ):
    Price.printPrice(inpt[6:])
      
  elif ( cmd == "alert" ):
    if Alert.handleAlert(inpt[6:]) == -1:
      usage()

  elif ( cmd == "io" ):
    TIO.handleIO(inpt[3:])
      
  elif ( cmd != "quit" ):
    print("Invalid Input")
    usage()
  

def main():

  # Introduction Message and Input
  printBanner()
  usage()
  print(">> ", end = ' ')
  inpt = input().strip()
  
  # Input Loop
  while inpt != "quit":
  
    handleInput(inpt) 
      
    print(">> ", end = ' ')
    inpt = input().strip()
    
  print("\nThank you for using TickerBell\n")
      
if __name__ == "__main__":
    # execute only if run as a script
    main()
