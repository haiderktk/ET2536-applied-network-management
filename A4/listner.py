#!/usr/bin/env python

#sudo snmptrapd -c /etc/snmp/snmptrapd.conf
#snmptrapd -f -Lo -c /etc/snmp/snmptrapd.conf
#ps aux | grep snmptrapd
#snmptrap -v 1 -c public localhost:50162 1.1.3.3.1 10.0.0.64 6 247 "" 1.1.3.3.31.55 i '0'
#snmptrap -v 1 -c public 127.0.0.1:50162 .1.3.6.1.4.1.41717.10 10.0.2.2 6 247 '' .1.3.6.1.4.1.2789.41717.20.1 s `hostname` .1.3.1.4.1.2789.41414.20.2 i `date -u +%s` .1.3.1.4.1.2789.41414.20.3 i "0" .1.3.1.4.1.2789.41414.20.4 i "139694272"

#snmptrap -v 1 -c public 192.168.1.110 .1.3.6.1.4.1.41717.20 10.0.2.2 6 247  .1.3.6.1.4.1.2789.41717.20.1 s haider-VirtualBox .1.3.1.4.1.2789.41414.20.2 i 1479845845 .1.3.1.4.1.2789.41414.20.3 i 2 .1.3.1.4.1.2789.41414.20.4 i 1479840373

#snmptrap -v 1 -c public 127.0.0.1:50162 .1.3.6.1.4.1.41717.10 10.0.2.2 6 247 '' .1.3.6.1.4.1.2789.41717.10.1 s `hostname` .1.3.1.4.1.2789.41414.10.2 i `date -u +%s`
#snmptrap -v 1 -c public 127.0.0.1:50162 .1.3.6.1.4.1.41717.10 10.0.2.2 6 247 '' .1.3.6.1.4.1.2789.41717.10.1 s 'hostname1' .1.3.1.4.1.2789.41414.10.2 i 2


#snmptrap -v 1 -c public 127.0.0.1 .1.3.6.1.4.1.41717.30 127.0.1.1 6 247 "" 
#.1.3.6.1.4.1.2789.41717.30.1 s haider-VirtualBox .1.3.1.4.1.2789.41414.30.2 i 1479853211 .1.3.1.4.1.2789.41414.30.3 i 2 .1.3.1.4
#.1.2789.41414.30.4 i 1479853069.1.3.6.1.4.1.2789.41717.30.5 s "hostname1" .1.3.1.4.1.2789.41414.30.6 i 1479853211 .1.3.1.4.1.2789.41414.30.7 i 2 .1.3.1.4.1.2789.41414.30.8 i 1479852876.1.3.6.1.4.1.2789.41717.30.9 s newdevice .1.3.1.4.1.2789.41414.30.10 i 1479853211 .1.3.1.4.1.2789.41414.30.11 i 2 .1.3.1.4.1.2789.41414.30.12 i 1479853158


#localhost
#UDP: [127.0.0.1]:48886->[127.0.0.1]:50162
#DISMAN-EVENT-MIB::sysUpTimeInstance 0:2:59:30.46
#SNMPv2-MIB::snmpTrapOID.0 SNMPv2-SMI::enterprises.41717.10.0.247
#SNMPv2-SMI::enterprises.2789.41717.20.1 "haider-VirtualBox"
#SNMPv2-SMI::org.1.4.1.2789.41414.20.2 1479767760
#SNMPv2-SMI::org.1.4.1.2789.41414.20.3 0
#SNMPv2-SMI::org.1.4.1.2789.41414.20.4 139694272
#SNMP-COMMUNITY-MIB::snmpTrapAddress.0 10.0.2.2
#SNMP-COMMUNITY-MIB::snmpTrapCommunity.0 "public"
#SNMPv2-MIB::snmpTrapEnterprise.0 SNMPv2-SMI::enterprises.41717.10

