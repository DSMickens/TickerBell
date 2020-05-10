import yfinance as yf
import yahoo_fin.stock_info as si
import smtplib
import ssl
from multiprocessing import Process
from time import sleep, time
from random import seed
from random import randint

alertProcess = None
alerts = {}
mode = {"cli":True, "email":False, "text":False}
emails = []
phoneNumbers = []

def checkAlerts():
  """
  Continuously checks a dictionary of specified alert stocks and prices
  and sends an alert if the price of the stock is hit.
  
  Params:
  alerts (Dictionary{int:[string, float, bool, bool]}: a dictionary of stock alerts
  """
  def printAlert(value, price):
    #set up server for email/text message
    port = 465
    password = 'T1ck3rB3ll'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
      server.login("TickerBellApp@gmail.com", password)
      #send out cli alert
      if (mode["cli"]):
        #create message for alert
        message ="""
        ******************************************
        *                 ALERT                  *
        *        {0:4}           ${1:<9.4f}       *
        ******************************************
        """.format(value[0], price)
        print(message)
        print(">>", end = ' ')
      #send out email alert
      if (mode["email"]):
        message = """\
        From: TickerBell\nSubject: New TickerBell Alert\n\n
        
        You have 1 new TickerBell Alert!
        
        Ticker: {0}
        Price: ${1:.4f}
        """.format(value[0], price)
        for email in emails:
          server.sendmail("TickerBellApp@gmail.com", email, message)
      #send out 
      if (mode["text"]):
        message ="""
        You have 1 new TickerBell Alert!
        
        Ticker: {0}
        Price: ${1:.4f}
        """.format(value[0], price)
        for number in phoneNumbers:
          server.sendmail("TickerBellApp@gmail.com", number, message)
  
  global alerts
  curtime = time()
  while (1):
    for key, value in alerts.items():
      if value[3]:
        price = si.get_live_price(value[0])
        if value[2]:
          if (float("{:.4f}".format(price)) <= value[1]):
            printAlert(value, price)
            alerts[key][3] = False
        else:
          if (float("{:.4f}".format(price)) >= value[1]):
            printAlert(value, price)
            alerts[key][3] = False 
        print(">> ", end = ' ')    
    while time() <= (curtime + 2):
      sleep(2)
    curtime = time()

def deleteAlert(inpt):
  global alerts
  delete = []
  try:
    ID = int(inpt)
    del alerts[ID]
  except KeyError:
    print("ID does not exist")
    return -1
  except ValueError:
    foundAlert = False
    for key, value in alerts.items():
      if (value[0] == inpt):
        delete.append(key)
    if len(delete) == 0:
      print("No alerts for ticker: {0} found".format(inpt))
    else:
      for key in delete:
        del alerts[key]

def createAlert(inpt):
  """
  Takes the alert command input and adds the fields to the alert dictionary
  
  Params:
  alerts (Dictionary{string:float}: a dictionary of stocks:prices alerts
  inpt (string): user input including the 'alert' command
  point: alert a low point if <= price. alert a high point if >= price. default = low
         current implementation does nothing with point and assumes all are <=
  """  
  #using global alerts
  global alerts
  
  #check if dictionary is max capacity (half of random numbers)
  if (len(alerts) == 50000):
    print("Dictionary Full!")
    return 
  
  #seed random number generator, generate random ID
  seed(time())
  ID = randint(0,99999)
  while ID in alerts:
    ID = randint(0,99999)
  
  #split input
  args = inpt.split(' ')
  
  #default arguments
  isLess = True
  isOn = True
  
  #if number of arguments is not in the acceptable range of arguments, fail
  if (len(args) > 4 or len(args) < 2):
    print("Invalid number of input arguments")
    return -1
    
  #if ticker symbol or price are invalid, fail
  try:
    yf.Ticker(args[0])
    ticker = args[0]
    price = float(args[1])
  except ValueError:
    print("Invalid price: {0}".format(args[1]))
    return -1
  except:
    print("Invalid ticker symbol: {0}".format(args[0]))
    return -1 
    
  #if optional isLess argument is invalid, fail
  if (len(args) >= 3):
    if (args[2].lower()) in ["more", "greater", "more than", "greater than", ">", ">="]:
      isLess = False
    elif (args[2].lower()) not in ["less", "fewer", "fewer than", "less than", "<", "<="]:
      print("Invalid argument: {0}".format(args[2]))
      return -1

  #if optional isOn argument is invalid, fail
  if (len(args) == 4):
    if (args[3].lower() == "off"):
      isOn = False
    elif (args[3].lower() != "on"):
      print("Invalid argument: {0}".format(args[3]))
      return -1
   
  #create the alert entry in the dictionary
  alerts[ID] = [ticker, price, isLess, isOn]
     
