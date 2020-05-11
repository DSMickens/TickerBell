import TickerBell
import Alert

def importState(filename):
  """
  imports a saved state from an import file. Uses 
  normal TickerBell commands to import file
  
  Params:
  filename (String): the name of the import file
  """
  try:
    fp = open(filename)
  except:
    print("Could not open file: {0}".format(filename))
    return -1
  
  for line in fp:
    line = line.strip()
    TickerBell.handleInput(line)
  
  fp.close()

def exportState(filename):
  """
  exports the current state into an export file. Produces a file
  with TickerBell commands to enable importing later.
  
  Params:
  filename (String): the name of the export file
  """
  try:
    fp = open(filename, 'w')
  except:
    print("Could not open file: {0}".format(filename))
    return -1
  
  #exporting alerts
  for key, value in Alert.alerts.items():
    ticker = value[0]
    price = value[1]
    trigger = "less" if value[2] else "more"
    status = "on" if value[3] else "off"
    fp.write("alert create {0} {1} {2} {3}\n".format(ticker, price, trigger, status))
  
  #exporting mode status
  for key, value in Alert.mode.items():
    mode = key
    status = "on" if value else "off"
    fp.write("alert mode {0} {1}\n".format(mode, status))
  
  #exporting emails
  for email in Alert.emails:
    fp.write("alert email add {0}\n".format(email))
  
  #exporting phone Numbers
  for phone in Alert.phoneNumbers:
    address = phone.split('@')
    number = address[0]
    gate = "@" + address[1]
    carrier = None
    for key, value in Alert.carriers.items():
      if gate == value:
        carrier = key
    if (carrier is not None):
      fp.write("alert text add {0} {1}\n".format(number, carrier))
  
  fp.close()

def handleIO(inpt):
  args = inpt.split(' ')
  cmd = args[0]
  filename = args[1]
  if (cmd == "import"):
    importState(filename)
  elif (cmd == "export"):
    exportState(filename)
  else:
    print("Invalid IO Arguments")
    return -1