#localhost
#UDP: [127.0.0.1]:59092->[127.0.0.1]:50162
#DISMAN-EVENT-MIB::sysUpTimeInstance 0:3:06:52.76
#SNMPv2-MIB::snmpTrapOID.0 SNMPv2-SMI::enterprises.41717.10.0.247
#SNMPv2-SMI::enterprises.2789.41717.10.1 "haider-VirtualBox"
#SNMPv2-SMI::org.1.4.1.2789.41414.10.2 0
#SNMP-COMMUNITY-MIB::snmpTrapAddress.0 10.0.2.2
#SNMP-COMMUNITY-MIB::snmpTrapCommunity.0 "public"
#SNMPv2-MIB::snmpTrapEnterprise.0 SNMPv2-SMI::enterprises.41717.10

import sys, os, signal
import time
import optparse
import datetime
import MySQLdb
import subprocess
from subprocess import call

import socket
hostme = socket.getfqdn()
myaddress = socket.gethostbyname(socket.gethostname())

#print addr
#print myaddress


#testtrap = "snmptrap -v 1 -c public 127.0.0.1 .1.3.6.1.4.1.41717.30 127.0.1.1 6 247 '\"\"' .1.3.6.1.4.1.2789.41717.30.1 s haider-VirtualBox .1.3.1.4.1.2789.41414.30.2 i 1479855510 .1.3.1.4.1.2789.41414.30.3 i 2 .1.3.1.4.1.2789.41414.30.4 i 1479853069 .1.3.6.1.4.1.2789.41717.30.5 s hostname1 .1.3.1.4.1.2789.41414.30.6 i 1479855510 .1.3.1.4.1.2789.41414.30.7 i 2 .1.3.1.4.1.2789.41414.30.8 i 1479852876 .1.3.6.1.4.1.2789.41717.30.9 s newdevice .1.3.1.4.1.2789.41414.30.10 i 1479855510 .1.3.1.4.1.2789.41414.30.11 i 2 .1.3.1.4.1.2789.41414.30.12 i 1479855508"

#os.system("echo "+testtrap)
#os.system(testtrap)

#exit()

#Keep appending the log file with incomming traps
running = True
outfile = open('/tmp/traps', 'a')

trapinfo = []

while running:
	try:
		input = raw_input()
		outfile.write(input+ '\n')
		trapinfo.append(input)
	except EOFError:
		running = False


outfile.close()
#outfile.write('infor from the array \n')
#for x in range(0, len(trapinfo)):
#	outfile.write(trapinfo[x])
#	outfile.write('\n')

#devicenameraw 			= 'SNMPv2-SMI::entesnmptrapd -f -Lo -c /location/of/trapd.confrprises.2789.41717.10.1 "haider-VirtualBox"' #trapinfo[4] #
#devicestatusraw	    	= 'SNMPv2-SMI::org.1.4.1.2789.41414.10.2 0'# trapinfo[5] #

devicenameraw 			= trapinfo[4]
devicestatusraw	    	= trapinfo[5]

s_dev = devicenameraw.split(" ", 2 )
dest = s_dev[1].strip()
devicename = str(dest[1:-1])


s_devst = devicestatusraw.split(" ", 2 )
devicestatus = str(s_devst[1].strip())

#print devicename
#print devicestatus

#exit()




#devicename 			= "haider-VirtualBox"
#devicestatus	    = '2'
curr_time 			= int(time.time())
oldstatus 	= ""
oldtime 	= ""
fqdnO		= ""


db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="sting901",  # your password
                     db="anm")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
sqlq = "SELECT * FROM `snmptraps` WHERE `device` = '"+devicename+"'"
#print sqlq

cur.execute(sqlq)

#SELECT * FROM `snmptraps` WHERE `device` LIKE 'haider'

if not cur.rowcount:
   	#print "No results found Inserting new entry"
   	try:
   		sqlq="INSERT INTO `anm`.`snmptraps` (`device`, `status`, `time`) VALUES ('"+devicename+"', '"+devicestatus+"', '"+str(curr_time)+"')"
   		#print sqlq
	   	cur.execute(sqlq)
	   	db.commit()
	except:
	   	db.rollback()