def printAlerts():
  """ 
  Prints contents of dictionary param (alerts) in a easy to read format
  """
  global alerts
  print("|   {0}   | {1} |    {2}    | {3} |".format("ID", "Ticker", "Trigger", "Status"))
  print("|--------+--------+---------------+--------|")
  for key, value in alerts.items():
    ticker = value[0]
    price = value[1] 
    operator = "<=" if value[2] else ">="
    status = "on" if value[3] else "off"
    print("| {0:<6d} |  {1:<4}  |  {2} {3:<9.4f} |  {4:>3}   |".format(key, ticker, operator, price, status))

def startAlert():
  """
  Begins a new process to run and check for alerts constantly.
  
  Params:
  alerts (Dictionary{string:float}; a dictionary of stocks:prices alerts
  """
  global alertProcess
  global alerts
  if len(alerts) == 0:
    print("No alerts have been made. Create an alert and start again.")
    return
  alertProcess = Process(target=checkAlerts)
  alertProcess.daemon=True
  alertProcess.start()
    
def stopAlert():
  """
  Terminates the alertProcess.
  """
  global alertProcess
  if alertProcess is not None:
    alertProcess.terminate()
    alertProcess = None
  else:
    print("Alert System not currently running")
    
def toggleAlert(status, inpt):
  """
  toggleAlert
  """
  global alerts
  try:
    ID = int(inpt)
    if (status):
      alerts[ID][3] = True
    else:
      alerts[ID][3] = False
  except ValueError:
    print("Invalid ID: {0}".format(inpt))
  except KeyError:
    print("No alert with ID: {0}".format(ID))
    
def setEmail(inpt):
  """
  setEmail
  """
  args = inpt.split(' ')
  if (len(args) != 2):
    print("Invalid number of arguments")
    return -1
  if args[0] == "add":
    emails.append(args[1])
  elif args[0] == "remove":
    for item in emails:
      if item == args[1]:
        emails.remove(item)
        
def setText(inpt):
  """
  setText
  """
  carriers = {"verizon":"@vtext.com", "at&t":"@txt.att.net", "tmobile":"tmomail.net",
              "sprint":"@messaging.sprintpcs.com","xfinity":"@vtext.com",
              "googlefi":"@msg.fi.google.com"}
  args = inpt.split(' ')
  if (len(args) != 3):
    print("Invalid number of arguments: {0}".format(args.len()))
    return -1
  if (args[2] not in carriers):
    print("Invalid carrier: {0}".format(args[2]))
    return -1
  if (args[0] == "add"):
    phoneNumbers.append(args[1] + carriers[args[2]])
  elif (args[0] == "remove"):
    try:
      del phoneNumbers[args[1] + carriers[args[2]]]
    except KeyError:
      print("No phone number {0} with carrier {1}".format(args[1], args[2]))
    
def setAlertMode(inpt):
  """
  setAlertMode
  """
  args = inpt.split(' ')
  if (args[0].lower() == "cli"):
    if (args[1] == "on"):
      mode["cli"] = True
    if (args[1] == "off"):
      mode["cli"] = False
  elif (args[0].lower() == "text"):
    if (args[1] == "on"):
      mode["text"] = True
    if (args[1] == "off"):
      mode["text"] = False
  elif (args[0].lower() == "email"):
    if (args[1] == "on"):
      mode["email"] = True
    if (args[1] == "off"):
      mode["email"] = False
  return
  
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
  if args[0] == "print":
    printAlerts()
  elif args[0] == "create":
    createAlert(inpt[7:])
  elif args[0] == "start":
    if alertProcess is not None:
      print("You must stop an existing alert system before starting a new one")
    else:
      startAlert()
  elif args[0] == "stop":
    stopAlert()
  elif args[0] == "delete":
    deleteAlert(inpt[7:])
  elif args[0] == "on":
    toggleAlert(True, inpt[3:])
  elif args[0] == "off":
    toggleAlert(False, inpt[4:])
  elif args[0] == "mode":
    setAlertMode(inpt[5:])
  elif args[0] == "email":
    setEmail(inpt[6:])
  elif args[0] == "text":
    setText(inpt[5:])
  else:
    print("Invalid Input")
  