#!/usr/bin/env python
#python probe.py localhost:5555:public 2 1.3.6.1.4.1.4171.40.3.0 1.3.6.1.4.1.4171.40.4.0


import sys, os, signal
import time
import optparse
import netsnmp

# Process command line arguments


if sys.argv[1] is '-h':
	print "Usage : prober <Agent IP:port:community> <sampling interval> <OID1> <OID2> ...... <OIDN>"
	exit()

if len(sys.argv)< 4:
	print "Usage : prober <Agent IP:port:community> <sampling interval> <OID1> <OID2> ...... <OIDN>"
	exit()






newstr = sys.argv[1]
sesinfo = newstr.split(":", 3 )
dest = sesinfo[0]+ ":" + sesinfo[1]
comm = sesinfo[2]



session = netsnmp.Session( DestHost=dest, Version=2, Community=comm )

sysUpTimeoid = "1.3.6.1.2.1.1.3.0"



prgname =sys.argv[0]
#print sys.argv[1]
#print sys.argv[2]

interval =float (sys.argv[2])
rateofchange = []

Dictionary = {}
KeyList = []

uptimeDictionary1 = {}
uptimeDictionary2 = {}
uptimeKeyList = []

for each_argv in sys.argv[3:]:
	KeyList.append(each_argv)
	uptimeKeyList.append(each_argv)


#Fetching the first values
count = 0
simpleCounter32 = []
for each_argv in sys.argv[3:]:
	#print each_argv
	vars = netsnmp.VarList( netsnmp.Varbind('.'+each_argv) )
	isitarr = session.get(vars) 
	#print( int(isitarr[0]))
	simpleCounter32.append(int(isitarr[0]))

	#doing uptime cancer shit
	upvars = netsnmp.VarList( netsnmp.Varbind('.'+sysUpTimeoid) )
	isitarrup = session.get(upvars) 
	#print( int(isitarrup[0]) )
	uptimeDictionary1[each_argv] = int(isitarrup[0])
	count += 1

time.sleep( interval )

loop = True
while (loop):

	#count = 0
	#simpleCounter32 = []
	#for each_argv in sys.argv[3:]:
		#print each_argv
	#	vars = netsnmp.VarList( netsnmp.Varbind('.'+each_argv) )
	#	isitarr = session.get(vars) 
	#	#print( int(isitarr[0]))
	#	simpleCounter32.append(int(isitarr[0]))

	#	#doing uptime cancer shit
	#	upvars = netsnmp.VarList( netsnmp.Varbind('.'+sysUpTimeoid) )
	#	isitarrup = session.get(upvars) 
	#	#print( int(isitarrup[0]) )
	#	uptimeDictionary1[each_argv] = int(isitarrup[0])

		
	#	count += 1

	#print simpleCounter32
	#print "Start : %s" % time.ctime()
	#time.sleep( interval )
	#print "End : %s" % time.ctime()


	newsimpleCounter32 = []
	for each_argv in sys.argv[3:]:
		#print each_argv
		vars = netsnmp.VarList( netsnmp.Varbind('.'+each_argv) )
		isitarr = session.get(vars) 
		#print( isitarr[0] )
		newsimpleCounter32.append(int(isitarr[0]))

		#doing uptime cancer shit
		upvars = netsnmp.VarList( netsnmp.Varbind('.'+sysUpTimeoid) )
		isitarrup = session.get(upvars) 
		uptimeDictionary2[each_argv] = int(isitarrup[0])


	#print newsimpleCounter32

	#now calculating the rate of change 

	newcount = 0
	wrap = False
	for each_argv in sys.argv[3:]:
	
		if uptimeDictionary2[each_argv]< uptimeDictionary1[each_argv]:
			print "Reboot Occured"
			uptimedif = interval
		else:
			uptimedif = (uptimeDictionary2[each_argv]-uptimeDictionary1[each_argv])/100
			#print "uptiem diff = " + str(uptimedif)

		if newsimpleCounter32[newcount]< simpleCounter32[newcount]:
   			print "Wrapped Occured"
   			wrap = True
   			#rat = 0
		else:
   			diff = newsimpleCounter32[newcount]-simpleCounter32[newcount]
			rat = diff/uptimedif
		
		#if wrap:
		#	rat = Dictionary[each_argv]
		
		print("Rate of change in counter for OID "+ each_argv  + " = " + str(rat) + " per second")
		#print("Old value= "+ str(simpleCounter32[newcount])  + "  new value = " + str(newsimpleCounter32[newcount])+ "And the diff seems to = "+str(diff)) 
		simpleCounter32[newcount] = newsimpleCounter32[newcount]
		upvars = netsnmp.VarList( netsnmp.Varbind('.'+sysUpTimeoid) )
		isitarrup = session.get(upvars) 
		uptimeDictionary1[each_argv] = int(isitarrup[0])

		newcount += 1
	
		if each_argv in Dictionary:
			#print "updating"
			newentry = (int(Dictionary[each_argv])+int(rat))/2
			#newentry = int(rat)
			Dictionary[each_argv] = newentry
		else:
			#print "new entry"
			Dictionary[each_argv] = rat


    
	print "------------------------------------------------------------------------------------"	
	time.sleep( interval )
	#print Dictionary
	#print KeyList
	#for Key in KeyList:
		#print Key,"=",Dictionary[Key]
	#print "One loop Done"