else:
	#print "found it! ...Updating entry"
	#print "FQDN	= "+str(row[1])
	#print "oldstatus = " +str(row[2])
	#print "oldtime   = " +str(row[3])
	for row in cur.fetchall():
		fqdnO 		= str(row[1])
		oldstatus 	= str(row[2])
		oldtime 	= str(row[3])
	sqlq= "UPDATE `snmptraps` SET `status` =" + str(devicestatus) + ", `time` =" + str(curr_time) + ", `p_status` =" + str(oldstatus) + ", `p_time` =" + str(oldtime) + " WHERE `device` = '"+devicename+"'"
	#print sqlq
	try:
	   cur.execute(sqlq)
	   db.commit()
	except:
	   db.rollback()


#grab device info to send traps to

ipadd 		= ""
communtiy 	= ""
echo = "echo"

sqlq = "SELECT * FROM `device` WHERE 1"
cur.execute(sqlq)
for row in cur.fetchall():
	#print "Info of the Device"
	#print "ip address = " +str(row[1])
	#print "community   = " +str(row[2])
	ipadd 		= str(row[1])
	communtiy 	= str(row[2])


#fail trap
if devicestatus == '3':
	print "sending Fail MIB::traps"
	trapcmd ="snmptrap -v 1 -c "+ str(communtiy) +" "+ipadd+" .1.3.6.1.4.1.41717.20 10.0.2.2 6 247 '\"\"' .1.3.6.1.4.1.2789.41717.20.1 s "
	trapcmd =trapcmd+"'"+fqdnO+"' .1.3.1.4.1.2789.41414.20.2 i '"+str(int(time.time()))+"' .1.3.1.4.1.2789.41414.20.3 i '"+oldstatus+"' .1.3.1.4.1.2789.41414.20.4 i '"+oldtime+"'"
	
	os.system(echo + " " + trapcmd)
	os.system(trapcmd)
	#print "trap sent.."
	#print trapcmd
#print "devicestatus = " +str(devicestatus)
#print "oldstatus   = " +str(oldstatus)



#Danger traps

danger = False

sqlq = "SELECT * FROM `snmptraps` WHERE `status` =2"

cur.execute(sqlq)
#print "number of rows returned"
#print cur.rowcount

dvname 		= " "
status 		= " "
trtime 		= " "
o_status 	= " "
o_trtime 	= " "


if cur.rowcount>=2:
	print "sending Danger MIB::traps"
	trapcmd ="snmptrap -v 1 -c "+ str(communtiy) +" "+ipadd+" .1.3.6.1.4.1.41717.30 '"+myaddress +"' 6 247 '\"\"' "
	n =0
	for row in cur.fetchall():
		dvname 		= str(row[1])
		status 		= str(row[2])
		trtime 		= str(row[3])
		o_status 	= str(row[4])
		o_trtime 	= str(row[5])
		if n ==0:
			trapcmd = trapcmd+".1.3.6.1.4.1.2789.41717.30.1 s '"+dvname+"' .1.3.1.4.1.2789.41414.30.2 i '"+str(int(time.time()))+"' .1.3.1.4.1.2789.41414.30.3 i '"+o_status+"' .1.3.1.4.1.2789.41414.30.4 i '"+o_trtime+"' "
		else:
			trapcmd = trapcmd+".1.3.6.1.4.1.2789.41717.30."+str(n*4+1)+" s '"+dvname+"' .1.3.1.4.1.2789.41414.30."+str(n*4+2)+" i '"+str(int(time.time()))+"' .1.3.1.4.1.2789.41414.30."+str(n*4+3)+" i '"+o_status+"' .1.3.1.4.1.2789.41414.30."+str(n*4+4)+" i '"+o_trtime+"' "
		n += 1
	#if devicestatus == "2" and oldstatus == "2":
	#print "sending Danger MIB::traps"
	
	
	
	#os.system(echo + " " + trapcmd)
	print trapcmd
	os.system(trapcmd)
	#subprocess.call([trapcmd]) 
	
	#test = subprocess.Popen([trapcmd], stdout=subprocess.PIPE)
	#output = test.communicate()[0]

	#print "trap sent.."
	#print trapcmd
	#print trapcmd
# print all the first cell of all the rows
#for row in cur.fetchall():
#    print row
#db.close()


