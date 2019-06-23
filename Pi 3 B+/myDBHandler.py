import mysql.connector
from time import *
import socket

def get_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
  return s.getsockname()[0]

hostName = get_ip()

def get_time():
  return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def getIpColumn():
  iterator = 0

  mydb = mysql.connector.connect(
    host=hostName,
    user="admin",
    passwd="test",
    database="DevicesDB"
  )
  mycursor = mydb.cursor()
  mycursor.execute("SELECT DISTINCT IP FROM Devices")
  result_set = mycursor.fetchall()
  return result_set

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
