from interfaces.interface_phidget import *

pif = PhidgetInterface()
pif.set_file_name("Test")
pif.connect()
time.sleep(2)
pif.save_data()
pif.disconnect()
