import yfinance as yf
import yahoo_fin.stock_info as si
import multiprocessing
import time
import TAlert
import TPosition
import TIO
import TInfo
#import imaplib

def usage():
  """Prints all usages of TickerBell"""
  print()
  print("""
  USAGE:
      alert create [ticker] [price] less/more (optional) on/off (optional)
      alert delete [ID/ticker]
      alert on/off [ID]
      alert print alerts/emails/numbers
      alert start/stop
      alert mode cli/email/text [on/off]
      alert email add/remove [address]
      alert phone add/remove [phone number] [carrier (spaces removed)]
      info data [ticker]
      info price [ticker] open/close (optional)
      info volume [ticker]
      io import/export [filename]
      position add/update [ticker] [price] [quantity]
      position remove [ticker]
      position print
      position status [ticker] (optional)
      help
      usage
      quit
  """)
  
def help():
  """Prints help functions for all commands"""
  print("""
  ALERT:\n
      The alert command lets you manage alerts and the alert system.
  \n    CREATE\n
          create lets you create a brand new alert.
          It requires four parameters.\n
          ticker    - the ticker symbol for the stock you want to create an alert for
          price     - the price at which, if hit, the alert will go off
          less/more - the direction of price movement that will sound the alert
                    - ex. 'less' will cause the alert to go off if price is less
                      than or equal to the live stock price
                    - this is an optional argument that defaults to 'less'
          on/off    - the status of the alert. The alert will only occur if the status
                      is 'on'.
  \n    ON/OFF\n
          on/off lets you turn an alert on or off.
          It requires one parameter.\n
          ID    - the ID of the existing alert to be turned on or off
  \n    PRINT\n
          print lets you print out saved alerts, email addresses, or phone numbers.
          It requires one parameter.\n
          choice    - the data you want to print. Options: alerts, emails, or numbers
  \n    START/STOP\n
          start/stop lets you start or stop the alert system.
  \n    MODE\n
          mode lets you turn on or off different alert modes.
          It requires two parameters.\n
          mode      - the alert mode that you want to turn on/off.
                      Options: cli, email, text.
          on/off    - the status of the mode. The alert will be sent through this mode
                      only if the status is 'on
  \n    EMAIL\n
          email lets you add or remove an email to/from the alert system.
          It requires two parameters.\n
          add/remove    - whether you want to save or delete a saved email address
          address       - the email address to save or delete
  \n    PHONE\n
          phone lets you add or remove a phone number to/from the alert system.
          It requires three parameters.\n
          add/remove    - whether you want to save or delete a saved phone number
          phone number  - the phone number to save or delete
          carrier       - the service carrier for the phone number with all spaces removed
  
  INFO:\n
      The info command lets you get some info about specified stocks
  \n    PRICE\n
          price lets you get the price at certain times based on specified arguments
          It requires one parameter and has two optional parameters\n
          ticker - the ticker symbol of the stock to check
          open/close/extended - optional. If given, the price at the most recent open,
                                close, or current extended hours price will be given.
          diff - optional. Will show the difference between the chosen price and the price 
                 at the most recent open.
        VOLUME\n
          volume lets you get volume information for a stock
          It requires one parameter and has one optional parameter\n
          ticker - the ticker symbol of the stock to check.
          average - optional. Will return the average volume for this stock instead
                    of the current day's volume.
  
  IO:\n
      The io command lets you manage input/output with files
  \n    IMPORT/EXPORT\n
          import/export lets you resume/save current TickerBell system states.
          It requires one parameter.\n
          filename  - the name of the file to import from or export to

  POSITION:\n
      The position command lets you manage and check currently held positions.
  \n    ADD/UPDATE\n
          add/update lets you add a new position or update an existing position.
          It requires three parameters.\n
          ticker    - the ticker symbol for the stock
          price     - the average price per share being held
          quantity  - the number of shares purchased
  \n    REMOVE\n
          remove lets you remove a held position.
          It requires one parameter.\n
          ticker    - the ticker symbol for the stock
  \n    STATUS\n
          status lets you check the live status of your held positions.
          It has one optional parameter.\n
          ticker  - the ticker symbol for the stock. If no parameter is given,
                    then all position status's will be displayed

  PRICE:\n
      The price command lets you view live stock prices
      There are no subcommands within price. It takes one argument.\n
      ticker - the ticker symbol to check the price of

  USAGE:\n
      The usage commands gives a format for how to use each of the other commands.

  QUIT:
      The quit command ends the current session.
  """)

def printBanner():
  """prints the TickerBell welcome banner""" 
  print("""
           __________                          _____               
          |___    ___|                        |  _  \        _  _  
              |  | _   ___  _  __  ____   ___ | | | |  ____ | || |  
              |  ||_| / __|| |/ / / _  \ /   \| |_| / / _  \| || | 
              |  | _ | |   |   / | |_| || ||_||  _ | | |_| || || | 
              |  || || |   |   \ | ____|| |   | | | \| ____|| || | 
              |  || || |__ | |\ \| \___ | |   | |_| || \___ | || | 
              |__||_| \___||_| \_\\\____||_|   |_____/ \____||_||_| 
  """)
  
def handleInput(inpt):
  """
  handles the user input line for stdin or from a file
  
  Params:
    inpt (String): user input line
    Return: fails if line can't be read in
  """
  args = inpt.split(' ')
  cmd = args[0]

  if ( cmd == "alert" ):
    if (TAlert.handleAlert(inpt[6:]) == -1):
      usage()
  elif ( cmd == "io" ):
    if (TIO.handleIO(inpt[3:]) == -1):
      usage()
  elif (cmd == "help" ):
    help()
  elif (cmd == "info" ):
    if (TInfo.infoHandler(inpt[5:]) == -1):
      usage()
  elif (cmd == "usage" ):
    usage()
  elif (cmd == "position" ):
    if (TPosition.positionHandler(inpt[9:]) == -1):
      usage()
  elif ( cmd != "quit" ):
    print("Invalid TickerBell Command: {0}".format(cmd))
    usage()
  
def main():
            # Introduction Banner
  printBanner()
            # Usage Report
  usage()
            # Input Prompt
  print(">> ", end = ' ')
            # Initial Input Received
  inpt = input().strip()
            # Input Loop
  while inpt != "quit":
            # Handle Input
    handleInput(inpt) 
            # Input Reprompt
    print(">> ", end = ' ')
            # User Input
    inpt = input().strip()
            #Exit Message
  print("\nThank you for using TickerBell\n")
      
if __name__ == "__main__":
    # execute only if run as a script
    main()
