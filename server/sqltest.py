#!/usr/bin/python

import datetime
import MySQLdb
import time
import matplotlib.pyplot as plt

db = 0
cursor = 0

def connect():

	global db
	global cursor

	# Open database connection
	db = MySQLdb.connect("localhost","test","test","test" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

def close():
	# disconnect from server
	db.close()

def getVersion():
	connect()

	# execute SQL query using execute() method.
	cursor.execute("SELECT VERSION()")

	# Fetch a single row using fetchone() method.
	data = cursor.fetchone()
	print "Database version : %s " % data

	close()


def insertRow(temp, hum, pres, datetime):

	connect()

	try:
		# Prepare SQL command

   		# Execute the SQL command
   		cursor.execute("insert into stats values (%s, %s, %s, %s)", (datetime, temp, hum, pres) )

   		# Commit your changes in the database
   		db.commit()
	except:
		print('problem')
   		# Rollback in case there is any error
   		db.rollback()


	close()

def getAverage(date):

	connect()
	
	sql = "SELECT * FROM stats \
	       WHERE datetime LIKE '%%%s%%'" % (date)
	try:
	   # Execute the SQL command
	   cursor.execute(sql)
	   # Fetch all the rows in a list of lists.
	   results = cursor.fetchall()
	   numOfRows = 0
	   tempSum = 0
	   humSum = 0
	   presSum = 0
	   tempList = []
	   daysList = []
	   humList = []
	   presList = []
	   for row in results:
	      numOfRows += 1
	      datetime = row[0]
	      temp = row[1]
	      hum = row[2]
	      pres = row[3]
	      tempSum += temp
	      humSum += hum
	      presSum += pres
	      tempList.append(temp)
	      humList.append(hum)
	      daysList.append(numOfRows)
	      presList.append(pres)
	      # Now print fetched result
	      #print "datetime=%s,temp=%s,hum=%d,pres=%s" % \
		#     (datetime, temp, hum, pres )

	#print("Temp: ",float(tempSum)/float(numOfRows),"Humidity: ",float(humSum)/float(numOfRows),"Pressure: ",float(presSum)/float(numOfRows))
	except:
	   print "Error: unable to fecth data"

	if numOfRows>0:
		print("Showing Average for {}".format(date)) 	
		print("Average Temperature: {}".format(tempSum/numOfRows))
		print("Average Humidity: {}".format(humSum/numOfRows))
		print("Average Pressure: {}".format(presSum/numOfRows))
		plt.figure(1)
		plt.subplot(212)
		plt.plot(daysList,tempList,'k--')
		plt.ylabel('Temperature Plot')
		plt.xlabel('Samples')
		plt.subplot(221)
		plt.plot(daysList,humList,'b--')
		plt.ylabel('Humidity Plot')
		plt.xlabel('Samples')
		plt.subplot(222)
		plt.plot(daysList,presList,'g--')
		plt.ylabel('Pressure Plot')
		plt.xlabel('Samples')
		plt.show()
	
	
	close()

	

#HOW-TO use functions
#insertRow(2.23,2.12,888,datetime.datetime.now())
#insertRow(42.23,24.22,800,datetime.datetime.now())
#insertRow(32.23,23.12,834,datetime.datetime.now())
#insertRow(26.23,32.1,868,datetime.datetime.now())
#insertRow(25.23,12.12,878,datetime.datetime.now())
#insertRow(24.23,42.22,818,datetime.datetime.now())
#getAverage("2018-01-04")









