#!/usr/bin/env python


import sys, os, signal
import optparse
import pprint
import time
import ConfigParser

# Make sure we use the local copy, not a system-wide one
sys.path.insert(0, os.path.dirname(os.getcwd()))
import netsnmpagent

prgname = sys.argv[0]

# Process command line arguments
parser = optparse.OptionParser()
parser.add_option(
	"-m",
	"--mastersocket",
	dest="mastersocket",
	help="Sets the transport specification for the master agent's AgentX socket",
	default="/var/run/agentx/master"
)
parser.add_option(
	"-p",
	"--persistencedir",
	dest="persistencedir",
	help="Sets the path to the persistence directory",
	default="/var/lib/net-snmp"
)
(options, args) = parser.parse_args()

# Get terminal width for usage with pprint
rows, columns = os.popen("stty size", "r").read().split()

# First, create an instance of the netsnmpAgent class. We specify the
# fully-qualified path to SIMPLE-MIB.txt ourselves here, so that you
# don't have to copy the MIB to /usr/share/snmp/mibs.
try:
	agent = netsnmpagent.netsnmpAgent(
		AgentName      = "SimpleAgent",
		MasterSocket   = options.mastersocket,
		PersistenceDir = options.persistencedir,
		MIBFiles       = [ os.path.abspath(os.path.dirname(sys.argv[0])) +
		                   "/SIMPLE-MIB-sub.txt" ]
	)
except netsnmpagent.netsnmpAgentException as e:
	print("{0}: {1}".format(prgname, e))
	sys.exit(1)



# Then we create all SNMP scalar variables we're willing to serve.

sysUpTime = agent.TimeTicks(
	oidstr   = "1.3.6.1.4.1.4171.40.1",
	initval  =  int(time.time())
)


Config = ConfigParser.ConfigParser()
Config.read(os.path.abspath(os.path.dirname(sys.argv[0])) + "/counters.conf")

count =1
simpleCounter32 = []
for each_section in Config.sections():
	count += 1
	newoid = "1.3.6.1.4.1.4171.40."+str(count)
	T=int(time.time())
	C=int(float(Config.get(each_section,'C')))
	
	#C=int(Config.get(each_section,'C'))

	y=C*T
	#print y
	#low32 = (1 << 32) - 1
	#print y& low32
	#print y& 0xFFFFFFFF 
	#print newoid 7FFFFFFF 0xFFFFFFFF
	simpleCounter32.append(agent.Counter32( oidstr   = newoid , initval  = y& 0xFFFFFFFF ))



        




# Finally, we tell the agent to "start". This actually connects the
# agent to the master agent. 1.3.6.1.4.1.4171.40.1 SIMPLE-MIB::simpleInteger
try:
	agent.start()
except netsnmpagent.netsnmpAgentException as e:
	print("{0}: {1}".format(prgname, e))
	sys.exit(1)

print("{0}: AgentX connection to snmpd established.".format(prgname))

# Helper function that dumps the state of all registered SNMP variables
def DumpRegistered():
	for context in agent.getContexts():
		print("{0}: Registered SNMP objects in Context \"{1}\": ".format(prgname, context))
		vars = agent.getRegistered(context)
		pprint.pprint(vars, width=columns)
		print
DumpRegistered()

# Install a signal handler that terminates our simple agent when
# CTRL-C is pressed or a KILL signal is received
def TermHandler(signum, frame):
	global loop
	loop = False
signal.signal(signal.SIGINT, TermHandler)
signal.signal(signal.SIGTERM, TermHandler)

# Install a signal handler that dumps the state of all registered values
# when SIGHUP is received
def HupHandler(signum, frame):
	DumpRegistered()
signal.signal(signal.SIGHUP, HupHandler)

# The simple agent's main loop. We loop endlessly until our signal
# handler above changes the "loop" variable.
print("{0}: Serving SNMP requests, send SIGHUP to dump SNMP object state, press ^C to terminate...".format(prgname))





loop = True
while (loop):
	# Block and process SNMP requests, if available
	agent.check_and_process()
	
	sysUpTime.update(int(time.time()))

	newcount =0
	print "starting update!"
	for each_section in Config.sections():
		T=int(time.time())
		C=int(float(Config.get(each_section,'C')))
		y=C*T
		simpleCounter32[newcount].update(y& 0xFFFFFFFF)
		newcount += 1
		#print "geting updated!=="
		#print newcount
		#print int(y)& 0xFFFFFFFF

print("{0}: Terminating.".format(prgname))
agent.shutdown()
