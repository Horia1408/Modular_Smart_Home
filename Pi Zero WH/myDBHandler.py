import mysql.connector
import setupHandler
from time import *

hostName = setupHandler.getSetupParamNo(0)

def get_time():
  return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def addOrUpdateInDB(ip, name, value, typeVar, location):
    mydb = mysql.connector.connect(
      host=hostName,
      user="admin",
      passwd="test",
      database="DevicesDB"
    )

    mycursor = mydb.cursor()

    sql = "REPLACE INTO Devices (IP, Name, Value, Type, Location) VALUES (%s, %s, %s, %s, %s)"
    val = (ip, name, value, typeVar, location)
    mycursor.execute(sql, val)

    mydb.commit()

    print get_time() + " [MyDBHandler] " + str(mycursor.rowcount) + " record(s) inserted"

def deleteFromDB(ip):
    mydb = mysql.connector.connect(
      host=hostName,
      user="admin",
      passwd="test",
      database="DevicesDB"
    )

    mycursor = mydb.cursor()

    sql = "DELETE FROM Devices WHERE IP = %s"
    adr = (ip, )

    mycursor.execute(sql, adr)

    mydb.commit()

    print get_time() + " [MyDBHandler] " + str(mycursor.rowcount) + "record(s) deleted"

# addOrUpdateInDB("192.168.1.1", "Nume1", "123", "Relay")
# deleteFromDB("192.168.1.2")
