import sys
sys.path.insert(0, '/var/fpwork/hcostina/Licenta/temperature/')
import myDBHandler
import setupHandler
import dht11
from time import *
import RPi.GPIO as GPIO
import time
import datetime
import socket
import thread

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(16, GPIO.IN)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

# variables
location_name = setupHandler.getSetupParamNo(1)
name16_light = "Light.1"
name25_temp = "Temperature.1"
name25_hum = "Humidity.1"
name_fan = "ColdBulb.1"
name_bulb = "WarmBulb.1"
name_rgb = "AmbiLight.1"
typeR = "Relay"
typeS = "Sensor"
typeRGB = "RGB"

lastStateTemperature = -250
lastStateHumidity = -1
lastStateLight = -1

RED = GPIO.PWM(13, 100)
GREEN = GPIO.PWM(19, 100)
BLUE = GPIO.PWM(12, 100)
RED.start(0)
GREEN.start(0)
BLUE.start(0)

# init libs
instance_of_temp = dht11.DHT11(pin=25)

# functions definition
def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
	return s.getsockname()[0]

def get_time():
	return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def init_relays():
	GPIO.output(14, True)
	GPIO.output(15, True)
	myDBHandler.addOrUpdateInDB(str(get_ip()), name_bulb, "0", typeR, location_name)
	print get_time() + " [Init_Relays] Initialize WarmBulb 1 with value 0"
	myDBHandler.addOrUpdateInDB(str(get_ip()), name_fan, "0", typeR, location_name)
	print get_time() + " [Init_Relays] Initialize Coldbulb 1 with value 0"
	myDBHandler.addOrUpdateInDB(str(get_ip()), name_rgb, "0,0,0", typeRGB, location_name)
	print get_time() + " [Init_Relays] Initialize AmbiLight1 with value (0, 0, 0)"
	

def change_Bulb1_state(state):
	if state == True:
		GPIO.output(14,True)
		myDBHandler.addOrUpdateInDB(str(get_ip()), name_bulb, "0", typeR, location_name)
		print get_time() + " [Change_Bulb1_state] WarmBulb1 turn off"
	else:
		GPIO.output(14,False)
		myDBHandler.addOrUpdateInDB(str(get_ip()), name_bulb, "1", typeR, location_name)
		print get_time() + " [Change_Bulb1_state] WarmBulb1 turn on"

def change_Fan1_state(state):
	if state == True:
		GPIO.output(15,True)
		myDBHandler.addOrUpdateInDB(str(get_ip()), name_fan, "0", typeR, location_name)
		print get_time() + " [change_Fan1_state] ColdBulb1 turn off"
	else:
		GPIO.output(15,False)
		myDBHandler.addOrUpdateInDB(str(get_ip()), name_fan, "1", typeR, location_name)
		print get_time() + " [change_Fan1_state] ColdBulb1 turn on"

def RGBsetColor(redArg, greenArg, blueArg):
    try:
        if ((int(redArg) <= 255) and (int(redArg)>=0) and (int(greenArg) <= 255) and (int(greenArg)>=0) and (int(blueArg) <= 255) and (int(blueArg)>=0)):
            RED.ChangeDutyCycle((int(redArg) / 255.0) * 100)
            GREEN.ChangeDutyCycle((int(greenArg) / 255.0) * 100)
            BLUE.ChangeDutyCycle((int(blueArg) / 255.0) * 100)
            myDBHandler.addOrUpdateInDB(str(get_ip()), name_rgb, redArg + "," + greenArg + "," + blueArg, typeRGB, location_name)
            print get_time() + " [RGBSetColor] Led Color set with parameters (" + redArg + ", " + greenArg + ", " + blueArg + ")"
        else :
            print get_time() + " [RGBSetColor] Invalid parameters (" + redArg + ", " + greenArg + ", " + blueArg + ")"
    except:
        print get_time() + " [RGBSetColor] Invalid parameters (" + redArg + ", " + greenArg + ", " + blueArg + ")"

def UpdateSensors():
	global lastStateTemperature
	global lastStateHumidity
	global lastStateLight
	resultForUse = instance_of_temp.read()
	if resultForUse.is_valid():
		actualTemp = resultForUse.temperature
		actualHumi = resultForUse.humidity
		if lastStateTemperature != actualTemp:
			myDBHandler.addOrUpdateInDB(str(get_ip()), name25_temp, str(actualTemp), typeS, location_name)
			lastStateTemperature = actualTemp
			print get_time() + " [Temperature] updated with value " + str(resultForUse.temperature) + "*C"
		if lastStateHumidity != actualHumi:
			myDBHandler.addOrUpdateInDB(str(get_ip()), name25_hum, str(actualHumi), typeS, location_name)
			lastStateHumidity = actualHumi
			print get_time() + " [Humidity] updated with value " + str(resultForUse.humidity) + "%"

	actualLight = GPIO.input(16)
	if (actualLight != lastStateLight):
		if (actualLight == 0):
			myDBHandler.addOrUpdateInDB(str(get_ip()), name16_light, "Bright", typeS, location_name)
			print get_time() + " [Light] updated with value Bright"
		else:
			myDBHandler.addOrUpdateInDB(str(get_ip()), name16_light, "Dark", typeS, location_name)
			print get_time() + " [Light] updated with value Dark"
		lastStateLight = actualLight

#non-loop
init_relays()

#multithread
def tcp_ip_thread( threadName):
	HOST = str(get_ip())
	PORT = 25565
	socTcpIp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print get_time() + " [" + threadName + "] Socket created "

	try:
		socTcpIp.bind((HOST, PORT))
	except socket.error:
        	print get_time() + " [" + threadName + "] Bind failed"

	socTcpIp.listen(5)
	print get_time() + " [" + threadName + "] Socket awaiting messages"
	(conn, addr) = socTcpIp.accept()
	print get_time() + " [" + threadName + "] Connected to " + str(addr)
	connectionExist = True;

   	# awaiting for message
	while True:
		if connectionExist:
			data = conn.recv(1024)
			print get_time() + " [" + threadName + "] Recieved message: " + data + " from " + str(addr)
			reply = ''

			# process your message
			if data == (name_bulb + ":True"):
				change_Bulb1_state(True)
				reply = "Bulb1 is off"

			elif data == (name_bulb + ":False"):
				change_Bulb1_state(False)
				reply = "Bulb1 is on"

			elif data == (name_fan + ":True"):
				change_Fan1_state(True)
				reply = "Fan1 is off"

			elif data == (name_fan + ":False"):
				change_Fan1_state(False)
				reply = "Fan1 is on"
			elif name_rgb in data:
				messageArray = data.split(':', 3)
				RGBsetColor(messageArray[1], messageArray[2], messageArray[3])
				reply = "AmbientalLight was changed"

			else:
				reply = 'Unknown command'

			# Sending reply
			conn.send(reply)
			conn.close()
			connectionExist = False
		else:
			print get_time() + " [" + threadName + "] Socket awaiting messages"
			(conn, addr) = socTcpIp.accept()
			print get_time() + " [" + threadName + "] Connected to " + str(addr)
			connectionExist = True;


# Create TCP/IP thread
try:
   thread.start_new_thread( tcp_ip_thread, ("TCP/IP", ) )
except:
   print get_time() + " [MultiThread] Error: unable to start thread"


# loop
while True:
	UpdateSensors()
		
#exit
conn.close()