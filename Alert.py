import yfinance as yf
import yahoo_fin.stock_info as si
from multiprocessing import Process
from time import sleep, time

alertProcess = None
alerts = {}

def checkAlerts(alerts):
  """
  Continuously checks a dictionary of specified alert stocks and prices
  and sends an alert if the price of the stock is hit.
  
  Params:
  alerts (Dictionary{string:float}: a dictionary of stocks:prices to check
  """
  curtime = time()
  while (1):
    for key, value in alerts.items():
      if (float("{:.4f}".format(si.get_live_price(key))) <= value):
        print("\n******************************************")
        print("*                 ALERT                  *")
        print("*        {0}            {1:.4f}          *".format(key, value))
        print("******************************************\n")
        print(">> ", end = ' ')
        return
    while time() <= (curtime + 1):
      sleep(1.1)
    curtime = time()

def createAlert(inpt, point = "low"):
  """
  Takes the alert command input and adds the fields to the alert dictionary
  
  Params:
  alerts (Dictionary{string:float}: a dictionary of stocks:prices alerts
  inpt (string): user input including the 'alert' command
  point: alert a low point if <= price. alert a high point if >= price. default = low
         current implementation does nothing with point and assumes all are <=
  """
  global alerts
  args = inpt.split(' ')
  if (len(args) != 4):
    print("Invalid number of input arguments")
    return -1
  try:
    yf.Ticker(args[2])
    alerts[args[2]] = float(args[3])
  except ValueError:
    print("Invalid price point")

def printAlerts():
  """Prints contents of dictionary param (alerts) in a easy to read format"""
  global alerts
  for key, value in alerts.items():
    print("{0}: {1}".format(key, value))

def startAlert():
  """
  Begins a new process to run and check for alerts constantly.
  
  Params:
  alerts (Dictionary{string:float}; a dictionary of stocks:prices alerts
  """
  global alertProcess
  alertProcess = Process(target=checkAlerts, args = (alerts,))
  alertProcess.daemon=True
  alertProcess.start()
    
def stopAlert():
  """Terminates the alertProcess."""
  global alertProcess
  alertProcess.terminate()
  alertProcess = None
    

def handleAlert(inpt):
  """
  takes input from TickerBell main input stream and distributes
  work across Alert module functions. Alert command has multiple 
  sub commands (start, stop, create) 
  
  Params:
  alerts (Dictionary{string:float}: a dictionary of stock:prices alerts
  """
  global alerts
  args = inpt.split(' ')
  if args[1] == "print":
    printAlerts()
  elif args[1] == "create":
    createAlert(inpt)
  elif args[1] == "start":
    if alertProcess is not None:
      print("You must stop an existing alert system before starting a new one")
    else:
      startAlert()
  elif args[1] == "stop":
    stopAlert()
  else:
    printf("Invalid Input")
  