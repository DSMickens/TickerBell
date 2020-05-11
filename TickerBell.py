import yfinance as yf
import yahoo_fin.stock_info as si
import multiprocessing
#import textwrap
import time
import Alert
import Price
import TIO

def usage():
  """Prints all usages of TickerBell"""
  print()
  print("USAGE:")
  print("    alert create [ticker] [price] less/more (optional) on/off (optional)")
  print("    alert delete [ID/ticker]")
  print("    alert on/off [ID]")
  print("    alert print alerts/emails/numbers")
  print("    alert start/stop")
  print("    alert mode cli/email/text [on/off]")
  print("    alert email add/remove [address]")
  print("    alert phone add/remove [phone number] [carrier (spaces removed)]")
  print("    io import/export [filename]")
  print("    price [ticker]")
  print("    quit")
  print()
  
def help():
  """Prints help functions for all commands"""
  #alert command
  print("ALERT:\n")
  print("    The alert command lets you manage alerts and the alert system.")
  print("\n    CREATE\n")
  print("        create lets you create a brand new alert.")
  print("        It requires four parameters.\n")
  print("        ticker    - the ticker symbol for the stock you want to create an alert for")
  print("        price     - the price at which, if hit, the alert will go off")
  print("        less/more - the direction of price movement that will sound the alert")
  print("                  - ex. 'less' will cause the alert to go off if price is less")
  print("                    than or equal to the live stock price")
  print("                  - this is an optional argument that defaults to 'less'")
  print("        on/off    - the status of the alert. The alert will only occur if the status")
  print("                    is 'on'.")
  print("\n    ON/OFF\n")
  print("        on/off lets you turn an alert on or off.")
  print("        It requires one parameter.\n")
  print("        ID    - the ID of the existing alert to be turned on or off")
  print("\n    PRINT\n")
  print("        print lets you print out saved alerts, email addresses, or phone numbers.")
  print("        It requires one parameter.\n")
  print("        choice    - the data you want to print. Options: alerts, emails, or numbers")
  print("\n    START/STOP\n")
  print("        start/stop lets you start or stop the alert system.")
  print("\n    MODE\n")
  print("        mode lets you turn on or off different alert modes.")
  print("        It requires two parameters.\n")
  print("        mode      - the alert mode that you want to turn on/off. Options: cli, email, text")
  print("        on/off    - the status of the mode. The alert will be sent through this mode")
  print("                    only if the status is 'on")
  print("\n    EMAIL\n")
  print("        email lets you add or remove an email to/from the alert system.")
  print("        It requires two parameters.\n")
  print("        add/remove    - whether you want to save or delete a saved email address")
  print("        address       - the email address to save or delete")
  print("\n    PHONE\n")
  print("        phone lets you add or remove a phone number to/from the alert system.")
  print("        It requires three parameters.\n")
  print("        add/remove    - whether you want to save or delete a saved phone number")
  print("        phone number  - the phone number to save or delete")
  print("        carrier       - the service carrier for the phone number with all spaces removed")
  print("")
  print("IO:\n")
  print("    The io command lets you manage input/output with files")
  print("\n    IMPORT/EXPORT\n")
  print("        import/export lets you resume/save current TickerBell system states.")
  print("        It requires one parameter.\n")
  print("        filname  - the name of the file to import from or export to")
  print("")
  print("PRICE:\n")
  print("    The price command lets you view live stock prices")
  print("    There are no subcommands within price. It takes one argument.\n")
  print("    ticker - the ticker symbol to check the price of")
  print("")
  print("QUIT:")
  print("    The quit command ends the current session.")
  print("\n")

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

  elif (cmd == "help" ):
    help()
      
  elif ( cmd != "quit" ):
    print("Invalid Input")
    usage()
  

def main():
  help()
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
