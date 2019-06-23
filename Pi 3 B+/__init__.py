import sys
import myDBHandler
import time
import datetime
import socket
import os

# functions definition
def checkEquipmentConectivity():
	for row in myDBHandler.getIpColumn():
	  hostname = str(row).split('\'')[1]
	  response = os.system("ping -c 1 " + hostname)
	  if response != 0:
	  	myDBHandler.deleteFromDB(hostname)

# loop
while True:
	checkEquipmentConectivity()
	time.sleep(10)